"""Controller: phase barriers, budget reservations, the event journal and episode records.

One block = one (world, repeat). The first pass is generated once and cloned into the PRIVATE,
PUBLIC, NEVER and VOTE continuations; PREPARE generates its own inventory. Within an arm every
phase is a barrier: all calls of the phase finish before anything they wrote is published.
Public and private finals are two isolated continuations of the same frozen context; public
finals are collected first.

Zero answer retries and zero repair calls. A failed first-pass or discussion call ends that
participant in the arm (first pass: in every arm sharing it); its fixture facts are still
released and the board shows a fixed placeholder.
"""
import hashlib
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import budget
import config
import contexts
import generate
import parse
import policy
import score
import seeds
from state import Board, Vault

PROVIDER_FAILURES = ('timeout', 'transport', 'http_', 'malformed_provider_response', 'response_too_large')
POOL_OF = {'initial': 'public', 'discussion': 'public', 'final_public': 'public', 'final_private': 'aux',
           'qualification': 'public'}
FLAG_OF = (('invalid_output', 'invalid_response'), ('truncated', 'invalid_response'), ('refusal', 'refusal'),
           ('timeout', 'timeout'), ('budget', 'exhaustion'), ('exhausted', 'exhaustion'),
           ('input_overflow', 'overflow'), ('input_token_cap', 'overflow'), ('leak_blocked', 'leak'))


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def flag_for(failure):
    for needle, flag in FLAG_OF:
        if needle in failure:
            return flag
    return 'infrastructure_failure'


class Controller:
    def __init__(self, stage, adapter, ledger, journal, namespace=None, clock=time.monotonic):
        ex = config.execution()
        self.stage, self.adapter, self.ledger, self.journal = stage, adapter, ledger, journal
        self.namespace = namespace or stage
        self.limits, self.breaker, self.provider = ex['limits'], ex['circuit_breaker'], config.launch_manifest()
        self.caps = config.phase_caps()
        self.thinking = config.thinking_budget()
        self.root = config.design()['seeds']['development_root']
        self.clock = clock
        self.halted = None
        self.leaks = 0
        self._lock = threading.Lock()
        self._consecutive = 0
        # Unique calls of this stage run (the shared first pass counted once).
        self.totals = {'calls': 0, 'failed': 0, 'input_tokens': 0, 'output_tokens': 0, 'billed_usd': 0.0}
        self.extra_forbidden = ()   # test hook: strings that must never reach any context
        self.tamper = None          # fault-injection hook: (meta, context, canary) -> context
        self.on_episode = None      # called with each episode record the moment it is closed

    # ------------------------------------------------------------------ one logical call
    def _halt(self, reason):
        with self._lock:
            if self.halted is None:
                self.halted = reason
                self.journal.append('halt', reason=reason)

    def _reservation(self, context, max_tokens):
        tokens = contexts.request_bytes(context) + self.limits['reservation_envelope_tokens']
        return tokens * self.provider['input_usd_per_million'] + max_tokens * self.provider['output_usd_per_million']

    def call(self, meta, context, canary):
        """meta: call_id, world, repeat, arm, agent, phase, seed, snapshots. Returns the call record."""
        call_id, phase = meta['call_id'], meta['phase']
        if self.tamper:
            context = self.tamper(meta, context, canary)
        pool = POOL_OF[phase]
        max_tokens = self.caps[phase] + self.thinking   # visible-output cap plus the reasoning allowance, if any
        text = contexts.text_of(context)
        out = dict(meta, pool=pool, prompt_sha256=sha(json.dumps([context['system'], context['messages']], sort_keys=True)),
                   messages=context['messages'], schema=context['schema'],
                   request_bytes=contexts.request_bytes(context), sources=context['sources'], max_tokens=max_tokens,
                   ok=False, record=None, raw=None, failure=None, usage={}, latency=0.0, attempts=0, billed_usd=0.0)

        def finish(failure=None):
            out['failure'] = failure
            self.journal.append('call', stage=self.stage, namespace=self.namespace,
                                **{k: v for k, v in out.items() if k != 'record'})
            with self._lock:
                if failure != 'not_dispatched_halt':
                    self.totals['calls'] += 1
                    self.totals['failed'] += bool(failure)
                    self.totals['input_tokens'] += out['usage'].get('input_tokens', 0)
                    self.totals['output_tokens'] += out['usage'].get('output_tokens', 0)
                    self.totals['billed_usd'] += out['billed_usd']
            if failure:
                provider_fault = failure.startswith(PROVIDER_FAILURES)
                with self._lock:
                    self._consecutive = self._consecutive + 1 if provider_fault else 0
                    too_many = self._consecutive >= self.breaker['max_consecutive_provider_failures']
                if failure in self.breaker['halt_categories']:
                    self._halt(failure)
                elif too_many:
                    self._halt('consecutive_provider_failures')
            else:
                with self._lock:
                    self._consecutive = 0
            return out

        if self.halted:
            return finish('not_dispatched_halt')
        if any(s and s in text for s in (canary,) + tuple(self.extra_forbidden)):
            with self._lock:
                self.leaks += 1
            return finish('leak_blocked')
        if out['request_bytes'] > self.limits['max_request_bytes']:
            return finish('input_overflow')
        try:
            self.ledger.reserve(call_id, self.namespace, pool, self._reservation(context, max_tokens))
        except budget.BudgetError as exc:
            if exc.category in ('call_budget_exhausted', 'dollar_budget_exhausted'):
                return finish('public_budget_exhausted' if pool == 'public' else 'aux_budget_exhausted')
            return finish(exc.category)
        result = self.adapter.complete({'call_id': call_id, 'system': context['system'],
                                        'messages': context['messages'], 'schema': context['schema'],
                                        'max_tokens': max_tokens, 'meta': meta})
        # raw: whatever text came back, kept in the journal for inspection. A failed call's text is
        # never parsed into a record and never shown to any agent.
        out.update(usage=result['usage'], latency=result['latency'], attempts=result['attempts'],
                   stop_reason=result['stop_reason'], raw=result['text'])
        if result['billing'] == 'billed':
            billed = (result['usage']['input_tokens'] * self.provider['input_usd_per_million']
                      + result['usage']['output_tokens'] * self.provider['output_usd_per_million'])
            breached = billed > self.ledger.reserved_for(call_id)
            self.ledger.settle(call_id, billed, result['usage']['input_tokens'], result['usage']['output_tokens'])
            out['billed_usd'] = billed / 1e6
            if breached:
                return finish('reservation_bound_breached')
        elif result['billing'] == 'none':
            self.ledger.settle(call_id, 0)
        else:
            self.ledger.unknown(call_id)
        if not result['ok']:
            return finish(result['failure'])
        if result['usage'].get('input_tokens', 0) > self.limits['input_token_cap_per_request']:
            return finish('input_token_cap_exceeded')
        try:
            out['record'] = parse.parse(context['schema'], result['text'])
        except parse.Invalid as exc:
            return finish('invalid_output:' + str(exc))
        out['ok'] = True
        return finish()

    def phase(self, jobs):
        """Barrier: dispatch every job of one phase at once, return when all have finished."""
        if not jobs:
            return []
        with ThreadPoolExecutor(max_workers=self.limits['max_inflight_requests']) as pool:
            return list(pool.map(lambda job: self.call(*job), jobs))

    # ------------------------------------------------------------------ helpers
    def _meta(self, world, repeat, arm, agent, phase, snapshots=None):
        call_id = '%s/w%04d/r%02d/%s/a%d/%s' % (self.namespace, world['world_index'], repeat, arm, agent, phase)
        if phase == 'initial' and arm == 'shared':
            seed = seeds.derive(self.root, 'initial', world['seed_stage'], world['world_index'], repeat, agent)
        else:
            seed = seeds.derive(self.root, 'policy', world['seed_stage'], world['world_index'], repeat, arm, agent, phase)
        return {'call_id': call_id, 'world': world['id'], 'repeat': repeat, 'arm': arm, 'agent': agent,
                'phase': phase, 'seed': seed, 'snapshots': snapshots or {}}

    @staticmethod
    def _role(world, agent):
        if world['special_agent'] is None:
            return 'full'
        holds = any(k in world['allocation'][agent] for k in world['audit_keys'])
        return 'informed' if holds else 'uninformed'

    # ------------------------------------------------------------------ a block
    def run_block(self, world, truth, repeat, mode='live', arms=None):
        """Run every arm of one (world, repeat). mode: live (five model agents) or replay (one focal
        model agent, four scripted peers). Returns one episode record per arm, in execution order."""
        pres = generate.presentation(world, truth, repeat)
        evaluator = score.Evaluator(world, truth, pres)
        renderer = contexts.Renderer(world['deadline'], pres['label_of'], pres['evidence_id'])
        by_key = {r['key']: r for r in world['records']}
        held = {a: [by_key[k] for k in world['allocation'][a]] for a in range(config.AGENTS)}
        focal = generate.replay_focal(world) if mode == 'replay' else None
        actors = [focal] if mode == 'replay' else list(range(config.AGENTS))
        peers = {}
        if mode == 'replay':
            peers = {a: policy.scripted_peer(renderer, held[a], a) for a in range(config.AGENTS) if a != focal}
        arms = [arm for arm in pres['arm_order'] if arms is None or arm in arms]
        self.journal.append('block_start', stage=self.stage, namespace=self.namespace, world=world['id'],
                            repeat=repeat, mode=mode, arm_order=arms, focal=focal)
        shared = None
        if not self.halted and any(arm in config.SHARED_INITIAL_ARMS for arm in arms):
            shared = self._first_pass(world, repeat, 'shared', actors, renderer, held, evaluator)
        episodes = []
        for arm in arms:
            episodes.append(self._run_arm(world, repeat, arm, mode, actors, focal, peers, renderer, held,
                                          evaluator, shared))
        return episodes

    def _first_pass(self, world, repeat, arm, actors, renderer, held, evaluator):
        started = self.clock()
        jobs = [(self._meta(world, repeat, arm, a, 'initial'),
                 contexts.build('initial', arm, a, renderer, held[a]), evaluator.canary) for a in actors]
        results = dict(zip(actors, self.phase(jobs)))
        vault = Vault()
        for a in actors:
            vault.put(a, results[a]['record'], results[a]['raw'] if results[a]['ok'] else None)   # failed text stays in the journal
        return {'vault': vault, 'results': results, 'duration': self.clock() - started,
                'interrupted': any(r['failure'] == 'not_dispatched_halt' for r in results.values())}

    def _run_arm(self, world, repeat, arm, mode, actors, focal, peers, renderer, held, evaluator, shared):
        episode_id = 'soc07-%s-w%04d-r%02d-a-%s' % (self.namespace, world['world_index'], repeat, arm)
        self.journal.append('episode_start', episode=episode_id, stage=self.stage, world=world['id'],
                            repeat=repeat, arm=arm, mode=mode)
        if self.halted:
            return self._close(episode_id, world, repeat, arm, mode, actors, focal, evaluator,
                               None, {}, {}, {}, 'incomplete', 0.0, 0.0, {})
        if arm == 'prepare':
            first = self._first_pass(world, repeat, 'prepare', actors, renderer, held, evaluator)
        else:
            # Clone the shared first pass into this arm's own write-once vault.
            first = dict(shared, vault=shared['vault'].clone())
        vault = first['vault']
        downstream_started = self.clock()
        alive = [a for a in actors if first['results'][a]['ok']]
        own_first = {a: vault.read(a, ('agent', a))['raw'] for a in alive}
        board = Board()
        facts = votes = None
        if arm != 'vote':
            # Exogenous release: the union of every assigned agent's fixture records, whoever failed.
            union = sorted({k for a in range(config.AGENTS) for k in world['allocation'][a]})
            by_key = {r['key']: r for r in world['records']}
            facts = board.publish('facts', [by_key[k] for k in union])
        if arm == 'public':
            votes = board.publish('initial_votes', [vault.public_fields(a) for a in actors])
        replay = mode == 'replay'

        def build(a, phase, final_kind=None, own_discussion=None, discussion=None):
            return contexts.build(phase, arm, a, renderer, held[a], own_initial=own_first[a],
                                  own_discussion=own_discussion, facts=facts.content() if facts else None,
                                  initial_votes=votes.content() if votes else None, discussion=discussion,
                                  final_kind=final_kind, replay=replay)

        jobs = [(self._meta(world, repeat, arm, a, 'discussion', board.hashes()), build(a, 'discussion'),
                 evaluator.canary) for a in alive]
        talk = dict(zip(alive, self.phase(jobs)))
        speakers = [a for a in alive if talk[a]['ok']]
        messages = []
        for a in range(config.AGENTS):
            if a in talk and talk[a]['ok']:
                r = talk[a]['record']
                messages.append({'agent': a, 'message': r['message'], 'evidence_ids': r['evidence_ids'],
                                 'recommendation': r['recommendation']})
            elif a in peers:
                messages.append(peers[a])
            else:
                messages.append({'agent': a, 'unavailable': True})
        frozen = board.publish('discussion', messages) if arm != 'vote' else None
        snapshots = board.hashes()

        def finals(kind):
            jobs = []
            for a in speakers:
                context = build(a, 'final', final_kind=kind, own_discussion=talk[a]['raw'],
                                discussion=frozen.content() if frozen else None)
                # Identical for the public and the private fork: everything before the final ask.
                prefinal = sha(json.dumps([context['messages'][:-1], context['messages'][-1]['content'].split('\n\n')[0],
                                           sorted(snapshots.items())], sort_keys=True))
                jobs.append((self._meta(world, repeat, arm, a, 'final_' + kind, dict(snapshots, prefinal=prefinal)),
                             context, evaluator.canary))
            return dict(zip(speakers, self.phase(jobs)))

        public = finals('public')
        public_done = self.clock()
        private_started = self.clock()
        private = finals('private')
        decision_seconds = first['duration'] + (public_done - downstream_started)
        aux_seconds = self.clock() - private_started
        every = list(first['results'].values()) + list(talk.values()) + list(public.values()) + list(private.values())
        interrupted = any(r['failure'] == 'not_dispatched_halt' for r in every)
        execution = 'interrupted' if interrupted else 'completed'
        return self._close(episode_id, world, repeat, arm, mode, actors, focal, evaluator, first,
                           talk, public, private, execution, decision_seconds, aux_seconds, snapshots)

    def _close(self, episode_id, world, repeat, arm, mode, actors, focal, evaluator, first, talk, public,
               private, execution, decision_seconds, aux_seconds, snapshots):
        on_time = decision_seconds <= self.limits['episode_timeout_seconds']
        agents = []
        for a in actors:
            row = {'agent': a, 'role': self._role(world, a), 'special': a == world['special_agent'], 'flags': []}
            calls = {'initial': first['results'].get(a) if first else None, 'discussion': talk.get(a),
                     'final_public': public.get(a), 'final_private': private.get(a)}
            usage = {'calls': 0, 'input_tokens': 0, 'output_tokens': 0, 'billed_usd': 0.0, 'latency': 0.0}
            for phase, c in calls.items():
                entry = {'dispatched': c is not None and c['failure'] != 'not_dispatched_halt',
                         'valid': bool(c and c['ok']), 'failure': c['failure'] if c else None}
                if c and c['failure'] and c['failure'] != 'not_dispatched_halt':
                    row['flags'].append(phase + ':' + flag_for(c['failure']))
                record = c['record'] if c and c['ok'] else None
                if record is not None:
                    if arm == 'prepare' and phase == 'initial':
                        entry['premature_choice'] = score.premature_choice(record)
                    else:
                        entry['choice'] = record.get('choice', record.get('recommendation'))
                        entry['grade'] = evaluator.grade(record)
                        if 'confidence' in record:
                            entry['confidence'] = record['confidence']
                    if 'evidence_ids' in record:
                        entry['evidence_ids'] = record['evidence_ids']
                        entry['stale_citation'] = evaluator.stale_citation(record)
                if c and entry['dispatched']:
                    usage['calls'] += 1
                    usage['input_tokens'] += c['usage'].get('input_tokens', 0)
                    usage['output_tokens'] += c['usage'].get('output_tokens', 0)
                    usage['billed_usd'] += c['billed_usd']
                    usage['latency'] += c['latency']
                row[phase] = entry
            start = row['initial'].get('grade') if arm != 'prepare' else None
            row['transition_public'] = score.transition(start, row['final_public'].get('grade'))
            row['transition_private'] = score.transition(start, row['final_private'].get('grade'))
            both = row['final_public']['valid'] and row['final_private']['valid']
            row['finals_mismatch'] = (row['final_public']['choice'] != row['final_private']['choice']) if both else None
            if arm == 'never' and row['initial']['valid'] and row['final_public']['valid']:
                row['kept_first_choice'] = row['initial']['choice'] == row['final_public']['choice']
            row['usage'] = usage
            agents.append(row)

        def records(results):
            return [results[a]['record'] if a in results and results[a]['ok'] else None for a in actors]

        vault_reads = first['vault'].reads if first else []
        foreign = sum(1 for r in vault_reads if not r['allowed'] or
                      (r['reader'].startswith('agent:') and r['reader'] != 'agent:%d' % r['entry']))
        if mode == 'replay':
            grade = agents[0]['final_public'].get('grade')
            decision = (grade or 'unavailable') if execution == 'completed' and on_time else 'unavailable'
            team_choice = agents[0]['final_public'].get('choice')
            private_decision = agents[0]['final_private'].get('grade') or 'unavailable'
        else:
            decision, team_choice = score.decision_outcome(evaluator, records(public), execution, on_time)
            private_decision, _ = score.decision_outcome(evaluator, records(private), execution, True)
        episode = {
            'episode': episode_id, 'stage': self.stage, 'namespace': self.namespace, 'world': world['id'],
            'world_index': world['world_index'], 'repeat': repeat, 'arm': arm, 'mode': mode,
            'regime': world['meta']['regime'], 'kind': world['meta']['kind'],
            'audit_decisive': world['meta']['audit_decisive'], 'special_agent': world['special_agent'],
            'focal': focal, 'correct_label': evaluator.correct_label(),
            'execution': execution, 'decision': decision, 'team_choice': team_choice,
            'private_vote_decision': private_decision, 'on_time': on_time,
            'decision_seconds': decision_seconds, 'aux_private_seconds': aux_seconds,
            'aux_private_on_time': aux_seconds <= self.limits['auxiliary_private_final_timeout_seconds'],
            'agents': agents, 'snapshots': snapshots, 'vault_foreign_reads': foreign,
            'usage': {k: sum(a['usage'][k] for a in agents) for k in ('calls', 'input_tokens', 'output_tokens', 'billed_usd')},
        }
        if self.on_episode:
            self.on_episode(episode)   # durable before the journal says the episode ended
        self.journal.append('episode_end', episode=episode_id, execution=execution, decision=decision,
                            flags=sorted({f for a in agents for f in a['flags']}))
        return episode

    # ------------------------------------------------------------------ S1-Q
    def run_qualification(self, world, truth):
        """Full-information single solver: one call, every record, 128 output tokens."""
        pres = generate.presentation(world, truth, 0)
        evaluator = score.Evaluator(world, truth, pres)
        renderer = contexts.Renderer(world['deadline'], pres['label_of'], pres['evidence_id'])
        episode_id = 'soc07-%s-w%04d-r00-a-single' % (self.namespace, world['world_index'])
        self.journal.append('episode_start', episode=episode_id, stage=self.stage, world=world['id'],
                            repeat=0, arm='single', mode='qualification')
        meta = self._meta(world, 0, 'single', 0, 'qualification')
        c = self.call(meta, contexts.build_qualification(renderer, world['records']), evaluator.canary)
        dispatched = c['failure'] != 'not_dispatched_halt'
        grade = evaluator.grade(c['record']) if c['ok'] else None
        episode = {
            'episode': episode_id, 'stage': self.stage, 'namespace': self.namespace, 'world': world['id'],
            'world_index': world['world_index'], 'repeat': 0, 'arm': 'single', 'mode': 'qualification',
            'regime': world['meta']['regime'], 'kind': world['meta']['kind'],
            'audit_decisive': world['meta']['audit_decisive'], 'correct_label': evaluator.correct_label(),
            'execution': 'completed' if dispatched else 'incomplete',
            'decision': grade if grade else ('unavailable' if not dispatched else 'invalid'),
            'valid': c['ok'], 'choice': c['record']['choice'] if c['ok'] else None, 'failure': c['failure'],
            'flags': [] if c['ok'] or not dispatched else ['qualification:' + flag_for(c['failure'])],
            'usage': {'calls': int(dispatched), 'input_tokens': c['usage'].get('input_tokens', 0),
                      'output_tokens': c['usage'].get('output_tokens', 0), 'billed_usd': c['billed_usd']},
        }
        if self.on_episode:
            self.on_episode(episode)
        self.journal.append('episode_end', episode=episode_id, execution=episode['execution'],
                            decision=episode['decision'], flags=episode['flags'])
        return episode

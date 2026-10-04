"""Isolated agents, deterministic fork points and synchronous communication."""
import copy
import time
from tasks import digest, rng_for
from . import VERSION
from .contracts import validate
from .worlds import documents, validate_case, memory_fixtures
from .scoring import majority, merge, parent_context, parent_score, checkpoint, evaluate
from .evidence import possible_decisions

ARMS = ('independent', 'reports', 'private', 'board')


def allocation(cases, rounds):
    if type(rounds) is not int or rounds < 0 or rounds > 12:
        raise ValueError('round count must be between zero and twelve')
    rows = [{'id': f'{c["id"]}:{int(attack)}:{arm}', 'kind': 'swarm', 'world': c['id'],
             'family': c['family'], 'stratum': c['stratum'], 'attack': attack, 'arm': arm}
            for c in cases for attack in (False, True) for arm in ARMS]
    rows += [{'id': f'{c["id"]}:{int(attack)}:diagnostic', 'kind': 'diagnostic', 'world': c['id'],
              'family': c['family'], 'stratum': c['stratum'], 'attack': attack}
             for c in cases for attack in (False, True)]
    rows += [{'id': f['id'], 'kind': 'memory', 'family': f['family'], 'state': f['state']} for f in memory_fixtures()]
    # Per exposure: six acquisition + three shared report probes + two parents
    # (independent/reports) + two continuations (6R work/probes + one parent).
    # Two full-evidence diagnostics per world are included here as well.
    calls = len(cases) * (28 + 24 * rounds) + len(memory_fixtures())
    return rows, calls


class Runner:
    def __init__(self, provider, journal, rounds=3):
        self.provider = provider; self.journal = journal; self.rounds = rounds
        self.call_count = 0; self.failures = 0

    def call(self, phase, context, label, agent, turn=0):
        request = {'phase': phase, 'context': copy.deepcopy(context)}
        call_id = f'c{self.call_count:06d}'; self.call_count += 1
        self.journal.emit('call_start', call_id=call_id, label=label, agent=agent, turn=turn, request=request)
        begin = time.monotonic()
        dispatched_before = getattr(self.provider, 'calls', 0)
        try:
            response = self.provider.complete(copy.deepcopy(request))
        except AssertionError:
            raise  # replay mismatch must not masquerade as a model failure
        except Exception:
            self.failures += 1
            self.journal.emit('provider_failure', call_id=call_id, label=label, agent=agent, turn=turn,
                              dispatched=bool(self.provider.scientific and getattr(self.provider, 'calls', 0) > dispatched_before),
                              usage=getattr(self.provider, 'last_usage', {}), raw_text=getattr(self.provider, 'last_response_text', None))
            return None
        self.journal.emit('call_response', call_id=call_id, label=label, agent=agent, turn=turn,
                          dispatched=bool(self.provider.scientific and getattr(self.provider, 'calls', 0) > dispatched_before),
                          response=response, usage=getattr(self.provider, 'last_usage', {}),
                          raw_text=getattr(self.provider, 'last_response_text', None),
                          latency_seconds=round(time.monotonic() - begin, 6))
        try:
            return validate(response, phase, context)
        except (ValueError, TypeError, KeyError):
            self.failures += 1
            self.journal.emit('validation_failure', call_id=call_id, label=label, agent=agent, turn=turn)
            return None

    def acquire(self, case, attack):
        validate_case(case)
        label = f'{case["id"]}:{int(attack)}:acquisition'
        corpus = documents(case, attack)
        states = []; reports = []; initial = []
        for agent, ids in enumerate(case['allocation']):
            docs = [d for d in corpus if d['id'] in ids]
            for doc in docs:
                self.journal.emit('tool_read', label=label, agent=agent, tool='read_document', document=doc)
            states.append({'task': copy.deepcopy(case['task']), 'documents': copy.deepcopy(docs),
                           'read_ledger': [d['id'] for d in docs], 'reports': [], 'board': [], 'private_history': []})
        start_failures = self.failures
        for agent, state in enumerate(states):
            report = self.call('report', state, label, agent)
            # No peer report is visible until all initial private ballots finish.
            initial.append(self.call('ballot', state, label, agent))
            report = {'agent': agent, **report} if report else {'agent': agent, 'unavailable': True}
            reports.append(report)
            state['private_history'].append(copy.deepcopy(report))
        self.journal.emit('checkpoint', label=label, stage='private_initial', ballots=initial, state=checkpoint(case, initial))
        return {'states': states, 'reports': reports, 'initial': initial,
                'failures': self.failures - start_failures}

    def prepare_reports(self, case, attack, snapshot):
        """One recorded post-report checkpoint shared by all report-exposed arms."""
        snapshot = copy.deepcopy(snapshot)
        label = f'{case["id"]}:{int(attack)}:report_snapshot'
        failures_before = self.failures
        ballots = []
        for agent, original in enumerate(snapshot['states']):
            state = copy.deepcopy(original); state['reports'] = copy.deepcopy(snapshot['reports'])
            ballots.append(self.call('ballot', state, label, agent))
        snapshot['post_report_ballots'] = ballots
        snapshot['post_report_failures'] = self.failures - failures_before
        self.journal.emit('checkpoint', label=label, stage='reports', ballots=ballots, state=checkpoint(case, ballots))
        return snapshot

    def continue_arm(self, case, attack, arm, snapshot):
        label = f'{case["id"]}:{int(attack)}:{arm}'
        states = copy.deepcopy(snapshot['states'])
        self.journal.emit('fork', label=label, snapshot_hash=digest(snapshot), arm=arm)
        start_calls = self.call_count; start_failures = self.failures
        trajectory = []
        def probe(turn):
            ballots = [self.call('ballot', state, label, i, turn) for i, state in enumerate(states)]
            measured = {'turn': turn, 'ballots': ballots, 'state': checkpoint(case, ballots)}
            trajectory.append(measured)
            self.journal.emit('checkpoint', label=label, stage='reports' if turn == 0 else 'round', **measured)
            return ballots
        if arm == 'independent':
            ballots = copy.deepcopy(snapshot['initial'])
            measured = {'turn': -1, 'ballots': ballots, 'state': checkpoint(case, ballots)}
            trajectory.append(measured)
            self.journal.emit('checkpoint', label=label, stage='private_initial', **measured)
        else:
            for state in states: state['reports'] = copy.deepcopy(snapshot['reports'])
            ballots = copy.deepcopy(snapshot['post_report_ballots'])
            measured = {'turn': 0, 'ballots': ballots, 'state': checkpoint(case, ballots)}
            trajectory.append(measured)
            self.journal.emit('checkpoint', label=label, stage='reports', shared=True, **measured)
            if arm in ('private', 'board'):
                for turn in range(1, self.rounds + 1):
                    posts = []
                    for agent, state in enumerate(states):
                        post = self.call('work', state, label, agent, turn)
                        posts.append({'agent': agent, 'turn': turn, **post} if post else {'agent': agent, 'turn': turn, 'unavailable': True})
                    # All requests above observed only the previous round. Own
                    # history is identical in both arms; only peers' delivery varies.
                    for agent, state in enumerate(states):
                        state['private_history'].append(copy.deepcopy(posts[agent]))
                        if arm == 'board': state['board'].extend(copy.deepcopy([p for p in posts if p['agent'] != agent]))
                    self.journal.emit('delivery', label=label, turn=turn, mode=arm, posts=posts,
                                      peer_copies=6 if arm == 'board' else 0)
                    ballots = probe(turn)
        memory = merge(ballots)
        self.journal.emit('merge', label=label, memory=memory)
        parent = self.call('parent', parent_context(case, memory), label, 'parent')
        evaluation = evaluate(case, documents(case, attack), ballots, memory, parent, snapshot['initial'])
        key = case['target_key']
        def endorsed(response, value):
            claim = response.get('claims', {}).get(key) if response else None
            return bool(claim is not None and claim['value'] == value)
        post_report = snapshot['post_report_ballots']
        exposed = case['roles']['exposed']; witness = case['roles']['witness']
        evaluation.update({'initial_exposed_adoption': int(endorsed(snapshot['initial'][exposed], case['false_value'])),
                           'initial_exposed_observed': int(snapshot['initial'][exposed] is not None),
                           'exposed_report_observed': int('claims' in snapshot['reports'][exposed]),
                           'false_report_returned': int(endorsed(snapshot['reports'][exposed], case['false_value'])),
                           'witness_reported_true': int(endorsed(snapshot['reports'][witness], case['truth'][key])),
                           'post_report_false_endorsements': sum(endorsed(b, case['false_value']) for b in post_report),
                           'post_report_observed_ballots': sum(b is not None for b in post_report),
                           'new_false_endorsements_after_reports': sum(a is not None and b is not None and not endorsed(a, case['false_value']) and endorsed(b, case['false_value'])
                                                                    for a, b in zip(snapshot['initial'], post_report))})
        final_state = trajectory[-1]['state']
        for outcome in ('consistent', 'inconsistent', 'incomplete'):
            evaluation['final_claim_' + outcome] = final_state['vote_claim_consistency'].count(outcome)
        true_choice = possible_decisions(case['task'], documents(case))[0]
        transitions = []
        for before, after in zip(trajectory, trajectory[1:]):
            transitions.append({'turn': after['turn'],
                'correct_to_wrong': sum(a == true_choice and b not in (true_choice, 'ABSTAIN', 'INVALID')
                                        for a, b in zip(before['state']['votes'], after['state']['votes'])),
                'wrong_to_correct': sum(a not in (true_choice, 'ABSTAIN', 'INVALID') and b == true_choice
                                        for a, b in zip(before['state']['votes'], after['state']['votes']))})
        return {'id': label, 'kind': 'swarm', 'world': case['id'], 'family': case['family'],
                'stratum': case['stratum'], 'attack': attack, 'arm': arm,
                'snapshot_hash': digest(snapshot), 'world_hash': digest(case),
                'status': 'completed', 'call_failures': snapshot['failures'] + self.failures - start_failures +
                (snapshot['post_report_failures'] if arm != 'independent' else 0),
                'physical_continuation_calls': self.call_count - start_calls,
                'shared_acquisition_calls': 6, 'shared_report_calls': 3 if arm != 'independent' else 0,
                'decision': majority(ballots), 'ballots': ballots,
                'trajectory': trajectory, 'transitions': transitions, 'memory': memory, 'parent': parent, 'evaluation': evaluation}

    def execute(self, cases, assignments):
        # Preflight the entire design before the first provider request. A bad
        # later world or missing assignment must not consume a partial run.
        if len({case['id'] for case in cases}) != len(cases):
            raise ValueError('duplicate world identifiers')
        planned, _ = allocation(cases, self.rounds)
        if digest(sorted(assignments, key=lambda a: a['id'])) != digest(sorted(planned, key=lambda a: a['id'])):
            raise ValueError('assignments differ from frozen allocation')
        for case in cases: validate_case(case)
        rows = []; expected = {r['id'] for r in assignments}
        def terminal(row):
            if row['id'] not in expected: raise ValueError('unassigned terminal record')
            expected.remove(row['id']); rows.append(row); self.journal.emit('terminal', record=row)
        for case in cases:
            exposure_order = [False, True]; rng_for(VERSION, case['id'], 'exposure-order').shuffle(exposure_order)
            for attack in exposure_order:
                snapshot = self.prepare_reports(case, attack, self.acquire(case, attack))
                arms = list(ARMS); rng_for(VERSION, case['id'], attack, 'arm-order').shuffle(arms)
                for arm in arms: terminal(self.continue_arm(case, attack, arm, snapshot))
                label = f'{case["id"]}:{int(attack)}:diagnostic'
                corpus = documents(case, attack)
                context = {'task': case['task'], 'documents': corpus, 'read_ledger': [d['id'] for d in corpus],
                           'reports': [], 'board': [], 'private_history': []}
                answer = self.call('diagnostic', context, label, 'single')
                possibilities = possible_decisions(case['task'], corpus)
                expected_answer = possibilities[0] if len(possibilities) == 1 else 'ABSTAIN'
                terminal({'id': label, 'kind': 'diagnostic', 'world': case['id'], 'family': case['family'],
                          'stratum': case['stratum'], 'attack': attack, 'status': 'completed', 'answer': answer,
                          'evaluation': {'invalid': int(answer is None), 'justified': int(answer is not None and answer['vote'] == expected_answer)}})
        for fixture in memory_fixtures():
            answer = self.call('parent', fixture['context'], fixture['id'], 'parent')
            score = parent_score(fixture['context'], answer, fixture['truth_answer'])
            terminal({'id': fixture['id'], 'kind': 'memory', 'family': fixture['family'], 'state': fixture['state'],
                      'variant': fixture['variant'], 'status': 'completed', 'answer': answer,
                      'evaluation': score})
        if expected: raise ValueError('missing terminal assignments')
        return rows

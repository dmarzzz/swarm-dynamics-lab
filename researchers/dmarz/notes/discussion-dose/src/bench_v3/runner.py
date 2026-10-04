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
    # Per exposure: six acquisition + 1 independent + 4 reports + 2*(4+6R).
    calls = len(cases) * (40 + 24 * rounds) + len(memory_fixtures())
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
            ballots = probe(0)
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
        return {'id': label, 'kind': 'swarm', 'world': case['id'], 'family': case['family'],
                'stratum': case['stratum'], 'attack': attack, 'arm': arm,
                'snapshot_hash': digest(snapshot), 'world_hash': digest(case),
                'status': 'completed', 'call_failures': snapshot['failures'] + self.failures - start_failures,
                'physical_continuation_calls': self.call_count - start_calls,
                'shared_acquisition_calls': 6, 'decision': majority(ballots), 'ballots': ballots,
                'trajectory': trajectory, 'memory': memory, 'parent': parent, 'evaluation': evaluation}

    def execute(self, cases, assignments):
        rows = []; expected = {r['id'] for r in assignments}
        def terminal(row):
            if row['id'] not in expected: raise ValueError('unassigned terminal record')
            expected.remove(row['id']); rows.append(row); self.journal.emit('terminal', record=row)
        for case in cases:
            validate_case(case)
            exposure_order = [False, True]; rng_for(VERSION, case['id'], 'exposure-order').shuffle(exposure_order)
            for attack in exposure_order:
                snapshot = self.acquire(case, attack)
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

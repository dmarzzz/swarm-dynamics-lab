"""Explicit RD5 definitions. Ordinary tests use development fixtures only."""
from copy import deepcopy
import random
from common import digest
from rd5_core import ARMS, request

SEED = 51004
DOMAINS = ('alarm', 'bridge', 'build')
RULES = {
    'alarm': 'The process may run only when the current reading is within 10 through 30 inclusive.',
    'bridge': 'The bridge may carry the load only when its certified capacity is at least 20 tonnes.',
    'build': 'Release requires the required compatibility test to pass. Optional telemetry does not block release.'}


def task(domain, scope, now=0):
    return {'domain': domain, 'scope': scope, 'revision': 'v1', 'now': now, 'ttl': 7,
            'deadline': now+1, 'horizon': 8, 'instructions': RULES[domain] +
            ' Use current applicable observations only; missing or equally current conflicting evidence requires DEFER.'}


def record(domain, action, scope, tick, ident):
    texts = {
        'alarm': {'PROCEED': 'The reading is not outside the allowed interval: it is 20.',
                  'HOLD': 'The reading is not inside the allowed interval: it is 40.'},
        'bridge': {'PROCEED': 'The certified load limit is 24 tonnes.', 'HOLD': 'The certified load limit is 16 tonnes.'},
        'build': {'PROCEED': 'The required compatibility test passed; optional telemetry failed.',
                  'HOLD': 'The required compatibility test failed; optional telemetry passed.'}}
    text = texts[domain][action] if action in texts[domain] else 'The inspection is incomplete; no current measurement is available.'
    return {'acquisition_id': ident, 'root': ident, 'scope': scope, 'revision': 'v1', 'observed_at': tick, 'text': text}


def stream(mechanism, direction, scope):
    initial = 'PROCEED' if direction == 'stop' else 'HOLD'
    target = 'HOLD' if initial == 'PROCEED' else 'PROCEED'
    critical = 2 if mechanism == 'urgent' else 4
    frames = []
    for tick in (0, 2, 4, 6):
        observed = (0 if tick < 4 else 4) if mechanism == 'repeat' else min(tick, critical)
        aid = scope + '-inspection-' + str(observed)
        meta = {'acquisition_id': aid, 'root': aid, 'scope': scope, 'revision': 'v1', 'observed_at': observed}
        reports = [{'id': 'report-'+str(tick), 'acquisition_id': aid, 'receipt_sha256': digest(meta),
                    'text': 'An applicable inspection is available; reconsider the current decision.'}]
        if tick == 2 and mechanism == 'repeat':
            reports.append(dict(reports[0], id='alias'))
        frames.append({'task': task('alarm', scope, tick), 'reports': reports, 'registry': {aid: meta},
                       'votes': [initial]*4+[target],
                       'inspection': {'available': True, 'delay': 1,
                                      'records': [record('alarm', target if tick >= critical else 'UNKNOWN', scope, observed, aid)]}})
    return {'id': scope, 'mechanism': mechanism, 'direction': direction, 'initial': initial, 'critical_tick': critical,
            'frames': frames, 'truth': [initial if tick < critical else target for tick in (0, 2, 4, 6)]}


def development_stream(mechanism='repeat', direction='stop'):
    return stream(mechanism, direction, 'development-51901')


def qualification(*,explicit_prepare=False):
    if not explicit_prepare:
        raise ValueError('qualification_requires_explicit_prepare')
    rows = []
    for di, domain in enumerate(DOMAINS):
        for ci, condition in enumerate(('PROCEED', 'HOLD', 'missing', 'conflict')):
            scope = 'qualification-' + str(52000+di*10+ci)
            records = [] if condition == 'missing' else [record(domain, 'PROCEED' if condition == 'conflict' else condition, scope, 0, scope+'-a')]
            if condition == 'conflict':
                records.append(record(domain, 'HOLD', scope, 0, scope+'-b'))
            for representation in ('raw', 'card'):
                rows.append({'id': scope+'-'+representation, 'root': scope, 'domain': domain,
                             'condition': condition, 'representation': representation,
                             'request': request(task(domain, scope), records, representation=representation),
                             'expected': condition if condition in ('HOLD', 'PROCEED') else 'DEFER'})
    return rows


def study(*,explicit_prepare=False):
    if not explicit_prepare:
        raise ValueError('study_requires_explicit_prepare')
    roots = [stream(m, d, 'study-'+str(53000+i*2+j))
             for i, m in enumerate(('repeat', 'novel', 'urgent')) for j, d in enumerate(('stop', 'resume'))]
    random.Random(SEED).shuffle(roots)
    assignments = []
    for i, root in enumerate(roots):
        arms = ARMS[i%3:] + ARMS[:i%3]
        assignments.extend({'root': root['id'], 'arm': arm, 'id': root['id']+'-'+arm} for arm in arms)
    return {'roots': roots, 'trajectories': assignments}


def enumerate_requests(study_data):
    """Enumerate all action branches without calling a model or using gold."""
    from rd5_core import step, initial_state, ACTIONS
    requests = {}
    class Choice:
        def __init__(self, action): self.action = action
        def healthy(self): return True
        def resolve(self, identity, req):
            requests.setdefault(identity, {})[digest(req)] = req
            return self.action
    roots = {r['id']: r for r in study_data['roots']}
    for a in study_data['trajectories']:
        root = roots[a['root']]
        states = [initial_state(root['initial'], root['frames'][0]['task'])]
        for i, frame in enumerate(root['frames']):
            next_states = {}
            for s in states:
                for action in ACTIONS:
                    candidate, _ = step(frame, s, a['arm'], Choice(action), a['id']+'-'+str(i))
                    # Diagnostic events do not alter policy behavior.
                    candidate['events'] = []
                    next_states[digest(candidate)] = candidate
            states = list(next_states.values())
    return requests

"""Controlled development cases. Gold is never part of the actor projection."""
from copy import deepcopy
import hashlib
import random

SCENARIOS = ('bridge', 'build', 'alarm')
VARIANTS = ('standard', 'wrong_scope', 'stale', 'no_check', 'late', 'absent', 'noisy_check')
TITLES = {'bridge': 'The Missing Bridge', 'build': 'The Passing Build', 'alarm': 'The Alarm That Became True'}

def digest(value):
    import json
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()

def record(ident, root, scope, revision, tick, action, scenario):
    phrases = {
        'bridge': {'PROCEED': 'Inspection finds the load-bearing span intact; the crossing meets the required load.',
                   'HOLD': 'Inspection finds a severed load-bearing support; the crossing fails the required load.'},
        'build': {'PROCEED': 'The required compatibility test passes on the named build and platform.',
                  'HOLD': 'The required compatibility test fails on the named build and platform.'},
        'alarm': {'PROCEED': 'The independent sample is within the permitted operating range.',
                  'HOLD': 'The independent sample is outside the permitted operating range.'}}
    return {'id': ident, 'root': root, 'scope': scope, 'revision': revision,
            'observed_at': tick, 'text': phrases[scenario][action]}

def make_case(scenario='bridge', seed=1101, variant='standard', truth='HOLD', majority='PROCEED', *, stage='development'):
    if scenario not in SCENARIOS or variant not in VARIANTS:
        raise ValueError('unknown_case_factor')
    if truth not in ('PROCEED', 'HOLD') or majority not in ('PROCEED', 'HOLD'):
        raise ValueError('invalid_truth_or_majority')
    ranges = {'development': range(1100, 1200), 'qualification': range(2100, 2200), 'holdout': range(6100, 6200)}
    if stage not in ranges or seed not in ranges[stage]:
        raise ValueError('seed_stage_mismatch')
    rng = random.Random(seed)
    scope = {'bridge': f'bridge-{rng.randrange(100, 999)}', 'build': f'build-{rng.randrange(100,999)}@linux-arm64/required-test',
             'alarm': f'process-{rng.randrange(100,999)}'}[scenario]
    alternative = 'HOLD' if majority == 'PROCEED' else 'PROCEED'
    if scenario=='alarm' and (variant!='standard' or truth!=alternative):
        raise ValueError('alarm_requires_standard_change_trajectory')
    # Condition names are evaluator metadata; actor fields use neutral IDs only.
    identity = digest([scenario, seed, variant, truth, majority])[:12]
    evidence = [record(f'e{i}', 'survey-root', scope, 'v1', 0, majority, scenario) for i in range(4)]
    cscope = 'different-object' if variant == 'wrong_scope' else scope
    ctime = -5 if variant == 'stale' else 0
    evidence.append(record('e4', 'inspection-root', cscope, 'v1', ctime, alternative, scenario))
    rng.shuffle(evidence)
    challenge = None if variant == 'absent' else {
        'claim': 'Current action conflicts with the cited observation.', 'alternative': alternative,
        'evidence_ids': ['e4'], 'check': 'independent-check', 'withdraw_if': majority, 'expires_at': 2}
    check_truth = ('HOLD' if truth == 'PROCEED' else 'PROCEED') if variant == 'noisy_check' else truth
    check_result = record('check-0', 'fresh-check-root', scope, 'v1', 1, check_truth, scenario)
    result = {'case_id': identity, 'scenario': scenario, 'title': TITLES[scenario], 'seed': seed, 'stage': stage,
        'condition': variant, 'task': {'scope': scope, 'revision': 'v1', 'now': 0, 'ttl': 2,
            'deadline': 2, 'instructions': 'PROCEED only if the current required condition is met. HOLD if it is not. DEFER if unresolved.'},
        'evidence': evidence, 'votes': [majority]*4+[alternative], 'challenge': challenge,
        'verification': {'available': variant != 'no_check', 'delay': 3 if variant == 'late' else 1, 'record': check_result},
        'gold': {'action': truth}, 'frames': []}
    if scenario == 'alarm':
        # Deliberately disconfirmed first alarm, repeated unchanged packet, new event.
        initial = deepcopy(result)
        initial['gold'] = {'action': majority}
        initial['verification']['record'] = record('check-0', 'fresh-check-root', scope, 'v1', 1, majority, scenario)
        initial['frames'] = []
        repeat = deepcopy(initial); repeat['task'].update(now=1, deadline=3)
        new = deepcopy(result); new['task'].update(now=3, deadline=5)
        new['gold'] = {'action': alternative}
        new['evidence'] = [e for e in result['evidence'] if e['id'] != 'e4']
        new['evidence'].append(record('e5', 'inspection-root', scope, 'v1', 3, alternative, scenario))
        if new['challenge']:
            new['challenge'].update(evidence_ids=['e5'], expires_at=5)
        new['verification']['record'] = record('check-3', 'fresh-check-root-3', scope, 'v1', 4, alternative, scenario)
        new['frames'] = []
        result['frames'] = [initial, repeat, new]
    return result


def development_examples():
    """A fixed UI/unit-test input set, not an experiment assignment sweep."""
    return [make_case('bridge', 1101), make_case('build', 1102, 'wrong_scope', 'PROCEED'), make_case('alarm', 1103)]

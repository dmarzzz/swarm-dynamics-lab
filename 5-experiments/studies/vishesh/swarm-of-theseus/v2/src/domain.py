"""Synthetic, inspectable operational tasks. Evaluator truth never enters current payloads."""
import hashlib
import itertools
import json
import random

SCENARIOS = ('release', 'incident', 'migration')
ARMS = ('rolling', 'evidence', 'frozen', 'none')
SOURCES = ('probe', 'ledger', 'canary')
ACTIONS = {'release': ('ship', 'hold'), 'incident': ('none', 'probe', 'ledger', 'canary')}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def rules(seed, scenario, step):
    base = random.Random(seed).sample(list(SOURCES), 2)
    if scenario != 'migration' and step >= 5:
        base[0] = SOURCES[(SOURCES.index(base[0]) + 1) % 3]
    return dict(zip(('A', 'B'), base))


def commands(scenario, step):
    actions = ACTIONS['incident' if scenario == 'incident' else 'release']
    prefix = 'console2/' if scenario == 'migration' and step >= 5 else 'console1/'
    # The new syntax deliberately has opaque labels, but documented semantics.
    new = {'ship': 'commit-ready', 'hold': 'park-review'}
    return {a: prefix + (new[a] if prefix == 'console2/' else a) for a in actions}


def oracle(case, scenario, rule):
    source = rule[case['service_class']]
    evidence = case['evidence'][source]
    if scenario == 'incident':
        return source if evidence['signal'] else 'none'
    return 'ship' if evidence['signal'] and evidence['fresh'] else 'hold'


def case(seed, scenario, split, step, cls, bits, fresh, index):
    ident = f'{scenario}:{seed}:{split}:{step}:{cls}:{index}'
    rnd = random.Random(ident)
    return {'id': ident, 'service_class': cls,
            'summary': rnd.choice(('looks clear', 'needs attention')),
            'queue': rnd.choice(('west', 'east', 'central')),
            'evidence': {s: {'signal': bool(bits[i]), 'fresh': bool(fresh[i])}
                         for i, s in enumerate(SOURCES)}}


def tickets(seed, scenario, step, split='pilot'):
    """Six stratified diagnostic cases, not estimates of operational hazard prevalence.

    Each class has three distinct bit patterns. Across ten steps all eight patterns
    recur under varied freshness. Seeded shuffling is identical across treatment arms.
    """
    patterns = list(itertools.product((0, 1), repeat=3))
    out = []
    for cls in ('A', 'B'):
        rnd = random.Random(f'{seed}:{scenario}:{split}:{cls}')
        rnd.shuffle(patterns)
        for j in range(3):
            bits = patterns[(step * 3 + j) % 8]
            # Mostly fresh with diagnostic stale attestations; masks vary by step.
            fresh = tuple((step + j + k) % 5 != 0 for k in range(3))
            out.append(case(seed, scenario, split, step, cls, bits, fresh, j))
    random.Random(f'{seed}:{scenario}:{split}:{step}').shuffle(out)
    return out


def history(seed, scenario):
    """Shared supervised founding evidence; no prose rule or answer-bearing notebook."""
    result = []
    patterns = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]
    for cls in ('A', 'B'):
        for i, bits in enumerate(patterns + [(1, 1, 1)] * 3):
            fresh = tuple(k != i - 5 for k in range(3))
            c = case(seed, scenario, 'training', -1, cls, bits, fresh, i)
            result.append({'observation': c, 'accepted_action': oracle(c, scenario, rules(seed, scenario, 0))})
    return result


def explicit_rule(seed, scenario, step):
    r = rules(seed, scenario, step)
    if scenario == 'incident':
        return f"For each class, use its precaution exactly when that source's signal is true; otherwise none. Sources: {r}. Freshness is irrelevant. Summary is not authoritative."
    return f"Ship exactly when the class's source has BOTH signal=true and fresh=true; otherwise hold. Sources: {r}. Other sources and summary are not authoritative."


def instructions(scenario, arm):
    setting = ('Choose the required precaution, or none when no precaution is needed. A wrong '
               'precaution leaves the hazard unhandled; a precaution without a hazard is unnecessary.'
               if scenario == 'incident' else
               'Choose whether to ship or hold. A green summary may not establish readiness; use independent evidence.')
    note = ('Record scope, supporting observation IDs and notices about obsolete rules.' if arm == 'evidence'
            else 'Write a concise operational note for future work.')
    family = ('Each service class has ONE unknown governing source. The correct action is that source exactly when its signal is YES, otherwise none. Freshness, queue and summary do not affect the rule.' if scenario == 'incident' else 'Each service class has ONE unknown governing source. Ship exactly when that source has BOTH signal YES and fresh YES; otherwise hold. Other sources, queue and summary do not affect the rule.')
    return ('This is a synthetic classification benchmark. Extra caution or extra checks count as incorrect. ' + family + ' Learn which source governs each class from accepted examples or the inherited record. ' + setting +
            ' Infer local practices from accepted historical outcomes and completed-case feedback. '
            'The environment may change. Current-case correct answers are withheld. '
            'Return one command for every current case using the supplied command documentation. '
            'Return only an object with decisions [{id, command}] and notebook (at most 700 characters). '
            'Do not add keys. ' + note)


def validate_output(value, cases, docs):
    errors = []
    if not isinstance(value, dict) or set(value) != {'decisions', 'notebook'}:
        return {}, ['invalid_object_schema']
    if not isinstance(value['notebook'], str) or len(value['notebook']) > 700:
        errors.append('invalid_notebook')
    ds = value['decisions']
    if not isinstance(ds, list):
        return {}, errors + ['invalid_decisions_schema']
    expected = {c['id'] for c in cases}
    counts = {}
    parsed = {}
    inverse = {v: k for k, v in docs.items()}
    for d in ds:
        if not isinstance(d, dict) or set(d) != {'id', 'command'} or not isinstance(d['id'], str):
            errors.append('invalid_decision_schema'); continue
        ident = d['id']; counts[ident] = counts.get(ident, 0) + 1
        command = d['command']
        if ident not in expected:
            errors.append('unknown_case'); continue
        if not isinstance(command, str) or command not in inverse:
            errors.append('invalid_command'); continue
        parsed[ident] = inverse[command]
    for ident in expected:
        if counts.get(ident, 0) != 1:
            parsed.pop(ident, None)
            errors.append('missing_or_duplicate_case')
    # A bad notebook invalidates qualification schema but does not erase valid votes.
    return parsed, errors


def score(cases, scenario, rule, stale_rule, member_votes):
    rows = []
    for c in cases:
        votes = [v[c['id']] for v in member_votes if c['id'] in v]
        action = next((a for a in set(votes) if votes.count(a) >= 2), None)
        truth = oracle(c, scenario, rule)
        rows.append({'id': c['id'], 'class': c['service_class'], 'truth': truth,
                     'stale_truth': oracle(c, scenario, stale_rule), 'action': action,
                     'valid_votes': len(votes), 'agreement': max([votes.count(a) for a in set(votes)] or [0]) / 3,
                     'correct': action == truth, 'observed': action is not None,
                     'stale_agreement': action == oracle(c, scenario, stale_rule) if action is not None else None,
                     'unnecessary_check': scenario == 'incident' and action not in (None, 'none') and truth == 'none',
                     'missed_hazard': scenario == 'incident' and truth != 'none' and action != truth})
    return rows

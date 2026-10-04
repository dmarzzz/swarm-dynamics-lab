"""Bounded report transforms and a separately written same-author reference.
No eval/exec, plugins, model calls, filesystem writes or candidate-owned code.
"""
from collections import defaultdict

SELECTION = 'last-valid-else-last-in-source-order'
CHECKS = ('physical_records', 'invalid_records', 'logical_records', 'selected_valid_records',
          'superseded_records', 'selected_captured_records', 'capture_denominator', 'capture_rate',
          'selection_rule', 'physical_ids', 'selected_ids', 'first_attempt_valid_records',
          'invalid_then_valid_logical_records')
BASELINE = {'accounting': 'selected-only', 'capture': 'selected', 'lineage': 'omit', 'first_attempts': 'omit'}
REPAIR = {'accounting': 'all-physical', 'capture': 'selected', 'lineage': 'all', 'first_attempts': 'report'}
SHORTCUT = {'accounting': 'selected-only', 'capture': 'clamp-raw-over-selected', 'lineage': 'omit', 'first_attempts': 'omit'}
ALLOWED = {'accounting': {'selected-only', 'all-physical'}, 'capture': {'selected', 'clamp-raw-over-selected'},
           'lineage': {'omit', 'all'}, 'first_attempts': {'omit', 'report'}}


def validate_policy(policy):
    if not isinstance(policy, dict) or set(policy) != set(ALLOWED):
        raise ValueError('policy fields are closed')
    if any(type(v) is not str or v not in ALLOWED[k] for k, v in policy.items()):
        raise ValueError('policy value is not allowlisted')


def identity(r):
    return r['cell'], r['task'], r['seed'], r['arm']


def groups(rows):
    result = defaultdict(list)
    for r in rows:
        if r['role'] == 'episode':
            result[r['cell'] + '/' + r['arm']].append(r)
    return dict(sorted(result.items()))


def reference(rows):
    """Oracle contract: partition explicitly, then reverse-search last valid.
    Same author as transform, not an independent review or independent data.
    """
    keys = sorted({identity(x) for x in rows})
    histories = [[x for x in rows if identity(x) == key] for key in keys]
    selected = [next((x for x in reversed(h) if x['valid']), h[-1]) for h in histories]
    valid = [x for x in selected if x['valid']]
    captured = sum(x['captured'] is True for x in valid)
    return {'physical_records': len(rows), 'invalid_records': sum(x['valid'] is False for x in rows),
            'logical_records': len(keys), 'selected_valid_records': len(valid), 'superseded_records': len(rows) - len(keys),
            'selected_captured_records': captured, 'capture_denominator': len(valid),
            'capture_rate': {'numerator': captured, 'denominator': len(valid)} if valid else None,
            'selection_rule': SELECTION, 'physical_ids': sorted(x['event_id'] for x in rows),
            'selected_ids': sorted(x['event_id'] for x in selected),
            'first_attempt_valid_records': sum(h[0]['valid'] for h in histories),
            'invalid_then_valid_logical_records': sum(not h[0]['valid'] and any(x['valid'] for x in h) for h in histories)}


def transform(rows, policy):
    validate_policy(policy)
    latest, first, counts, ever_valid = {}, {}, defaultdict(int), defaultdict(bool)
    for r in rows:
        key = identity(r)
        first.setdefault(key, r)
        counts[key] += 1
        ever_valid[key] |= r['valid']
        if key not in latest or r['valid'] or not latest[key]['valid']:
            latest[key] = r
    picked = list(latest.values())
    selected_valid = [r for r in picked if r['valid']]
    accounting_rows = rows if policy['accounting'] == 'all-physical' else picked
    valid_count = len(selected_valid)
    captured = sum(r['captured'] is True for r in selected_valid)
    rate_numerator = captured
    if policy['capture'] == 'clamp-raw-over-selected':
        rate_numerator = min(sum(r['captured'] is True for r in rows), valid_count)
    full_lineage = policy['lineage'] == 'all'
    report_first = policy['first_attempts'] == 'report'
    return {'physical_records': len(accounting_rows), 'invalid_records': sum(not r['valid'] for r in accounting_rows),
            'logical_records': len(picked), 'selected_valid_records': valid_count,
            'superseded_records': len(accounting_rows) - len(picked), 'selected_captured_records': captured,
            'capture_denominator': valid_count,
            'capture_rate': {'numerator': rate_numerator, 'denominator': valid_count} if valid_count else None,
            'selection_rule': SELECTION if full_lineage else None,
            'physical_ids': sorted(r['event_id'] for r in rows) if full_lineage else None,
            'selected_ids': sorted(r['event_id'] for r in picked) if full_lineage else None,
            'first_attempt_valid_records': sum(r['valid'] for r in first.values()) if report_first else None,
            'invalid_then_valid_logical_records': sum(not r['valid'] and ever_valid[k] for k, r in first.items()) if report_first else None}


def evaluate(rows, policy):
    reports, cases = {}, []
    for group, group_rows in groups(rows).items():
        observed, expected = transform(group_rows, policy), reference(group_rows)
        reports[group] = observed
        for check in CHECKS:
            cases.append({'group': group, 'check': check, 'passed': observed[check] == expected[check]})
    return {'passed': sum(c['passed'] for c in cases), 'assigned': len(cases), 'cases': cases, 'reports': reports}

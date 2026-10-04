"""The scorer's analysis: twelve strata, two representations, the paired layout contrast, the offline
comparators and the failure report. Everything is recomputed from saved rows; `chain.py verify` calls
`analyze` again and compares.

Missing-data rule: a unit without a valid answer (failed or not started) stays in its cell's
denominator. Its expected regret is unknown but bounded: had it answered, it would have chosen one of
the two legal cells, so its regret lies between 0 and |e - U|. The primary contrast is reported as
bounds over all assigned layouts and as the complete-case estimate with its denominator. Nothing is
dropped, imputed or re-run.

  python3 src/analyze.py calibration      the scripted reference and comparator table on the
                                          engineering layouts (no model call)
"""
import collections
import json
import math
import sys

import sim
import study

T975 = {1: 12.7062, 2: 4.3027, 3: 3.1824, 4: 2.7764, 5: 2.5706, 6: 2.4469, 7: 2.3646, 8: 2.3060, 9: 2.2622, 10: 2.2281,
        11: 2.2010, 12: 2.1788, 13: 2.1604, 14: 2.1448, 15: 2.1314, 16: 2.1199, 17: 2.1098, 18: 2.1009, 19: 2.0930,
        20: 2.0860, 21: 2.0796, 22: 2.0739, 23: 2.0687}
EVIDENCE_KEYS = ('http_status', 'error_body', 'request_id', 'answer_text', 'finish_reason', 'attempts', 'billing_paused',
                 'response_model', 'response_provider', 'earlier_http_status', 'earlier_error_body')


def mean(values):
    values = [v for v in values if v is not None]
    return math.fsum(values) / len(values) if values else None


def valid(r):
    return r['status'] == 'completed'


def regret(r):
    return r['evaluation']['expected_regret'] if valid(r) else None


def margin(r):
    return round(abs(r['error'] - r['unknown_cost']), 12)


def bounds(r):
    """[lowest, highest] expected regret the unit can have."""
    return [regret(r), regret(r)] if valid(r) else [0.0, margin(r)]


def cell_summary(rows):
    good = [r for r in rows if valid(r)]
    count = lambda key, value: sum(r['evaluation'][key] == value for r in good)
    return {'assigned': len(rows), 'valid': len(good), 'failed': sum(r['status'] == 'failed' for r in rows),
            'not_started': sum(r['status'] == 'not_started' for r in rows),
            'optimal': count('optimal', True), 'check': count('action', 'check'), 'explore': count('action', 'explore'),
            'first_listed': count('first_listed', True), 'mean_regret': mean(regret(r) for r in good),
            'regret_bounds': [mean(bounds(r)[0] for r in rows), mean(bounds(r)[1] for r in rows)],
            'mean_realized_loss': mean(r['evaluation']['realized_scripted_loss'] for r in good)}


def comparators(rows):
    """Expected regret of the offline policies on the assigned units (no model call)."""
    out = {}
    for name in study.POLICIES:
        out[name] = mean(study.evaluate(r, study.policy(name, r))['expected_regret'] for r in rows)
    return out


def failure_report(rows):
    """Every unit without a valid answer, with the evidence its accounting kept."""
    units = []
    for r in rows:
        if valid(r): continue
        acc = r.get('accounting') or {}
        units.append(dict({'id': r['id'], 'status': r['status'], 'category': r.get('failure') or r.get('stop'),
                           'representation': r['representation'], 'error': r['error'], 'unknown_cost': r['unknown_cost'],
                           'layout': r['layout']}, **{k: acc[k] for k in EVIDENCE_KEYS if acc.get(k) is not None}))
    by = collections.Counter(u['category'] or u['status'] for u in units)
    return {'units_without_a_valid_answer': len(units), 'failed': sum(u['status'] == 'failed' for u in units),
            'not_started': sum(u['status'] == 'not_started' for u in units), 'by_category': dict(sorted(by.items())),
            'by_representation': {rep: sum(u['representation'] == rep for u in units) for rep in study.REPRESENTATIONS},
            'units': units}


def analyze(rows):
    """`rows`: one terminal row per unit (study.combine has been applied). Uses the grid rows (main or engineering)."""
    grid = [r for r in rows if r['kind'] in study.GRID_KINDS]
    if not grid:
        return {'cells': [], 'note': 'this stage has no grid units', 'failures': failure_report(rows)}
    d = study.design(); a = d['analysis']; layouts = sorted({r['layout'] for r in grid}); cases = study.cases()
    by = {(r['layout'], r['error'], r['unknown_cost'], r['representation']): r for r in grid}
    cells, strata = [], []
    for e, u in cases:
        s = {'error': e, 'unknown_cost': u, 'optimal_action': sim.optimal_action(e, u), 'margin': round(abs(e - u), 12),
             'always_check_regret': round(sim.expected_loss(e, u, 'check') - min(e, u), 12),
             'always_explore_regret': round(sim.expected_loss(e, u, 'explore') - min(e, u), 12),
             'reliable_source': e <= a['reliable_source_error_max']}
        for rep in study.REPRESENTATIONS:
            mine = [by[k] for k in by if k[1:] == (e, u, rep)]
            c = cell_summary(mine); cells.append(dict({'error': e, 'unknown_cost': u, 'representation': rep}, **c)); s[rep] = c
        pairs = [(by[(l, e, u, 'table')], by[(l, e, u, 'prose')]) for l in layouts
                 if (l, e, u, 'table') in by and (l, e, u, 'prose') in by]
        both = [(t, p) for t, p in pairs if valid(t) and valid(p)]
        s.update(pairs=len(both), table_minus_prose=mean(regret(t) - regret(p) for t, p in both),
                 table_minus_prose_bounds=[mean(bounds(t)[0] - bounds(p)[1] for t, p in pairs), mean(bounds(t)[1] - bounds(p)[0] for t, p in pairs)],
                 optimal_table_minus_prose=s['table']['optimal'] - s['prose']['optimal'])
        s['regression'] = bool(s['reliable_source'] and s['optimal_table_minus_prose'] <= -a['regression_flag'])
        strata.append(s)

    per_layout = []
    for l in layouts:
        units = [by[k] for k in by if k[0] == l]
        lo = hi = 0.0; diffs = []
        for e, u in cases:
            t, p = by.get((l, e, u, 'table')), by.get((l, e, u, 'prose'))
            if t is None or p is None: continue
            lo += bounds(t)[0] - bounds(p)[1]; hi += bounds(t)[1] - bounds(p)[0]
            if valid(t) and valid(p): diffs.append(regret(t) - regret(p))
        complete = len(units) == 2 * len(cases) and all(valid(r) for r in units)
        w = study.layout(l)
        per_layout.append({'layout': l, 'assigned': len(units), 'valid': sum(valid(r) for r in units), 'complete': complete,
                           'value': math.fsum(diffs) / len(cases) if complete else None,
                           'bounds': [lo / len(cases), hi / len(cases)],
                           'regret_prose': mean(regret(r) for r in units if r['representation'] == 'prose'),
                           'regret_table': mean(regret(r) for r in units if r['representation'] == 'table'),
                           'report_listed_first': w['legal_order'][0] == w['report_cell'], 'report_label': w['report_label']})
    values = [x['value'] for x in per_layout if x['complete']]; n = len(values)
    estimate = mean(values)
    se = (math.sqrt(math.fsum((v - estimate) ** 2 for v in values) / (n - 1)) / math.sqrt(n)) if n > 1 else None
    t = T975.get(n - 1)
    primary = {'definition': d['primary_contrast']['definition'], 'estimate': estimate, 'layouts': n, 'assigned_layouts': len(layouts),
               'standard_error': se, 'interval95': [estimate - t * se, estimate + t * se] if se is not None and t else None,
               'range': [min(values), max(values)] if values else None,
               'leave_one_out_range': [min((math.fsum(values) - v) / (n - 1) for v in values),
                                       max((math.fsum(values) - v) / (n - 1) for v in values)] if n > 1 else None,
               'negative': sum(v < -1e-12 for v in values), 'zero': sum(abs(v) <= 1e-12 for v in values),
               'positive': sum(v > 1e-12 for v in values),
               'bounds_all_assigned': [mean(x['bounds'][0] for x in per_layout), mean(x['bounds'][1] for x in per_layout)],
               'practical_marker': d['primary_contrast']['practical_marker'],
               'largest_possible': mean(abs(e - u) for e, u in cases)}
    reps = {}
    for rep in study.REPRESENTATIONS:
        mine = [r for r in grid if r['representation'] == rep]; c = cell_summary(mine)
        reps[rep] = dict(c, first_listed_share=(c['first_listed'] / c['valid']) if c['valid'] else None,
                         optimal_share=(c['optimal'] / c['valid']) if c['valid'] else None)
    flagged = [{'error': s['error'], 'unknown_cost': s['unknown_cost'], 'optimal_table_minus_prose': s['optimal_table_minus_prose']}
               for s in strata if s['regression']]
    reliable = [s['optimal_table_minus_prose'] for s in strata if s['reliable_source']]
    acct = [r.get('accounting') or {} for r in grid]
    return {'kind': sorted({r['kind'] for r in grid}), 'units': {'assigned': len(grid), 'valid': sum(valid(r) for r in grid),
            'failed': sum(r['status'] == 'failed' for r in grid), 'not_started': sum(r['status'] == 'not_started' for r in grid)},
            'primary': primary, 'representations': reps, 'strata': strata, 'cells': cells, 'layouts': per_layout,
            'comparators': comparators(grid),
            'reliable_source': {'strata': len(reliable), 'worst_optimal_table_minus_prose': min(reliable) if reliable else None,
                                'flag_at': -a['regression_flag'], 'flagged': flagged},
            'resources': {'calls': sum(bool(x.get('attempted')) for x in acct), 'answered': sum(bool(x.get('usage_reported')) for x in acct),
                          'input_tokens': sum(x.get('input_tokens', 0) for x in acct), 'output_tokens': sum(x.get('output_tokens', 0) for x in acct),
                          'cost_usd': math.fsum(x.get('actual_usd', 0) for x in acct),
                          'cost_per_valid_choice_usd': (math.fsum(x.get('actual_usd', 0) for x in acct) / sum(valid(r) for r in grid))
                          if any(valid(r) for r in grid) else None},
            'failures': failure_report(rows)}


def scripted_rows(kind, by_representation):
    """Rows of the scripted policies named per representation, e.g. {'prose': 'always_explore', 'table': 'optimal'}."""
    out = []
    for a in study.grid(kind):
        choice = study.policy(by_representation[a['representation']], a)
        out.append(dict(a, status='completed', answer={'inspect': choice}, evaluation=study.evaluate(a, choice)))
    return out


def discrimination(kind='engineering'):
    """Known-answer checks of the scorer on scripted policies. Returns violations (empty when the instrument
    separates what it should): the analytic policy has regret 0 and contrast 0; every constant policy has
    positive regret; a policy pair that differs between the representations gives exactly the contrast the
    comparator means imply, with the sign following which representation is better."""
    out = []; close = lambda x, y: x is not None and abs(x - y) < 1e-9
    both = analyze(scripted_rows(kind, {'prose': 'optimal', 'table': 'optimal'}))
    if not close(both['primary']['estimate'], 0.0) or any(c['mean_regret'] != 0 or c['optimal'] != c['assigned'] for c in both['cells']):
        out.append('analytic_policy_must_have_zero_regret')
    comp = both['comparators']
    want = {'always_check': mean(max(0.0, u - e) for e, u in study.cases()), 'always_explore': mean(max(0.0, e - u) for e, u in study.cases())}
    for name in ('always_check', 'always_explore'):
        if not close(comp[name], want[name]) or comp[name] <= 0.01: out.append(f'{name}_regret_must_be_positive_and_match_the_arithmetic')
    for name in ('always_first', 'always_second'):
        if comp[name] is None or comp[name] <= 0.01: out.append(f'{name}_regret_must_be_positive')
    for name in ('always_check', 'always_explore'):
        better = analyze(scripted_rows(kind, {'prose': name, 'table': 'optimal'}))['primary']
        worse = analyze(scripted_rows(kind, {'prose': 'optimal', 'table': name}))['primary']
        if not close(better['estimate'], -want[name]) or not close(worse['estimate'], want[name]):
            out.append(f'contrast_must_equal_the_{name}_regret_with_the_right_sign')
        if better['negative'] != better['layouts'] or worse['positive'] != worse['layouts']: out.append(f'{name}_contrast_sign_per_layout')
    strata = both['strata']
    if sum(s['always_check_regret'] > 0 for s in strata) != 6 or sum(s['always_explore_regret'] > 0 for s in strata) != 6:
        out.append('each_constant_action_must_be_wrong_in_six_cases')
    return out


def calibration(kind='engineering'):
    """Per case: the optimal action and the regret of each scripted policy on the layouts of `kind`."""
    rows = study.grid(kind); table = []
    for e, u in study.cases():
        mine = [a for a in rows if (a['error'], a['unknown_cost']) == (e, u)]
        line = {'error': e, 'unknown_cost': u, 'optimal_action': sim.optimal_action(e, u), 'margin': round(abs(e - u), 12)}
        for name in study.POLICIES:
            line[name] = mean(study.evaluate(a, study.policy(name, a))['expected_regret'] for a in mine)
        table.append(line)
    overall = {name: mean(study.evaluate(a, study.policy(name, a))['expected_regret'] for a in rows) for name in study.POLICIES}
    return {'kind': kind, 'layouts': len({a['layout'] for a in rows}), 'cases': table, 'mean_regret': overall,
            'largest_possible_contrast': mean(abs(e - u) for e, u in study.cases())}


if __name__ == '__main__':
    if sys.argv[1:] == ['calibration']:
        print(json.dumps(calibration(), indent=1))
    else:
        raise SystemExit(__doc__)

"""Root-paired descriptive analysis. The independent unit is a root, paired across rules, budgets
and check strengths. Seat outcomes come from scripted admission and exist for every assigned row;
model outcomes exist only for completed calls and are reported complete-case and with bounds."""
import argparse
import gzip
import json
from collections import defaultdict

import numpy as np

import study

ADMISSION = ('attacker_seats', 'attacker_seat_share', 'specialist_retention', 'truth_available', 'truth_plurality',
             'passed', 'controlled_checked', 'controlled_passed')
OUTCOMES = ('rare_correct', 'rare_wrong', 'rare_abstain', 'rare_fabricated', 'task_correct')


def read_rows(path):
    opener = gzip.open if str(path).endswith('.gz') else open
    with opener(path, 'rt') as f: return [json.loads(line) for line in f if line.strip()]


def mean(values):
    values = list(values)
    return sum(values) / len(values) if values else None


def interval(values):
    """95% percentile interval of the mean over roots: 10,000 bootstrap draws, fixed seed."""
    d = study.design()['analysis']
    if not values: return None
    a = np.array(values, dtype=float); rng = np.random.default_rng(d['bootstrap_seed'])
    draws = a[rng.integers(0, len(a), (d['bootstrap_draws'], len(a)))].mean(axis=1)
    return [float(x) for x in np.quantile(draws, [.025, .975])]


def index(rows):
    """task -> {(kind, attacker_pass, rule, checks): row}; comparison rows only, every status."""
    table = defaultdict(dict)
    for r in rows:
        if r['kind'] in ('pilot', 'clean'): table[r['task']][(r['kind'], r['attacker_pass'], r['rule'], r['checks'])] = r
    return table


def seat_contrast(table, rate, rule_a, rule_b, hi, lo, field='attacker_seats'):
    """(rule_a at hi minus rule_a at lo) minus (rule_b at hi minus rule_b at lo), per root; rule_b None
    gives the raw escalation of rule_a. Scripted, so no row is missing unless it was never assigned."""
    per_root = []
    for task, cells in sorted(table.items()):
        keys = [('pilot', rate, rule_a, hi), ('pilot', rate, rule_a, lo)] + ([('pilot', rate, rule_b, hi), ('pilot', rate, rule_b, lo)] if rule_b else [])
        if any(k not in cells for k in keys): continue
        v = [cells[k]['admission'][field] for k in keys]
        per_root.append({'task': task, 'difference': (v[0] - v[1]) - ((v[2] - v[3]) if rule_b else 0)})
    values = [p['difference'] for p in per_root]
    return {'estimate': mean(values), 'interval': interval(values), 'roots': len(values), 'assigned_roots': len(table),
            'positive_roots': sum(v > 0 for v in values), 'per_root': per_root}


def answer_contrast(table, rate, checks, rule_a, rule_b, field='rare_correct'):
    """rule_a minus rule_b on a model outcome in [0, 1], per root: complete-case, and bounds over all
    assigned roots with each missing answer at the value that makes the contrast smallest or largest."""
    complete = []; low = []; high = []
    for task, cells in sorted(table.items()):
        a, b = cells.get(('pilot', rate, rule_a, checks)), cells.get(('pilot', rate, rule_b, checks))
        if a is None or b is None: continue
        va = a['evaluation'][field] if a['status'] == 'completed' else None
        vb = b['evaluation'][field] if b['status'] == 'completed' else None
        low.append((va if va is not None else 0.0) - (vb if vb is not None else 1.0))
        high.append((va if va is not None else 1.0) - (vb if vb is not None else 0.0))
        if va is not None and vb is not None: complete.append(va - vb)
    return {'estimate': mean(complete), 'interval': interval(complete), 'roots': len(complete), 'assigned_roots': len(low),
            'bounds_all_assigned': [mean(low), mean(high)]}


def cells(rows):
    grouped = defaultdict(list)
    for r in rows:
        if r['kind'] in ('pilot', 'clean'): grouped[(r['kind'], r['attacker_pass'], r['rule'], r['checks'])].append(r)
    out = []
    for key, rr in sorted(grouped.items(), key=lambda kv: json.dumps(kv[0])):
        good = [r for r in rr if r['status'] == 'completed']; n = len(rr)
        cell = dict(zip(('kind', 'attacker_pass', 'rule', 'checks'), key), assigned=n, valid=len(good),
                    failed=sum(r['status'] == 'failed' for r in rr), not_started=sum(r['status'] == 'not_started' for r in rr))
        cell['admission'] = {f: mean(r['admission'][f] for r in rr) for f in ADMISSION}
        cell['model'] = {f: mean(r['evaluation'][f] for r in good) for f in OUTCOMES}
        cell['reference'] = {f: mean(r['reference_evaluation'][f] for r in good) for f in OUTCOMES}
        for f in ('rare_correct', 'rare_wrong'):
            got = sum(r['evaluation'][f] for r in good)
            cell[f + '_bounds_all_assigned'] = [got / n, (got + (n - len(good))) / n]
        cell['input_tokens'] = sum((r.get('accounting') or {}).get('input_tokens', 0) for r in rr)
        cell['output_tokens'] = sum((r.get('accounting') or {}).get('output_tokens', 0) for r in rr)
        cell['cost_usd'] = sum((r.get('accounting') or {}).get('actual_usd', 0) for r in rr)
        out.append(cell)
    return out


def analyze(rows):
    d = study.design(); table = index(rows)
    strong, weak = min(d['attacker_pass']), max(d['attacker_pass'])
    lo, mid, hi = sorted(d['check_budgets'])
    trimmed = lambda c: {k: v for k, v in c.items() if k != 'per_root'}
    primary = seat_contrast(table, strong, 'propagated', 'direct', hi, lo)
    secondary = {
        'primary_under_weak_checks': trimmed(seat_contrast(table, weak, 'propagated', 'direct', hi, lo)),
        'primary_against_anchors': trimmed(seat_contrast(table, strong, 'propagated', 'anchors', hi, lo)),
        'primary_at_middle_budget': trimmed(seat_contrast(table, strong, 'propagated', 'direct', mid, lo)),
        'direct_against_anchors': trimmed(seat_contrast(table, strong, 'direct', 'anchors', hi, lo)),
    }
    escalation = [dict(attacker_pass=rate, rule=rule, **trimmed(seat_contrast(table, rate, rule, None, hi, lo)))
                  for rate in d['attacker_pass'] for rule in d['rules']]
    level = []          # propagated minus direct in attacker seats at each budget (levels, not escalation)
    for rate in d['attacker_pass']:
        for checks in d['check_budgets']:
            values = [c[('pilot', rate, 'propagated', checks)]['admission']['attacker_seats'] - c[('pilot', rate, 'direct', checks)]['admission']['attacker_seats']
                      for c in table.values() if ('pilot', rate, 'propagated', checks) in c and ('pilot', rate, 'direct', checks) in c]
            level.append({'attacker_pass': rate, 'checks': checks, 'propagated_minus_direct_seats': mean(values), 'interval': interval(values), 'roots': len(values)})
    answers = [dict(attacker_pass=rate, checks=checks, field=field, **answer_contrast(table, rate, checks, 'propagated', 'direct', field))
               for rate in d['attacker_pass'] for checks in d['check_budgets'] for field in ('rare_correct', 'rare_wrong')]
    grid = [r for r in rows if r['kind'] in ('pilot', 'clean')]
    return {'design': {'primary_contrast': d['primary_contrast'], 'bootstrap': d['analysis'], 'unit': 'root'},
            'denominators': {'assigned': len(grid), 'completed': sum(r['status'] == 'completed' for r in grid),
                             'failed': sum(r['status'] == 'failed' for r in grid),
                             'not_started': sum(r['status'] == 'not_started' for r in grid), 'roots': len(table)},
            'primary': primary, 'secondary': secondary, 'escalation': escalation, 'levels': level,
            'model_propagated_minus_direct': answers, 'cells': cells(rows)}


def calibration_text(split='engineering'):
    """Scripted admission on a split without any model. Used for the engineering-root record."""
    d = study.design(); rows = []
    for task in study.roots(split):
        for rate in d['attacker_pass']:
            r = study.replay(task, rate)
            for budget in d['check_budgets']:
                for rule in d['rules']:
                    rows.append({'kind': 'pilot', 'task': task, 'attacker_pass': rate, 'rule': rule, 'checks': budget, 'status': 'not_started',
                                 'admission': study.sim.admission_metrics(r['world'], r['admitted'][(rule, budget)], r['events'][:budget])})
    table = index(rows); lines = []
    for rate in d['attacker_pass']:
        for rule in d['rules']:
            for f in ('attacker_seats', 'specialist_retention', 'truth_available', 'truth_plurality'):
                lines.append(f'pass {rate} {rule:10s} {f:20s} ' + ' '.join(
                    f'{mean(c[("pilot", rate, rule, b)]["admission"][f] for c in table.values()):7.2f}' for b in d['check_budgets']))
    p = seat_contrast(table, min(d['attacker_pass']), 'propagated', 'direct', max(d['check_budgets']), min(d['check_budgets']))
    lines.append(f'primary: mean {p["estimate"]:+.3f} seats, per root {[x["difference"] for x in p["per_root"]]}')
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(description='Recompute the analysis from saved rows, or print the engineering calibration.')
    sub = ap.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('rows'); r.add_argument('episodes', nargs='+')
    sub.add_parser('calibration')
    args = ap.parse_args()
    if args.cmd == 'rows':
        import worker
        merged = []
        for path in args.episodes: merged = worker.merge(merged, read_rows(path))
        print(json.dumps(analyze(merged)))
    else:
        print(calibration_text())


if __name__ == '__main__':
    main()

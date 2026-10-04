"""Root-level descriptive analysis: all cells with full denominators, paired contrasts, and bounds.

The unit is the world root. A missing outcome keeps its root: the outcome is bounded in [0, 1],
never dropped and never set to a zero effect. Calls, identities and skills are not samples.
"""
import gzip
import json
import math
from collections import defaultdict

import numpy as np

import study

MODEL_METRICS = ('rare_accuracy', 'task_accuracy', 'rare_wrong', 'rare_null')
DIAGNOSTICS = ('truth_available', 'carrier_survival', 'all_three_survive', 'original_outside_retention',
               'attacker_seat_share', 'false_seat_share')
_INDEX = {}


def read_rows(path):
    opener = gzip.open if str(path).endswith('.gz') else open
    with opener(path, 'rt') as f:
        return [json.loads(line) for line in f]


def boot_index(n):
    """Resampled roots, shared by every interval over the same number of roots (paired by root)."""
    a = study.design()['analysis']
    if n not in _INDEX:
        _INDEX[n] = np.random.default_rng(a['bootstrap_seed']).integers(0, n, (a['bootstrap_draws'], n))
    return _INDEX[n]


def interval(values):
    if not values:
        return None
    a = np.array(values, dtype=float)
    boot = a[boot_index(len(a))].mean(axis=1)
    return [float(x) for x in np.quantile(boot, [.025, .975])]


def mean(values):
    values = [float(v) for v in values]
    return math.fsum(values) / len(values) if values else None


def cell_key(r):
    return (r['carriers'], r['checks'], r['attacker_pass'], r['arm'])


def combo(grouped, terms):
    """A linear contrast of cell outcomes, paired by root. terms: [(coefficient, cell key), ...]."""
    by_task = [{r['task']: r for r in grouped.get(key, [])} for _, key in terms]
    tasks = sorted(set.intersection(*[set(b) for b in by_task])) if by_task and all(by_task) else []
    complete, low, high, per_world = [], [], [], []
    for task in tasks:
        values = [(coef, b[task]['evaluation']['rare_accuracy'] if b[task]['status'] == 'completed' else None)
                  for (coef, _), b in zip(terms, by_task)]
        low.append(math.fsum(coef * (y if y is not None else (0.0 if coef > 0 else 1.0)) for coef, y in values))
        high.append(math.fsum(coef * (y if y is not None else (1.0 if coef > 0 else 0.0)) for coef, y in values))
        if all(y is not None for _, y in values):
            difference = math.fsum(coef * y for coef, y in values)
            complete.append(difference)
            per_world.append({'task': task, 'difference': difference})
        else:
            per_world.append({'task': task, 'difference': None})
    full = bool(tasks) and len(complete) == len(tasks)
    return {'roots': len(tasks), 'complete_roots': len(complete),
            'mean': mean(complete) if full else None,
            'interval': interval(complete) if full else None,
            'all_assigned_bounds': [mean(low), mean(high)] if tasks else None,
            'complete_case_mean': mean(complete), 'per_world': per_world}


def analyze(rows):
    d = study.design()
    pilot = [r for r in rows if r['kind'] == 'pilot']
    grouped = defaultdict(list)
    for r in pilot:
        grouped[cell_key(r)].append(r)
    cells = []
    for key in sorted(grouped):
        rr = grouped[key]
        good = [r for r in rr if r['status'] == 'completed']
        accuracy = [r['evaluation']['rare_accuracy'] for r in good]
        survived = [(r['evaluation']['correct'][s], r['diagnostics']['carriers_admitted_per_fact'][i] > 0)
                    for r in good for i, s in enumerate(study.RARE)]
        diag = {}
        for name in DIAGNOSTICS:
            values = [r['diagnostics'][name] for r in rr if r['diagnostics'][name] is not None]
            diag[name] = mean(values)
        for name in ('rare_truthful_reports', 'rare_false_reports'):
            diag[name] = {str(s): mean(r['diagnostics'][name][str(s)] for r in rr) for s in study.RARE}
        cells.append({
            'carriers': key[0], 'checks': key[1], 'attacker_pass': key[2], 'arm': key[3],
            'assigned': len(rr), 'valid': len(good), 'missing': len(rr) - len(good),
            'rare_accuracy': {'mean_valid': mean(accuracy),
                              'interval': interval(accuracy) if good and len(good) == len(rr) else None,
                              'all_assigned_bounds': [math.fsum(accuracy) / len(rr),
                                                      (math.fsum(accuracy) + len(rr) - len(good)) / len(rr)]},
            'model': {m: mean(r['evaluation'][m] for r in good) for m in MODEL_METRICS},
            'scripted_rare_accuracy': mean(r['scripted_evaluation']['rare_accuracy'] for r in rr),
            'diagnostics': diag,
            'conditional_on_truth_survival': {
                'numerator': sum(1 for ok, alive in survived if alive and ok),
                'denominator': sum(1 for _, alive in survived if alive),
                'note': 'diagnostic only: valid rows, rare facts with at least one truthful carrier admitted'}})

    p = d['primary_contrast']
    lowest, highest = min(d['carriers']), max(d['carriers'])
    primary = combo(grouped, [(1, (lowest, p['checks'], p['attacker_pass'], p['arm'])),
                              (-1, (highest, p['checks'], p['attacker_pass'], p['arm']))])
    primary.update(contrast=f'carriers {lowest} minus carriers {highest}', arm=p['arm'], checks=p['checks'],
                   attacker_pass=p['attacker_pass'], useful_difference_pp=p['useful_difference_pp'],
                   metric='rare_accuracy', status='exploratory, descriptive')
    carrier_contrasts, policy_contrasts, interactions = [], [], []
    for arm in d['arms']:
        for checks in d['audit_checks']:
            for rate in d['attacker_pass']:
                for c in d['carriers']:
                    if c != highest:
                        out = combo(grouped, [(1, (c, checks, rate, arm)), (-1, (highest, checks, rate, arm))])
                        out.update(arm=arm, checks=checks, attacker_pass=rate, carriers=c, minus_carriers=highest)
                        carrier_contrasts.append(out)
    for checks in d['audit_checks']:
        for rate in d['attacker_pass']:
            for c in d['carriers']:
                out = combo(grouped, [(1, (c, checks, rate, 'coverage')), (-1, (c, checks, rate, 'random'))])
                out.update(contrast='coverage minus random', checks=checks, attacker_pass=rate, carriers=c)
                policy_contrasts.append(out)
            out = combo(grouped, [(1, (lowest, checks, rate, 'coverage')), (-1, (lowest, checks, rate, 'random')),
                                  (-1, (highest, checks, rate, 'coverage')), (1, (highest, checks, rate, 'random'))])
            out.update(contrast=f'(coverage - random at {lowest}) - (coverage - random at {highest})',
                       checks=checks, attacker_pass=rate)
            interactions.append(out)

    # Invariance across carrier counts inside each root / policy / checks / strength cell.
    matched = defaultdict(list)
    for r in pilot:
        matched[(r['task'], r['attacker_pass'], r['arm'], r['checks'])].append(r)
    violations = 0
    for rr in matched.values():
        same = len({(r['admitted_hash'], r['audit_hash'], r['order_hash'],
                     r['diagnostics']['original_outside_admitted'], r['diagnostics']['attacker_admitted'],
                     r['diagnostics']['false_seat_share']) for r in rr}) == 1
        violations += (not same) or len(rr) != len(d['carriers'])
    hashes = defaultdict(list)
    for r in pilot:
        hashes[r['packet_hash']].append(r['id'])
    duplicates = sorted(ids for ids in hashes.values() if len(ids) > 1)
    good = [r for r in rows if r['status'] == 'completed']
    latency = [r['accounting']['latency_seconds'] for r in rows if r.get('accounting', {}).get('latency_seconds') is not None]
    return {
        'unit': 'world root', 'rows': len(rows), 'pilot_rows': len(pilot),
        'roots': sorted({r['task'] for r in pilot}),
        'cells': cells, 'cell_count': len(cells),
        'primary': primary if pilot else None,
        'carrier_contrasts': carrier_contrasts if pilot else [],
        'policy_contrasts': policy_contrasts if pilot else [],
        'policy_by_rarity_interactions': interactions if pilot else [],
        'invariance': {'matched_cells': len(matched), 'violations': int(violations)},
        'duplicate_packets': {'distinct_packets': len(hashes), 'assignments': len(pilot), 'duplicate_groups': duplicates},
        'qualification': study.qualification(rows) if any(r['kind'] == 'qualification' for r in rows) else None,
        'resources': {'completed': len(good),
                      'model_calls': sum(bool(r.get('accounting', {}).get('attempted')) for r in rows),
                      'input_tokens': sum(r.get('accounting', {}).get('input_tokens', 0) for r in rows),
                      'output_tokens': sum(r.get('accounting', {}).get('output_tokens', 0) for r in rows),
                      'cost_usd': math.fsum(r.get('accounting', {}).get('actual_usd', 0) for r in rows),
                      'mean_latency_seconds': mean(latency)},
        'bootstrap': dict(d['analysis'], resample_unit='world root'),
    }


if __name__ == '__main__':
    import sys
    print(json.dumps(analyze(read_rows(sys.argv[1])), indent=2))

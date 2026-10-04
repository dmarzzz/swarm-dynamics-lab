"""Root-level descriptive analysis: all cells with full denominators, paired contrasts, and bounds.

The unit is the world root. A failed or not-started call keeps its root: its outcome is bounded in
[0, 1], never dropped and never set to a zero effect. Calls, packets, identities and skills are
not samples. A cell is (carriers, policy, prompt, effort): 5 x 2 x 2 x 2 = 40.
"""
import gzip
import json
import math
from collections import Counter, defaultdict

import numpy as np

import study

METRICS = ('rare_accuracy', 'rare_fabricated', 'rare_null', 'rare_other')
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
    return (r['carriers'], r['arm'], r['prompt'], r['effort'])


def combo(grouped, terms, metric):
    """A linear contrast of cell outcomes, paired by root. terms: [(coefficient, cell key), ...].

    Every outcome lies in [0, 1], so a missing endpoint contributes its bounds: the contrast is
    then reported as bounds over all assigned roots, with the complete-case mean alongside.
    """
    by_task = [{r['task']: r for r in grouped.get(key, [])} for _, key in terms]
    tasks = sorted(set.intersection(*[set(b) for b in by_task])) if by_task and all(by_task) else []
    complete, low, high, per_world = [], [], [], []
    for task in tasks:
        values = [(coef, b[task]['evaluation'][metric] if b[task]['status'] == 'completed' else None)
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
    return {'metric': metric, 'roots': len(tasks), 'complete_roots': len(complete),
            'mean': mean(complete) if full else None,
            'interval': interval(complete) if full else None,
            'all_assigned_bounds': [mean(low), mean(high)] if tasks else None,
            'complete_case_mean': mean(complete), 'per_world': per_world}


def _conditional(good, field):
    """Outcome counts among rare facts whose packet holds a truthful report (admitted, or checked)."""
    counts = Counter()
    for r in good:
        for i, outcome in enumerate(r['evaluation']['rare_outcome']):
            if r['diagnostics'][field][i] > 0:
                counts[outcome] += 1
    return {'denominator': sum(counts.values()), **{o: counts[o] for o in study.OUTCOMES},
            'note': 'conditional diagnostic: valid rows, rare facts with such a truthful report in the packet'}


def _cell(key, rr):
    good = [r for r in rr if r['status'] == 'completed']
    out = {'carriers': key[0], 'arm': key[1], 'prompt': key[2], 'effort': key[3],
           'assigned': len(rr), 'valid': len(good), 'missing': len(rr) - len(good),
           'failed': sum(r['status'] == 'failed' for r in rr), 'not_started': sum(r['status'] == 'not_started' for r in rr)}
    for m in METRICS:
        values = [r['evaluation'][m] for r in good]
        out[m] = {'mean_valid': mean(values),
                  'interval': interval(values) if good and len(good) == len(rr) else None,
                  'all_assigned_bounds': [math.fsum(values) / len(rr), (math.fsum(values) + len(rr) - len(good)) / len(rr)]}
    counts = Counter(o for r in good for o in r['evaluation']['rare_outcome'])
    out['rare_facts'] = {'answered': 3 * len(good), **{o: counts[o] for o in study.OUTCOMES}}
    out['task_accuracy'] = mean(r['evaluation']['task_accuracy'] for r in good)
    out['conditional_on_truth_admitted'] = _conditional(good, 'carriers_admitted_per_fact')
    out['conditional_on_checked_truth_admitted'] = _conditional(good, 'rare_truthful_checked')
    # Same-packet reference rules (offline, every assigned row) and the model minus each on valid rows.
    reference = {}
    for name in study.REFERENCE_RULES:
        reference[name] = {m: mean(r['reference'][name][m] for r in rr) for m in ('rare_accuracy', 'rare_fabricated', 'rare_null')}
        for m in ('rare_accuracy', 'rare_fabricated'):
            reference[name]['model_minus_' + m] = mean(r['evaluation'][m] - r['reference'][name][m] for r in good)
    out['reference'] = reference
    diag = {name: mean(r['diagnostics'][name] for r in rr if r['diagnostics'][name] is not None) for name in DIAGNOSTICS}
    for name in ('rare_truthful_reports', 'rare_false_reports'):
        diag[name] = mean(r['diagnostics'][name][str(s)] for r in rr for s in study.RARE)
    for name in ('rare_truthful_checked', 'rare_false_checked'):
        diag[name] = mean(v for r in rr for v in r['diagnostics'][name])
    out['diagnostics'] = diag
    usage = [r['accounting'] for r in rr if (r.get('accounting') or {}).get('usage_reported')]
    out['mean_output_tokens'] = mean(a['output_tokens'] for a in usage)
    out['mean_latency_seconds'] = mean(a['latency_seconds'] for a in usage if a.get('latency_seconds') is not None)
    return out


def contrasts(grouped):
    """The preregistered primary and secondary contrasts. Keys are (carriers, policy, prompt, effort)."""
    d = study.design()
    p = d['primary_contrast']
    lowest, highest = min(d['carriers']), max(d['carriers'])

    def make(label, metric, terms, **extra):
        out = combo(grouped, terms, metric)
        out.update(label=label, **extra)
        return out
    primary = make('fabricated-answer rate, prompt base minus prompt rule', p['metric'],
                   [(1, (p['carriers'], p['arm'], 'base', p['effort'])), (-1, (p['carriers'], p['arm'], 'rule', p['effort']))],
                   carriers=p['carriers'], arm=p['arm'], effort=p['effort'], useful_difference_pp=p['useful_difference_pp'],
                   status='exploratory, descriptive')
    secondary = []
    for arm in d['arms']:
        c = lowest
        secondary.append(make('effort: low minus high under prompt base', 'rare_fabricated',
                              [(1, (c, arm, 'base', 'low')), (-1, (c, arm, 'base', 'high'))], carriers=c, arm=arm))
        secondary.append(make('rule at effort high: prompt base minus prompt rule', 'rare_fabricated',
                              [(1, (c, arm, 'base', 'high')), (-1, (c, arm, 'rule', 'high'))], carriers=c, arm=arm))
        secondary.append(make('interaction: rule effect at low minus rule effect at high', 'rare_fabricated',
                              [(1, (c, arm, 'base', 'low')), (-1, (c, arm, 'rule', 'low')),
                               (-1, (c, arm, 'base', 'high')), (1, (c, arm, 'rule', 'high'))], carriers=c, arm=arm))
        if arm != p['arm']:
            secondary.append(make('rule at effort low: prompt base minus prompt rule', 'rare_fabricated',
                                  [(1, (c, arm, 'base', 'low')), (-1, (c, arm, 'rule', 'low'))], carriers=c, arm=arm))
    cost = []
    for carriers in d['cost_side']['carriers']:
        for arm in d['arms']:
            for effort in d['efforts']:
                cost.append(make('cost side: accuracy, prompt rule minus prompt base', 'rare_accuracy',
                                 [(1, (carriers, arm, 'rule', effort)), (-1, (carriers, arm, 'base', effort))],
                                 carriers=carriers, arm=arm, effort=effort))
            for prompt in d['prompts']:
                cost.append(make('cost side: accuracy, effort high minus low', 'rare_accuracy',
                                 [(1, (carriers, arm, prompt, 'high')), (-1, (carriers, arm, prompt, 'low'))],
                                 carriers=carriers, arm=arm, prompt=prompt))
    by_carriers = []
    for carriers in d['carriers']:
        for arm in d['arms']:
            for effort in d['efforts']:
                for metric in ('rare_fabricated', 'rare_accuracy', 'rare_null'):
                    by_carriers.append(make('prompt rule minus prompt base', metric,
                                            [(1, (carriers, arm, 'rule', effort)), (-1, (carriers, arm, 'base', effort))],
                                            carriers=carriers, arm=arm, effort=effort))
    replication = make('replication of the earlier primary: accuracy, 1 carrier minus 81 (never pooled with the earlier cohort)',
                       'rare_accuracy', [(1, (lowest, 'random', 'base', 'low')), (-1, (highest, 'random', 'base', 'low'))],
                       arm='random', prompt='base', effort='low')
    return primary, secondary, cost, by_carriers, replication


def analyze(rows):
    d = study.design()
    models = sorted({r['model'] for r in rows if r.get('model')})
    if len(models) > 1:
        raise ValueError('mixed_models')        # every table is for one model; models are never pooled
    pilot = [r for r in rows if r['kind'] == 'pilot']
    grouped = defaultdict(list)
    for r in pilot:
        grouped[cell_key(r)].append(r)
    cells = [_cell(key, grouped[key]) for key in sorted(grouped)]
    primary = secondary = cost = by_carriers = replication = None
    if pilot:
        primary, secondary, cost, by_carriers, replication = contrasts(grouped)

    # Invariance: audits, admission and order identical across carrier counts and configurations of a
    # root and policy; the four configurations of a packet share one packet hash.
    matched, packets = defaultdict(list), defaultdict(list)
    for r in pilot:
        matched[(r['task'], r['attacker_pass'], r['arm'], r['checks'])].append(r)
        packets[(r['task'], r['arm'], r['carriers'])].append(r)
    violations = 0
    for rr in matched.values():
        same = len({(r['admitted_hash'], r['audit_hash'], r['order_hash'],
                     r['diagnostics']['original_outside_admitted'], r['diagnostics']['attacker_admitted'],
                     r['diagnostics']['false_seat_share']) for r in rr}) == 1
        violations += (not same) or len(rr) != len(d['carriers']) * len(d['configurations'])
    configuration_violations = sum(
        len({r['packet_hash'] for r in rr}) != 1 or sorted((r['prompt'], r['effort']) for r in rr) != sorted(study.configurations())
        for rr in packets.values())
    hashes = defaultdict(set)
    for key, rr in packets.items():
        hashes[rr[0]['packet_hash']].add(key)
    good = [r for r in rows if r['status'] == 'completed']
    good_pilot = [r for r in pilot if r['status'] == 'completed']
    failures = Counter(r.get('error') for r in rows if r['status'] == 'failed')
    resources = {}
    for effort in d['efforts']:
        usage = [r['accounting'] for r in rows if r.get('effort') == effort and (r.get('accounting') or {}).get('usage_reported')]
        latency = [a['latency_seconds'] for a in usage if a.get('latency_seconds') is not None]
        resources[effort] = {'calls': len(usage), 'cost_usd': math.fsum(a['actual_usd'] for a in usage),
                             'mean_input_tokens': mean(a['input_tokens'] for a in usage),
                             'mean_output_tokens': mean(a['output_tokens'] for a in usage),
                             'max_output_tokens': max([a['output_tokens'] for a in usage], default=None),
                             'mean_latency_seconds': mean(latency), 'max_latency_seconds': max(latency, default=None),
                             'mean_cost_usd': mean(a['actual_usd'] for a in usage)}
    return {
        'model': models[0] if models else None,
        'unit': 'world root', 'rows': len(rows), 'pilot_rows': len(pilot),
        'roots': sorted({r['task'] for r in pilot}),
        'cells': cells, 'cell_count': len(cells),
        'primary': primary,
        'secondary': secondary or [], 'cost_side': cost or [], 'rule_minus_base_by_carriers': by_carriers or [],
        'replication_of_earlier_primary': replication,
        'overall': {m: mean(r['evaluation'][m] for r in good_pilot) for m in ('rare_fabricated', 'rare_accuracy')},
        'reference_cells': study.reference_cell_means(rows) if pilot else [],
        'invariance': {'matched_cells': len(matched), 'violations': int(violations),
                       'packets': len(packets), 'configuration_violations': int(configuration_violations)},
        'duplicate_packets': {'distinct_packets': len(hashes), 'packets': len(packets),
                              'duplicate_groups': sorted(sorted(map(list, keys)) for keys in hashes.values() if len(keys) > 1)},
        'qualification': study.qualification(rows) if any(r['kind'] == 'qualification' for r in rows) else None,
        'missing': {'failed': sum(r['status'] == 'failed' for r in rows),
                    'not_started': sum(r['status'] == 'not_started' for r in rows),
                    'failure_categories': dict(sorted((str(k), v) for k, v in failures.items())),
                    'rule': 'every failed or not-started call stays in its cell denominator with outcome bounds 0 and 1'},
        'resources': {'completed': len(good),
                      'model_calls': sum(bool((r.get('accounting') or {}).get('attempted')) for r in rows),
                      'input_tokens': sum((r.get('accounting') or {}).get('input_tokens', 0) for r in rows),
                      'output_tokens': sum((r.get('accounting') or {}).get('output_tokens', 0) for r in rows),
                      'cost_usd': math.fsum((r.get('accounting') or {}).get('actual_usd', 0) for r in rows),
                      'count_fallbacks': sum(bool((r.get('accounting') or {}).get('count_fallback')) for r in rows),
                      'by_effort': resources},
        'bootstrap': dict(d['analysis'], resample_unit='world root'),
    }


if __name__ == '__main__':
    import sys
    print(json.dumps(analyze(read_rows(sys.argv[1])), indent=2))

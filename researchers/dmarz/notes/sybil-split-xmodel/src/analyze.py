"""Root-cluster descriptive estimates: full denominators, paired contrasts, bounded missing outcomes.

The parent's analysis (sybil-split-opus/src/analyze.py) unchanged, on this chain's model, plus one
secondary block, `versus_parent`: this model minus the parent's Opus 5.5 answers on the same
byte-identical packets, paired by root (the parent's recorded S1 rows, pinned by SHA-256), per cell
and for the primary contrast; never pooled. Descriptive only.

The independent unit is a root (one graph and task), paired across identity counts, policies,
budgets and check strengths within its graph family. Calls, skills and identities are not samples.
"""
import argparse
import gzip
import json
from collections import defaultdict

import numpy as np

import sim
import study

SOURCES = {'model': 'evaluation', 'plurality': 'scripted_evaluation', 'identity_plurality': 'identity_evaluation'}
OUTCOMES = ('rare_wrong', 'rare_accuracy', 'rare_abstain', 'rare_fabricated', 'task_accuracy')
ADMISSION = ('attacker_seat_share', 'attacker_row_share', 'attacker_identities_admitted', 'attacker_rows_admitted',
             'specialist_retention', 'honest_rare_rows', 'attacker_checked', 'attacker_passed', 'packet_rows', 'checks')


def read_rows(path):
    opener = gzip.open if str(path).endswith('.gz') else open
    with opener(path, 'rt') as f: return [json.loads(line) for line in f if line.strip()]


def mean(values):
    values = list(values)
    return sum(values) / len(values) if values else None


def interval(by_family):
    """Percentile interval of the equally weighted mean of family means; roots are resampled
    with replacement inside each family (10,000 draws, fixed seed)."""
    d = study.design()['analysis']
    arrays = [np.array(v, dtype=float) for v in by_family.values() if len(v)]
    if not arrays or len(arrays) != len(by_family): return None
    rng = np.random.default_rng(d['bootstrap_seed'])
    draws = np.mean([a[rng.integers(0, len(a), (d['bootstrap_draws'], len(a)))].mean(axis=1) for a in arrays], axis=0)
    return [float(x) for x in np.quantile(draws, [.025, .975])]


def index(rows):
    """(family, task) -> {(attacker_pass, arm, checks, k): row}; pilot rows only, every status."""
    table = defaultdict(dict)
    for r in rows:
        if r['kind'] == 'pilot': table[(r['family'], r['task'])][(r['attacker_pass'], r['arm'], r['checks'], r['k'])] = r
    return table


def value(row, source, field):
    if row is None or row.get('status') != 'completed': return None
    return row[SOURCES[source]][field]


def contrast(table, terms, source='model', field='rare_wrong', lo=0.0, hi=1.0):
    """terms: [(weight, (attacker_pass, arm, checks, k)), ...]. Per root the weighted sum; a root
    with any missing term is left out of the complete-case estimate and kept in the bounds, where
    each missing outcome takes the value in [lo, hi] that makes the contrast smallest or largest."""
    families = study.design()['families']
    complete = {f: [] for f in families}; low = {f: [] for f in families}; high = {f: [] for f in families}; per_root = []
    for (family, task), cells in sorted(table.items()):
        vals = [(wt, value(cells.get(key), source, field)) for wt, key in terms]
        missing = sum(v is None for _, v in vals)
        d_low = sum(wt * (v if v is not None else (lo if wt > 0 else hi)) for wt, v in vals)
        d_high = sum(wt * (v if v is not None else (hi if wt > 0 else lo)) for wt, v in vals)
        low[family].append(d_low); high[family].append(d_high)
        d = None
        if not missing:
            d = sum(wt * v for wt, v in vals); complete[family].append(d)
        per_root.append({'family': family, 'task': task, 'difference': d, 'missing_terms': missing})
    def weighted(groups):
        means = [mean(v) for v in groups.values()]
        return None if any(m is None for m in means) else sum(means) / len(means)
    return {'estimate': weighted(complete), 'interval': interval(complete),
            'by_family': {f: {'mean': mean(v), 'roots': len(v), 'interval': interval({f: v})} for f, v in complete.items()},
            'assigned_roots': {f: len(v) for f, v in low.items()},
            'bounds_all_assigned': [weighted(low), weighted(high)], 'per_root': per_root}


def split_terms(rate, checks, arm, k_high=27, k_low=1):
    return [(1, (rate, arm, 0 if arm == 'no_verification' else checks, k_high)),
            (-1, (rate, arm, 0 if arm == 'no_verification' else checks, k_low))]


def interaction_terms(rate, checks, arm_a, arm_b, k_high=27, k_low=1):
    """(arm_a at k_high minus k_low) minus (arm_b at k_high minus k_low)."""
    return split_terms(rate, checks, arm_a, k_high, k_low) + [(-wt, key) for wt, key in split_terms(rate, checks, arm_b, k_high, k_low)]


def cells(rows):
    grouped = defaultdict(list)
    for r in rows:
        if r['kind'] == 'pilot': grouped[(r['family'], r['attacker_pass'], r['arm'], r['checks'], r['k'])].append(r)
    out = []
    for key, rr in sorted(grouped.items()):
        good = [r for r in rr if r['status'] == 'completed']
        cell = dict(zip(('family', 'attacker_pass', 'arm', 'checks', 'k'), key), assigned=len(rr), valid=len(good),
                    failed=sum(r['status'] == 'failed' for r in rr), not_started=sum(r['status'] == 'not_started' for r in rr))
        for source, name in SOURCES.items():
            have = [r for r in good if name in r]
            cell[source] = {f: mean(r[name][f] for r in have) for f in OUTCOMES}
        # admission is computed before any model call, so it is known for every assigned row
        cell['admission_all_assigned'] = {f: mean(r['admission'][f] for r in rr if 'admission' in r) for f in ADMISSION}
        # all-assigned bounds on the model's wrong-answer rate: a missing outcome is 0 or 1
        got = sum(r['evaluation']['rare_wrong'] for r in good)
        cell['rare_wrong_bounds_all_assigned'] = [got / len(rr), (got + len(rr) - len(good)) / len(rr)]
        cell['input_tokens'] = sum(r.get('accounting', {}).get('input_tokens', 0) for r in rr)
        cell['output_tokens'] = sum(r.get('accounting', {}).get('output_tokens', 0) for r in rr)
        cell['cost_usd'] = sum(r.get('accounting', {}).get('actual_usd', 0) for r in rr)
        out.append(cell)
    return out


def test_retest(rows):
    """Assignments of one root that received byte-identical packets (for example no-check cells at
    both check strengths): how often the model returned the same answer."""
    groups = defaultdict(list)
    for r in rows:
        if r['kind'] == 'pilot' and r['status'] == 'completed' and r.get('backend') != 'scripted':
            groups[(r['family'], r['task'], r['packet_hash'])].append(json.dumps(r['answer'], sort_keys=True))
    repeated = [v for v in groups.values() if len(v) > 1]
    return {'packets_seen_more_than_once': len(repeated), 'calls_in_those_groups': sum(len(v) for v in repeated),
            'groups_with_identical_answers': sum(len(set(v)) == 1 for v in repeated)}


def versus_parent(rows, table):
    """This model minus the parent's model on the same assignments (same ids, same packets)."""
    try:
        parent_rows = list(study.parent_s1_records().values())
    except (OSError, ValueError):
        return {'note': 'parent records unavailable'}
    if not any(r['kind'] == 'pilot' and r.get('id') in {p['id'] for p in parent_rows} for r in rows):
        return {'note': 'no assignment shared with the parent run (not an S1 stage)'}
    ptable = index(parent_rows); d = study.design(); a = d['attacker']
    terms = interaction_terms(min(a['attacker_pass']), max(d['check_budgets']), 'degree', 'coverage')
    mine, theirs = contrast(table, terms), contrast(ptable, terms)
    per = {f: [] for f in d['families']}
    for m, o in zip(mine['per_root'], theirs['per_root']):
        assert (m['family'], m['task']) == (o['family'], o['task'])
        if m['difference'] is not None and o['difference'] is not None: per[m['family']].append(m['difference'] - o['difference'])
    means = [mean(v) for v in per.values()]
    primary = {'this_model': mine['estimate'], 'parent_model': theirs['estimate'],
               'difference': None if any(x is None for x in means) else sum(means) / len(means),
               'interval': interval(per), 'roots': {f: len(v) for f, v in per.items()}}
    by_id = {r['id']: r for r in parent_rows}; cells_out = []; same = total = 0
    grouped = defaultdict(list)
    for r in rows:
        o = by_id.get(r.get('id'))
        if r['kind'] != 'pilot' or o is None: continue
        if r['status'] == 'completed' and o['status'] == 'completed':
            total += 1; same += r['answer']['values'] == o['answer']['values']
        grouped[(r['attacker_pass'], r['arm'], r['checks'], r['k'])].append((r, o))
    for key, pairs in sorted(grouped.items()):
        cell = dict(zip(('attacker_pass', 'arm', 'checks', 'k'), key))
        for field in ('rare_wrong', 'rare_accuracy', 'rare_abstain'):
            fam = {f: [] for f in d['families']}
            for r, o in pairs:
                if r['status'] == 'completed' and o['status'] == 'completed':
                    fam[r['family']].append(r['evaluation'][field] - o['evaluation'][field])
            ms = [mean(v) for v in fam.values()]
            cell[field] = {'difference': None if any(x is None for x in ms) else sum(ms) / len(ms),
                           'by_family': {f: mean(v) for f, v in fam.items()}, 'pairs': sum(len(v) for v in fam.values())}
        cells_out.append(cell)
    return {'primary': primary, 'cells': cells_out, 'identical_answers': same, 'compared_answers': total}


def analyze(rows):
    d = study.design(); table = index(rows); a = d['attacker']
    informative, unreliable = min(a['attacker_pass']), max(a['attacker_pass'])
    large = max(d['check_budgets']); pc = d['primary_contrast']
    assert (pc['attacker_pass'], pc['checks'], pc['metric']) == (informative, large, 'rare_wrong')
    def trimmed(c):
        return {k: v for k, v in c.items() if k != 'per_root'}
    primary = contrast(table, interaction_terms(informative, large, 'degree', 'coverage'))
    secondary = {
        'primary_under_unreliable_checks': trimmed(contrast(table, interaction_terms(unreliable, large, 'degree', 'coverage'))),
        'primary_at_small_budget': trimmed(contrast(table, interaction_terms(informative, min(d['check_budgets']), 'degree', 'coverage'))),
        'primary_by_plurality': trimmed(contrast(table, interaction_terms(informative, large, 'degree', 'coverage'), 'plurality')),
        'primary_by_identity_plurality': trimmed(contrast(table, interaction_terms(informative, large, 'degree', 'coverage'), 'identity_plurality')),
        'random_minus_coverage': trimmed(contrast(table, interaction_terms(informative, large, 'random', 'coverage'))),
        'degree_minus_random': trimmed(contrast(table, interaction_terms(informative, large, 'degree', 'random'))),
        'primary_on_rare_accuracy': trimmed(contrast(table, interaction_terms(informative, large, 'degree', 'coverage'), field='rare_accuracy')),
    }
    multiplicity = []
    for rate in a['attacker_pass']:
        for arm in d['arms']:
            for checks in ([0] if arm == 'no_verification' else d['check_budgets']):
                for k in a['identities'][1:]:
                    for source in ('model', 'plurality'):
                        c = contrast(table, split_terms(rate, checks, arm, k, a['identities'][0]), source)
                        multiplicity.append(dict(attacker_pass=rate, arm=arm, checks=checks, k=k, source=source, **trimmed(c)))
    gaps = []
    for rate in a['attacker_pass']:
        for arm in d['arms']:
            for checks in ([0] if arm == 'no_verification' else d['check_budgets']):
                for k in a['identities']:
                    for field in ('rare_wrong', 'rare_accuracy'):
                        per = {f: [] for f in d['families']}
                        for (family, task), cc in table.items():
                            r = cc.get((rate, arm, checks, k))
                            if r is not None and r['status'] == 'completed':
                                per[family].append(r['evaluation'][field] - r['scripted_evaluation'][field])
                        means = [mean(v) for v in per.values()]
                        gaps.append(dict(attacker_pass=rate, arm=arm, checks=checks, k=k, field=field,
                                         model_minus_plurality=None if any(m is None for m in means) else sum(means) / len(means),
                                         interval=interval(per), roots={f: len(v) for f, v in per.items()}))
    pilot = [r for r in rows if r['kind'] == 'pilot']
    return {'design': {'primary_contrast': pc, 'useful_difference': pc['useful_difference_pp'] / 100,
                       'bootstrap': d['analysis'], 'unit': 'root (graph and task), stratified by graph family'},
            'denominators': {'assigned': len(pilot), 'completed': sum(r['status'] == 'completed' for r in pilot),
                             'failed': sum(r['status'] == 'failed' for r in pilot),
                             'not_started': sum(r['status'] == 'not_started' for r in pilot),
                             'roots': {f: len({t for (ff, t) in table if ff == f}) for f in d['families']}},
            'primary': primary, 'secondary': secondary, 'multiplicity': multiplicity,
            'model_minus_plurality': gaps, 'test_retest': test_retest(rows), 'cells': cells(rows),
            'versus_parent': versus_parent(rows, table)}


def scripted_cells(split='engineering', attacker=None, by_identity=False):
    """Plurality outcomes on a split without any model, for a given attacker configuration.
    Used for the engineering-root calibration record; never run on comparison roots for tuning."""
    d = study.design(); a = dict(d['attacker']); a.update(attacker or {}); c = study.cfg()
    grouped = defaultdict(list)
    for family, task in study.roots(split):
        for rate in a['attacker_pass']:
            for k in a['identities']:
                w = study.world(family, task, k, rate, attacker=a)
                for rec in sim.checkpoints(w, d['check_budgets'], d['arms'], c):
                    g = sim.grade(sim.plurality(w, rec['admitted'], by_identity), w['answers'], w['fabricated'])
                    grouped[(family, rate, rec['arm'], rec['checks'], k)].append(dict(rec['admission'], **g))
    return {key: {f: mean(r[f] for r in rr) for f in rr[0]} for key, rr in grouped.items()}


def calibration_text(split='engineering', attacker=None, by_identity=False,
                     fields=('rare_wrong', 'rare_accuracy', 'attacker_identities_admitted', 'specialist_retention')):
    d = study.design(); table = scripted_cells(split, attacker, by_identity); ks = d['attacker']['identities']; lines = []
    for family in d['families']:
        for rate in d['attacker']['attacker_pass']:
            lines.append(f'{family}, attacker pass {rate}: columns are k = {", ".join(map(str, ks))}')
            for arm in d['arms']:
                for checks in ([0] if arm == 'no_verification' else d['check_budgets']):
                    parts = ['  '.join(f'{table[(family, rate, arm, checks, k)][f]:5.2f}' for k in ks) for f in fields]
                    lines.append(f'  {arm:15s} {checks:2d} | ' + ' | '.join(parts))
    lines.append('fields: ' + ' | '.join(fields))
    for rate in d['attacker']['attacker_pass']:
        big = max(d['check_budgets'])
        per = [(table[(f, rate, 'degree', big, 27)]['rare_wrong'] - table[(f, rate, 'degree', big, 1)]['rare_wrong'])
               - (table[(f, rate, 'coverage', big, 27)]['rare_wrong'] - table[(f, rate, 'coverage', big, 1)]['rare_wrong'])
               for f in d['families']]
        lines.append(f'plurality value of the primary contrast at attacker pass {rate}: ' +
                     ', '.join(f'{f} {v:+.3f}' for f, v in zip(d['families'], per)) + f', equal-weight mean {sum(per) / len(per):+.3f}')
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(description='Recompute the analysis from saved rows, or print the engineering calibration.')
    sub = ap.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('rows'); r.add_argument('episodes')
    c = sub.add_parser('calibration'); c.add_argument('--internal-links', choices=['ring2', 'none'])
    c.add_argument('--by-identity', action='store_true')
    args = ap.parse_args()
    if args.cmd == 'rows':
        print(json.dumps(analyze(read_rows(args.episodes))))
    else:
        print(calibration_text('engineering', {'internal_links': args.internal_links} if args.internal_links else None, args.by_identity))


if __name__ == '__main__':
    main()

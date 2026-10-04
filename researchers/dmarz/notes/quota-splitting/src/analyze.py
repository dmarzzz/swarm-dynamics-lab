"""Root-cluster descriptive estimates: full denominators, paired contrasts, bounded missing outcomes.

The independent unit is a root (one job and team order), paired across the 8 conditions and the
3 pressures. Episodes, rounds, calls and identities are not samples.

  python3 src/analyze.py calibration          reference planners on the engineering roots (no model)
  python3 src/analyze.py rows <episodes.jsonl[.gz]> [--planner maximising]
"""
import argparse
import gzip
import json

import numpy as np

import study

KINDS = ('comparison', 'engineering')
FIELDS = ('subagents_created', 'units_beyond_share', 'completion')
# (name, condition, minus condition) of every prespecified contrast, evaluated at each pressure
CONTRASTS = (('B_minus_N', 'B', 'N'), ('Bp_minus_B', 'Bp', 'B'), ('C_minus_B', 'C', 'B'), ('D_minus_N', 'D', 'N'),
             ('E1_minus_B', 'E1', 'B'), ('E2_minus_B', 'E2', 'B'), ('A_minus_N', 'A', 'N'))


def read_rows(path):
    opener = gzip.open if str(path).endswith('.gz') else open
    with opener(path, 'rt') as f: return [json.loads(line) for line in f if line.strip()]


def mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else None


def actor(stage):
    """Whose episodes a stage's analysis describes: the model's, or in the scripted stage the
    `maximising` planner's (labelled as scripted wherever it is shown)."""
    return 'maximising' if stage == 'S0' else None


def interval(values):
    """Percentile interval of the mean over roots; roots resampled with replacement."""
    d = study.design()['analysis']
    if not values: return None
    a = np.array(values, dtype=float); rng = np.random.default_rng(d['bootstrap_seed'])
    draws = a[rng.integers(0, len(a), (d['bootstrap_draws'], len(a)))].mean(axis=1)
    return [float(x) for x in np.quantile(draws, [.025, .975])]


def value(row, field):
    if row is None or row.get('status') != 'completed': return None
    return row['outcome'][field]


def span(field, w):
    """Smallest and largest value an outcome can take in one episode (for missing-outcome bounds)."""
    if field == 'subagents_created': return 0.0, float(w['max_subagents'])
    if field == 'units_beyond_share': return 0.0, float(max(0, w['job_units'] - w['quota']))
    return 0.0, 1.0


def contrast(table, roots, a, b, pressure, field='subagents_created'):
    """Per root: outcome in condition `a` minus outcome in condition `b` at one pressure. A root
    with a missing outcome is left out of the complete-case estimate and kept in the bounds, where
    each missing outcome takes the value that makes the contrast smallest or largest."""
    complete, low, high, per_root = [], [], [], []
    for root in roots:
        lo, hi = span(field, study.world(root, pressure))
        va, vb = value(table.get((root, a, pressure)), field), value(table.get((root, b, pressure)), field)
        low.append((va if va is not None else lo) - (vb if vb is not None else hi))
        high.append((va if va is not None else hi) - (vb if vb is not None else lo))
        d = None if va is None or vb is None else va - vb
        if d is not None: complete.append(d)
        per_root.append({'root': root, 'difference': d, 'missing_terms': (va is None) + (vb is None)})
    return {'estimate': mean(complete), 'interval': interval(complete), 'roots': len(complete), 'assigned_roots': len(roots),
            'bounds_all_assigned': [mean(low), mean(high)] if roots else [None, None], 'per_root': per_root}


def cell(rows, condition, pressure, limit):
    mine = [r for r in rows if r['condition'] == condition and r['pressure'] == pressure]
    good = [r for r in mine if r['status'] == 'completed']; n = len(good)
    def m(fn): return mean(fn(r) for r in good)
    spawn_turns = [note for r in good for note in r.get('spawn_notes', [])]
    out = {'condition': condition, 'pressure': pressure, 'assigned': len(mine), 'valid': n,
           'failed': sum(r['status'] == 'failed' for r in mine), 'interrupted': sum(r['status'] == 'interrupted' for r in mine),
           'not_started': sum(r['status'] == 'not_started' for r in mine),
           'subagents_created': m(lambda r: r['outcome']['subagents_created']),
           'units_beyond_share': m(lambda r: r['outcome']['units_beyond_share']),
           'beyond_share_of_quota': m(lambda r: r['outcome']['units_beyond_share'] / r['outcome']['quota']),
           'scripted_lost': m(lambda r: r['outcome']['scripted_lost']),
           'scripted_received_share': m(lambda r: 1 - r['outcome']['scripted_lost'] / (3 * r['outcome']['quota'])),
           'completion': m(lambda r: r['outcome']['completion']),
           'job_complete': m(lambda r: float(r['outcome']['job_complete'])),
           'deadline_miss': m(lambda r: float(not r['outcome']['job_complete'])),
           'turns': m(lambda r: r['outcome']['turns']),
           'clean_turn_rate': (sum(r['outcome']['clean_turns'] for r in good) / max(1, sum(r['outcome']['turns'] for r in good))) if n else None,
           'finished_early': m(lambda r: float(r['outcome']['finish_round'] is not None)),
           'fees_paid': m(lambda r: r['outcome']['fees_paid']),
           'not_applied': {}, 'spawn_turns': len(spawn_turns),
           'spawn_turns_mentioning_quota': sum(note['mentions_quota'] for note in spawn_turns)}
    for r in good:
        for key, count in r['outcome']['not_applied'].items(): out['not_applied'][key] = out['not_applied'].get(key, 0) + count
    out['subagents_bounds_all_assigned'] = [None, None] if not mine else [
        (sum(r['outcome']['subagents_created'] for r in good) + 0 * (len(mine) - n)) / len(mine),
        (sum(r['outcome']['subagents_created'] for r in good) + limit * (len(mine) - n)) / len(mine)]
    out['reference'] = {mode: {field: m(lambda r: r['reference'][mode][field]) for field in FIELDS}
                        for mode in study.design()['reference_planners']} if n else None
    out['minus_reference'] = {mode: {field: out[field] - out['reference'][mode][field] for field in FIELDS}
                              for mode in study.design()['reference_planners']} if n else None
    return out


def analyze(rows, planner=None):
    """Everything reported for a set of episode rows. `planner` selects the model's rows (None)
    or one scripted planner's rows."""
    d = study.design(); limit = d['world']['max_subagents']; top = max(d['pressures'])
    rows = [r for r in rows if r['kind'] in KINDS and r['planner'] == planner]
    table = {(r['root'], r['condition'], r['pressure']): r for r in rows}
    roots = sorted({r['root'] for r in rows})
    cells = [cell(rows, c, p, limit) for c in d['conditions'] for p in d['pressures']]
    primary = contrast(table, roots, 'B', 'N', top)
    secondary = {}
    for name, a, b in CONTRASTS:
        for p in d['pressures']:
            for field in FIELDS:
                c = contrast(table, roots, a, b, p, field)
                secondary[f'{name}@{p}:{field}'] = {k: c[k] for k in ('estimate', 'interval', 'roots', 'assigned_roots', 'bounds_all_assigned')}
    control = []
    for root in roots:
        vals = [value(table.get((root, 'N', p)), 'subagents_created') for p in d['pressures']]
        if all(v is not None for v in vals): control.append({'root': root, 'subagents': vals, 'range': max(vals) - min(vals)})
    by_cell = {(c['condition'], c['pressure']): c for c in cells}
    return {'actor': planner or 'model', 'primary': dict(primary, definition=d['primary_contrast']['definition'],
                                                         useful_difference=d['primary_contrast']['useful_difference']),
            'secondary': secondary, 'cells': cells,
            'control_replicates': {'roots': len(control), 'identical': sum(c['range'] == 0 for c in control),
                                   'mean_range': mean(c['range'] for c in control), 'per_root': control},
            'headline': {'units_beyond_share': by_cell[('B', top)]['units_beyond_share'], 'job_completion': mean(c['completion'] for c in cells)},
            'denominators': {'assigned': len(rows), 'valid': sum(r['status'] == 'completed' for r in rows),
                             'failed': sum(r['status'] == 'failed' for r in rows),
                             'interrupted': sum(r['status'] == 'interrupted' for r in rows),
                             'not_started': sum(r['status'] == 'not_started' for r in rows), 'roots': len(roots)}}


def scripted_rows(stage='S0'):
    """Rows as the worker writes them in the scripted stage, without a hub or files."""
    rows = []
    for a in study.assignments(stage):
        answers = study.scripted_answers(a, a['planner'] or 'parallel'); turns, outcome = study.replay(a, answers)
        turns = [dict(t, answer=study.stored(ans), accounting={'attempted': False}) for t, ans in zip(turns, answers)]
        r = {key: a[key] for key in study.ROW_FIELDS}
        r.update(status='completed', turns=turns, outcome=outcome, reference=study.reference(a), spawn_notes=study.spawn_notes(turns))
        rows.append(r)
    return rows


def calibration():
    """Cell means of the three reference planners on the engineering roots (scripted, not model evidence)."""
    d = study.design(); rows = scripted_rows('S0'); out = {}
    for mode in d['reference_planners']:
        a = analyze(rows, mode)
        out[mode] = {'primary': a['primary']['estimate'],
                     'cells': {f'{c["condition"]}@{c["pressure"]}': {k: c[k] for k in ('subagents_created', 'units_beyond_share', 'completion', 'turns', 'clean_turn_rate')}
                               for c in a['cells']}}
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True); sub.add_parser('calibration')
    r = sub.add_parser('rows'); r.add_argument('path'); r.add_argument('--planner')
    a = ap.parse_args()
    if a.cmd == 'calibration':
        cal = calibration(); d = study.design()
        for mode, c in cal.items():
            print(f'{mode}: subagents created | units beyond one quota | share of job done   (columns: pressure {d["pressures"]}; SCRIPTED, 2 engineering roots)')
            for cond in d['conditions']:
                cells = [c['cells'][f'{cond}@{p}'] for p in d['pressures']]
                print(f'  {cond:3s} ' + ' '.join(f'{x["subagents_created"]:.2f}' for x in cells) + ' | ' +
                      ' '.join(f'{x["units_beyond_share"]:5.1f}' for x in cells) + ' | ' + ' '.join(f'{x["completion"]:.2f}' for x in cells))
            print(f'  primary contrast (B minus N at pressure {max(d["pressures"])}): {c["primary"]:+.2f}')
    else:
        print(json.dumps(analyze(read_rows(a.path), a.planner), sort_keys=True))


if __name__ == '__main__':
    main()

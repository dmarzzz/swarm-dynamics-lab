"""Root-paired descriptive analysis of one model's chain, and the paired comparison with the parent
(sybil-scarcity-opus, claude-opus-5-5) on the identical packets. The independent unit is a world
root. Model outcomes exist only for completed calls; they are reported complete-case with
denominators and with bounds in which each missing outcome is 0 or 1. Nothing is pooled across
models: the parent's outcomes are only ever subtracted root by root, cell by cell."""
import argparse
import gzip
import hashlib
import json
import math
from collections import defaultdict

import numpy as np

import study

OUTCOMES = ('rare_accuracy', 'rare_fabricated', 'rare_null', 'rare_other_wrong', 'rare_wrong', 'task_accuracy')
DIAGNOSTICS = ('truth_available', 'carrier_survival', 'attacker_seat_share', 'original_outside_retention')
CELL = ('arm', 'checks', 'attacker_pass', 'carriers')


def mean(values):
    values = list(values)
    return math.fsum(values) / len(values) if values else None


def interval(values):
    """95% percentile interval of the mean over roots: 10,000 bootstrap draws, fixed seed."""
    d = study.design()['analysis']
    if not values: return None
    a = np.array(values, dtype=float); rng = np.random.default_rng(d['bootstrap_seed'])
    draws = a[rng.integers(0, len(a), (d['bootstrap_draws'], len(a)))].mean(axis=1)
    return [float(x) for x in np.quantile(draws, [.025, .975])]


def key(r):
    return tuple(r[k] for k in CELL)


def table(rows):
    """cell -> task -> row; S1 grid rows of every status."""
    t = defaultdict(dict)
    for r in rows:
        if r['kind'] == 'pilot': t[key(r)][r['task']] = r
    return t


def paired(t, hi, lo, field='rare_accuracy'):
    """(hi minus lo) per root over the roots assigned in both cells: complete-case values, and bounds
    with each missing outcome at 0 or 1."""
    complete, low, high = [], [], []
    for task in sorted(set(t.get(hi, {})) & set(t.get(lo, {}))):
        a, b = t[hi][task], t[lo][task]
        va = a['evaluation'][field] if a['status'] == 'completed' else None
        vb = b['evaluation'][field] if b['status'] == 'completed' else None
        low.append((0.0 if va is None else va) - (1.0 if vb is None else vb))
        high.append((1.0 if va is None else va) - (0.0 if vb is None else vb))
        if va is not None and vb is not None: complete.append({'task': task, 'difference': va - vb})
    values = [x['difference'] for x in complete]
    return {'estimate_pp': None if not values else 100 * mean(values),
            'interval_pp': None if not values else [100 * x for x in interval(values)],
            'bounds_pp': None if not low else [100 * mean(low), 100 * mean(high)],
            'complete_roots': len(values), 'assigned_roots': len(low), 'per_root': complete}


def cells(t):
    out = []
    for k in sorted(t, key=lambda k: json.dumps(k)):
        rr = list(t[k].values()); good = [r for r in rr if r['status'] == 'completed']; n = len(rr)
        cell = dict(zip(CELL, k), assigned=n, valid=len(good), failed=sum(r['status'] == 'failed' for r in rr),
                    not_started=sum(r['status'] == 'not_started' for r in rr))
        cell['model'] = {f: mean(r['evaluation'][f] for r in good) for f in OUTCOMES}
        cell['reference_plurality'] = {f: mean(r['reference_evaluation'][f] for r in good) for f in OUTCOMES}
        cell['diagnostics'] = {f: mean(r['diagnostics'][f] for r in rr if r['diagnostics'][f] is not None) for f in DIAGNOSTICS}
        got = math.fsum(r['evaluation']['rare_accuracy'] for r in good)
        cell['rare_accuracy_bounds_all_assigned'] = [got / n, (got + (n - len(good))) / n] if n else None
        cell['normalized_answers'] = sum(bool((r.get('answer') or {}).get('normalized')) for r in good)
        out.append(cell)
    return out


def parent_rows():
    """The parent's sanitized S1 rows (claude-opus-5-5), pinned by SHA-256. None if unavailable."""
    path = study.parent_dir() / 'records' / 's1-episodes.jsonl.gz'
    if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != study.design()['parent']['s1_episodes_sha256']:
        return None
    with gzip.open(path, 'rt') as f:
        return {r['id']: r for r in (json.loads(line) for line in f if line.strip())}


def versus_parent(rows):
    """Per cell, this model minus Opus 5.5 on the same root and the same packet (packet hashes must
    match), both answers graded by this study's grader. Descriptive; never pooled."""
    parent = parent_rows()
    if parent is None: return {'available': False}
    diffs = defaultdict(list); mismatched = 0; theirs = defaultdict(list)
    for r in rows:
        if r['kind'] != 'pilot': continue
        p = parent.get(r['id'])
        if p is None or p['packet_hash'] != r['packet_hash']: mismatched += 1; continue
        if p.get('status') != 'completed': continue
        e_p = study.evaluate(r, p['answer'])
        theirs[key(r)].append(e_p)
        if r['status'] == 'completed':
            diffs[key(r)].append({f: r['evaluation'][f] - e_p[f] for f in OUTCOMES})
    out = []
    for k in sorted(set(diffs) | set(theirs), key=lambda k: json.dumps(k)):
        acc = [d['rare_accuracy'] for d in diffs[k]]
        out.append(dict(zip(CELL, k), paired_roots=len(acc),
                        model_minus_parent_pp={f: None if not diffs[k] else 100 * mean(d[f] for d in diffs[k]) for f in OUTCOMES},
                        rare_accuracy_interval_pp=None if not acc else [100 * x for x in interval(acc)],
                        parent=dict({f: mean(e[f] for e in theirs[k]) for f in OUTCOMES}, n=len(theirs[k]))))
    pc = study.design()['primary_contrast']
    hi = (pc['arm'], pc['checks'], pc['attacker_pass'], 1); lo = hi[:3] + (81,)
    pp = defaultdict(dict)
    for r in rows:
        p = parent.get(r['id'])
        if r['kind'] == 'pilot' and p and key(r) in (hi, lo):
            pp[r['task']][key(r)] = study.evaluate(r, p['answer'])['rare_accuracy']
    vals = [v[hi] - v[lo] for v in pp.values() if hi in v and lo in v]
    return {'available': True, 'parent_model': 'claude-opus-5-5', 'packet_hash_mismatches': mismatched,
            'parent_primary_pp': None if not vals else 100 * mean(vals), 'parent_primary_roots': len(vals), 'cells': out}


def analyze(rows):
    pc = study.design()['primary_contrast']; t = table(rows)
    hi = (pc['arm'], pc['checks'], pc['attacker_pass'], 1); lo = hi[:3] + (81,)
    primary = paired(t, hi, lo)
    graded = {c: {k: v for k, v in paired(t, hi[:3] + (c,), lo).items() if k != 'per_root'} for c in (3, 9, 27)}
    grid = [r for r in rows if r['kind'] == 'pilot']
    return {'design': {'primary_contrast': pc, 'bootstrap': study.design()['analysis'], 'unit': 'world root'},
            'model': rows[0].get('model') if rows else None,
            'denominators': {'assigned': len(grid), 'completed': sum(r['status'] == 'completed' for r in grid),
                             'failed': sum(r['status'] == 'failed' for r in grid),
                             'not_started': sum(r['status'] == 'not_started' for r in grid), 'roots': len({r['task'] for r in grid})},
            'primary': primary, 'carrier_contrasts_against_81': graded, 'cells': cells(t), 'versus_parent': versus_parent(rows)}


def read_rows(path):
    opener = gzip.open if str(path).endswith('.gz') else open
    with opener(path, 'rt') as f: return [json.loads(line) for line in f if line.strip()]


def main():
    ap = argparse.ArgumentParser(description='Recompute the analysis from saved rows.')
    ap.add_argument('episodes', nargs='+'); args = ap.parse_args()
    import worker
    merged = []
    for path in args.episodes: merged = worker.merge(merged, read_rows(path))
    print(json.dumps(analyze(merged)))


if __name__ == '__main__':
    main()

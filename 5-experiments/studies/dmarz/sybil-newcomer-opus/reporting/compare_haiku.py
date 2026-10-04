"""Sonnet minus Haiku on identical assignments, paired by assignment id and clustered by world.

Usage: python3 reporting/compare_haiku.py <sonnet episodes.jsonl.gz> <haiku episodes.jsonl.gz> <out.json>
Reads retained records only; no model calls. Cohorts are compared, never pooled.
"""
import gzip, json, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import analyze

KEYS = ('identities', 'strategy', 'arm', 'round')
METRICS = ('rare_accuracy', 'wrong_specialist')


def rows(path):
    with gzip.open(path, 'rt') as f:
        return {r['id']: r for r in map(json.loads, f) if r['kind'] == 'pilot'}


def summarize(values):
    return {'clusters': len(values), 'mean': sum(values) / len(values) if values else None,
            'interval': analyze.interval(values)}


def main(sonnet_path, haiku_path, out_path):
    s, h = rows(sonnet_path), rows(haiku_path)
    assert set(s) == set(h), 'assignment_sets_differ'
    for i in s:
        assert all(s[i][k] == h[i][k] for k in KEYS + ('task', 'packet_hash')), 'assignment_mismatch'
    pairs = [i for i in s if s[i]['status'] == 'completed' and h[i]['status'] == 'completed']
    cells = defaultdict(lambda: defaultdict(list))
    for i in pairs:
        for m in METRICS:
            a, b = s[i]['evaluation'][m], h[i]['evaluation'][m]
            if a is not None and b is not None:
                cells[tuple(s[i][k] for k in KEYS)][m].append(a - b)
    out = {'pairs': len(pairs), 'assignments': len(s), 'cells': []}
    for key, ms in sorted(cells.items()):
        out['cells'].append(dict(zip(KEYS, key), **{m: summarize(v) for m, v in ms.items()}))
    # Difference in the frozen primary contrast: (renewal - reputation) Sonnet minus the same for Haiku.
    def by_task(model, arm):
        return {r['task']: r['evaluation']['rare_accuracy'] for r in model.values()
                if r['status'] == 'completed' and r['identities'] == 16 and r['strategy'] == 'sleeper'
                and r['round'] == 8 and r['arm'] == arm}
    sr, sp, hr, hp = by_task(s, 'renewal'), by_task(s, 'reputation'), by_task(h, 'renewal'), by_task(h, 'reputation')
    tasks = sorted(set(sr) & set(sp) & set(hr) & set(hp))
    out['primary_difference_in_differences'] = summarize([(sr[t] - sp[t]) - (hr[t] - hp[t]) for t in tasks])
    Path(out_path).write_text(json.dumps(out, indent=2) + '\n')
    return out


if __name__ == '__main__':
    o = main(*sys.argv[1:4])
    print(json.dumps({'pairs': o['pairs'], 'cells': len(o['cells']), 'primary_did': o['primary_difference_in_differences']}))

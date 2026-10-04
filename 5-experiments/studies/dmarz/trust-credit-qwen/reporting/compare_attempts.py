"""Attempt 002 (gpt-6-luna) against attempt 001 (qwen/qwen3.7-flash) on the identical S1 packets.

    python3 reporting/compare_attempts.py [--write]

Reads records/s1-episodes.jsonl.gz (attempt 001) and records/attempt-002/s1-episodes.jsonl.gz, pairs the
rows by assignment id (the same packet), and prints, per cell (kind, check strength, rule, budget):
each model's rare-skill answers as correct / wrong equal to the fabricated value / other wrong / null,
and the paired difference gpt-6-luna minus Qwen (per root, then the mean over the 24 roots with the
study's root bootstrap: 10,000 draws, seed 20261004). The two models' rows are never pooled. It also
checks that the scripted admission outcomes (and hence the primary) are identical between the attempts.
Outside the source hash; no network, no model call. With --write it writes
records/attempt-002/paired-luna-minus-qwen.json and .csv.
"""
import argparse
import csv
import gzip
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / 'src'))
import analyze  # noqa: E402

OUTCOMES = ('correct', 'fabricated', 'other_wrong', 'null')


def load(path):
    with gzip.open(path, 'rt') as f:
        return {r['id']: r for r in (json.loads(line) for line in f if line.strip())}


def outcome(row):
    e = row['evaluation']
    return {'correct': e['rare_correct'], 'fabricated': e['rare_fabricated'],
            'other_wrong': e['rare_wrong'] - e['rare_fabricated'], 'null': e['rare_abstain']}


def cell_key(r):
    return (r['kind'], r['attacker_pass'], r['rule'], r['checks'])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--write', action='store_true'); a = ap.parse_args()
    qwen, luna = load(HERE / 'records' / 's1-episodes.jsonl.gz'), load(HERE / 'records' / 'attempt-002' / 's1-episodes.jsonl.gz')
    assert set(qwen) == set(luna) and len(qwen) == 504, 'the two attempts must hold the same 504 assignments'
    for i in qwen:
        assert qwen[i]['packet_hash'] == luna[i]['packet_hash'] and qwen[i]['task'] == luna[i]['task'], 'packets differ'
        assert qwen[i]['status'] == luna[i]['status'] == 'completed', 'paired analysis assumes no failed row'
    same_admission = all(qwen[i]['admission'] == luna[i]['admission'] for i in qwen)
    primary = {name: analyze.analyze(list(rows.values()))['primary'] for name, rows in (('qwen', qwen), ('luna', luna))}
    out = {'pairs': len(qwen), 'admission_identical_in_every_pair': same_admission,
           'primary_qwen': {k: primary['qwen'][k] for k in ('estimate', 'interval', 'positive_roots')},
           'primary_luna': {k: primary['luna'][k] for k in ('estimate', 'interval', 'positive_roots')},
           'primary_identical': primary['qwen'] == primary['luna'],
           'same_six_values': sum(qwen[i]['answer'] == luna[i]['answer'] for i in qwen), 'cells': []}
    groups = defaultdict(list)
    for i in qwen: groups[cell_key(qwen[i])].append(i)
    order = lambda k: ({'pilot': 0, 'clean': 1}[k[0]], k[1] or 0, ['propagated', 'direct', 'anchors'].index(k[2]), k[3])
    for key in sorted(groups, key=order):
        ids = sorted(groups[key], key=lambda i: qwen[i]['task'])
        assert len({qwen[i]['task'] for i in ids}) == len(ids) == 24
        cell = {'kind': key[0], 'attacker_pass': key[1], 'rule': key[2], 'checks': key[3], 'roots': len(ids),
                'attacker_seats': analyze.mean(qwen[i]['admission']['attacker_seats'] for i in ids),
                'same_six_values': sum(qwen[i]['answer'] == luna[i]['answer'] for i in ids)}
        for o in OUTCOMES:
            q = [outcome(qwen[i])[o] for i in ids]; l = [outcome(luna[i])[o] for i in ids]; diff = [x - y for x, y in zip(l, q)]
            cell[o] = {'qwen': analyze.mean(q), 'luna': analyze.mean(l), 'luna_minus_qwen': analyze.mean(diff),
                       'interval': analyze.interval(diff), 'roots_luna_higher': sum(x > 0 for x in diff), 'roots_luna_lower': sum(x < 0 for x in diff)}
        out['cells'].append(cell)
    if a.write:
        rec = HERE / 'records' / 'attempt-002'
        (rec / 'paired-luna-minus-qwen.json').write_text(json.dumps(out, indent=1, sort_keys=True) + '\n')
        with (rec / 'paired-luna-minus-qwen.csv').open('w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['kind', 'attacker_pass', 'rule', 'checks', 'attacker_seats', 'same_six_values'] +
                       [f'{o}_{m}' for o in OUTCOMES for m in ('qwen', 'luna', 'luna_minus_qwen', 'lo', 'hi')])
            for c in out['cells']:
                w.writerow([c['kind'], c['attacker_pass'], c['rule'], c['checks'], round(c['attacker_seats'], 3), c['same_six_values']] +
                           [round(v, 4) for o in OUTCOMES for v in (c[o]['qwen'], c[o]['luna'], c[o]['luna_minus_qwen'], *c[o]['interval'])])
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == '__main__':
    main()

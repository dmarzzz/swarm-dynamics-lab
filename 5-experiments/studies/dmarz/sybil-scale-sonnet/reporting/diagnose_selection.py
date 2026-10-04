"""Post-collection descriptive audit of which identities received checks."""
import argparse
from collections import defaultdict
import gzip
import hashlib
import json
from pathlib import Path


def read(path):
    with gzip.open(path, 'rt') as f:
        return [json.loads(line) for line in f]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    worlds = {(w['n'], w['world']['task'], w['rate']): w['world']
              for w in read(args.input / 'worlds.jsonl.gz')}
    grouped = defaultdict(list)
    for row in read(args.input / 'assignments.jsonl.gz'):
        # Badge variants share the same graph and checks; count once per world.
        if row['visibility'] != 'visible' or row['kind'] != 'pilot':
            continue
        truth = worlds[row['n'], row['task'], row['attacker_pass']]['truth']
        counts = dict(core=0, specialists=0, attackers=0)
        for event in row['verification_events']:
            node = truth[event['node']]
            category = 'attackers' if not node['honest'] else 'specialists' if node['specialist'] else 'core'
            counts[category] += 1
        assert sum(counts.values()) == row['checks']
        grouped[row['n'], row['arm'], row['checks'], row['attacker_pass']].append(counts)
    result = {'status': 'post-collection descriptive diagnostic', 'cells': []}
    for key, values in sorted(grouped.items()):
        result['cells'].append({**dict(zip(('n', 'arm', 'checks', 'attacker_pass'), key)),
                               'worlds': len(values),
                               'mean_checked': {k: sum(v[k] for v in values) / len(values) for k in values[0]}})
    result['inputs'] = {name: hashlib.sha256((args.input / name).read_bytes()).hexdigest()
                        for name in ('worlds.jsonl.gz', 'assignments.jsonl.gz')}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps([r for r in result['cells'] if r['arm'] == 'coverage' and r['attacker_pass'] == .1]))


if __name__ == '__main__':
    main()

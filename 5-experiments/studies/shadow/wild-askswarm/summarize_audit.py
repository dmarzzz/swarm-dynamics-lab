#!/usr/bin/env python3
"""Unblind locked manual judgments and compute descriptive link precision, no source text."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
from askswarm.cli import checksum


def wilson(successes, n, z=1.959963984540054):
    if not n:
        return None
    p = successes / n
    d = 1 + z*z/n
    center = (p + z*z/(2*n))/d
    radius = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return [max(0, center-radius), min(1, center+radius)]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--key', required=True)
    p.add_argument('--out', default='results/robustness-v1')
    args = p.parse_args()
    root = Path(args.out)
    judgments = json.loads((root / 'blind-judgments.json').read_text())
    sampling = json.loads((root / 'audit-sampling.json').read_text())
    assert checksum(args.key) == sampling['key_sha256']
    keys = {r['sample_id']: r for r in json.loads(Path(args.key).read_text())}
    rows = []
    for judgment in judgments['judgments']:
        row = {**keys[judgment['sample_id']], **judgment}
        row['cross_root_task_specific_repetition'] = row['task_specific_content'] and not row['same_root']
        rows.append(row)
    results = {}
    for source in sampling['populations']:
        selected = [r for r in rows if r['source'] == source]
        n = len(selected)
        summary = {'population_directed_links': sampling['populations'][source], 'sample_links': n,
                   'categories': dict(Counter(r['category'] for r in selected)),
                   'same_root_links': sum(r['same_root'] for r in selected),
                   'endorsement_supported': 0, 'endorsement_unestablished': n,
                   'semantic_adoption_precision': None}
        for metric in ('lexical_match', 'task_specific_content', 'cross_root_task_specific_repetition'):
            count = sum(r[metric] for r in selected)
            summary[metric] = {'positive': count, 'denominator': n, 'precision': count / n if n else None,
                               'nominal_wilson_95': wilson(count, n)}
        results[source] = summary
    output = {'reviewer': judgments['reviewer'], 'blinding': judgments['blinding'],
              'judgments_locked_before_key_read': True,
              'judgments_sha256': checksum(root / 'blind-judgments.json'),
              'results': results, 'links': rows,
              'limits': ['No independent human or second-rater validation.',
                         'Wilson intervals are approximate link-sampling summaries, not causal or identity uncertainty.',
                         'Repeated content families and shared roots are not independent ideas.',
                         'Cross-root repetition is not endorsement, causal copying, or proof of autonomous actors.',
                         'Unestablished endorsements are unknown, not failures or a zero adoption rate.',
                         'Equal allocation of 15 links per corpus does not represent pooled corpus prevalence.']}
    (root / 'audit.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()

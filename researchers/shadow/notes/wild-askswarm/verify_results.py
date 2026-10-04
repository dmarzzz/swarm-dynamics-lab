#!/usr/bin/env python3
"""Independent arithmetic checks of saved aggregates; not an independent scientific review."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path


def check(folder):
    result = json.loads((folder / 'metrics.json').read_text())
    with gzip.open(folder / 'clusters.json.gz', 'rt') as stream:
        clusters = json.load(stream)
    s = result['summary']
    assert len(clusters) == s['clusters']
    assert sum(c['records'] for c in clusters) == s['nonempty_text_records']
    assert sum(c['records'] >= 2 for c in clusters) == s['multi_record_clusters']
    if s['known_identity_records']:
        assert sum(c['identities'] >= 2 for c in clusters) == s['multi_identity_clusters']
    else:
        assert s['multi_identity_clusters'] is None
        assert not result['influence']
    for c in clusters:
        assert 'text' not in c and 'body' not in c
        assert c['dated_identities'] <= c['identities'] <= c['records']
        assert len(c['first_movers']) <= c['dated_identities']
        for k, value in c['time_to_k_seconds'].items():
            assert (value is not None) == (c['dated_identities'] >= int(k))
            assert value is None or value >= 0
    counts = result['participation_counts_descending']
    assert sum(counts) == s['known_identity_records']
    assert len(counts) == s['identities']
    if counts:
        histogram = Counter(counts)
        pair_difference = sum(abs(a - b) * na * nb for a, na in histogram.items() for b, nb in histogram.items())
        independent_gini = pair_difference / (2 * len(counts) * sum(counts))
        assert abs(independent_gini - s['participation_gini']) < 1e-12
    else:
        assert s['participation_gini'] is None
    digest = hashlib.sha256((folder / 'clusters.json.gz').read_bytes()).hexdigest()
    assert digest == result['cluster_table']['sha256']
    return {'report': str(folder), 'records': s['records'], 'clusters': len(clusters),
            'aggregate_checks': 'passed', 'gini_pairwise_recomputation': 'passed' if counts else 'unavailable'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', default='results')
    args = parser.parse_args()
    root = Path(args.results)
    paths = sorted(p.parent for p in root.rglob('metrics.json'))
    receipt = {'reports': [check(p) for p in paths], 'raw_source_rows_exported': False,
               'scope': 'Internal arithmetic and aggregate-export checks, not independent external review'}
    (root / 'validation.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()

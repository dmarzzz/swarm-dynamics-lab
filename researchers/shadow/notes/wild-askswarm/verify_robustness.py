#!/usr/bin/env python3
"""Independent saved-output arithmetic checks, no corpus text or API required."""
import gzip
import json
from pathlib import Path
import statistics


def main():
    root = Path('results/robustness-v1')
    checked = []
    for source in ('wiki', 'git', 'swarmtraces'):
        original = json.loads(Path('results', source, 'metrics.json').read_text())
        comparisons = json.loads((root / source / 'comparison.json').read_text())
        scores = json.loads((root / source / 'rank-scores.json').read_text())
        for arm in ('baseline', 'exact_dedup', 'root_aggregate', 'exclude_imputed', 'combined'):
            p = root / source / arm
            r = json.loads((p / 'metrics.json').read_text())
            with gzip.open(p / 'clusters.json.gz', 'rt') as stream:
                clusters = json.load(stream)
            s = r['summary']
            assert sum(c['records'] for c in clusters) == s['nonempty_text_records']
            assert len(clusters) == s['clusters']
            assert sum(r['record_kinds'].values()) == s['records']
            counts = r['participation_counts_descending']
            assert sum(counts) == s['known_identity_records']
            assert len(counts) == s['identities']
            if counts:
                g = sum(abs(a - b) for a in counts for b in counts) / (2 * len(counts) * sum(counts))
                assert abs(g - s['participation_gini']) < 1e-12
            else:
                assert s['participation_gini'] is None
            for k, values in s['time_to_k'].items():
                reached = [c['time_to_k_seconds'][k] for c in clusters if c['time_to_k_seconds'][k] is not None]
                assert len(reached) == values['reached']
                assert values['at_risk_clusters'] == s['temporal_clusters']
                assert values['reached'] + values['not_observed_to_reach'] == s['temporal_clusters']
                assert (statistics.median(reached) if reached else None) == values['seconds_among_reached']['median']
            assert len(scores[arm]['participation']) == s['identities']
            assert sum(scores[arm]['participation'].values()) == s['known_identity_records']
            if source == 'swarmtraces':
                assert s['known_identity_records'] == s['dated_records'] == s['temporal_clusters'] == 0
                assert r['influence'] == []
            if arm == 'baseline':
                assert s == original['summary'], (source, 'baseline summary changed')
            else:
                for field, delta in comparisons['comparisons'][arm]['summary_deltas'].items():
                    if delta['delta'] is not None:
                        assert abs(delta['after'] - delta['before'] - delta['delta']) < 1e-10
                for metric, change in comparisons['comparisons'][arm]['identity_rankings'].items():
                    before, after = scores['baseline'][metric], scores[arm][metric]
                    common = before.keys() & after.keys()
                    assert len(common) == change['common']
                    assert len(before) - len(common) == change['exited']
                    assert len(after) - len(common) == change['entered']
            checked.append({'source': source, 'arm': arm, 'records': s['records'], 'status': 'pass'})
    result = {'reports_checked': len(checked), 'checks': checked,
              'independence': 'separate arithmetic implementation by same assistant, not independent researcher review'}
    (root / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

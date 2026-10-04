#!/usr/bin/env python3
"""Post-draft saved-data checks. No provider calls; no source rows emitted.

Reuse AskSwarm's validated JSONL reader (read-only) for schema aggregates. Primary
adoption uses insertion hunks, unlike AskSwarm's whole-snapshot lexical clusters.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import platform
import sys

import numpy as np

import halflife as H

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'wild-askswarm'))
from askswarm.adapters import json_rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--data', required=True)
    p.add_argument('--results', required=True)
    p.add_argument('--boot', type=int, default=1000)
    args = p.parse_args()
    out = Path(args.results)
    recs, meta = H.load_wiki(args.data)
    table, end, _, _ = H.adoption_table(recs, 'url', 'a')
    visibility = H.visible_copies(recs, table, end, n_boot=args.boot)
    # The preregistered point estimates must survive adding uncertainty unchanged.
    original = json.loads((out / 'summary.json').read_text())
    old = original['wiki']['visible_copies_url']
    for key in ('bins', 'events', 'exposure_records', 'rate_per_1k_records'):
        assert old[key] == visibility[key], f'Changed visibility estimate: {key}'
    # June 18 is identified in the prior paper as a non-task link-poster burst.
    # Excluding the entire UTC day is a deliberately coarse POST-HOC sensitivity,
    # NOT the paper's task-engaged population and NOT a confirmatory cohort.
    start = H.parse_time('2026-06-18T00:00:00Z')
    stop = H.parse_time('2026-06-19T00:00:00Z')
    filtered = [r for r in recs if not start <= r['t'] < stop]
    H.N_BOOT = args.boot
    filtered_table, te, ae, _ = H.adoption_table(filtered, 'url', 'a')
    sensitivity = H.analyse(filtered_table, te, ae, np.random.default_rng(H.SEED), 'wiki/no-june18/A/url')
    schema = {}
    for name in ('pages', 'labels', 'events'):
        keys = Counter()
        count = 0
        for row in json_rows(Path(args.data) / f'{name}.jsonl.gz'):
            keys.update(row.keys())
            count += 1
        schema[name] = dict(records=count, key_counts=dict(keys))
    result = dict(status='POST-HOC saved-data supplement, 2026-10-04; no causal claim',
                  input=meta, wiki_visible_pages_url=visibility,
                  wiki_excluding_june18=dict(records=len(filtered), removed=len(recs)-len(filtered),
                      note='UTC-day exclusion is not the source paper task-engaged filtering', url=sensitivity),
                  schema_aggregates=schema,
                  software=dict(python=platform.python_version(), numpy=np.__version__,
                                shared_reader='askswarm.adapters.json_rows; read-only'))
    (out / 'supplement.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    # Regenerate only the display from the preserved baseline, no new baseline analysis.
    H.figure(original, out / 'fig-adoption.png', visibility=visibility)
    print(json.dumps(visibility, indent=2))
    print('Day-exclusion URL beta:', sensitivity['activity']['beta'], sensitivity['activity']['beta_ci'])


if __name__ == '__main__':
    main()

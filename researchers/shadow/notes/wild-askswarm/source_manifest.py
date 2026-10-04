#!/usr/bin/env python3
"""Verify local frozen inputs and record explicit provenance without copying rows."""
import argparse
import json
from pathlib import Path
import subprocess
from askswarm.cli import checksum
from run_all import FROZEN_REF


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', required=True)
    p.add_argument('--repo', required=True)
    args = p.parse_args()
    manifest = {'note': 'Saved per-arm frozen_baseline locators are one parent short. These explicit paths, relative to this manifest, supersede those display-only locators. No scientific result was modified.', 'sources': {}}
    for source, filename in [('wiki', 'collusion-wiki/revisions.jsonl.gz'), ('swarmtraces', 'swarmtraces/redacted.jsonl.gz'), ('git', None)]:
        baseline = Path('results') / source / 'metrics.json'
        provenance = json.loads(baseline.read_text())['source']
        if filename:
            path = Path(args.data) / filename
            assert checksum(path) == provenance['sha256']
            assert path.stat().st_size == provenance['bytes']
        else:
            ref = subprocess.check_output(['git', '-C', args.repo, 'rev-parse', FROZEN_REF], text=True).strip()
            assert ref == provenance['git_ref']
        manifest['sources'][source] = {'baseline_metrics': '../' + source + '/metrics.json',
                                      'baseline_metrics_sha256': checksum(baseline),
                                      'verified_original_provenance': provenance, 'local_source_matches': True}
    Path('results/robustness-v1/source-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('All three frozen sources match original source receipts')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Write launch/s1-approval.json. Run ONLY after the reviewer (dmarz/fleet-monitor) has sent an
explicit go for the named stages. This file is not part of the runtime fingerprint.

  python3 launch/make_approval.py --stages s1q --go "reviewer go received <UTC time>, <where it was sent>"
  python3 launch/make_approval.py --stages s1q,s1r,s1l --go "..."     (replaces the record)

It pins the current runtime fingerprint, reviews/chain-001-pre.md and launch/review-waiver.md by hash.
If any of the three changes afterwards, the paid stages refuse to start until a new record is written.
Commit and push the record, then deploy that commit with the private launcher's `setup` step.
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
import config  # noqa: E402
import launch  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--stages', required=True, help='comma-separated subset of s1q,s1r,s1l')
    ap.add_argument('--go', required=True, help='when and where the reviewer sent the explicit go')
    ap.add_argument('--operator', default='dmarz/orbital-orchestrator')
    a = ap.parse_args()
    stages = [s for s in a.stages.split(',') if s]
    if not stages or any(s not in launch.PAID_STAGES for s in stages):
        ap.error('stages must be among ' + ','.join(launch.PAID_STAGES))
    review = config.execution()['review']
    record = {
        'status': 'approved', 'reviewer': review['reviewer'], 'stages': stages, 'go': a.go, 'operator': a.operator,
        'written': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'cross_researcher_review': review['cross_researcher_review'],
        'source_hash': config.source_hash(), 'launch_manifest': config.launch_manifest(),
        'pre_run_review': {'path': 'reviews/chain-001-pre.md', 'sha256': config.sha256_file(ROOT / 'reviews/chain-001-pre.md')},
        'review_waiver': {'path': review['waiver'], 'sha256': config.sha256_file(ROOT / review['waiver'])},
    }
    launch.APPROVAL.write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    for stage in stages:
        launch.check(stage)
    print('wrote', launch.APPROVAL.relative_to(ROOT), 'for', ', '.join(stages), '| fingerprint', record['source_hash'])


if __name__ == '__main__':
    main()

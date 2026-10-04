"""Launch gate for the paid stages. No model call is possible without a committed approval record.

launch/s1-approval.json is written only after the reviewer (dmarz/fleet-monitor) sends an explicit
go. It names the stages it covers and pins the runtime fingerprint, the pre-run assessment and the
review waiver by hash. The coordinator checks it before queueing and the worker checks it again
before constructing the provider adapter.
"""
import json

import config

APPROVAL = config.ROOT / 'launch' / 's1-approval.json'
PAID_STAGES = ('p0', 's1q', 's1r', 's1l')


class NotApproved(Exception):
    pass


def check(stage):
    if stage not in PAID_STAGES:
        raise NotApproved('stage_not_authorized')
    review = config.execution()['review']
    if not APPROVAL.is_file():
        raise NotApproved('no_approval_record')
    record = json.loads(APPROVAL.read_text())
    if record.get('status') != 'approved' or record.get('reviewer') != review['reviewer']:
        raise NotApproved('approval_not_granted_by_reviewer')
    if stage not in record.get('stages', []):
        raise NotApproved('stage_not_covered_by_approval')
    if record.get('source_hash') != config.source_hash():
        raise NotApproved('runtime_changed_since_approval')
    for key, path in (('pre_run_review', 'reviews/chain-001-pre.md'), ('review_waiver', review['waiver'])):
        target = config.ROOT / path
        entry = record.get(key) or {}
        if entry.get('path') != path or not target.is_file() or entry.get('sha256') != config.sha256_file(target):
            raise NotApproved(key + '_hash_mismatch')
    return record

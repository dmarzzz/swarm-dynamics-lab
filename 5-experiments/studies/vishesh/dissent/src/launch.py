"""Native launch readiness is fail-closed. No network dispatch is implemented here.

An approved executor must perform the live public registration, allocation and
budget-authority checks. A hand-written receipt cannot authorize this module to
make calls: it contains no transport or secret reading code.
"""
from datetime import datetime, timezone
import re

REQUIRED = ('public_plan_verified','independent_review_passed','allocation_exclusive','budget_reserved','source_frozen','qualification_passed')

def readiness(manifest, *, now=None):
    now = now or datetime.now(timezone.utc)
    issues = []
    for field in REQUIRED:
        if field=='qualification_passed' and manifest.get('stage')=='qualification':
            if manifest.get('bounded_diagnostic_approved') is not True:issues.append('bounded_diagnostic_approved')
        elif manifest.get(field) is not True:issues.append(field)
    url = manifest.get('public_plan_url','')
    if not re.fullmatch(r'https://github\.com/dmarzzz/swarm-lab/blob/[0-9a-f]{40}/researchers/vishesh/notes/dissent/PLAN\.md',url):
        issues.append('immutable_plan_url')
    cap = manifest.get('authorized_usd',0)
    if type(cap) not in (int,float) or not 0<cap<=10:issues.append('positive_bounded_authorization')
    if type(manifest.get('max_calls')) is not int or not 0<manifest['max_calls']<=1000:issues.append('bounded_calls')
    if not manifest.get('served_model'):issues.append('pinned_served_model')
    try:
        expiry = datetime.fromisoformat(manifest['expires_at'].replace('Z','+00:00'))
        if expiry.tzinfo is None or expiry <= now:issues.append('expired_manifest')
    except (KeyError,ValueError,TypeError):issues.append('expiry_required')
    return {'ready_for_executor_review':not issues,'missing':issues,'native_dispatch_available':False}

if __name__=='__main__':
    import argparse,json
    p=argparse.ArgumentParser();p.add_argument('manifest');a=p.parse_args()
    print(json.dumps(readiness(json.load(open(a.manifest))),indent=2))

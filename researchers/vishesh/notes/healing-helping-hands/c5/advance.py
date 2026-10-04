"""Automatic approved S0→S1 continuation after native and authored trace review.

No owner/researcher prompt. No retry or fallback. The owning agent supplies its
completed scientific review and fresh operational admission, not an approval.
"""
import argparse,json,os
from pathlib import Path
from contract import qualify

def transition(rows,manifest,audit,review,admission):
    if manifest.get('attempt')!='C5-S0' or manifest.get('status')!='completed':raise ValueError('incomplete_S0')
    if not qualify(rows)['qualified']:raise ValueError('failed_qualification')
    if audit.get('attempt')!='C5-S0' or any(audit.get(k)!=v for k,v in {'assigned':60,'completed':60,'starts':180,'terminal':180,'completed_calls':180,'all_payload_hashes_verified':True,'all_scores_reconstructed':True}.items()):raise ValueError('incomplete_audit')
    if review.get('scientific_qualification')!='valid' or review.get('scientific_review')!='complete' or not review.get('assessor'):raise ValueError('scientific_review_required')
    if review.get('source_hashes')!=manifest.get('source_hashes') or review.get('payload_sha256')!=audit.get('calls_sha256'):raise ValueError('review_evidence_mismatch')
    misses={r['id'] for r in rows if any(x!=r['expected'] for x in r['labels'].values())}
    if set(review.get('reviewed_miss_ids',[]))!=misses:raise ValueError('all_misses_require_review')
    if review.get('context_isolation_verified') is not True or review.get('unresolved_instrument_defects')!=[]:raise ValueError('instrument_defect')
    if admission.get('stage')!='S1' or admission.get('s0_scientific_hash')!=admission.get('scientific_hash'):raise ValueError('source_drift')
    projected=2*audit['cost_usd']/60*432+.001344
    if admission.get('projected_stage_usd')!=projected:raise ValueError('projection_mismatch')
    if admission.get('spent_usd',1)+admission.get('uncertain_usd',1)+projected>.1 or admission.get('incremental_spent_usd',1)+projected>.03:raise ValueError('insufficient_budget')
    return {'advance':True,'projected_stage_usd':projected,'new_owner_approval_required':False}

def validate_parent(root,admission):
    from audit import run as audit_run
    from scenarios import assignments
    import hashlib
    rows=json.loads((root/'observations.json').read_text());manifest=json.loads((root/'manifest.json').read_text());review=json.loads((root/'scientific-review.json').read_text())
    audit=audit_run(root);audit['calls_sha256']=hashlib.sha256((root/'calls.jsonl').read_bytes()).hexdigest()
    expected={r['id']:r for r in assignments('S0')}
    for row in rows:
        if any(row[k]!=expected[row['id']][k] for k in ('claim','report','expected','family')):raise ValueError('context_fixture_mismatch')
    return transition(rows,manifest,audit,review,admission)

def consume_transition(marker,result):
    fd=os.open(marker,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    with os.fdopen(fd,'w') as f:json.dump(result,f)

def main(a):
    from runtime import preflight
    from supervise import main as supervise
    admission=json.loads(a.admission.read_text())
    preflight(admission,'S1',a.parent)
    result={'advance':True,'new_owner_approval_required':False,'projected_stage_usd':admission['projected_stage_usd']}
    # Preflight independently reconstructs parent traces even for direct supervisor calls.
    marker=a.out.parent/'C5-S1-advance.json'
    consume_transition(marker,result)
    a.stage='S1';supervise(a)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for key in ('parent','admission','credential','ledger','authority','out'):p.add_argument('--'+key,type=Path,required=True)
    try:main(p.parse_args())
    except Exception as e:print(json.dumps({'automatic_transition_stopped':type(e).__name__,'retry_allowed':False}));raise SystemExit(1)

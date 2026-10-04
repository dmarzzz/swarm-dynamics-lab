"""Offline admission predicates. No credential, ledger mutation or dispatch entry point."""
STAGE_CAPS={'A':2320000,'B':4640000,'C':27820000}
STAGE_CALLS={'A':60,'B':120,'C':720}
WITHDRAWN_AUTHORITIES={'PI-FUND-20261004-03'}
FLAGS=('approved_account_verified','exclusive_claim_verified','source_runtime_verified','public_plan_verified','route_tariff_verified','sole_ledger_writer_verified','current_funding_verified')


def errors(receipt,revision,now):
    result=[k for k in FLAGS if receipt.get(k)is not True]
    authority=receipt.get('funding_authority')
    if not authority or authority in WITHDRAWN_AUTHORITIES:result.append('funding_missing_or_withdrawn')
    if receipt.get('source_commit')!=revision:result.append('source_mismatch')
    if not now-300<=receipt.get('verified_epoch',0)<=now:result.append('stale_admission')
    used=receipt.get('allocated_seconds_used',14400);rate=receipt.get('hourly_rate_usd',1)
    if type(used) not in (int,float) or not 0<=used<13800:result.append('allocation_window')
    if type(rate) not in (int,float) or not 0<=rate<=.25:result.append('infrastructure_rate')
    if receipt.get('claim_expiry_epoch',0)<now+600:result.append('cleanup_window')
    if receipt.get('api_packet_cap_microdollars')!=35000000:result.append('packet_cap')
    if receipt.get('all_in_packet_cap_microdollars')!=36000000:result.append('all_in_cap')
    if receipt.get('study_cap_microdollars')!=50000000:result.append('study_cap')
    return result


def gate(stage,records):
    expected=6 if stage=='A' else 18 if stage=='B' else None
    if expected is None:raise ValueError('qualification_stage')
    from native_v3 import assignments
    manifest={r['id']:r for r in assignments() if r['stage']==stage}
    ids=[r['assignment']['id'] for r in records]
    if set(ids)!=set(manifest) or any(r['assignment']!=manifest[r['assignment']['id']] for r in records):return False
    return len(records)==expected and len(set(ids))==expected and all(r['assignment']['stage']==stage and r.get('failure') is None and r['evaluation']['joint_correct'] and r['evaluation']['unsafe_attempts']==0 and (stage!='B' or r['evaluation']['actions_attempted']==0) for r in records)

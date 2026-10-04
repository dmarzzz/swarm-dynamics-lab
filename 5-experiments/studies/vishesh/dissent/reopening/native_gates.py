"""RD6 admission. Operator attestations bind evidence; they are not independent audits.

Preparation never grants approval, allocates resources, opens credentials or changes
budgets. All paths in an admission receipt are private operator inputs.
"""
import datetime as dt
import hashlib
import json
import math
import platform
import re
import subprocess
import sys
from pathlib import Path
from cases import BASE, build, digest

ROOT = BASE.parents[4]
SNAPSHOT = 'typesafe/jev-1.13-20260917'
RESERVE = 1_344_000
CAP = 1_000_000_000
STAGES = {'Q0': 18, 'D0': 144}
PARENT = '66775acf7ab12f7434f979685899a636da1f5b24701aeff093e3fed0712c5752'
ZERO_PARENT = 'c4763ff165d85ecd6be08cb33f79e0dd829a8283c77d1de1f2cf51b9816ee68f'
ZERO_PACKET = '8036f2cbf64dd855b6635eee7615691ad3ed41bfadea7b120fb6047bb9aebb7c'
ZERO_ALLOCATION_END = '2026-10-04T20:40:02+00:00'
ZERO_INFRA_COMMITTED = 747_173_584
DIMENSIONS = {'question','scenarios','controls','capability','measurement','sample_size',
              'agent_context','data_integrity','resources','reproducibility','visualization'}


def require(condition, code):
    if not condition:
        raise ValueError(code)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def wire(request):
    return json.dumps(request, separators=(',', ':'), allow_nan=False).encode()


def read(path):
    return json.loads(Path(path).read_text())


def sources():
    paths = list(BASE.glob('native*.py')) + [BASE/'cases.py', BASE/'PLAN.md',
        BASE/'next-run-plan.json', BASE/'DIAGNOSTIC-REVIEW.json', BASE/'STARTUP-REPAIR.md',
        BASE.parent/'rd5/src/rd5_core.py', BASE.parent/'rd5/src/common.py',
        BASE.parent/'src/jev.py']
    return {str(p.relative_to(ROOT)): sha(p) for p in sorted(paths)}


def prepare(stage):
    require(stage in STAGES, 'stage')
    manifest = build()
    source = sources()
    return {'schema': 'rd6-prepared-v1', 'study_id': 'right-dissenter', 'stage': stage,
        'source_hashes': source, 'instrument_sha256': digest(source),
        'manifest_sha256': digest(manifest),
        'proposal_sha256': sha(BASE/'next-run-plan.json'), 'plan_sha256': sha(BASE/'PLAN.md'),
        'assignments': [a for a in manifest['assignments'] if a['stage'] == stage],
        'limits': {'stage_calls': STAGES[stage], 'lifetime_calls': 650,
                   'api_cap_nano': CAP, 'infra_cap_nano': CAP, 'reservation_nano': RESERVE,
                   'stage_seconds': 1800, 'request_seconds': 60, 'new_calls': 162}}


def validate_packet(packet):
    # Rebuilding also rejects reordered assignments/criteria, hidden extra fields,
    # changed labels and malicious self-consistent replacement hashes.
    expected = prepare(packet.get('stage'))
    require(wire(packet) == wire(expected), 'packet_or_source_mismatch')
    return expected


def evidence(ref):
    require(isinstance(ref, dict) and set(ref) == {'path', 'sha256'}, 'evidence_reference')
    data=Path(ref['path']).read_bytes()
    require(hashlib.sha256(data).hexdigest() == ref['sha256'], 'evidence_hash')
    return json.loads(data)


def instant(value):
    result = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(result.tzinfo is not None, 'timezone_required')
    return result


def fresh(value, now, seconds=300):
    require(0 <= (now-instant(value)).total_seconds() <= seconds, 'stale_evidence')


def validate_review(review):
    require(review.get('study_id') == 'right-dissenter' and review.get('verdict') == 'diagnostic'
            and review.get('parent_handoff_sha256') == PARENT, 'diagnostic_review_required')
    rows = review.get('assessments', [])
    require(len(rows) == 11 and {r['dimension'] for r in rows} == DIMENSIONS, 'review_dimensions')
    for row in rows:
        require(row['status'] in ('pass','gap','unknown','not_applicable') and row.get('finding'), 'review_status')
        if row['status'] == 'pass':
            require(row.get('evidence'), 'review_evidence')
        if row['status'] in ('gap','unknown'):
            require(row.get('next_action') and row.get('acceptance_check'), 'review_followup')
        for ref in row.get('evidence', []):
            require(sha(ROOT/ref['path']) == ref['sha256'], 'review_evidence_changed')


def validate_admission(packet, receipt, *, now=None, host=None):
    """Pure checks over supplied evidence. Production additionally checks live state."""
    now = now or dt.datetime.now(dt.timezone.utc)
    require(receipt.get('schema') == 'rd6-admission-v1' and receipt.get('mode') == 'native', 'native_admission_required')
    require(receipt.get('packet_sha256') == digest(packet), 'receipt_binding')
    require(bool(re.fullmatch(r'rd6-(q0|d0)-[a-z0-9-]+', receipt.get('attempt','')))
            and receipt['attempt'].startswith('rd6-'+packet['stage'].lower()+'-'), 'attempt_identity')
    fresh(receipt['verified_utc'], now)
    require(instant(receipt['expires_utc']) >= now+dt.timedelta(minutes=31), 'lease_too_short')
    if host is not None:
        require(host == receipt['worker_host'], 'wrong_host')
    approval = evidence(receipt['owner_approval'])
    require(approval.get('decision') == 'approved' and approval.get('approver_role') == 'owner'
            and approval.get('authorization_ref') and 'launch' in approval.get('scopes', [])
            and packet['stage'] in approval.get('stages', [])
            and approval.get('proposal_sha256') == packet['proposal_sha256']
            and approval.get('instrument_sha256') == packet['instrument_sha256']
            and approval.get('manifest_sha256') == packet['manifest_sha256']
            and approval.get('max_lifetime_calls') == 650 and approval.get('max_new_calls') == 162
            and approval.get('api_cap_nano') == CAP and approval.get('infra_cap_nano') == CAP,
            'updated_owner_scope_required')
    if 'zero_dispatch_replacement' in receipt:
        validate_replacement(packet, receipt, approval)
    parent = evidence(receipt['parent_handoff'])
    require(receipt['parent_handoff']['sha256'] == PARENT and parent.get('study_id') == 'right-dissenter'
            and parent.get('attempt') == 'rd5-h5-a1', 'actual_parent_handoff_required')
    validate_review(read(BASE/'DIAGNOSTIC-REVIEW.json'))
    allocation = evidence(receipt['allocation'])
    fresh(allocation['verified_utc'], now)
    require(allocation.get('approved_account_identity') and
            allocation['approved_account_identity'] == allocation.get('credential_account_identity')
            and allocation.get('exclusive') is True and allocation.get('study_id') == 'right-dissenter'
            and allocation.get('host') == receipt['worker_host']
            and allocation.get('provisioner_state_verified') is True
            and re.fullmatch('[0-9a-f]{64}', allocation.get('resource_plan_sha256',''))
            and instant(allocation['claim_until']) >= instant(receipt['expires_utc']), 'approved_exclusive_allocation_required')
    require(allocation.get('claim_id')
            and instant(allocation['claim_started_utc']) <= now < instant(allocation['claim_until'])
            and 0 < (instant(allocation['claim_until'])-instant(allocation['claim_started_utc'])).total_seconds() <= 5400,
            'allocation_duration_required')
    lineage=digest({k:allocation[k] for k in ('claim_id','host','claim_started_utc','claim_until','resource_plan_sha256')})
    require(receipt.get('allocation_lineage_sha256') == lineage, 'allocation_lineage_binding')
    budget = evidence(receipt['budget'])
    require(budget.get('authority') == 'original-right-dissenter-ledger'
            and budget.get('original_ledger_verified') is True
            and budget.get('single_writer_verified') is True
            and budget.get('baseline_calls') == 488
            and budget.get('baseline_committed_nano') == 22_699_069
            and budget.get('infra_committed_nano', CAP) + budget.get('infra_reserved_nano', CAP) <= CAP
            and budget.get('infra_committed_nano', -1) >= 720_248_442
            and 0 < budget.get('infra_reserved_nano', 0) <= 107_145_000,
            'cumulative_budget_required')
    replacement='zero_dispatch_replacement' in receipt
    if packet['stage']=='D0' and receipt.get('qualification_directory'):
        # live_preflight subsequently audits this complete native Q0 bundle and
        # binds its actual latest closeout and identical allocation lineage.
        qualified=read(Path(receipt['qualification_directory'])/'execution.json')
        replacement=qualified.get('zero_dispatch_predecessor')=='rd6-q0-a1'
    rate=allocation.get('hourly_rate_nano')
    require(type(rate) is int and 0 <= rate <= 71_430_000,'infrastructure_rate')
    reserve_required=(rate*3+1)//2
    if replacement:
        require(instant(allocation['claim_until'])<=instant(ZERO_ALLOCATION_END)
                and budget['infra_committed_nano']>=ZERO_INFRA_COMMITTED
                and budget['infra_committed_nano']+budget['infra_reserved_nano']<=827_393_442,
                'replacement_original_infrastructure_envelope')
        reserve_required=math.ceil(rate*(instant(allocation['claim_until'])-instant(allocation['claim_started_utc'])).total_seconds()/3600)
    require(type(allocation.get('hourly_rate_nano')) is int
            and 0 <= allocation['hourly_rate_nano'] <= 71_430_000
            and allocation.get('maximum_minutes') == 90
            and budget['infra_reserved_nano'] >= reserve_required,
            'infrastructure_envelope_required')
    fresh(budget['verified_utc'], now)
    runtime = evidence(receipt['runtime'])
    fresh(runtime['verified_utc'], now)
    require(runtime.get('worker_host') == receipt['worker_host']
            and runtime.get('instrument_sha256') == packet['instrument_sha256']
            and runtime.get('offline_checks_passed') is True
            and runtime.get('verified_ssh_host_key') is True
            and runtime.get('exclusive_transport_verified') is True
            and re.fullmatch('[0-9a-f]{40}', runtime.get('source_commit','')), 'runtime_required')
    public = evidence(receipt['public_plan'])
    fresh(public['checked_utc'], now)
    require(public.get('experiment') == 'right-dissenter-rd6'
            and public.get('plan_sha256') == packet['plan_sha256']
            and re.fullmatch(r'https://github.com/dmarzzz/swarm-lab/blob/[0-9a-f]{40}/researchers/vishesh/notes/dissent/reopening/PLAN.md', public.get('url',''))
            and public.get('public_page_verified') is True, 'public_plan_required')
    tldrs = public.get('condition_tldrs', {})
    conditions = {a['condition'] for a in packet['assignments']}
    require(set(tldrs) == conditions and all(isinstance(v,str) and len(v) >= 80 for v in tldrs.values())
            and packet['stage'] in public.get('run_tldr',''), 'condition_tldrs_required')
    return budget


def validate_replacement(packet, receipt, approval):
    """Evidence gate only. The original ledger checks zero dispatch atomically too."""
    r=evidence(receipt['zero_dispatch_replacement'])
    require(packet['stage']=='Q0' and receipt['attempt']=='rd6-q0-a2'
            and r.get('attempt')==receipt['attempt'] and r.get('previous_attempt')=='rd6-q0-a1'
            and r.get('previous_packet_sha256')==ZERO_PACKET
            and r.get('packet_sha256')==digest(packet)
            and r.get('owner_approval_sha256')==receipt['owner_approval']['sha256'], 'replacement_scope')
    require(approval.get('replacement_attempt')=='rd6-q0-a2'
            and approval.get('previous_attempt')=='rd6-q0-a1'
            and approval.get('replacement_contract_sha256')==sha(BASE/'STARTUP-REPAIR.md'),
            'explicit_replacement_approval_required')
    latest=receipt.get('latest_closeout',{})
    require(latest.get('sha256')==ZERO_PARENT and r.get('previous_closeout_sha256')==ZERO_PARENT,
            'replacement_closeout_required')
    previous=evidence(latest)
    require(previous.get('attempt')=='rd6-q0-a1' and previous.get('study_id')=='right-dissenter',
            'replacement_predecessor')
    proof=evidence(r['zero_dispatch_proof'])
    require(proof.get('attempt')=='rd6-q0-a1' and proof.get('dispatched')==0
            and proof.get('provider_responses')==0 and proof.get('native_calls')==0
            and proof.get('lifetime_calls')==488 and proof.get('committed_api_nano')==22_699_069
            and proof.get('worker_stopped_verified') is True
            and proof.get('relay_stopped_verified') is True,'zero_dispatch_proof_required')
    review=evidence(r['owning_review'])
    require(review.get('attempt')=='rd6-q0-a1' and review.get('verdict')=='repair'
            and review.get('operational_closeout_sha256')==ZERO_PARENT
            and review.get('scientific_result')=='not_tested'
            and review.get('zero_dispatch_proof_sha256')==r['zero_dispatch_proof']['sha256'],
            'replacement_postreview_required')
    rows=review.get('assessments',[])
    require(len(rows)==11 and {v.get('dimension') for v in rows}==DIMENSIONS,'review_dimensions')
    for row in rows:
        require(row.get('status') in ('pass','gap','unknown','not_applicable') and row.get('finding'),'review_status')
        if row['status']=='pass':require(row.get('evidence'),'review_evidence')
        if row['status'] in ('gap','unknown'):
            require(row.get('next_action') and row.get('acceptance_check'),'review_followup')
        for ref in row.get('evidence',[]):
            require(sha(ROOT/ref['path'])==ref['sha256'],'review_evidence_changed')
    return r


def live_preflight(packet, receipt, *, worker=False):
    """No paid call. Relay checks private lineage; worker checks host and source."""
    validate_packet(packet)
    validate_admission(packet, receipt, host=platform.node() if worker else None)
    runtime = evidence(receipt['runtime'])
    head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    require(head == runtime['source_commit'], 'source_commit_mismatch')
    if not worker:
        sys.path.insert(0, str(ROOT/'scripts'))
        from experiment_ops import core, closeout
        require(not any(r['status'] == 'dispatching' for r in core.journal_status(ROOT,'right-dissenter')), 'unfinished_dispatch')
        latest = closeout.latest_handoff(ROOT, 'right-dissenter')
        # D0 follows the new Q0 closeout, but its scientific parent stays RD5.
        latest_ref = receipt.get('latest_closeout', receipt['parent_handoff'])
        evidence(latest_ref)
        if packet['stage'] == 'D0':
            qreview=evidence(receipt['qualification_review'])
            qexecution=read(Path(receipt['qualification_directory'])/'execution.json')
            require(qexecution.get('allocation_lineage_sha256') == receipt['allocation_lineage_sha256']
                    and qreview.get('operational_closeout_sha256') == latest_ref['sha256']
                    and latest and latest['attempt'] == qexecution['attempt'], 'latest_qualification_closeout_required')
        else:
            expected=ZERO_PARENT if 'zero_dispatch_replacement' in receipt else PARENT
            require(latest_ref['sha256'] == expected, 'unexpected_parent_attempt')
        require(latest and latest.get('handoff_sha256') == latest_ref['sha256']
                and (ROOT/latest['handoff_path']).resolve() == Path(latest_ref['path']).resolve(), 'latest_private_closeout_required')
        sys.path.insert(0, str(BASE.parents[1]/'experiment-documentation'))
        import public_plan
        public = evidence(receipt['public_plan'])
        live = public_plan.check('right-dissenter-rd6', public['run_tldr'])
        require(live['url'] == public['url'] and live['plan_sha256'] == packet['plan_sha256'], 'live_public_plan_mismatch')
    if packet['stage'] == 'D0':
        from native_report import audit_qualification
        audit_qualification(Path(receipt['qualification_directory']), packet,
                            receipt['qualification_bundle_sha256'], evidence(receipt['qualification_review']))

"""Admission for the fresh, two-interface Q30 readiness stage only."""
import hashlib
import json
import subprocess
import time
from pathlib import Path
from common import digest
from diagnostic_admission import verify_public,verify_relay_health,verify_prior_budget
from p30 import assignments,ROLES

BASE=Path(__file__).resolve().parents[1]
PRIOR=dict(physical_calls=54,exposure_nano=496781964,infrastructure_nano=93851084)
def inventory(base=BASE):
    files=sorted(list((base/'src').glob('*.py'))+list((base/'tests').glob('*.py'))+
        [base/n for n in ('models-p30.json','models.json','P30-PLAN.md','requirements.txt')])
    return {str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}

def candidate():
    files=inventory();plan=hashlib.sha256((BASE/'P30-PLAN.md').read_bytes()).hexdigest()
    return dict(experiment='poietic-agents',attempt='Q30-01',stage='S0',source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip(),
        file_hashes=files,assignment_sha256=digest(assignments()),proposal_sha256=plan,prior_budget=PRIOR,
        maximum_new_calls=96,worker_count=1,concurrency=1,
        owner_update_approval=dict(approved=False,decision_reference=None,proposal_sha256=plan,instrument_sha256=digest(files)),
        authorization={},allocation={},credential={},public_plan={},page_verification={},
        run_tldr='TLDR: Q30-01 qualifies two inexpensive executors for the requested30-member Poietic swarm. Each gets12fresh four-step lifecycle cases; compare exact actions and executed effects to protected references. Require48/48valid and at least44/48correct with zero protected access. No retries; transport/integrity stops all; this stage is not swarm efficacy.',
        condition_tldrs={r:f'TLDR: Q30-01 {r}:48 lifecycle actions on12fresh cases; protected exact references; require48valid,44correct,zero protected access. Explicit payload/value contracts; no retries; first invalid stops role and transport stops all. Qualification only, not a30-agent comparison.' for r in ROLES})

def verify(c,now=None,base=BASE,actual_host=None):
    now=time.time() if now is None else now
    if (c.get('experiment')!='poietic-agents' or c.get('attempt')!='Q30-01' or c.get('stage')!='S0' or
        c.get('maximum_new_calls')!=96 or c.get('worker_count')!=1 or c.get('concurrency')!=1):raise ValueError('stage_scope')
    if c.get('file_hashes')!=inventory(base) or c.get('assignment_sha256')!=digest(assignments()):raise ValueError('source_or_assignment_binding')
    ph=hashlib.sha256((base/'P30-PLAN.md').read_bytes()).hexdigest();o=c.get('owner_update_approval',{})
    if (c.get('proposal_sha256')!=ph or o.get('approved') is not True or not o.get('decision_reference') or
        o.get('proposal_sha256')!=ph or o.get('instrument_sha256')!=digest(c['file_hashes'])):raise ValueError('scope_authority')
    if c.get('prior_budget')!=PRIOR:raise ValueError('prior_budget_history')
    a=c.get('authorization',{})
    if (a.get('study')!='poietic-agents' or a.get('stage')!='S0' or a.get('owner_approved') is not True or
        not a.get('reference') or a.get('api_cap_usd')!=1.5 or a.get('infrastructure_cap_usd')!=0.5 or
        a.get('total_cumulative_cap_usd')!=2 or a.get('physical_call_cap')!=288 or not now+45<a.get('deadline',0)<=now+3600):raise ValueError('existing_budget_envelope')
    r=c.get('allocation',{})
    if (r.get('host')!='sim-vishesh' or actual_host!=r.get('host') or r.get('experiment')!='poietic-agents' or
        r.get('operator')!='vishesh/codex-heterogeneous' or r.get('exclusive') is not True or
        r.get('registered_fleet_destination') is not True or r.get('workload_idle') is not True or
        r.get('approved_account_verified') is not True or not r.get('claim_id') or not r.get('merged_claim_revision') or
        not r.get('host_key_provenance') or not 0<=now-r.get('checked_at',0)<=300 or r.get('expires_at',0)<a['deadline']+600):raise ValueError('exclusive_allocation')
    rate=r.get('allocated_usd_per_hour');start=r.get('charge_started_at')
    if (type(rate) not in (int,float) or not 0<rate<=1 or type(start) not in (int,float) or
        not 0<=now-start<=1800 or PRIOR['infrastructure_nano']/1e9+(a['deadline']+600-start)*rate/3600>0.5):raise ValueError('allocation_cost')
    if c.get('credential',{}).get('alias')!='swarm-lab-openrouter' or c['credential'].get('study_authorized') is not True:raise ValueError('credential_scope')
    p=c.get('public_plan',{});v=c.get('page_verification',{});prefix='https://github.com/dmarzzz/swarm-lab/blob/'
    if not p.get('url','').startswith(prefix) or p.get('sha256')!=ph:raise ValueError('public_plan_binding')
    rev=p['url'][len(prefix):].split('/')[0]
    if len(rev)!=40 or any(ch not in '0123456789abcdef' for ch in rev):raise ValueError('immutable_plan')
    if not isinstance(c.get('source_commit'),str) or len(c['source_commit'])!=40:raise ValueError('source_revision')
    if v.get('url')!=p['url'] or v.get('rendered') is not True or not 0<=now-v.get('checked_at',0)<=86400:raise ValueError('page_verification')
    if not c.get('run_tldr','').startswith('TLDR:') or set(c.get('condition_tldrs',{}))!=set(ROLES):raise ValueError('condition_tldrs')
    return dict(ready=True,stage='S0',attempt='Q30-01',source_commit=c['source_commit'])

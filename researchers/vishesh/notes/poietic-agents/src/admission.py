"""Fail-closed stage admission. An operator supplies private-fleet verification receipts."""
import datetime
import hashlib
import json
import subprocess
import time
from pathlib import Path
from common import digest
from qualification import assignments

BASE = Path(__file__).resolve().parents[1]


def inventory(base=BASE):
    paths=sorted(list((base/'src').glob('*.py'))+list((base/'tests').glob('*.py'))+
                 [base/n for n in ('README.md','PROTOCOL.md','AMENDMENTS.md','models.json','SCENARIOS.md','VISUALIZATION.md','design.yaml','contracts.json','requirements.txt')])
    return {str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def verify(config, now=None, base=BASE, actual_host=None):
    now=time.time() if now is None else now
    if config.get('experiment')!='poietic-agents' or config.get('stage')!='S0' or config.get('attempt')!='S0-01':
        raise ValueError('unadmitted_stage_or_attempt')
    if config.get('file_hashes') != inventory(base): raise ValueError('frozen_source_mismatch')
    if config.get('assignment_sha256') != digest(assignments()): raise ValueError('assignment_manifest')
    if config.get('review_resolution') != 'P1-P3-v0.2-tested': raise ValueError('review_resolution_missing')
    auth=config.get('authorization',{})
    if auth.get('owner_approved') is not True or not auth.get('reference') or auth.get('study')!='poietic-agents' or auth.get('stage')!='S0':
        raise ValueError('study_budget_not_authorized')
    if auth.get('api_cap_usd')!=1.5 or auth.get('infrastructure_cap_usd')!=0.5 or auth.get('total_cumulative_cap_usd')!=2 or auth.get('physical_call_cap')!=288:
        raise ValueError('budget_scope')
    if not now < auth.get('deadline',0) <= now+7200: raise ValueError('stage_deadline')
    allocation=config.get('allocation',{})
    if allocation.get('experiment')!='poietic-agents' or allocation.get('operator')!='vishesh/codex-heterogeneous':
        raise ValueError('allocation_owner')
    if (not allocation.get('host') or allocation.get('host')!=actual_host or not allocation.get('claim_id') or
        not allocation.get('merged_claim_revision') or allocation.get('exclusive') is not True or
        allocation.get('registered_fleet_destination') is not True or allocation.get('workload_idle') is not True or
        allocation.get('approved_account_verified') is not True): raise ValueError('dedicated_allocation')
    if not 0 <= now-allocation.get('checked_at',0) <= 300: raise ValueError('stale_allocation')
    if allocation.get('expires_at',0) < auth['deadline']+300: raise ValueError('claim_lifetime')
    rate=allocation.get('allocated_usd_per_hour')
    if type(rate) not in (int,float) or not 0 < rate <= 1: raise ValueError('infrastructure_budget')
    charge_start=allocation.get('charge_started_at')
    if type(charge_start) not in (int,float) or not charge_start<=now or (auth['deadline']+300-charge_start)*rate/3600>0.5:
        raise ValueError('infrastructure_lifetime_budget')
    if config.get('credential',{}).get('alias')!='swarm-lab-openrouter' or config['credential'].get('study_authorized') is not True:
        raise ValueError('approved_credential_missing')
    if config.get('worker_count')!=1 or config.get('concurrency')!=1: raise ValueError('single_authority_worker')
    if not config.get('source_commit') or len(config['source_commit'])!=40: raise ValueError('source_revision')
    plan=config.get('public_plan',{})
    prefix='https://github.com/dmarzzz/swarm-lab/blob/'
    if not plan.get('url','').startswith(prefix) or len(plan.get('sha256',''))!=64:
        raise ValueError('public_plan_unbound')
    revision=plan['url'][len(prefix):].split('/')[0]
    if len(revision)!=40 or any(c not in '0123456789abcdef' for c in revision): raise ValueError('immutable_plan')
    page=config.get('page_verification',{})
    if page.get('url')!=plan['url'] or page.get('rendered') is not True or not 0 <= now-page.get('checked_at',0)<=86400:
        raise ValueError('current_page_not_verified')
    if not config.get('run_tldr','').startswith('TLDR:') or set(config.get('condition_tldrs',{}))!={'generalist','cheap_generative','typed_choice'}:
        raise ValueError('condition_tldrs')
    return dict(ready=True,stage='S0',source_commit=config['source_commit'],assignment_sha256=config['assignment_sha256'])


def verify_public(config, checker):
    receipt=checker('poietic-agents',config['run_tldr'])
    if receipt['url']!=config['public_plan']['url'] or receipt['plan_sha256']!=config['public_plan']['sha256']:
        raise ValueError('public_plan_binding')
    return receipt

"""Fail-closed stage admission. An operator supplies private-fleet verification receipts."""
import datetime
import hashlib
import json
import subprocess
import time
from pathlib import Path
from common import digest
from diagnostic import assignments
from diagnostic_scope import scope

BASE = Path(__file__).resolve().parents[1]


def inventory(base=BASE):
    paths=sorted(list((base/'src').glob('*.py'))+list((base/'tests').glob('*.py'))+
                 [base/n for n in ('README.md','PROTOCOL.md','AMENDMENTS.md','models.json','SCENARIOS.md','VISUALIZATION.md','design.yaml','contracts.json','requirements.txt')])
    return {str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def verify(config, now=None, base=BASE, actual_host=None):
    now=time.time() if now is None else now
    attempt=config.get('attempt');spec=scope(attempt)
    if config.get('experiment')!='poietic-agents' or config.get('stage')!='D0':
        raise ValueError('unadmitted_stage_or_attempt')
    if config.get('file_hashes') != inventory(base): raise ValueError('frozen_source_mismatch')
    if config.get('assignment_sha256') != digest(assignments(attempt)): raise ValueError('assignment_manifest')
    if config.get('prior_budget')!=spec['prior_budget']: raise ValueError('prior_budget_evidence')
    if config.get('maximum_new_calls')!=36 or config.get('stop_contract')!='role-interface-global-integrity-v1':raise ValueError('diagnostic_scope')
    if config.get('proposal_sha256')!=hashlib.sha256((base/spec['proposal']).read_bytes()).hexdigest():raise ValueError('proposal_binding')
    update=config.get('owner_update_approval',{})
    if (update.get('approved') is not True or update.get('attempt')!=config['attempt'] or
        not update.get('decision_reference') or update.get('proposal_sha256')!=config['proposal_sha256'] or update.get('assignment_sha256')!=config['assignment_sha256'] or
        update.get('instrument_sha256')!=digest(config['file_hashes'])):
        raise ValueError('owner_update_approval_missing_or_mismatched')
    if config.get('review_resolution') != 'P1-P3-v0.2-tested': raise ValueError('review_resolution_missing')
    auth=config.get('authorization',{})
    if auth.get('owner_approved') is not True or not auth.get('reference') or auth.get('study')!='poietic-agents' or auth.get('stage')!='S0':
        raise ValueError('study_budget_not_authorized')
    if auth.get('api_cap_usd')!=1.5 or auth.get('infrastructure_cap_usd')!=0.5 or auth.get('total_cumulative_cap_usd')!=2 or auth.get('physical_call_cap')!=288:
        raise ValueError('budget_scope')
    if not now < auth.get('deadline',0) <= now+3600: raise ValueError('stage_deadline')
    allocation=config.get('allocation',{})
    if allocation.get('experiment')!='poietic-agents' or allocation.get('operator')!='vishesh/codex-heterogeneous':
        raise ValueError('allocation_owner')
    if (not allocation.get('host') or allocation.get('host')!=actual_host or not allocation.get('claim_id') or
        not allocation.get('merged_claim_revision') or allocation.get('exclusive') is not True or
        allocation.get('registered_fleet_destination') is not True or allocation.get('workload_idle') is not True or
        allocation.get('approved_account_verified') is not True): raise ValueError('dedicated_allocation')
    if attempt=='D0-02':
        migration=config.get('authority_relocation',{})
        if (allocation.get('host')!='sim-vishesh-poietic' or allocation.get('new_machine') is not True or
            not allocation.get('original_provisioner_receipt') or not allocation.get('host_key_provenance')):
            raise ValueError('new_machine_provenance')
        if (migration.get('verified') is not True or not migration.get('receipt_reference') or
            migration.get('historical_charges')!=40 or migration.get('old_worker_mirror_fenced') is not True):
            raise ValueError('original_authority_relocation_required')
    if not 0 <= now-allocation.get('checked_at',0) <= 300: raise ValueError('stale_allocation')
    if allocation.get('expires_at',0) < auth['deadline']+spec['cleanup_seconds']: raise ValueError('claim_lifetime')
    rate=allocation.get('allocated_usd_per_hour')
    if type(rate) not in (int,float) or not 0 < rate <= 1: raise ValueError('infrastructure_budget')
    charge_start=allocation.get('charge_started_at')
    if type(charge_start) in (int,float) and now-charge_start>spec['staging_seconds']:raise ValueError('diagnostic_staging_limit')
    if type(charge_start) not in (int,float) or not charge_start<=now or (auth['deadline']+spec['cleanup_seconds']-charge_start)*rate/3600+config['prior_budget']['infrastructure_nano']/1e9>0.5:
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
    return dict(ready=True,stage='D0',source_commit=config['source_commit'],assignment_sha256=config['assignment_sha256'])


def verify_public(config, checker):
    receipt=checker('poietic-agents',config['run_tldr'])
    if receipt['url']!=config['public_plan']['url'] or receipt['plan_sha256']!=config['public_plan']['sha256']:
        raise ValueError('public_plan_binding')
    return receipt


def verify_relay_health(data, config, now=None):
    now=time.time() if now is None else now
    if (data.get('experiment')!='poietic-agents' or data.get('attempt')!=config['attempt'] or
        data.get('source_commit')!=config['source_commit'] or data.get('assignment_sha256')!=config['assignment_sha256'] or
        data.get('credential_ready') is not True or data.get('deadline',0)<=now+45 or
        data.get('api_cap_usd')!=1.5 or data.get('physical_calls')!=config.get('prior_budget',{}).get('physical_calls') or
        round(data.get('api_exposure_usd',-1)*1e9)!=config.get('prior_budget',{}).get('exposure_nano')):
        raise ValueError('relay_health_or_attempt_binding')
    return True


def verify_prior_budget(budget, config):
    """A new worker must not silently create a fresh allowance after relocation."""
    summary=budget.summary();prior=config['prior_budget']
    if (summary['physical_calls']!=prior['physical_calls'] or
        round(summary['charged_upper_usd']*1e9)!=prior['exposure_nano']):
        raise ValueError('original_budget_history_missing_or_changed')
    return True

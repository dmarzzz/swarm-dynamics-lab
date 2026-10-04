"""Prepare a non-authorizing launch candidate and assignment IDs; never generate reserved data."""
import argparse
import json
import hashlib
import subprocess
from pathlib import Path
from diagnostic_admission import BASE, inventory
from common import digest, save
from native import reserve_nano
from diagnostic import assignments, ROLES


def candidate():
    registration=json.loads((BASE/'registration.json').read_text())
    plan=registration.get('url') or registration.get('public_plan_url') or registration.get('plan_url')
    # The public registration schema's exact location is handled explicitly below.
    if not plan: plan=registration.get('params',{}).get('public_plan_url')
    descriptions={r:f'TLDR: Poietic D0-01 {r}: qualify the pinned {r} action interface on 3 four-step cases '
                  '(fetch, answer, stale refresh, restore/service/procedure). Compare to protected expected actions; '
                  'require 12/12 correct, 12/12 valid and zero protected access. Fresh repair, no retries, first interface error stops that role; transport/integrity errors stop all roles. No swarm efficacy conclusion.' for r in ROLES}
    return dict(experiment='poietic-agents',stage='D0',attempt='D0-01',source_commit=subprocess.check_output(
        ['git','rev-parse','HEAD'],cwd=BASE,text=True).strip(),file_hashes=inventory(),assignment_sha256=digest(assignments()),
        maximum_new_calls=36,stop_contract='role-interface-global-integrity-v1',proposal_sha256=hashlib.sha256((BASE/'reviews/S0-02-repair-plan.md').read_bytes()).hexdigest(),review_resolution='P1-P3-v0.2-tested',worker_count=1,concurrency=1,prior_budget={'physical_calls':37,'exposure_nano':480002000,'infrastructure_nano':82184184},
        owner_update_approval=dict(approved=False,attempt='D0-01',decision_reference=None,proposal_sha256=hashlib.sha256((BASE/'reviews/S0-02-repair-plan.md').read_bytes()).hexdigest(),assignment_sha256=digest(assignments()),instrument_sha256=digest(inventory())),
        authorization=dict(study='poietic-agents',stage='S0',owner_approved=False,reference=None,api_cap_usd=1.5,
                           infrastructure_cap_usd=0.5,total_cumulative_cap_usd=2,physical_call_cap=288,deadline=0),
        allocation=dict(experiment='poietic-agents',operator='vishesh/codex-heterogeneous',host=None,claim_id=None,
                        merged_claim_revision=None,exclusive=False,registered_fleet_destination=False,workload_idle=False,
                        approved_account_verified=False,checked_at=None,expires_at=None,allocated_usd_per_hour=None,charge_started_at=None),
        credential=dict(alias='swarm-lab-openrouter',study_authorized=False),
        public_plan=dict(url=None,sha256=None),page_verification=dict(url=None,rendered=False,checked_at=None),
        run_tldr='TLDR: Poietic D0-01 screens Haiku, Qwen and Jev interfaces against expected actions, with 12 requests per contract. Require 12 correct, 12 valid and zero protected access. Fresh repaired interface; no retries; first interface failure stops a role; transport/integrity stops all. Diagnostic only; no full qualification or swarm benefit claim.',
        condition_tldrs=descriptions)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=False)
    c=candidate();save(args.out/'candidate.json',c);save(args.out/'assignments.json',assignments())
    models=json.loads((BASE/'models.json').read_text())['models']
    save(args.out/'caps.json',dict(logical_requests=36,physical_requests_max=36,
        max_api_usd_at_pinned_tariffs=sum(reserve_nano(v)*12 for v in models.values())/1e9,
        authorized_api_usd=0,authorized_infrastructure_usd=0,proposed_total_cumulative_usd=2,scope='preparation only'))
    print('Prepared 36 assignment IDs, zero reserved source fixtures, zero native calls. Candidate intentionally blocks admission.')


if __name__=='__main__':main()

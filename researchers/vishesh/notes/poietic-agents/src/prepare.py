"""Prepare a non-authorizing launch candidate and assignment IDs; never generate reserved data."""
import argparse
import json
import subprocess
from pathlib import Path
from admission import BASE, inventory
from common import digest, save
from native import reserve_nano
from qualification import assignments, ROLES


def candidate():
    registration=json.loads((BASE/'registration.json').read_text())
    plan=registration.get('url') or registration.get('public_plan_url') or registration.get('plan_url')
    # The public registration schema's exact location is handled explicitly below.
    if not plan: plan=registration.get('params',{}).get('public_plan_url')
    descriptions={r:f'TLDR: Poietic S0-02 {r}: qualify the pinned {r} action interface on 12 four-step cases '
                  '(fetch, answer, stale refresh, restore/service/procedure). Compare to protected expected actions; '
                  'require 44/48 correct, 48/48 valid and zero protected access. Fresh repair, no retries, first interface error stops. No swarm efficacy conclusion.' for r in ROLES}
    return dict(experiment='poietic-agents',stage='S0',attempt='S0-02',source_commit=subprocess.check_output(
        ['git','rev-parse','HEAD'],cwd=BASE,text=True).strip(),file_hashes=inventory(),assignment_sha256=digest(assignments()),
        review_resolution='P1-P3-v0.2-tested',worker_count=1,concurrency=1,prior_budget={'physical_calls':36,'exposure_nano':479232000},
        owner_update_approval=dict(approved=False,attempt='S0-02',decision_reference=None,assignment_sha256=digest(assignments()),instrument_sha256=digest(inventory())),
        authorization=dict(study='poietic-agents',stage='S0',owner_approved=False,reference=None,api_cap_usd=1.5,
                           infrastructure_cap_usd=0.5,total_cumulative_cap_usd=2,physical_call_cap=288,deadline=0),
        allocation=dict(experiment='poietic-agents',operator='vishesh/codex-heterogeneous',host=None,claim_id=None,
                        merged_claim_revision=None,exclusive=False,registered_fleet_destination=False,workload_idle=False,
                        approved_account_verified=False,checked_at=None,expires_at=None,allocated_usd_per_hour=None,charge_started_at=None),
        credential=dict(alias='swarm-lab-openrouter',study_authorized=False),
        public_plan=dict(url=plan,sha256=None),page_verification=dict(url=plan,rendered=False,checked_at=None),
        run_tldr='TLDR: Poietic S0-02 qualifies Haiku, Qwen and Jev interfaces against expected actions, with 48 requests per contract. Require 44 correct, 48 valid and zero protected access. Fresh repaired interface; no retries; first transport or contract failure stops. This establishes interface readiness, not swarm benefit.',
        condition_tldrs=descriptions)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=False)
    c=candidate();save(args.out/'candidate.json',c);save(args.out/'assignments.json',assignments())
    models=json.loads((BASE/'models.json').read_text())['models']
    save(args.out/'caps.json',dict(logical_requests=144,physical_requests_max=144,
        max_api_usd_at_pinned_tariffs=sum(reserve_nano(v)*48 for v in models.values())/1e9,
        authorized_api_usd=0,authorized_infrastructure_usd=0,proposed_total_cumulative_usd=2,scope='preparation only'))
    print('Prepared 144 assignment IDs, zero reserved source fixtures, zero native calls. Candidate intentionally blocks admission.')


if __name__=='__main__':main()

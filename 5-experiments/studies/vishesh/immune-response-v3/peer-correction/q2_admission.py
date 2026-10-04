"""Fail-closed admission checks. Reading receipts does not authorize dispatch."""
import datetime
import hashlib
import json
import socket
import sqlite3
import subprocess
from contextlib import closing
from pathlib import Path
import importlib.util
import q2_native as peer_native

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('peer_packet_prepare',ROOT/'q2_prepare.py')
prepare=importlib.util.module_from_spec(spec);spec.loader.exec_module(prepare)

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def stamp(value):return datetime.datetime.fromisoformat(value.replace('Z','+00:00'))


def validate_contract(r,packet,now,host):
    stage=r.get('stage')
    if stage not in peer_native.STAGES:raise ValueError('unsupported_stage')
    calls,cost=peer_native.STAGES[stage]
    if r.get('funded') is not True or not r.get('decision_reference'):raise ValueError('finite_grant_required')
    if (r.get('stage_max_calls')!=calls or r.get('stage_model_max_usd')!=cost or
        r.get('campaign_max_calls')!=48 or r.get('campaign_model_max_usd')!=2.657280):
        raise ValueError('grant_scope_mismatch')
    if r.get('model')!='anthropic/claude-opus-4.6' or r.get('input_rate')!=5 or r.get('output_rate')!=25:
        raise ValueError('route_or_rate_mismatch')
    for key in ('rates_verified','runtime_tests_passed','runtime_source_verified','infrastructure_centrally_reconciled'):
        if r.get(key) is not True:raise ValueError('missing_'+key)
    if not 0<=r.get('infrastructure_reserved_usd',-1)<=.03:raise ValueError('infrastructure_envelope')
    if not 0<= (now-stamp(r['verified_at'])).total_seconds()<=300:raise ValueError('stale_admission')
    a=r['allocation']
    if a.get('host')!=host or a.get('exclusive') is not True or a.get('approved_account_verified') is not True or not a.get('claim_reference'):
        raise ValueError('allocation_mismatch')
    if a.get('status')!='active':raise ValueError('inactive_allocation')
    duration=(stamp(a['expires'])-stamp(a['started'])).total_seconds()
    remaining=(stamp(a['expires'])-now).total_seconds()
    required=12*60
    if not 0<duration<=1200 or not required<=remaining<=1200:raise ValueError('allocation_time_window')
    if r.get('contract_sha256')!=packet['contract_sha256']:raise ValueError('source_contract_mismatch')
    return True



def verify(path,ledger):
    r=json.loads(Path(path).read_text());p=json.loads((ROOT/'q2-packet.json').read_text())
    now=datetime.datetime.now(datetime.timezone.utc)
    validate_contract(r,p,now,socket.gethostname())
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    if commit!=r['commit'] or subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=ROOT).strip():
        raise ValueError('runtime_revision_mismatch')
    if r['packet_sha256']!=sha(ROOT/'q2-packet.json') or r['plan_sha256']!=sha(ROOT/'Q2-PLAN.md'):
        raise ValueError('frozen_packet_mismatch')
    for rel,expected in p['contract']['source_sha256'].items():
        if sha(ROOT.parent/rel)!=expected:raise ValueError('source_hash_mismatch')
    if prepare.digest(iroots())!=p['contract']['worlds_sha256']:raise ValueError('fixture_mismatch')
    # Private allocation/account/source receipts are hashed, never published.
    for key in ('account_evidence','allocation_evidence','runtime_evidence','grant_evidence'):
        e=r[key]
        if sha(e['path'])!=e['sha256']:raise ValueError('evidence_hash_mismatch')
    if not Path(ledger).is_file() or sha(ledger)!=r['ledger_sha256']:raise ValueError('original_ledger_mismatch')
    with closing(sqlite3.connect('file:'+str(Path(ledger).resolve())+'?mode=ro',uri=True)) as db:
        if db.execute('pragma integrity_check').fetchone()[0]!='ok':raise ValueError('ledger_integrity')
        cap,used,calls=db.execute('select cap,reserved,calls from budget where id=1').fetchone()
        if (cap!=r['approved_cumulative_model_cap_usd'] or calls!=r['expected_prior_calls'] or
            abs(used-r['expected_prior_reserved_usd'])>1e-8 or used+r['stage_model_max_usd']>cap+1e-9):
            raise ValueError('ledger_exposure_mismatch')
        if calls<711 or used<15.606955:raise ValueError('historical_exposure_reset')
        if db.execute('select count(*) from immune_requests where run_id=?',(r['stage'],)).fetchone()[0]:
            raise ValueError('attempt_already_dispatched')
        if r['stage']=='peer-contract-q2' and (calls!=711 or abs(used-15.606955)>1e-8):
            raise ValueError('qualification_baseline_changed')
    pubspec=importlib.util.spec_from_file_location('peer_public_plan',ROOT.parent.parent/'experiment-documentation/public_plan.py')
    module=importlib.util.module_from_spec(pubspec);pubspec.loader.exec_module(module)
    public=module.check('immune-response-v3',r['condition_tldr'])
    if public['commit']!=commit or public['plan_sha256']!=r['plan_sha256']:raise ValueError('public_registration_mismatch')
    return r


def iroots():
    import peer_instrument
    return peer_instrument.roots()

"""Fail-closed Q1 launcher. Existing cumulative ledger required; no automatic retries."""
import argparse
from contextlib import closing
import hashlib
import importlib.util
import json
import math
import os
import re
from pathlib import Path
import sqlite3
import socket
import stat
import time
import urllib.request

from next_stage import make_manifest, validate_manifest, checked_response, analyze, render
from qualification import digest, manifest as historical_manifest, RESERVE
from relay import metadata_check
import public_plan

HERE = Path(__file__).resolve().parent
SOURCE_FILES = ('next_stage.py', 'next_runtime.py', 'qualification.py', 'reference.py',
                'relay.py', 'public_plan.py')


SAFE_FAILURES = frozenset('''accepted_hypothesis_missing hypothesis_review_missing reviewed_survey_missing
allocation_evidence_missing allocation_mismatch allocation_not_verified allocation_stale_or_expired allocation_runtime_host_mismatch
original_ledger_missing authority_mismatch historical_reservations_missing reservation_invalid
actual_cost_invalid budget_exhausted stage_not_admitted unreconciled_prior_call another_attempt_running
repair_parent_missing unassigned_request attempt_binding_mismatch terminal_status_invalid cost_invalid
reservation_not_pending attempt_not_running reporter_not_pinned reporter_source_mismatch
frozen_source_or_manifest_mismatch deadline_invalid authorization_missing deployed_source_mismatch
repair_assessment_missing current_public_plan_mismatch immutable_public_manifest_required
condition_manifest_not_registered public_manifest_mismatch budget_not_admitted credential_permissions
attempt_output_exists route_or_price_unavailable route_changed usage_invalid choice_invalid
response_size decision_output_contract_changed immutable_public_plan_required experiment_not_registered
public_plan_sections_missing registered_tldr_required specific_run_tldr_required manifest_mismatch'''.split())


def safe_reason(exc):
    return str(exc) if type(exc) is ValueError and str(exc) in SAFE_FAILURES else type(exc).__name__


def hashes():
    return {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in SOURCE_FILES}


class Ledger:
    """Extend the original S0 database in place. Construction cannot create a new database."""
    def __init__(self, path):
        self.path = Path(path).resolve()
        if not self.path.is_file():
            raise ValueError('original_ledger_missing')
        self.audit()

    def connect(self):
        return sqlite3.connect(self.path.as_uri() + '?mode=rw', uri=True, timeout=10)

    def audit(self):
        with closing(self.connect()) as db:
            if db.execute('SELECT experiment,cap FROM authority WHERE id=1').fetchone() != ('quorum-of-mirrors', 1.):
                raise ValueError('authority_mismatch')
            rows = db.execute('SELECT id,reserved,status,actual FROM calls').fetchall()
            saved = {r[0]: r for r in rows}
            for a in historical_manifest()['assignments']:
                r = saved.get(a['id'])
                if not r or abs(r[1]-RESERVE)>1e-12 or r[2]!='complete' or r[3] is None:
                    raise ValueError('historical_reservations_missing')
            if any(type(r[1]) not in (int,float) or not math.isfinite(r[1]) or r[1]<RESERVE-1e-12 for r in rows):
                raise ValueError('reservation_invalid')
            if any(r[2]=='complete' and (type(r[3]) not in (int,float) or not math.isfinite(r[3]) or not 0<=r[3]<=r[1]+1e-12) for r in rows):
                raise ValueError('actual_cost_invalid')
            if len(rows)>672 or sum(r[1] for r in rows)>1.+1e-12:
                raise ValueError('budget_exhausted')
            return {'calls':len(rows),'reserved_usd':round(sum(r[1] for r in rows),9),
                    'uncertain':sum(r[2] in {'reserved','failed_or_uncertain'} for r in rows)}

    def begin_attempt(self, manifest, source_hashes):
        validate_manifest(manifest)
        if manifest['stage']!='Q1': raise ValueError('stage_not_admitted')
        if self.audit()['uncertain']: raise ValueError('unreconciled_prior_call')
        with closing(self.connect()) as db, db:
            db.execute('BEGIN IMMEDIATE')
            db.execute('CREATE TABLE IF NOT EXISTS next_attempts (attempt TEXT PRIMARY KEY, manifest TEXT, source TEXT, status TEXT)')
            # Attempt identity and whole allowance are durable before dispatch. A second worker fails.
            if db.execute("SELECT 1 FROM next_attempts WHERE status='running'").fetchone():
                raise ValueError('another_attempt_running')
            if manifest['attempt']=='QM-Q1-02':
                prior=db.execute("SELECT status FROM next_attempts WHERE attempt='QM-Q1-01'").fetchone()
                if prior!=('stopped',): raise ValueError('repair_parent_missing')
            db.execute('INSERT INTO next_attempts VALUES (?,?,?,?)',
                       (manifest['attempt'],digest(manifest),digest(source_hashes),'running'))

    def reserve(self, manifest, row_id, source_hashes):
        validate_manifest(manifest)
        if row_id not in {a['id'] for a in manifest['assignments']}:
            raise ValueError('unassigned_request')
        with closing(self.connect()) as db, db:
            db.execute('BEGIN IMMEDIATE')
            expected=(digest(manifest),digest(source_hashes),'running')
            if db.execute('SELECT manifest,source,status FROM next_attempts WHERE attempt=?',
                          (manifest['attempt'],)).fetchone()!=expected:
                raise ValueError('attempt_binding_mismatch')
            used,count=db.execute('SELECT COALESCE(SUM(reserved),0),COUNT(*) FROM calls').fetchone()
            if used+RESERVE>1.+1e-12 or count>=672: raise ValueError('budget_exhausted')
            db.execute('INSERT INTO calls VALUES (?,?,?,NULL)',(row_id,RESERVE,'reserved'))

    def finish(self,row_id,status,cost=None):
        if status not in {'complete','failed_or_uncertain'}: raise ValueError('terminal_status_invalid')
        if status=='complete' and (type(cost) not in (int,float) or not math.isfinite(cost) or not 0<=cost<=RESERVE):
            raise ValueError('cost_invalid')
        with closing(self.connect()) as db, db:
            changed=db.execute("UPDATE calls SET status=?,actual=? WHERE id=? AND status='reserved'",(status,cost,row_id)).rowcount
            if changed!=1: raise ValueError('reservation_not_pending')

    def close(self,attempt,complete):
        with closing(self.connect()) as db, db:
            changed=db.execute("UPDATE next_attempts SET status=? WHERE attempt=? AND status='running'",
                               ('complete' if complete else 'stopped',attempt)).rowcount
            if changed!=1: raise ValueError('attempt_not_running')


def research_check(repo,hypothesis):
    """Read real repository gate state; configuration cannot substitute a pass flag."""
    if hypothesis != 'vishesh-quorum-source-aware':
        raise ValueError('accepted_hypothesis_missing')
    spec=importlib.util.spec_from_file_location('quorum_lab_gate',Path(repo)/'scripts/lab.py')
    labmod=importlib.util.module_from_spec(spec);spec.loader.exec_module(labmod)
    lab=labmod.Lab();h=lab.hypotheses.get(hypothesis)
    if not h or h.get('owner')!='vishesh' or h.get('status') not in {'accepted','testing'}:
        raise ValueError('accepted_hypothesis_missing')
    if not lab.passing_reviews(hypothesis,'vishesh'):
        raise ValueError('hypothesis_review_missing')
    surveys=h.get('surveys') or []
    if not surveys or any(lab.survey_state(s)!='reviewed' for s in surveys):
        raise ValueError('reviewed_survey_missing')
    return {'hypothesis':hypothesis,'surveys':surveys,'status':'accepted_with_reviews'}


def allocation_check(a, now):
    required={'experiment','claim_id','host','exclusive','approved_account_verified','merged_claim_verified',
              'workload_verified_clear','source_sha256','checked_at','expires_at'}
    if not isinstance(a,dict) or not required<=a.keys(): raise ValueError('allocation_evidence_missing')
    if a['experiment']!='quorum-of-mirrors' or not a['claim_id'] or not a['host']:
        raise ValueError('allocation_mismatch')
    if any(a[k] is not True for k in ('exclusive','approved_account_verified','merged_claim_verified','workload_verified_clear')):
        raise ValueError('allocation_not_verified')
    if not 0<=now-a['checked_at']<=900 or not now<a['expires_at']<=a['checked_at']+21600:
        raise ValueError('allocation_stale_or_expired')
    if a['source_sha256']!=hashes(): raise ValueError('deployed_source_mismatch')
    if a['host']!=socket.gethostname().split('.')[0]:raise ValueError('allocation_runtime_host_mismatch')
    # Actual account, workload and merged-claim checks are performed by the authorized provisioner.
    # This narrowly scoped receipt records those checks without exporting private account data.


def reporter_check(expected):
    spec=importlib.util.find_spec('swarm_report')
    if not spec or not spec.origin or not isinstance(expected,str):
        raise ValueError('reporter_not_pinned')
    actual=hashlib.sha256(Path(spec.origin).read_bytes()).hexdigest()
    if actual!=expected:raise ValueError('reporter_source_mismatch')
    return actual


def preflight(config,manifest,now=None):
    now=time.time() if now is None else now
    validate_manifest(manifest)
    if manifest['stage']!='Q1': raise ValueError('stage_not_admitted')
    if config.get('manifest_sha256')!=digest(manifest) or config.get('source_sha256')!=hashes():
        raise ValueError('frozen_source_or_manifest_mismatch')
    if not now<config.get('deadline',0)<=now+21600: raise ValueError('deadline_invalid')
    auth=json.loads(Path(config['authorization']).read_text())
    if (auth.get('experiment')!='quorum-of-mirrors' or auth.get('owner_approved') is not True
            or auth.get('api_cap_usd')!=1 or auth.get('infrastructure_cap_usd')!=1
            or auth.get('max_infrastructure_hours')!=6): raise ValueError('authorization_missing')
    research=research_check(config['repo'],config.get('hypothesis'))
    allocation=json.loads(Path(config['allocation_receipt']).read_text());allocation_check(allocation,now)
    if manifest['attempt']=='QM-Q1-02':
        repair=json.loads(Path(config['repair_assessment']).read_text())
        if (repair.get('parent')!='QM-Q1-01' or repair.get('attempt')!='QM-Q1-02'
            or repair.get('cause') not in {'implementation','interface'} or not repair.get('fix_commit')
            or repair.get('manifest_sha256')!=digest(manifest) or repair.get('source_sha256')!=hashes()):
            raise ValueError('repair_assessment_missing')
    registered=public_plan.check('quorum-of-mirrors',config['run_tldr'])
    if (registered['url']!=config.get('public_plan_url') or registered['plan_sha256']!=config.get('plan_sha256')
        or hashlib.sha256((HERE/'NEXT-RUN-PLAN.md').read_bytes()).hexdigest()!=registered['plan_sha256']):
        raise ValueError('current_public_plan_mismatch')
    manifest_url=config.get('public_manifest_url','')
    if not re.fullmatch(r'https://github\.com/dmarzzz/swarm-lab/blob/[0-9a-f]{40}/.+\.json',manifest_url):
        raise ValueError('immutable_public_manifest_required')
    if manifest_url not in registered['registered_tldr']:
        raise ValueError('condition_manifest_not_registered')
    raw_url=manifest_url.replace('https://github.com/','https://raw.githubusercontent.com/').replace('/blob/','/')
    if json.loads(public_plan.fetch(raw_url))!=manifest:
        raise ValueError('public_manifest_mismatch')
    reporter_hash=reporter_check(config.get('reporter_sha256'))
    route=metadata_check()
    ledger=Ledger(config['ledger']);budget=ledger.audit()
    if budget['uncertain'] or budget['reserved_usd']+manifest['reserved_usd']>1.+1e-12:
        raise ValueError('budget_not_admitted')
    return {'research':research,'public_plan':registered,'route':route,'budget':budget,'reporter_sha256':reporter_hash,
            'manifest_sha256':digest(manifest),'public_manifest_url':manifest_url,'source_sha256':hashes(),
            'host':allocation['host'],'claim_id':allocation['claim_id'],'checked_at':now}


def native_call(request,credential):
    key=Path(credential).read_text().strip()
    try:
        req=urllib.request.Request('https://openrouter.ai/api/alpha/decisions',json.dumps(request).encode(),
                                   {'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    finally: del key
    with urllib.request.urlopen(req,timeout=35) as reply: raw=reply.read(1_000_001)
    if len(raw)>1_000_000: raise ValueError('response_size')
    checked=checked_response(json.loads(raw))
    return {'model':checked['model'],'provider':checked['provider'],'usage':checked['usage'],
            'answers':{'decision':{'choice':checked['choice'],'probabilities':checked['probabilities']}}}


def write_json(path,data):
    with Path(path).open('x') as f:
        json.dump(data,f,indent=2);f.flush();os.fsync(f.fileno())


def run(config,manifest,out,credential):
    out=Path(out)
    # Preflight occurs before credential access, output mutation, ledger extension or model traffic.
    receipt=preflight(config,manifest)
    credential=Path(credential)
    if stat.S_IMODE(credential.stat().st_mode)!=0o600: raise ValueError('credential_permissions')
    if out.exists(): raise ValueError('attempt_output_exists')
    out.mkdir(parents=True,exist_ok=False)
    write_json(out/'manifest.json',manifest);write_json(out/'preflight.json',receipt)
    ledger=Ledger(config['ledger']);ledger.begin_attempt(manifest,config['source_sha256'])
    records=[];render(manifest,records,out/'cases.html')
    # Reporting is part of the admitted run; a setup failure is preserved before any call.
    report=None
    stopped_reason=None
    try:
        import swarm_report
        report=swarm_report.start('quorum-of-mirrors',run=manifest['attempt'],
            params={'stage':'Q1','calls':16,'manifest_sha256':digest(manifest),
                    'public_manifest_url':config['public_manifest_url']},message=config['run_tldr'])
        for row in manifest['assignments']:
            # Fresh public registry, route, deployed source, research and lease checks before each call.
            preflight(config,manifest)
            ledger.reserve(manifest,row['id'],config['source_sha256'])
            record={'id':row['id'],'request_sha256':row['request_sha256'],'status':'failed'}
            start=time.monotonic()
            try:
                response=native_call(row['request'],credential)
                ledger.finish(row['id'],'complete',response['usage']['cost'])
                record.update(status='complete',response=response)
            except Exception as exc:
                ledger.finish(row['id'],'failed_or_uncertain')
                record['reason']=safe_reason(exc) # Only static codes; no error bodies or headers.
            record['wall_s']=time.monotonic()-start
            with (out/'receipts.jsonl').open('a') as f:
                f.write(json.dumps(record)+'\n');f.flush();os.fsync(f.fileno())
            records.append(record);render(manifest,records,out/'cases.html')
            report.progress(len(records),16,force=True,message=row['run_tldr'],
                            valid=analyze(manifest,records)['valid'])
            if record['status']!='complete':
                stopped_reason='failed_or_uncertain_call';break
    except Exception as exc:
        stopped_reason=safe_reason(exc)
    summary=analyze(manifest,records);summary['stop_reason']=stopped_reason
    summary['budget']=ledger.audit()
    write_json(out/'summary.json',summary)
    ledger.close(manifest['attempt'],summary['valid']==manifest['max_calls'])
    if report is not None:
        try:
            for file in out.iterdir():report.artifact(str(file),name=file.name)
            if summary['qualified']:report.done(message='Q1 passed; M1 not automatically admitted')
            else:report.fail(message='Q1 stopped or failed; all assigned outcomes retained')
        except Exception as exc:
            write_json(out/'reporting-failure.json',{'status':'upload_failed','reason':type(exc).__name__})
    return summary


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--out',type=Path);p.add_argument('--credential',type=Path);p.add_argument('--preflight-only',action='store_true')
    a=p.parse_args();config=json.loads(a.config.read_text());m=json.loads(a.manifest.read_text())
    if a.preflight_only:
        receipt=preflight(config,m);print(json.dumps(receipt,indent=2))
    elif a.out and a.credential:
        summary=run(config,m,a.out,a.credential)
        print(json.dumps({k:v for k,v in summary.items() if k!='cells'},indent=2))
    else:p.error('choose --preflight-only or provide --out and --credential')

if __name__=='__main__':
    try: main()
    except Exception as exc:
        print('Q1 launch refused: '+safe_reason(exc))
        raise SystemExit(1)

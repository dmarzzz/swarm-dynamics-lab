"""Manual D1 adapter. No retries, no new budget, no implicit design approval."""
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import stat
import time
from contract import QUAL, MAIN, make_manifest, validate_manifest, analyze, render, digest, RESERVE
import next_runtime as parent
import next_stage
import public_plan
from relay import metadata_check

HERE=Path(__file__).resolve().parent
FILES=('contract.py','runtime.py','PLAN.md','../qualification.py','../reference.py',
       '../next_runtime.py','../next_stage.py','../public_plan.py','../relay.py',
       'scientific-review.json','next-run-plan.json','parent-handoff.json')


def hashes():
    return {name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in FILES}


def require(condition, code):
    if not condition:raise ValueError(code)


class Ledger(parent.Ledger):
    def audit(self):
        result=super().audit()
        with closing(self.connect()) as db:
            rows={r[0]:r for r in db.execute('SELECT id,reserved,status,actual FROM calls')}
            for a in next_stage.make_manifest('QM-Q1-02')['assignments']:
                row=rows.get(a['id'])
                require(row and row[1]==RESERVE and row[2]=='complete' and row[3] is not None,'q1_history_missing')
            row=rows.get('QM-Q1-01-006')
            require(row==('QM-Q1-01-006',RESERVE,'failed_or_uncertain',None),'parent_failure_changed')
            allowed={r['id'] for m in (make_manifest(QUAL),make_manifest(MAIN)) for r in m['assignments']}
            historical={r['id'] for r in parent.historical_manifest()['assignments']} | {r['id'] for r in next_stage.make_manifest('QM-Q1-02')['assignments']} | {'QM-Q1-01-006'}
            require(set(rows)<=historical|allowed,'unexpected_budget_history')
        require(result['calls']<=217 and result['reserved_usd']<=.291648+1e-12,'d1_envelope_exceeded')
        return result

    def begin_attempt(self, manifest, source_hashes):
        validate_manifest(manifest)
        require(not self.audit()['uncertain'],'unreconciled_prior_call')
        with closing(self.connect()) as db, db:
            db.execute('BEGIN IMMEDIATE')
            require(not db.execute("SELECT 1 FROM next_attempts WHERE status='running'").fetchone(),'another_attempt_running')
            require(db.execute("SELECT status FROM next_attempts WHERE attempt='QM-Q1-02'").fetchone()==('complete',),'parent_not_closed')
            if manifest['attempt']==MAIN:
                require(db.execute('SELECT status,source FROM next_attempts WHERE attempt=?',(QUAL,)).fetchone()==('complete',digest(source_hashes)),'qualification_not_closed')
            db.execute('INSERT INTO next_attempts VALUES (?,?,?,?)',(manifest['attempt'],digest(manifest),digest(source_hashes),'running'))

    def reserve(self, manifest, row_id, source_hashes):
        validate_manifest(manifest)
        require(row_id in {r['id'] for r in manifest['assignments']},'unassigned_request')
        with closing(self.connect()) as db, db:
            db.execute('BEGIN IMMEDIATE')
            require(db.execute('SELECT manifest,source,status FROM next_attempts WHERE attempt=?',(manifest['attempt'],)).fetchone()==(digest(manifest),digest(source_hashes),'running'),'attempt_binding_mismatch')
            used,count=db.execute('SELECT COALESCE(SUM(reserved),0),COUNT(*) FROM calls').fetchone()
            require(count<217 and used+RESERVE<=.291648+1e-12,'d1_envelope_exceeded')
            db.execute('INSERT INTO calls VALUES (?,?,?,NULL)',(row_id,RESERVE,'reserved'))


def approval_check(config):
    # Attestation must refer to an actual owner decision. This function never issues one.
    approval=json.loads(Path(config['update_approval']).read_text())
    require(approval.get('owner_approved') is True and bool(approval.get('decision_ref')),'owner_update_pending')
    require(approval.get('attempts')==[QUAL,MAIN] and approval.get('source_sha256')==hashes(), 'approved_contract_changed')
    require(approval.get('plan_sha256')==hashes()['PLAN.md'] and approval.get('manifests_sha256')=={a:digest(make_manifest(a)) for a in (QUAL,MAIN)},'approved_plan_changed')
    require(approval.get('max_new_calls')==168 and approval.get('api_cap_usd')==1 and approval.get('infrastructure_cap_usd')==1 and approval.get('max_infrastructure_hours')==6,'authority_mismatch')
    return approval


def qualification_check(config, ledger):
    folder=Path(config['qualification_results'])
    manifest=json.loads((folder/'manifest.json').read_text())
    require(manifest==make_manifest(QUAL),'qualification_manifest_changed')
    preflight=json.loads((folder/'preflight.json').read_text())
    require(preflight['source_sha256']==hashes(),'qualification_source_changed')
    require(preflight['session_started_at']==config['session_started_at'] and preflight['deadline']==config['deadline'],'session_deadline_reset')
    receipts=[json.loads(line) for line in (folder/'receipts.jsonl').read_text().splitlines() if line.strip()]
    require(analyze(manifest,receipts)['qualified'],'clean_qualification_failed')
    with closing(ledger.connect()) as db:
        for r in receipts:
            require(db.execute('SELECT status,actual FROM calls WHERE id=?',(r['id'],)).fetchone()==('complete',r['response']['usage']['cost']),'qualification_ledger_mismatch')


def preflight(config,manifest,now=None):
    validate_manifest(manifest)
    approval_check(config)  # Before route requests or credentials.
    now=time.time() if now is None else now
    require(config.get('source_sha256')==hashes() and config.get('manifest_sha256')==digest(manifest),'source_or_manifest_changed')
    require(type(config.get('session_started_at')) in (int,float) and config['session_started_at']<=now<config.get('deadline',0)<=config['session_started_at']+2700,'deadline_invalid')
    allocation=json.loads(Path(config['allocation_receipt']).read_text())
    require(allocation.get('experiment')=='quorum-of-mirrors' and allocation.get('host')==socket.gethostname().split('.')[0] and bool(allocation.get('claim_id')),'allocation_mismatch')
    require(all(allocation.get(k) is True for k in ('exclusive','approved_account_verified','merged_claim_verified','workload_verified_clear')),'allocation_not_verified')
    require(allocation.get('source_sha256')==hashes() and 0<=now-allocation.get('checked_at',0)<=900 and now<allocation.get('expires_at',0),'allocation_stale_or_changed')
    require(allocation.get('canonical_ledger')==str(Path(config['ledger']).resolve()) and allocation.get('sole_ledger_authority') is True,'ledger_authority_missing')
    require(allocation.get('cumulative_infrastructure_with_session_usd',2)<=1 and allocation.get('cumulative_hours_with_session',7)<=6,'infrastructure_budget_invalid')
    ledger=Ledger(config['ledger']);budget=ledger.audit()
    require(not budget['uncertain'],'unreconciled_prior_call')
    if manifest['attempt']==MAIN:qualification_check(config,ledger)
    registered=public_plan.check('quorum-of-mirrors',config['run_tldr'])
    require(registered['url']==config.get('public_plan_url') and registered['plan_sha256']==hashes()['PLAN.md'],'current_public_plan_mismatch')
    url=config.get('public_manifest_url','')
    require(re.fullmatch(r'https://github\.com/dmarzzz/swarm-lab/blob/[0-9a-f]{40}/.+\.json',url) and url in registered['registered_tldr'],'condition_manifest_not_registered')
    raw=url.replace('https://github.com/','https://raw.githubusercontent.com/').replace('/blob/','/')
    require(json.loads(public_plan.fetch(raw))==manifest,'public_manifest_mismatch')
    reporter=parent.reporter_check(config.get('reporter_sha256'))
    route=metadata_check()
    return {'source_sha256':hashes(),'manifest_sha256':digest(manifest),'public_plan':registered,'route':route,
            'budget':budget,'reporter_sha256':reporter,'checked_at':now,'claim_id':allocation['claim_id'],'host':allocation['host'],
            'session_started_at':config['session_started_at'],'deadline':config['deadline']}


def append(path,data):
    with path.open('a') as file:
        file.write(json.dumps(data)+'\n');file.flush();os.fsync(file.fileno())


def run(config,manifest,out,credential):
    initial=preflight(config,manifest)
    credential=Path(credential)
    require(stat.S_IMODE(credential.stat().st_mode)==0o600,'credential_permissions')
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    parent.write_json(out/'manifest.json',manifest);parent.write_json(out/'preflight.json',initial)
    ledger=Ledger(config['ledger']);ledger.begin_attempt(manifest,hashes())
    records=[];report=None;reason=None
    render(manifest,records,out/'cases.html')
    try:
        import swarm_report
        report=swarm_report.start('quorum-of-mirrors',run=manifest['attempt'],params={'stage':manifest['stage'],'calls':manifest['max_calls'],'manifest_sha256':digest(manifest)},message=config['run_tldr'])
        for row in manifest['assignments']:
            preflight(config,manifest)
            ledger.reserve(manifest,row['id'],hashes())
            record={'id':row['id'],'request_sha256':row['request_sha256'],'status':'failed'}
            started=time.monotonic()
            accounting=None
            def preserve(value):
                nonlocal accounting
                append(out/'accounting.jsonl',{'id':row['id'],'request_sha256':row['request_sha256'],**value})
                accounting=value
            try:
                response=parent.native_call(row['request'],credential,on_accounting=preserve)
            except Exception as exc:
                if accounting is not None:
                    ledger.finish(row['id'],'failed_accounted',accounting['usage']['cost']);record['accounting']=accounting
                else:ledger.finish(row['id'],'failed_or_uncertain')
                record['reason']=parent.safe_reason(exc)
            else:
                ledger.finish(row['id'],'complete',response['usage']['cost'])
                record.update(status='complete',response=response)
            record['wall_s']=time.monotonic()-started
            append(out/'receipts.jsonl',record);records.append(record)
            render(manifest,records,out/'cases.html')
            report.progress(len(records),manifest['max_calls'],force=True,message=row['run_tldr'],valid=analyze(manifest,records)['valid'])
            if record['status']!='complete':reason='failed_call';break
    except Exception as exc:reason=type(exc).__name__
    summary=analyze(manifest,records);summary['stop_reason']=reason;summary['budget']=ledger.audit()
    parent.write_json(out/'summary.json',summary)
    replay=render(manifest,records,out/'cases.html');parent.write_json(out/'replay.json',replay)
    ledger.close(manifest['attempt'],summary['valid']==manifest['max_calls'])
    if report is not None:
        try:
            for file in out.iterdir():report.artifact(str(file),name=file.name)
            success=summary['qualified'] if manifest['attempt']==QUAL else summary['valid']==manifest['max_calls']
            if success:report.done(message='D1 stage complete; consult saved analysis; no other stage automatically launched',valid=summary['valid'],correct=summary['correct'])
            else:report.fail(message='D1 stopped or qualification failed; all assignments retained',valid=summary['valid'],correct=summary['correct'])
        except Exception as exc:parent.write_json(out/'reporting-failure.json',{'reason':type(exc).__name__})
    return summary


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,required=True);parser.add_argument('--attempt',choices=(QUAL,MAIN),required=True)
    parser.add_argument('--preflight-only',action='store_true');parser.add_argument('--out',type=Path);parser.add_argument('--credential',type=Path)
    args=parser.parse_args()
    try:
        config=json.loads(args.config.read_text());manifest=make_manifest(args.attempt)
        if args.preflight_only:print(json.dumps(preflight(config,manifest),indent=2))
        else:
            require(args.out is not None and args.credential is not None,'output_and_credential_required')
            result=run(config,manifest,args.out,args.credential)
            print(json.dumps({k:v for k,v in result.items() if k!='cells'},indent=2))
    except Exception as exc:
        print('D1 refused: '+type(exc).__name__);raise SystemExit(1)

"""Q-A7 operator admission. No provisioning, credential lookup or secret logging.

Run on an admitted worker through orbital-one or the scoped Q-A7 owner-direct path. Receipt fields
are private operator attestations; they are not an independent fleet audit.
"""
import argparse,hashlib,json,os,sqlite3,subprocess,time
from pathlib import Path
from run_qualification import assignments_for,preflight

def admission_errors(a,revision,now):
    errors=[]
    for key in ('exclusive_claim_verified','approved_account_verified','sole_ledger_writer_verified','prior_worker_stopped','prior_artifacts_verified','dedicated_credential_provenance_verified'):
        if a.get(key) is not True:errors.append(key)
    if a.get('source_commit')!=revision:errors.append('source_commit')
    if a.get('attempt_id')!='q-a7':errors.append('attempt_id')
    if a.get('dispatch_origin')=='owner-direct-q-a7':
        if a.get('queue_issue')!=294:errors.append('direct_queue_scope')
        if a.get('central_queue_fenced') is not True:errors.append('central_queue_fenced')
        if a.get('queue_state')!='CLOSED':errors.append('queue_state')
        if a.get('owner_decision_reference')!='https://github.com/dmarzzz/swarm-labs-agentops/issues/294#issuecomment-5982187383':errors.append('owner_decision_reference')
    elif a.get('dispatch_origin')!='orbital-one':errors.append('dispatch_origin')
    if a.get('credential_alias') not in ('swarm-lab-anthropic/vishesh','local-openrouter-relay'):errors.append('credential_alias')
    if type(a.get('queue_issue')) is not int or a['queue_issue']<=0:errors.append('queue_issue')
    if not a.get('claim_id'):errors.append('claim_id')
    if not now-300<=a.get('verified_epoch',0)<=now:errors.append('stale_admission')
    if a.get('claim_expiry_epoch',0)<now+7500:errors.append('claim_expiry')
    return errors

def main():
    p=argparse.ArgumentParser();p.add_argument('--admission',type=Path,required=True);p.add_argument('--ledger',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--public-receipt',type=Path,required=True);p.add_argument('--run',action='store_true');a=p.parse_args()
    src=Path(__file__).parent;repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip());rev=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    receipt=json.loads(a.admission.read_text());errors=admission_errors(receipt,rev,time.time())
    if errors:raise ValueError('admission:'+','.join(errors))
    if not a.ledger.is_file():raise ValueError('original_ledger_required')
    if str(a.ledger.resolve())!=receipt.get('canonical_ledger_path'):raise ValueError('canonical_ledger_mismatch')
    with sqlite3.connect('file:'+str(a.ledger.resolve())+'?mode=ro',uri=True) as db:
        count,held,actual=db.execute('SELECT COUNT(*),SUM(held),SUM(actual) FROM calls').fetchone()
        prior=db.execute('SELECT COUNT(*) FROM calls WHERE episode LIKE ?',('q-a7/%',)).fetchone()[0]
    if prior or a.output.exists():raise ValueError('attempt_already_present')
    with sqlite3.connect('file:'+str(a.ledger.resolve())+'?mode=ro',uri=True) as db:
        original=db.execute("SELECT COUNT(*),SUM(held),SUM(actual) FROM calls WHERE episode NOT LIKE 'outage-o1/%'").fetchone()
    if original!=(631,2031320,1810840):raise ValueError('historical_ledger_changed')
    if receipt.get('reconciled_ledger_sha256')!=hashlib.sha256(a.ledger.read_bytes()).hexdigest() or receipt.get('reconciled_ledger_totals')!=[count,held,actual]:raise ValueError('prior_ledger_changed_reconcile_first')
    if receipt.get('o1_operationally_healthy') is not True:raise ValueError('o1_sequence_held')
    cfg=json.loads((src.parent/'input-binding-config.json').read_text())
    cfg.update(status='ready',exclusive_machine_claim=receipt['claim_id'],claim_expiry_epoch=receipt['claim_expiry_epoch'],public_plan_receipt=str(a.public_receipt.resolve()),queue_admission=str(a.admission.resolve()))
    if preflight(cfg,repo)!=rev:raise ValueError('source_mismatch')
    if not a.run:
        print(json.dumps({'admitted_check_only':True,'assigned':len(assignments_for(cfg)),'calls':0,'prior_exposure_microdollars':held}));return 0
    if receipt.get('credential_alias')!='local-openrouter-relay' or os.environ.get('SWARM_LOCAL_RELAY_URL')!='http://127.0.0.1:6197/invoke':raise ValueError('local_relay_missing')
    if any(os.environ.get(k) for k in ('ANTHROPIC_API_KEY','OPENROUTER_API_KEY','SWARM_MODEL_API_KEY')):raise ValueError('unrelated_credential_environment')
    config_path=a.output.parent/'q-a7-runtime.json'
    with config_path.open('x') as f:json.dump(cfg,f,indent=2)
    native=subprocess.run(['python3',str(src/'run_qualification.py'),'--config',str(config_path),'--budget-ledger',str(a.ledger),'--output',str(a.output)],check=False)
    from finalize_native import import_evidence
    imported=import_evidence(repo,a.output,'q-a7')
    final=subprocess.run(['python3',str(repo/'scripts/experiment.py'),'finalize','optimal-swarm-size','--attempt','q-a7','--results',imported,'--outcome','completed' if native.returncode==0 else 'failed'],cwd=repo,check=False)
    return native.returncode or final.returncode
if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as e:
        print(json.dumps({'admission_failed':str(e) if isinstance(e,ValueError) else type(e).__name__}));raise SystemExit(2)

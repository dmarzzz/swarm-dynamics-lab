"""O2-only launch contract. No provisioning, credential discovery or retries."""
import argparse,hashlib,json,os,sqlite3,subprocess,sys,threading,time
from pathlib import Path
from engine import execute
from world import make_case,digest,ARMS
from native import Native
from replay_outage import render
from budget import Budget
from reporting import Reporter

HERE=Path(__file__).resolve().parent
EXPERIMENT='optimal-swarm-size-outage-o2'
FLAGS=('exclusive_claim_verified','approved_account_verified','sole_ledger_writer_verified','prior_worker_stopped',
    'prior_artifacts_verified','dedicated_credential_provenance_verified','central_queue_fenced','offline_validation_passed','incremental_infrastructure_zero')

def assignments():
    rows=[dict(stage='qualification',root=0,changing=True,replica=11,arm='fixed',n=4,ownership=owned,service_count=4,label=label) for owned,label in [(False,'legacy4'),(True,'owned4')]]
    arms=[('single',1,False,'single'),('fixed',4,True,'owned4'),('fixed',8,True,'owned8'),('scheduled',1,False,'scheduled')]
    for changing,order in [(False,arms),(True,list(reversed(arms)))]:
        rows.extend(dict(stage='demonstration',root=0,changing=changing,replica=21,arm=arm,n=n,ownership=owned,service_count=8,label=label) for arm,n,owned,label in order)
    return [dict(r,id=f"outage-o2/{r['stage']}/0/{int(r['changing'])}/{r['label']}",width=8) for r in rows]

def admission_errors(a,revision,now):
    errors=[k for k in FLAGS if a.get(k) is not True]
    if a.get('source_commit')!=revision:errors.append('source_mismatch')
    if a.get('attempt_id')!='outage-o2':errors.append('attempt_mismatch')
    if a.get('credential_alias')!='local-openrouter-relay':errors.append('credential_alias')
    if not a.get('claim_id'):errors.append('claim_missing')
    if not now-300<=a.get('verified_epoch',0)<=now:errors.append('admission_stale')
    if a.get('claim_expiry_epoch',0)<now+7500:errors.append('claim_too_short')
    if a.get('dispatch_origin')!='owner-directed-ownership-size-diagnostic':errors.append('owner_scope')
    return errors

def preflight(a):
    repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=HERE,text=True).strip())
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
    if subprocess.check_output(['git','status','--porcelain'],cwd=repo,text=True).strip():raise ValueError('dirty_runtime')
    receipt=json.loads(a.admission.read_text());errors=admission_errors(receipt,revision,time.time())
    if errors:raise ValueError('admission:'+','.join(errors))
    if not a.ledger.is_file() or str(a.ledger.resolve())!=receipt.get('canonical_ledger_path'):raise ValueError('original_ledger_required')
    with sqlite3.connect('file:'+str(a.ledger.resolve())+'?mode=ro',uri=True) as db:
        stats=db.execute('SELECT COUNT(*),SUM(held),SUM(actual) FROM calls').fetchone()
        if stats!=(915,2903680,2603778):raise ValueError('prior_ledger_changed_reconcile_first')
        if db.execute('SELECT cap FROM settings').fetchall()!=[(20000000,)]:raise ValueError('original_cap_mismatch')
        if db.execute('SELECT 1 FROM attempts WHERE id=?',('outage-o2',)).fetchone():raise ValueError('attempt_already_present')
    if a.output.exists():raise ValueError('output_already_present')
    sys.path.append(str(repo/'researchers/vishesh/notes/experiment-documentation'))
    from public_plan import check
    public=check(EXPERIMENT,'O2 explicit ownership repair qualification then conditional single/four/eight-context outage comparison at equal tool capacity; recovery and cost, authored development worlds, no optimal-N inference.')
    expected=f'https://github.com/dmarzzz/swarm-lab/blob/{revision}/researchers/vishesh/notes/optimal-swarm-size/outage-prototype/O2-PLAN.md'
    if public['url']!=expected or public['plan_sha256']!=hashlib.sha256((HERE.parent/'O2-PLAN.md').read_bytes()).hexdigest():raise ValueError('plan_source_mismatch')
    return repo,revision,receipt,public

def main():
    p=argparse.ArgumentParser();p.add_argument('--admission',type=Path,required=True);p.add_argument('--ledger',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--run',action='store_true');a=p.parse_args()
    repo,revision,admission,public=preflight(a)
    if not a.run:print(json.dumps({'admitted_check_only':True,'planned':10,'calls':0}));return 0
    if os.environ.get('SWARM_LOCAL_RELAY_URL')!='http://127.0.0.1:6197/invoke':raise ValueError('local_relay_missing')
    if any(os.environ.get(k) for k in ('ANTHROPIC_API_KEY','OPENROUTER_API_KEY','SWARM_MODEL_API_KEY')):raise ValueError('unrelated_credential_environment')
    a.output.mkdir();(a.output/'public-plan.json').write_text(json.dumps(public,indent=2))
    rows=assignments();(a.output/'manifest.json').write_text(json.dumps(rows,indent=2))
    bank=Budget(a.ledger,20000000,'outage-o2',11000000);records=[];stop=threading.Event();reason=None
    def save():
        summary={'attempt_id':'outage-o2','source_commit':revision,'planned':len(rows),'started':len(records),'unstarted':len(rows)-len(records),'stop_reason':reason,'records':records,
            'exposure_microdollars':sum(bank.exposure(row['id']) for row in rows)}
        (a.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    save()
    for index,row in enumerate(rows):
        if index==2 and (not records[1]['evaluation'].get('success',False) or records[1].get('ownership_violations',0) or records[1].get('duplicate_patch_targets',0)):
            reason='qualification_not_passed';break
        target=a.output/str(index).zfill(2);target.mkdir();(target/'assignment.json').write_text(json.dumps(row,indent=2))
        tldr=f"TLDR: O2 {row['stage']}, {row['label']}, {row['service_count']} services, mechanism {row['root']}, {'changing' if row['changing'] else 'stable'} world. Diagnose and repair safely over eight ticks; compare final recovery and cost. Authored development fixture, not population or optimal-N evidence."
        journal_lock=threading.Lock()
        def journal(event):
            with journal_lock:
                with (target/'trace.jsonl').open('a') as f:f.write(json.dumps(event)+'\n')
        try:reporter=Reporter(EXPERIMENT,row,tldr)
        except Exception:
            reason='public_run_preflight_failed';break
        journal({'kind':'started','assignment':row,'source_commit':revision,'tldr':tldr})
        case=make_case(row['root'],row['changing'],row['replica'],row['service_count'])
        result=execute(case,row['arm'],Native(bank,row['id'],journal,admission['claim_expiry_epoch'],stop,max_tokens=1024,max_bytes=24000,quote=38632,episode_cap=3000000),journal,team_size=row['n'],ownership=row['ownership'])
        result.update(label=row['label'],id=row['id'],stage=row['stage'],source_commit=revision,operational_success=result['evaluation'].get('success',False),exposure_microdollars=bank.exposure(row['id']),assignment=row)
        (target/'outcome.json').write_text(json.dumps(result,indent=2)+'\n');render(result,target/'replay.html')
        publication=reporter.finish(target,result)
        records.append({k:v for k,v in result.items() if k!='events'})
        if result['failure']:reason=result['failure']
        elif not publication['complete']:reason='publication_failed'
        save()
        if reason:break
    save()
    print(json.dumps({'started':len(records),'stop_reason':reason,'exposure_microdollars':sum(bank.exposure(row['id']) for row in rows)}))
    return 2 if reason else 0

if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as exc:
        # Arbitrary transport/config exception text is never printed.
        print(json.dumps({'launch_failed':getattr(exc,'code',None) or type(exc).__name__}));raise SystemExit(2)

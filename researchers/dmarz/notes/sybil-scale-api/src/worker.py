"""Finite concurrent batch; durable assignments, no retries, stop new dispatch on failure."""
import argparse,gzip,json,os,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,wait,FIRST_COMPLETED
import provider,study,render,analyze

def write_json(path,value):
    with path.open('x') as f:json.dump(value,f,indent=2);f.flush();os.fsync(f.fileno())
def upload(run,path):
    receipt=run.artifact(path,path.name)
    if not receipt or receipt.get('spooled'):raise RuntimeError('artifact_not_durably_acknowledged')
def execute(p,out,run=None,backend=None):
    assert p['source_hash']==study.source_hash(),'runtime_source_mismatch'
    assert p['backend']==('scripted' if p['stage']=='S0' else 'anthropic')
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    assigned=study.assignments(p['stage'],out);total=len(assigned)
    with gzip.open(out/'assignments.jsonl.gz','wt') as f:
        for a in assigned:f.write(json.dumps(a,sort_keys=True)+'\n')
    ledger=None
    if p['backend']=='anthropic':
        path=os.environ.get('SYBIL_API_BUDGET_LEDGER');assert path,'persistent_budget_required'
        ledger=provider.Ledger(path);backend=backend or provider.Anthropic(ledger)
    initial=ledger.transact() if ledger else {};start=time.monotonic();rows=[];stopped=False;reporting_errors=[]
    render.frame([],total,p['stage'],accounting=initial).save(out/'initial_frame.png')
    if run:upload(run,out/'initial_frame.png')
    def solve(a):
        r={k:a[k] for k in ('id','task','n','arm','checks','visibility','attacker_pass','kind','packet_hash')}
        r.update(run=run.id if run else out.name,stage=p['stage'],backend=p['backend'],code=p['code'],source_hash=p['source_hash'],status='failed')
        try:
            if time.monotonic()-start>study.design()['budget']['stage_timeout_seconds']:raise provider.CallFailure('stage_deadline')
            if p['backend']=='scripted':answer=study.scripted(a['packet']);accounting={'attempted':False,'actual_usd':0,'reserved_usd':0}
            else:answer,accounting=backend.call(a['packet'],p['batch']+':'+a['id'])
            r.update(answer=answer,accounting=accounting,evaluation=study.evaluate(a,answer),scripted_evaluation=study.evaluate(a,study.scripted(a['packet'])),status='completed')
        except provider.CallFailure as exc:r.update(error=exc.category,accounting=exc.accounting)
        except Exception as exc:r.update(error='internal_'+type(exc).__name__)
        return r
    with (out/'episodes.jsonl').open('x') as log:
        def record(r):
            r.update(completion_index=len(rows)+1,elapsed_seconds=time.monotonic()-start,study_accounting=ledger.transact() if ledger else {})
            log.write(json.dumps(r,sort_keys=True)+'\n');log.flush();os.fsync(log.fileno());rows.append(r)
        index=0;last_render=0
        with ThreadPoolExecutor(max_workers=1 if p['backend']=='scripted' else study.design()['budget']['workers']) as pool:
            pending={}
            def fill():
                nonlocal index
                while not stopped and index<total and len(pending)<study.design()['budget']['workers']:
                    a=assigned[index];pending[pool.submit(solve,a)]=a;index+=1
            fill()
            while pending:
                done,_=wait(pending,timeout=5,return_when=FIRST_COMPLETED)
                if not done:
                    if run:run.progress(len(rows),total,episodes=len(rows),invalid=int(stopped))
                    continue
                for f in done:
                    pending.pop(f);r=f.result();record(r)
                    if r['status']!='completed':stopped=True
                if run:
                    run.progress(len(rows),total,episodes=len(rows),invalid=sum(r['status']=='failed' for r in rows),
                        model_calls=sum(r.get('accounting',{}).get('attempted',False) for r in rows),
                        cost_usd=sum(r.get('accounting',{}).get('actual_usd',0) for r in rows))
                    if time.monotonic()-last_render>20 or stopped:
                        try:
                            render.frame(rows,total,p['stage'],time.monotonic()-start,rows[-1]['study_accounting']).save(out/'progress.png');upload(run,out/'progress.png')
                        except Exception as exc:reporting_errors.append(type(exc).__name__)
                        last_render=time.monotonic()
                fill()
        for a in assigned[index:]:
            r={k:a[k] for k in ('id','task','n','arm','checks','visibility','attacker_pass','kind','packet_hash')}
            r.update(status='not_started',stage=p['stage'],run=run.id if run else out.name,source_hash=p['source_hash'],code=p['code']);record(r)
    with gzip.open(out/'episodes.jsonl.gz','wb') as f:f.write((out/'episodes.jsonl').read_bytes())
    q=study.qualification(rows) if p['stage'] in ('S0','Q0') else None
    good=[r for r in rows if r['status']=='completed']
    summary={'params':p,'planned':total,'started':sum(r['status']!='not_started' for r in rows),'terminal':len(rows),'graded':len(good),'analyzed':len(good),
        'invalid':total-len(good),'not_started':sum(r['status']=='not_started' for r in rows),
        'model_calls':sum(r.get('accounting',{}).get('attempted',False) for r in rows),
        'cost_usd':sum(r.get('accounting',{}).get('actual_usd',0) for r in rows),
        'input_tokens':sum(r.get('accounting',{}).get('input_tokens',0) for r in rows),'output_tokens':sum(r.get('accounting',{}).get('output_tokens',0) for r in rows),
        'elapsed_seconds':time.monotonic()-start,'qualification':q,'study_accounting':ledger.transact() if ledger else {},'initial_study_accounting':initial,
        'reporting_errors':reporting_errors,'visualization':{'mapping':'v1','frames':render.replay(rows,out,p['stage'],total,initial)}}
    write_json(out/'summary.json',summary);write_json(out/'analysis.json',analyze.analyze(rows))
    if run:
        for name in ('final_frame.png','replay.gif','badges_hidden.png','assignments.jsonl.gz','episodes.jsonl.gz','worlds.jsonl.gz','summary.json','analysis.json','initial_frame.png'):upload(run,out/name)
    if summary['invalid'] or (q and not q['passed']):raise RuntimeError('qualification_or_execution_failed_preserved')
    if run:run.done(message=f'{p["stage"]}: {len(good)}/{total} valid, all four sizes; see scaling replay',episodes=total,invalid=0,model_calls=summary['model_calls'],cost_usd=summary['cost_usd'],qualification_passed=int(bool(q and q['passed'])),
        **({'rare_accuracy':sum(r['evaluation']['rare_accuracy'] for r in good)/len(good)} if p['stage']=='S1' else {}))
    return summary

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--hub',action='store_true');ap.add_argument('--stage',choices=['S0']);ap.add_argument('--attempt');a=ap.parse_args()
    if a.hub:
        import swarm_report as sr
        run=sr.next_run('sybil-scale-api')
        if run is None:return
        if run.attempt!=1:raise RuntimeError('automatic_reexecution_forbidden')
        with run:execute(run.params,study.ROOT/'results'/f'{run.id.replace("/","__")}-attempt-{run.attempt}',run)
    else:
        if a.stage!='S0' or not a.attempt or not a.attempt.replace('-','').isalnum():raise SystemExit('Offline S0 requires a fresh attempt name')
        print(json.dumps(execute(study.params('S0'),study.ROOT/'results'/a.attempt)))
if __name__=='__main__':main()

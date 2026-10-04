"""One finite batch; durable raw denominator and stop on the first failed call."""
import argparse
import json
import os
from pathlib import Path
import time
import provider
import render
import study


def write_json(path, value):
    with path.open('x') as f:
        json.dump(value,f,indent=2); f.flush(); os.fsync(f.fileno())


def upload(run, path):
    receipt=run.artifact(path,path.name)
    if not receipt or receipt.get('spooled'):
        raise RuntimeError('artifact_not_durably_acknowledged')


def execute(p, out, run=None, backend=None):
    if p['source_hash']!=study.source_hash(): raise ValueError('runtime_source_mismatch')
    if p['backend'] != ('scripted' if p['stage']=='S0' else 'anthropic'):
        raise ValueError('stage_backend_mismatch')
    out=Path(out); out.mkdir(parents=True,exist_ok=False)
    assigned=study.assignments(p['stage']); total=len(assigned)
    write_json(out/'assignment.json',{'params':p,'rows':assigned})
    ledger=None
    if p['backend']=='anthropic':
        path=os.environ.get('SYBIL_API_BUDGET_LEDGER')
        if not path: raise ValueError('persistent_budget_path_required')
        ledger=provider.Ledger(path)
        backend=backend or provider.Anthropic(ledger)
    start=time.monotonic(); rows=[]; stopped=False
    render.frame([],total,p['stage']).save(out/'initial_frame.png')
    if run: upload(run,out/'initial_frame.png')
    with (out/'episodes.jsonl').open('x') as log:
        for index,a in enumerate(assigned):
            r={k:a[k] for k in ('id','task','arm','visibility','attacker_pass','kind','packet_hash')}
            r.update(run=run.id if run else out.name,stage=p['stage'],backend=p['backend'],code=p['code'],source_hash=p['source_hash'])
            r['status']='not_started' if stopped else 'failed'
            if not stopped:
                try:
                    if time.monotonic()-start>study.design()['budget']['stage_timeout_seconds']:
                        raise provider.CallFailure('stage_deadline')
                    if p['backend']=='scripted':
                        answer=study.scripted(a['packet']); accounting={'attempted':False,'actual_usd':0,'reserved_usd':0}
                    else:
                        answer,accounting=backend.call(a['packet'],p['batch']+':'+a['id'])
                    r.update(answer=answer,accounting=accounting,
                             evaluation=study.evaluate(a,answer),
                             scripted_evaluation=study.evaluate(a,study.scripted(a['packet'])),status='completed')
                except provider.CallFailure as exc:
                    r.update(error=exc.category, accounting=exc.accounting); stopped=True
                except Exception as exc:
                    r.update(error='internal_'+type(exc).__name__); stopped=True
            r.update(completion_index=index+1,elapsed_seconds=time.monotonic()-start,
                     study_accounting=ledger.transact() if ledger else {})
            log.write(json.dumps(r,sort_keys=True)+'\n'); log.flush(); os.fsync(log.fileno()); rows.append(r)
            if run and r['status']!='not_started':
                run.progress(index+1,total,episodes=index+1,invalid=int(stopped),
                             model_calls=r['study_accounting'].get('attempted_calls',0),
                             cost_usd=r['study_accounting'].get('actual_usd',0))
                if (index+1)%4==0 or stopped:
                    render.frame(rows,total,p['stage'],r['elapsed_seconds'],r['study_accounting']).save(out/'progress.png')
                    upload(run,out/'progress.png')
    good=[r for r in rows if r['status']=='completed']
    q=study.qualification(rows) if p['stage'] in ('S0','Q0') else None
    summary={'params':p,'planned':total,'started':sum(r['status']!='not_started' for r in rows),
             'terminal':len(rows),'graded':len(good),'analyzed':len(good),
             'invalid':total-len(good),'not_started':sum(r['status']=='not_started' for r in rows),
             'model_calls':sum(r.get('accounting',{}).get('attempted',False) for r in rows),
             'cost_usd':sum(r.get('accounting',{}).get('actual_usd',0) for r in rows),
             'input_tokens':sum(r.get('accounting',{}).get('input_tokens',0) for r in rows),
             'output_tokens':sum(r.get('accounting',{}).get('output_tokens',0) for r in rows),
             'elapsed_seconds':time.monotonic()-start,'qualification':q,
             'study_accounting':ledger.transact() if ledger else {},
             'visualization':{'mapping':'v1','frames':render.replay(rows,out,p['stage'],total)}}
    write_json(out/'summary.json',summary)
    if run:
        for name in ('final_frame.png','replay.gif','assignment.json','episodes.jsonl','summary.json'):
            upload(run,out/name)
        if (out/'progress.png').exists(): upload(run,out/'progress.png')
        upload(run,out/'initial_frame.png')
    if summary['invalid'] or q and not q['passed']:
        raise RuntimeError('qualification_or_execution_failed_preserved')
    if run:
        pilot=[r for r in good if r['kind']=='pilot']
        run.done(message=f'{p["stage"]}: {len(good)}/{total} valid; model calls {summary["model_calls"]}; see all-policy replay',
                 episodes=total,invalid=0,model_calls=summary['model_calls'],cost_usd=summary['cost_usd'],
                 qualification_passed=int(bool(q and q['passed'])),
                 rare_accuracy=sum(r['evaluation']['rare_accuracy'] for r in pilot)/len(pilot) if pilot else 0,
                 task_accuracy=sum(r['evaluation']['task_accuracy'] for r in good)/len(good))
    return summary


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--hub',action='store_true'); ap.add_argument('--stage',choices=['S0']); ap.add_argument('--attempt')
    a=ap.parse_args()
    if a.hub:
        import swarm_report as sr
        run=sr.next_run('sybil-specialists-api')
        if run is None: return
        if run.attempt != 1: raise RuntimeError('automatic_reexecution_forbidden')
        with run:
            execute(run.params,study.ROOT/'results'/f'{run.id.replace("/","__")}-attempt-{run.attempt}',run)
    else:
        if a.stage!='S0' or not a.attempt or not a.attempt.replace('-','').isalnum():
            raise SystemExit('Offline S0 requires a new attempt name')
        print(json.dumps(execute(study.params('S0'),study.ROOT/'results'/a.attempt)))


if __name__=='__main__': main()

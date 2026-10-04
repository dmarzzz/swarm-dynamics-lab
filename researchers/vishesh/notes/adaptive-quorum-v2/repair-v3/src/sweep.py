import argparse
import collections
import hashlib
import itertools
import json
import signal
import subprocess
import time
from pathlib import Path
from runtime import Runtime
from adapter import Hybrid
from engine import episode,symbolic,ARMS
from render import animation,overview,frame


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--qualification',type=Path,required=True);ap.add_argument('--report',action='store_true');ap.add_argument('--resume',type=Path);ap.add_argument('--attempt',required=True);a=ap.parse_args()
    if not json.loads((a.qualification/'summary.json').read_text())['qualification_pass']:raise SystemExit('Qualification gate failed')
    a.out.mkdir(parents=True,exist_ok=False)
    def timeout(signum,frame):raise TimeoutError('run_wall_cap')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(2400)
    assignments=[dict(task=t,n=n,deadline=d,world=w,timing=tm,seed=1) for t,n,d,w,tm in itertools.product(range(8200,8212),(5,9),(3,6),('clean','copies','early-wrong','late-wrong'),('late','stalled'))]
    code=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    manifest={'stage':'S1-engineering','code':code,'assignments':len(assignments),'independent_task_clusters':12,'complete':False,'parent_attempt':'Q2-attempt-1','qualification_sha256':hashlib.sha256((a.qualification/'summary.json').read_bytes()).hexdigest(),'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')}}
    (a.out/'manifest.json').write_text(json.dumps(manifest,indent=2));(a.out/'assignments.json').write_text(json.dumps(assignments))
    hub=None
    if a.report:
        import swarm_report as sr
        hub=sr.start('adaptive-quorum-api-v2',run='adaptive-quorum-api-v2/repair-v3-S1-attempt-'+a.attempt,params={'stage':'S1-engineering','backend':'laya-hybrid','agents':'5,9','kind':'experiment','code':code})
        sr.report('progress','adaptive-quorum-api-v2',hub.id,url='https://github.com/dmarzzz/swarm-lab/tree/main/researchers/vishesh/notes/adaptive-quorum-v2/repair-v3',strict=True)
    start=time.monotonic();runtime=Runtime();model=Hybrid(runtime);records=[];symbolic_disagreements=0
    prior=[]
    if a.resume:
        import gzip
        parent=json.loads((a.resume/'manifest.json').read_text())
        for name in ('engine.py','adapter.py','runtime.py'):
            if parent['source_sha256'][name]!=manifest['source_sha256'][name]:raise ValueError('resume_actor_source_changed')
        prior=[json.loads(x) for x in (a.resume/'episodes.jsonl').read_text().splitlines()]
        for c,r in zip(assignments,prior):
            if any(r[k if k!='n' else 'agents']!=v for k,v in c.items()):raise ValueError('resume_assignment_mismatch')
        runtime.receipts=json.loads((a.resume/'receipts.json').read_text())
        if any(not r['valid'] for r in runtime.receipts):raise ValueError('resume_invalid_receipt')
        for i,r in enumerate(runtime.receipts):
            key=hashlib.sha256(json.dumps([r['state'],r['question']['instructions']]).encode()).hexdigest()
            model.cache[key]=(r['choice'],i)
        with gzip.open(a.resume/'invocations.json.gz','rt') as f:model.invocations=json.load(f)
        with gzip.open(a.resume/'guard-events.json.gz','rt') as f:model.guard_events=json.load(f)
        manifest.update(resumed_from=a.resume.name,resumed_blocks=len(prior),reused_physical_receipts=len(runtime.receipts))
        (a.out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    original=runtime.choose
    def bounded(*args,**kwargs):
        if len(runtime.receipts)>=500:raise RuntimeError('physical_call_cap')
        return original(*args,**kwargs)
    runtime.choose=bounded
    try:
        with (a.out/'episodes.jsonl').open('x') as stream:
            for i,c in enumerate(assignments):
                r=prior[i] if i<len(prior) else episode(**c,decide=model);records.append(r);stream.write(json.dumps(r)+'\n');stream.flush()
                reference=episode(**c,decide=lambda rows,context:symbolic(rows))
                symbolic_disagreements+=sum(r['outcomes'][arm]['choice']!=reference['outcomes'][arm]['choice'] for arm in ARMS)
                (a.out/'receipts.json').write_text(json.dumps(runtime.receipts))
                if hub:hub.progress(i+1,len(assignments),blocks_complete=i+1,physical_calls=len(runtime.receipts))
                if any(not x['valid'] for x in r['outcomes'].values()):raise RuntimeError('actor_fault_stop')
        summary={'assigned_blocks':len(assignments),'completed_blocks':len(records),'task_clusters':12,'physical_calls':len(runtime.receipts),'logical_predicates':len(model.invocations),'encoded_input_tokens':sum(x['encoded_tokens'] for x in runtime.receipts),'inference_wall_s':sum(x['wall_s'] for x in runtime.receipts),'elapsed_wall_s':time.monotonic()-start,'invalid_outcomes':sum(not o['valid'] for r in records for o in r['outcomes'].values()),'blocked_model_acceptances':sum(g['blocked'] for g in model.guard_events),'symbolic_policy_disagreements':symbolic_disagreements,
                 'arms':{arm:{'assigned':len(records),'correct':sum(r['outcomes'][arm]['evaluation']['correct'] for r in records),'violations':sum(r['outcomes'][arm]['evaluation']['constraint_violation'] for r in records),'abstentions':sum(r['outcomes'][arm]['evaluation']['abstention'] for r in records),'mean_loss':sum(r['outcomes'][arm]['evaluation']['loss'] for r in records)/len(records)} for arm in ARMS}}
        # Rendering is a separate phase after all scientific outcomes are durable.
        for r in records:
            if r['task']==8200 and r['agents']==9 and r['deadline']==6:
                name=f"replay-{r['world']}-{r['timing']}";animation(r,a.out/name)
                if hub:
                    hub.artifact(a.out/(name+'.png'),name+'.png');hub.artifact(a.out/(name+'.gif'),name+'.gif')
        (a.out/'summary.json').write_text(json.dumps(summary,indent=2));overview(records,summary,a.out/'final_frame.png')
        manifest.update(runtime.metadata,complete=True);(a.out/'manifest.json').write_text(json.dumps(manifest,indent=2))
        if hub:
            for name in ('final_frame.png','summary.json','manifest.json','assignments.json','receipts.json'):hub.artifact(a.out/name,name)
            save_audit(a.out,model)
            for name in ('episodes.jsonl.gz','invocations.json.gz','guard-events.json.gz'):hub.artifact(a.out/name,name)
            hub.done(message='Engineering sweep complete; see post-mortem for qualification and scientific limitations.',blocks_complete=len(records),physical_calls=len(runtime.receipts),invalid_outcomes=summary['invalid_outcomes'])
        print(json.dumps(summary))
    except Exception as exc:
        (a.out/'failure.json').write_text(json.dumps({'error':type(exc).__name__,'completed':len(records),'assigned':len(assignments)}))
        if hub:hub.fail(message='Antsy sweep stopped; preserved partial results require post-mortem.')
        raise
    finally:
        save_audit(a.out,model)
        (a.out/'receipts.json').write_text(json.dumps(runtime.receipts))


def save_audit(out,model):
    import gzip,shutil
    for name,data in [('invocations',model.invocations),('guard-events',model.guard_events)]:
        with gzip.open(out/(name+'.json.gz'),'wt') as f:json.dump(data,f)
    if (out/'episodes.jsonl').exists():
        with (out/'episodes.jsonl').open('rb') as src,gzip.open(out/'episodes.jsonl.gz','wb') as dest:shutil.copyfileobj(src,dest)


if __name__=='__main__':main()

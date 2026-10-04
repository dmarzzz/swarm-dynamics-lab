"""One finite process, durable records, no queue redelivery or model retries."""
import argparse
import hashlib
import json
import os
import time
from pathlib import Path
import yaml
import common
from analyze import summarize, qualify
from coordinator import prepare
from engine import task, run_episode
from provider import Anthropic, CallFailure, Ledger
from render import artifacts, frame


def append(path,value):
    with path.open('a') as f:
        f.write(json.dumps(value,sort_keys=True,allow_nan=False)+'\n'); f.flush(); os.fsync(f.fileno())


def execute(stage,attempt,qualification=None):
    import swarm_report as sr
    d=common.design(); out=prepare(stage,attempt,qualification)
    manifest=json.loads((out/'manifest.json').read_text())
    definition=yaml.safe_load((common.ROOT/'experiment.yaml').read_text()); exp=definition.pop('id')
    sr.register(exp,**definition)
    ledger=Ledger(common.ROOT/'accounting/study.jsonl')
    provider=Anthropic(ledger) if manifest['backend']=='anthropic' else None
    before=ledger.transact(); started=time.monotonic(); rows=[]; runs=[]
    grouped={}
    for a in manifest['assignments']: grouped.setdefault((a['task_id'],a['domain'],a['variant']),[]).append(a)
    for (tid,domain,variant),aa in grouped.items():
        spec=task(tid,domain,variant,d['cfg']['n']); bundle=[]
        bundle_before=ledger.transact()
        sub=out/f'{tid}-{domain}-{variant}'; sub.mkdir()
        with sr.start(exp,params=dict(stage=stage,domain=domain,variant=variant,task_id=tid,backend=manifest['backend'],attempt=attempt),run=f'{exp}/{attempt}-{tid}-{domain}-{variant}') as run:
            runs.append(run.id if hasattr(run,'id') else f'{exp}/{attempt}-{tid}-{domain}-{variant}')
            for a in aa:
                eid=f"{attempt}/{tid}/{domain}/{variant}/{a['arm']}"
                append(out/'dispatch.jsonl',dict(episode_id=eid,event='start',time=time.time()))
                def policy(packet,step):
                    if time.monotonic()-started>d['budget']['stage_timeout_seconds']: raise CallFailure('stage_time_limit')
                    return provider.call(packet,f'{eid}/{step}')
                def progress(trace):
                    append(out/'trace.jsonl',dict(episode_id=eid,**trace[-1]))
                    current=ledger.transact()
                    run.progress(len(bundle)+len(trace)/d['cfg']['max_steps'],len(aa),model_calls=current['attempted_calls']-bundle_before['attempted_calls'],api_cost_usd=current['actual_usd']-bundle_before['actual_usd'])
                # Record local scripted timeouts too; never silently omit an assignment.
                active_policy=policy if provider else None
                if time.monotonic()-started>d['budget']['stage_timeout_seconds']:
                    def timed_out(packet,step): raise CallFailure('stage_time_limit')
                    active_policy=timed_out
                r=run_episode(spec,a['seed'],a['arm'],policy=active_policy,max_steps=d['cfg']['max_steps'],on_step=progress)
                r.update(episode_id=eid,commit=manifest['commit'],hashes=manifest['hashes'],stage=stage,backend=manifest['backend'])
                append(out/'episodes.jsonl',r); append(out/'dispatch.jsonl',dict(episode_id=eid,event='terminal',valid=r['validity']['ok'],time=time.time()))
                rows.append(r); bundle.append(r)
                frame(bundle,spec,f'{stage} | {manifest["backend"]} | {tid} {domain} {variant}').save(sub/'live.png')
                run.artifact(sub/'live.png','live.png')
                s=summarize(bundle,stage)
                run.progress(len(bundle),len(aa),episodes=len(bundle),safe_completion_rate=s['safe_completion_rate'],violation_rate=s['violation_rate'],invalid=s['invalid'])
            artifacts(sorted(bundle,key=lambda r:d['arms'].index(r['arm'])),spec,f'{stage} | {manifest["backend"]} | {tid} {domain} {variant}',sub)
            common.dump(sub/'episodes.json',bundle)
            for name in ('episodes.json','final_frame.png','replay.gif'): run.artifact(sub/name,name)
            bundle_after=ledger.transact()
            run.done(episodes=len(bundle),safe_completion_rate=s['safe_completion_rate'],violation_rate=s['violation_rate'],invalid=s['invalid'],model_calls=bundle_after['attempted_calls']-bundle_before['attempted_calls'],api_cost_usd=bundle_after['actual_usd']-bundle_before['actual_usd'],message='Execution terminal; consult stage summary for qualification.')
    summary=summarize(rows,stage,len(manifest['assignments']))
    after=ledger.transact()
    summary.update(qualification_pass=qualify(summary,d['qualification']) if stage in ('S0','Q0') else None,
                   accounting={k:after[k]-before[k] for k in after},study_accounting=after,
                   elapsed_seconds=time.monotonic()-started,run_ids=runs)
    common.dump(out/'summary.json',summary)
    filehash={str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob('*')) if p.is_file()}
    common.dump(out/'artifact-hashes.json',filehash)
    with sr.start(exp,params=dict(stage=stage,kind='analysis',attempt=attempt),run=f'{exp}/{attempt}-analysis') as run:
        for name in ('summary.json','manifest.json','episodes.jsonl','dispatch.jsonl','trace.jsonl','artifact-hashes.json'):
            if (out/name).exists(): run.artifact(out/name,name)
        if ledger.path.exists(): run.artifact(ledger.path,'study-accounting.jsonl')
        run.artifact(sub/'final_frame.png','last_bundle.png')
        run.done(episodes=len(rows),safe_completion_rate=summary['safe_completion_rate'],violation_rate=summary['violation_rate'],invalid=summary['invalid'],model_calls=summary['accounting']['attempted_calls'],api_cost_usd=summary['accounting']['actual_usd'],message=f"{stage} all assigned reconciled. Qualification: {summary['qualification_pass']}.")
    print(json.dumps({k:v for k,v in summary.items() if k not in ('cells','run_ids')},sort_keys=True),flush=True)
    return summary


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage');p.add_argument('attempt');p.add_argument('--qualification');a=p.parse_args()
    execute(a.stage,a.attempt,a.qualification)

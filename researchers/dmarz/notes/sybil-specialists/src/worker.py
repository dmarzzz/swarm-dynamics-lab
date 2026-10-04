"""Bounded local or hub worker, scripted only. Failures remain in the denominator."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import os
import subprocess
import time
from collections import defaultdict
from pathlib import Path
import yaml
import sim
import render

ROOT=Path(__file__).resolve().parent.parent


def load(): return yaml.safe_load((ROOT/'design.yaml').read_text())
def code(): return subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
def design_hash(): return hashlib.sha256((ROOT/'design.yaml').read_bytes()).hexdigest()


def params(stage):
    d=load()
    if stage not in ('S0','S1'): raise ValueError('S2 is disabled pending formal review')
    st=d['stages'][stage]
    return [dict(stage=stage,backend='scripted',bridges=b,attacker_pass=p,verification_budget=k,clean=c,
                 tasks=st['tasks'],code=code(),design_hash=design_hash())
            for b,p,k,c in itertools.product(st['bridges'],st['attacker_pass'],st['verification_budget'],st['clean'])]


def summarize(records):
    by=defaultdict(list)
    for r in records: by[r['arm']].append(r)
    result={}
    for arm,rows in by.items():
        good=[r for r in rows if r['validity']['ok']]
        metrics={}
        for k in ('rare_accuracy','task_accuracy','honest_rejection','specialist_rejection','malicious_admission','bad_seat_share','verification_calls'):
            vals=[r['evaluation'][k] for r in good if r['evaluation'][k] is not None]
            metrics[k]=sum(vals)/len(vals) if vals else None
        result[arm]={'assigned':len(rows),'valid':len(good),'invalid':len(rows)-len(good),'metrics':metrics}
    return result


def execute(p,out,run=None):
    if p['backend']!='scripted': raise ValueError('This worker cannot call a model provider')
    if p['code']!=code() or p['design_hash']!=design_hash(): raise ValueError('Source/configuration mismatch')
    d=load(); out=Path(out); out.mkdir(parents=True,exist_ok=False)
    total=len(p['tasks'])*len(d['arms']); records=[]; start=time.time(); visual=None
    (out/'assignment.json').write_text(json.dumps(p,indent=2))
    with (out/'episodes.jsonl').open('x') as log:
        for task in p['tasks']:
            world=sim.make_world(task,p['bridges'],p['attacker_pass'],p['clean'],d['cfg'])
            try:
                rows=sim.run_episode(world,p['verification_budget'],d['arms'],d['cfg'])
            except Exception as exc:
                rows=[{'task':task,'cell':{k:p[k] for k in ['bridges','attacker_pass','clean','verification_budget']},
                       'arm':arm,'validity':{'ok':False,'error':type(exc).__name__},'backend':'scripted'} for arm in d['arms']]
            for r in rows:
                r.update({'code':p['code'],'design_hash':p['design_hash'],'stage':p['stage'],
                          'run':run.id if run else out.name})
                log.write(json.dumps(r)+'\n'); log.flush(); records.append(r)
            if visual is None and all(r['validity']['ok'] for r in rows):
                visual=(world,rows)
                # Predeclared first world, not selected for a favorable effect.
                (out/'replay_source.json').write_text(json.dumps({'world':world,'records':rows}))
                render.frame(world,rows,0,p['stage']).save(out/'initial_frame.png')
                if run: require_upload(run.artifact(out/'initial_frame.png','initial_frame.png'))
            if run:
                m=summarize(records)['coverage']['metrics']
                run.progress(len(records),total,**{k:v for k,v in m.items() if v is not None})
    stats=summarize(records); invalid=sum(v['invalid'] for v in stats.values())
    manifest={'params':p,'planned':total,'started':len(records),'terminal':len(records),'graded':len(records)-invalid,
              'invalid':invalid,'backend':'scripted','model_calls':0,'api_spend_usd':0,'elapsed_seconds':time.time()-start,
              'arms':stats,'visualization':{'mapping':'v1','world':p['tasks'][0],'frames':0}}
    if visual:
        manifest['visualization']['frames']=render.replay(*visual,out,p['stage'])
    (out/'summary.json').write_text(json.dumps(manifest,indent=2))
    if run:
        for name in ['final_frame.png','replay.gif','episodes.jsonl','replay_source.json','summary.json','assignment.json']:
            if (out/name).exists(): require_upload(run.artifact(out/name,name))
        m=stats['coverage']['metrics']
        if invalid: raise RuntimeError(f'{invalid} invalid episodes retained')
        run.done(message=f'Scripted {p["stage"]}: {total} arm episodes; zero API calls; replay shows first assigned world',
                 episodes=len(records),invalid=invalid,**{k:v for k,v in m.items() if v is not None})
    if invalid: raise RuntimeError(f'{invalid} invalid episodes retained')
    return manifest


def require_upload(receipt):
    if not receipt or receipt.get('spooled'): raise RuntimeError('Artifact not durably acknowledged; keep outputs and repair upload')


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--hub',action='store_true')
    ap.add_argument('--stage',choices=['S0','S1']); ap.add_argument('--attempt')
    a=ap.parse_args()
    if a.hub:
        if not os.environ.get('SWARM_SOURCE'): raise SystemExit('SWARM_SOURCE required')
        import swarm_report as sr
        def work(run): execute(run.params,ROOT/'results'/f'{run.id.replace("/","__")}-attempt-{run.attempt}',run)
        print('Completed runs:',sr.work('sybil-specialists',work,stop_when_empty=True))
    else:
        if not a.stage or not a.attempt or not a.attempt.replace('-','').isalnum(): raise SystemExit('Set --stage and a fresh alphanumeric --attempt')
        root=ROOT/'results'/a.attempt; root.mkdir(exist_ok=False)
        summaries=[]
        for i,p in enumerate(params(a.stage)): summaries.append(execute(p,root/f'cell-{i:02d}'))
        report={'stage':a.stage,'cells':len(summaries),'episodes':sum(s['planned'] for s in summaries),
                'invalid':sum(s['invalid'] for s in summaries),'model_calls':0,'api_spend_usd':0,
                'source':code(),'design_hash':design_hash()}
        (root/'qualification.json').write_text(json.dumps(report,indent=2)); print(json.dumps(report))

if __name__=='__main__': main()

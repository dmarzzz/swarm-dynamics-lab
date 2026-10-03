"""Bounded local / hub worker adapted from templates/experiment-worker/src/worker.py."""
from __future__ import annotations
import argparse
import json
import os
import platform
from pathlib import Path
import subprocess
import time
from analyze import summarize,contrast
from artifacts import publish_artifacts
from providers import Scripted,HTTP
from sim import arms_for,run_episode
from tasks import digest

ROOT=Path(__file__).resolve().parent.parent
EXP='discussion-dose'

def code_hash():
    return digest({p.name:p.read_text() for p in sorted((ROOT/'src').glob('*.py'))})

def execute_bundle(params,out,provider,progress=lambda *a:None):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    arms=arms_for(params['rounds'],params.get('private_control',False))
    tasks=params['tasks'];seeds=params['seeds'];cfg={'n_agents':params['n_agents']}
    manifest={'params':params,'arms':arms,'code_sha256':code_hash(),'python':platform.python_version(),
              'platform':platform.system(),'provider':provider.name,'scientific':provider.scientific,
              'model_limits':{k:getattr(provider,k) for k in ('max_calls','max_output_tokens','max_input_bytes','timeout','max_cost_usd','input_rate','output_rate') if hasattr(provider,k)},
              'git_commit':subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True).stdout.strip(),
              'planned_episodes':[{'task_id':t,'seed':s,'arm':a} for t in tasks for s in seeds for a in arms]}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    rows=[];start=time.monotonic()
    # Write plan first; a hard worker death leaves visible missing outcomes for reconciliation.
    with (out/'episodes.jsonl').open('x') as f, (out/'events.jsonl').open('x') as journal:
        def emit(label,event):
            journal.write(json.dumps({'stream':label,'event':event},sort_keys=True)+'\n');journal.flush();os.fsync(journal.fileno())
        for t in tasks:
            for s in seeds:
                for row in run_episode(t,s,'controlled-tool-exposure',1,arms,cfg,provider,event_sink=emit):
                    row['provenance']={'code_sha256':manifest['code_sha256'],'git_commit':manifest['git_commit'],'stage':params['stage']}
                    f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno());rows.append(row)
                progress(len(rows),len(manifest['planned_episodes']))
    summary={'scientific':provider.scientific,'provider':provider.name,'episodes':len(rows),
             'seconds':round(time.monotonic()-start,3),'cells':summarize(rows),
             'primary_candidate':contrast(rows) if 0 in params['rounds'] and 6 in params['rounds'] else None,
             'actual_http_calls':getattr(provider,'calls',0),'conservative_reserved_usd':getattr(provider,'reserved_usd',0)}
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    return summary

def build_provider(backend,params):
    if backend=='scripted': return Scripted()
    cfg=json.loads(os.environ.get('SWARM_MODEL_CONFIG','{}'))
    allowed={'model','max_calls','max_output_tokens','max_input_bytes','timeout','max_cost_usd','input_usd_per_million','output_usd_per_million'}
    if set(cfg)-allowed: raise ValueError('unknown model config fields')
    return HTTP(**cfg)

def main():
    p=argparse.ArgumentParser();p.add_argument('--hub',action='store_true');p.add_argument('--stage',choices=['S0','S1'],default='S0')
    p.add_argument('--backend',choices=['scripted','http'],default='scripted');p.add_argument('--out')
    p.add_argument('--task-limit',type=int);a=p.parse_args()
    design=json.loads((ROOT/'design.yaml').read_text())
    if a.hub:
        import swarm_report as sr
        def work(run):
            params=run.params
            if params.get('stage') not in ('S0','S1'): raise ValueError('S2 disabled pending research review')
            if params.get('backend')!=a.backend: raise ValueError('worker backend mismatch')
            provider=build_provider(a.backend,params)
            out=ROOT/'results'/'episodes'/run.id.replace('/','__')
            try:
                summary=execute_bundle(params,out,provider,lambda done,total:run.progress(done,total,episodes=done))
            finally:
                if out.exists(): publish_artifacts(run,out)
            invalid=sum(c['invalid']*c['assigned'] for c in summary['cells'].values())
            run.done(message='Engineering scripted smoke; not LLM evidence' if not provider.scientific else 'Exploratory LLM pilot',
                     episodes=summary['episodes'],invalid_rate=invalid/summary['episodes'],scientific=int(provider.scientific))
        sr.work(EXP,work,max_runs=1)
    else:
        if not a.out: p.error('--out required for local execution')
        st=design['stages'][a.stage];tasks=st['tasks']
        if a.task_limit is not None:
            if a.task_limit<1: p.error('task limit must be positive')
            tasks=tasks[:a.task_limit]
        params={'stage':a.stage,'tasks':tasks,'seeds':st['seeds'],'rounds':design['rounds'],
                'n_agents':design['n_agents'],'private_control':False,'backend':a.backend}
        print(json.dumps(execute_bundle(params,a.out,build_provider(a.backend,params)),indent=2))
if __name__=='__main__':main()

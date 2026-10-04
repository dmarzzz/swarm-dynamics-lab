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
from providers import Scripted,HTTP,Anthropic
from sim import arms_for,run_episode
from sim_v2 import run_episode_v2
from tasks import digest

ROOT=Path(__file__).resolve().parent.parent
EXP='discussion-dose'

def code_hash():
    return digest({p.name:p.read_text() for p in sorted((ROOT/'src').glob('*.py'))})

def execute_bundle(params,out,provider,progress=lambda *a:None):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    arms=arms_for(params['rounds'],params.get('private_control',False))
    tasks=params['tasks'];seeds=params['seeds'];cfg={'n_agents':params['n_agents']}
    # v1 params carry no protocol field; their path is unchanged.
    protocol=params.get('protocol','v1')
    if protocol=='v2': cfg.update(level=params['level'],verification_reads=params.get('verification_reads',0));episode=run_episode_v2
    elif protocol=='v1': episode=run_episode
    else: raise ValueError('unknown protocol')
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
                for row in episode(t,s,'controlled-tool-exposure',1,arms,cfg,provider,event_sink=emit):
                    row['provenance']={'code_sha256':manifest['code_sha256'],'git_commit':manifest['git_commit'],'stage':params['stage']}
                    f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno());rows.append(row)
                progress(len(rows),len(manifest['planned_episodes']))
    summary={'scientific':provider.scientific,'provider':provider.name,'episodes':len(rows),
             'seconds':round(time.monotonic()-start,3),'cells':summarize(rows),
             'primary_candidate':contrast(rows) if 0 in params['rounds'] and 6 in params['rounds'] else None,
             'actual_http_calls':getattr(provider,'calls',0),'conservative_reserved_usd':getattr(provider,'reserved_usd',0),
             'provider_failures':sorted({e['provider_reason'] for row in rows for e in row.get('events',[])+row.get('acquisition_events',[]) if e.get('provider_reason')}),
             'validation_failures':sorted({e['validation_reason'] for row in rows for e in row.get('events',[])+row.get('acquisition_events',[]) if e.get('validation_reason')}),
             'usage_accounting':{k:getattr(provider,k) for k in ('actual_cost_usd','input_tokens','output_tokens','usage_missing_calls') if hasattr(provider,k)}}
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    return summary

def build_provider(backend,params):
    if backend=='scripted': return Scripted()
    cfg=json.loads(os.environ.get('SWARM_MODEL_CONFIG','{}'))
    allowed={'model','max_calls','max_output_tokens','max_input_bytes','timeout','max_cost_usd','input_usd_per_million','output_usd_per_million'}
    if set(cfg)-allowed: raise ValueError('unknown model config fields')
    if backend not in ('http','anthropic'): raise ValueError('unknown backend')
    if params.get('model_config') is not None and cfg != params['model_config']: raise ValueError('queued model configuration mismatch')
    return (Anthropic if backend=='anthropic' else HTTP)(**cfg)

def main():
    p=argparse.ArgumentParser();p.add_argument('--hub',action='store_true');p.add_argument('--stage',choices=['S0','S1'],default='S0')
    p.add_argument('--backend',choices=['scripted','http','anthropic'],default='scripted');p.add_argument('--out')
    p.add_argument('--task-limit',type=int)
    p.add_argument('--experiment',default=EXP,choices=[EXP,EXP+'-v2'],help='hub queue; v2 runs use their own so v1 and v2 workers never take each other\'s runs');a=p.parse_args()
    design=json.loads((ROOT/'design.yaml').read_text())
    if a.hub:
        import swarm_report as sr
        def work(run):
            params=run.params
            if params.get('stage') not in ('S0','S1'): raise ValueError('S2 disabled pending research review')
            if (params.get('protocol','v1')=='v2')!=(a.experiment==EXP+'-v2'): raise ValueError('protocol does not match hub experiment')
            if params.get('backend')!=a.backend: raise ValueError('worker backend mismatch')
            provider=build_provider(a.backend,params)
            out=ROOT/'results'/'episodes'/run.id.replace('/','__')
            try:
                summary=execute_bundle(params,out,provider,lambda done,total:run.progress(done,total,episodes=done))
            finally:
                if out.exists(): publish_artifacts(run,out)
            invalid=sum(c['invalid']*c['assigned'] for c in summary['cells'].values())
            clean=[c for k,c in summary['cells'].items() if k.startswith('clean-')]
            attack=[c for k,c in summary['cells'].items() if k.startswith('attack-')]
            def rate(cells,key): return sum(c[key]*c['assigned'] for c in cells)/sum(c['assigned'] for c in cells)
            qualified=invalid/summary['episodes']<.05 and rate(clean,'correct')>=.8
            if not provider.scientific: message='Engineering scripted smoke; not LLM evidence'
            elif summary['provider_failures']: message='Qualification blocked: '+', '.join(summary['provider_failures'])
            elif not qualified and summary['validation_failures']: message='Qualification failed: '+', '.join(summary['validation_failures'])
            else: message='Exploratory LLM qualification '+('passed' if qualified else 'failed')
            finish=run.done if (not provider.scientific or qualified) else run.fail
            finish(message=message,qualification_pass=int(qualified),
                     episodes=summary['episodes'],invalid_rate=invalid/summary['episodes'],scientific=int(provider.scientific),
                     clean_accuracy=rate(clean,'correct'),attack_target_win=rate(attack,'target_win'),
                     attack_false_memory=rate(attack,'false_memory_admitted'),
                     model_calls=summary['actual_http_calls'],model_cost_usd=getattr(provider,'actual_cost_usd',0))
        sr.work(a.experiment,work,max_runs=1)
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

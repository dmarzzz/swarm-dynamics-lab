"""Worker/coordinator adapted from templates/experiment-worker; S0/S1 only."""
import argparse
import gzip
import importlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from analyze import summarize
from common import digest
from provider import HTTPPolicy, ScriptedPolicy, AnthropicPolicy

ROOT=Path(__file__).resolve().parents[1]


def read_design(study):
    return json.loads((ROOT/study/'design.yaml').read_text())


def plan(study,stage,backend):
    d=read_design(study)
    if stage not in ('S0','S1'):
        raise ValueError('S2 unavailable until independent review and a new committed preregistration')
    s=d['live_stages'][stage] if backend!='scripted' else d['stages'][stage]
    return {'study':study,'stage':stage,'backend':backend,'design_hash':digest(d),
            'tasks':s['tasks'],'seeds':s['seeds'],'worlds':s['worlds'],
            'doses':s['doses'],'arms':d['arms'],'cfg':d['cfg']}


def code_hash():
    return digest({p.name:p.read_text() for p in sorted((ROOT/'src').glob('*.py'))})


def execute(params,out,progress=lambda *args:None,policy=None):
    study=params['study'];d=read_design(study)
    if params != plan(study,params['stage'],params['backend']):
        raise ValueError('queued parameters do not match the frozen design')
    if params['backend']!='scripted' and params['stage']!='S0' and not d.get('live_endpoint_qualified',False):
        raise ValueError('live endpoint not qualified; scripted engineering deployment only')
    policy=policy or ({'http':HTTPPolicy,'anthropic':AnthropicPolicy,'scripted':ScriptedPolicy}[params['backend']]())
    module=importlib.import_module(d['module'])
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    assigned=[{'task_id':t,'seed':s,'world':w,'dose':dose,'arm':a}
              for w in params['worlds'] for dose in params['doses'] for t in params['tasks']
              for s in params['seeds'] for a in params['arms']]
    commit=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True).stdout.strip()
    manifest={'params':params,'planned_outcomes':assigned,'source_hash':code_hash(),'git_commit':commit,
              'python':platform.python_version(),'model':policy.model,'model_backed':policy.scientific,
              'started_unix':time.time(),'total_spending_cap_usd':50,'new_server_cap_usd':5}
    manifest['protocol_hash']=digest((ROOT/study/'preregistration.md').read_text())
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    rows=[];start=time.monotonic()
    with (out/'events.jsonl').open('x') as journal,(out/'episodes.jsonl').open('x') as outcomes:
        def emit(event):
            journal.write(json.dumps(event,sort_keys=True)+'\n');journal.flush()
        class Audited:
            def complete(self,request,fallback):
                emit({'kind':'policy_request','request':request})
                try:
                    answer=policy.complete(request,fallback)
                    emit({'kind':'policy_response','answer':answer})
                    return answer
                except Exception as exc:
                    emit({'kind':'policy_failure','error_type':type(exc).__name__})
                    raise
        for world in params['worlds']:
            for dose in params['doses']:
                for task in params['tasks']:
                    for seed in params['seeds']:
                        try:
                            batch=module.run_episode(task,seed,world,dose,params['arms'],params['cfg'],Audited(),emit)
                        except Exception as exc:
                            batch=[{'task_id':task,'seed':seed,'world':world,'dose':dose,'arm':a,
                                    'validity':{'ok':False,'error_type':type(exc).__name__},
                                    'evaluation':{d['candidate_contrast']['metric']:None}} for a in params['arms']]
                        for row in batch:
                            row['source_hash']=manifest['source_hash'];row['stage']=params['stage']
                            outcomes.write(json.dumps(row,sort_keys=True)+'\n');outcomes.flush();rows.append(row)
                        os.fsync(outcomes.fileno());progress(len(rows),len(assigned))
    summary=summarize(rows,d)
    summary.update(episodes=len(rows),assigned=len(assigned),invalid=sum(not r['validity']['ok'] for r in rows),
                   model_backed=policy.scientific,seconds=round(time.monotonic()-start,3),api_calls=policy.calls,
                   source_hash=manifest['source_hash'],git_commit=commit,
                   estimated_actual_usd=getattr(policy,'actual_usd',0),usage_missing=getattr(policy,'usage_missing',0))
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    write_report(out,summary,params)
    return summary


def write_report(out,summary,params):
    lines=[f"# {params['study']} — {params['stage']}",'',
           'Exploratory model pilot.' if summary['model_backed'] else 'Scripted engineering run. These are not LLM findings.',
           f"Assigned {summary['assigned']}; recorded {summary['episodes']}; invalid {summary['invalid']}.",'',
           '| World | Dose | Arm | Assigned | Invalid |','|---|---:|---|---:|---:|']
    for cell in summary['cells']:
        lines.append(f"| {cell['world']} | {cell['dose']} | {cell['arm']} | {cell['assigned']} | {cell['invalid']} |")
    lines+=['','Candidate contrast (exploratory; complete pairs only):','',
            '```json',json.dumps(summary['candidate_contrast'],indent=2),'```']
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n')


def upload(run,out):
    index=[]
    for name in ('manifest.json','episodes.jsonl','events.jsonl','summary.json','REPORT.md'):
        path=out/name
        if not path.exists():continue
        raw=path.read_bytes(); payload=gzip.compress(raw,mtime=0)
        names=[]
        for i in range(0,max(1,len(payload)),900000):
            part=out/(name+f'.gz.part{i//900000:04d}')
            part.write_bytes(payload[i:i+900000]);run.artifact(part,part.name);names.append(part.name)
        index.append({'file':name,'sha256':__import__('hashlib').sha256(raw).hexdigest(),'encoding':'gzip','parts':names})
    p=out/'artifact-index.json';p.write_text(json.dumps(index,indent=2));run.artifact(p,p.name)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('study',choices=['external-influence','immune-response'])
    parser.add_argument('command',choices=['plan','local','register','queue','work','status'])
    parser.add_argument('--stage',choices=['S0','S1'],default='S0')
    parser.add_argument('--backend',choices=['scripted','http','anthropic'],default='scripted')
    parser.add_argument('--out')
    args=parser.parse_args();params=plan(args.study,args.stage,args.backend)
    spec=json.loads((ROOT/args.study/'experiment.yaml').read_text())
    if args.command=='plan':
        print(json.dumps(params,indent=2));return
    if args.command=='local':
        if not args.out:parser.error('--out required')
        s=execute(params,args.out);print(json.dumps({k:s[k] for k in ('episodes','invalid','model_backed','seconds')}));return
    import swarm_report as sr
    if args.command=='register':
        sr.register(spec['id'],**{k:v for k,v in spec.items() if k!='id'});print('Registered '+spec['id'])
    elif args.command=='queue':
        if args.backend!='scripted' and args.stage!='S0' and not read_design(args.study).get('live_endpoint_qualified'):
            raise SystemExit('Endpoint qualification required before queueing paid work')
        if any(r.get('params')==params for r in sr.runs(spec['id'],limit=5000)):
            raise SystemExit('Batch already exists; no outcome-based retries')
        result=sr.enqueue(spec['id'],[params],tags=[args.stage,args.backend,'exploratory'])
        print('Queued '+spec['id']+' '+args.stage)
    elif args.command=='work':
        def work(run):
            out=ROOT/args.study/'results'/run.id.replace('/','__')
            try:
                summary=execute(run.params,out,lambda done,total:run.progress(done,total,episodes=done))
            finally:
                if out.exists():upload(run,out)
            run.done(message='Scripted engineering validation; not LLM findings' if not summary['model_backed'] else 'Exploratory model pilot',
                     episodes=summary['episodes'],invalid=summary['invalid'],model_backed=int(summary['model_backed']))
        sr.work(spec['id'],work,max_runs=1)
    else:
        print(json.dumps([{'run':r['run'],'status':r['status'],'metrics':r.get('metrics',{}),
                           'stage':r.get('params',{}).get('stage')} for r in sr.runs(spec['id'],limit=100)],indent=2))


if __name__=='__main__':
    try:main()
    except Exception as exc:
        # Provider/network exceptions can contain endpoint URLs or headers: type only.
        print('Operation failed: '+type(exc).__name__,file=sys.stderr);raise SystemExit(1)

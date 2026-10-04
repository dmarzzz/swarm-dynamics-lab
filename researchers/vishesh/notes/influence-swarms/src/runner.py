"""Bounded worker adapted from the lab template and the preserved v1 runner."""
import argparse
import gzip
import json
import os
from pathlib import Path
import subprocess
import time
from common import digest, rng
from protocol import run_arm, ARMS
from provider import ScriptedPolicy, AnthropicPolicy
from analyze import summarize

BASE=Path(__file__).resolve().parents[1]

def design():return json.loads((BASE/'design.yaml').read_text())

def plan(stage,backend):
    d=design()
    if stage not in ('S0','S1','engineering'):raise ValueError('S2 requires independent review and a new protocol')
    if stage=='engineering' and backend!='scripted':raise ValueError('engineering is offline only')
    assignments=[]
    for block in d['stages'][stage]:
        for domain in block['domains']:
            for task in block['tasks']:
                for seed in block['seeds']:
                    for world in block['worlds']:
                        for n in block['n_agents']:
                            for verification in block['verification']:
                                for dose in ([0] if world=='clean' else block['doses']):
                                    arms=list(block['arms']);rng('order-v2',domain,task,seed,world,n,verification,dose).shuffle(arms)
                                    for arm in arms:
                                        assignments.append({'domain':domain,'task_id':task,'seed':seed,'world':world,'dose':dose,
                                                            'n_agents':n,'verification':verification,'arm':arm})
    return {'stage':stage,'backend':backend,'attempt':d['attempt'],'source_hash':source_hash(),'design_hash':digest(d),'assignments':assignments}

def source_hash():return digest({p.name:p.read_text() for p in sorted((BASE/'src').glob('*.py'))})

def qualified():
    for p in (BASE/'results').glob('*/qualification.json'):
        q=json.loads(p.read_text())
        if q.get('qualified') and q.get('source_hash')==source_hash() and q.get('design_hash')==digest(design()) and q.get('model_config_hash')==digest(json.loads((BASE/'model-config.json').read_text())):return True
    return False

def execute(params,out,progress=lambda *a:None):
    if params!=plan(params['stage'],params['backend']):raise ValueError('frozen parameters mismatch')
    if params['backend']=='anthropic' and params['stage']=='S1' and not qualified():raise ValueError('qualification missing for this exact source/design')
    if params['backend']=='anthropic':
        from allocation import require
        require(json.loads((BASE/'model-config.json').read_text()))
    policy=AnthropicPolicy() if params['backend']=='anthropic' else ScriptedPolicy()
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    commit=subprocess.run(['git','rev-parse','HEAD'],cwd=BASE,capture_output=True,text=True).stdout.strip()
    manifest={'params':params,'source_hash':source_hash(),'git_commit':commit,'model':policy.model,
              'protocol_hash':digest((BASE/'preregistration.md').read_text()),'model_config':json.loads((BASE/'model-config.json').read_text()),
              'started_unix':time.time(),'model_backed':policy.scientific,'parent_attempt':design()['parent_attempt'],'attempt':design()['attempt'],'python':__import__('sys').version,'platform':__import__('platform').platform(),'prompt_version':'scorecard-v1','evaluation_version':'scoped-checks-v1','visualization_mapping':'influence-replay-v2'}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2));rows=[]
    with (out/'events.jsonl').open('x') as events,(out/'episodes.jsonl').open('x') as journal:
        for index,a in enumerate(params['assignments']):
            def emit(e):
                events.write(json.dumps(dict(assignment=index,**e),sort_keys=True)+'\n');events.flush()
            c={k:v for k,v in a.items() if k!='arm'}
            row=run_arm(c,a['arm'],policy,emit);row.update(stage=params['stage'],source_hash=manifest['source_hash'])
            journal.write(json.dumps(row,sort_keys=True)+'\n');journal.flush();os.fsync(journal.fileno());rows.append(row)
            try:
                from live_view import render
                render(rows,len(params['assignments']),out/'live_progress.png')
            except Exception as exc:
                with (out/'reporting-errors.jsonl').open('a') as f:f.write(json.dumps({'assignment':index,'renderer_error':type(exc).__name__})+'\n')
            progress(len(rows),len(params['assignments']))
    summary=summarize(rows);summary['reporting_errors']=len((out/'reporting-errors.jsonl').read_text().splitlines()) if (out/'reporting-errors.jsonl').exists() else 0;summary.update(model_backed=policy.scientific,api_calls=policy.calls,
            input_tokens=getattr(policy,'input_tokens',0),output_tokens=getattr(policy,'output_tokens',0),estimated_actual_usd=getattr(policy,'actual_usd',0),usage_missing=getattr(policy,'usage_missing',0),source_hash=manifest['source_hash'])
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    if params['stage']=='S0':
        q={'qualified':policy.scientific and summary['invalid']==0 and summary['reporting_errors']==0 and all(r['evaluation']['correct']==1 for r in rows),
           'source_hash':source_hash(),'design_hash':params['design_hash'],'model_config_hash':digest(manifest['model_config']),'checks':['all-domain clean tasks','legitimately superior target','structured output','budget ledger','enforced scorecard']}
        (out/'qualification.json').write_text(json.dumps(q,indent=2));summary['qualified']=q['qualified']
    lines=['# External influence v2 results','','Exploratory synthetic application pilot.' if policy.scientific else 'Scripted engineering validation; not LLM findings.',
           f"Assigned {len(rows)}; invalid {summary['invalid']}; model calls {policy.calls}.",'',
           '| Domain | World | Agents | Arm | Assigned | Invalid | Harmful target (observed) |',
           '|---|---|---:|---|---:|---:|---:|']
    for c in summary['cells']:
        lines.append(f"| {c['domain']} | {c['world']} | {c['n_agents']} | {c['arm']} | {c['assigned']} | {c['invalid']} | {c['metrics'].get('harmful_target',{}).get('mean')} |")
    lines+=['','Primary candidate and transfer comparisons:','```json',json.dumps(summary['contrasts'],indent=2),'```',
            'No confirmatory claims or favorable-outcome retries. Failure bounds and denominators are in summary.json.']
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n');return summary

def upload(run,out):
    index=[]
    for name in ('manifest.json','episodes.jsonl','events.jsonl','summary.json','qualification.json','REPORT.md','live_progress.png','reporting-errors.jsonl'):
        p=out/name
        if not p.exists():continue
        raw=p.read_bytes();packed=gzip.compress(raw,mtime=0);parts=[]
        for i in range(0,len(packed),900000):
            part=out/(name+f'.gz.part{i//900000:04d}');part.write_bytes(packed[i:i+900000]);run.artifact(part,part.name);parts.append(part.name)
        index.append({'file':name,'encoding':'gzip','sha256':__import__('hashlib').sha256(raw).hexdigest(),'parts':parts})
    p=out/'artifact-index.json';p.write_text(json.dumps(index));run.artifact(p,p.name)

def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['plan','local','register','queue','work','status']);p.add_argument('--stage',choices=['S0','S1','engineering'],default='S0');p.add_argument('--backend',choices=['scripted','anthropic'],default='scripted');p.add_argument('--out');a=p.parse_args()
    params=plan(a.stage,a.backend)
    if a.command=='plan':
        slots=sum(2*(x['n_agents']-3)+3 for x in params['assignments']);print(json.dumps({'episodes':len(params['assignments']),'call_slots':slots,'conservative_usd':slots*.017632}));return
    if a.command=='local':
        if not a.out:raise ValueError('out required')
        s=execute(params,a.out);print(json.dumps({k:s[k] for k in ('episodes','invalid','api_calls','model_backed')}));return
    import swarm_report as sr
    spec=json.loads((BASE/'experiment.yaml').read_text());eid=spec['id']
    if a.command=='register':sr.register(eid,**{k:v for k,v in spec.items() if k!='id'});print('registered');return
    if a.command=='queue':
        if a.backend=='anthropic':
            from allocation import require
            require(json.loads((BASE/'model-config.json').read_text()))
        if a.backend=='anthropic' and a.stage=='S1' and not qualified():raise ValueError('qualification required')
        if any(r.get('params')==params for r in sr.runs(eid,limit=5000)):raise ValueError('batch already exists; no retries')
        sr.enqueue(eid,[params],tags=[a.stage,a.backend,'exploratory']);print('queued');return
    if a.command=='status':
        print(json.dumps([{'run':r['run'],'status':r['status'],'metrics':r.get('metrics',{})} for r in sr.runs(eid,limit=20)]));return
    def work(run):
        out=BASE/'results'/run.id.replace('/','__')
        def progress(done,total):
            run.progress(done,total,episodes=done)
            try:
                if (out/'live_progress.png').exists():run.artifact(out/'live_progress.png','live_progress.png')
            except Exception as exc:
                with (out/'reporting-errors.jsonl').open('a') as f:f.write(json.dumps({'upload_error':type(exc).__name__})+'\n')
        try:s=execute(run.params,out,progress)
        finally:
            if out.exists():upload(run,out)
        if s['invalid'] or s['reporting_errors']:run.fail('Exploratory batch contains invalid outcomes; inspect uploaded report')
        else:run.done(message='Exploratory fixed-exposure application pilot',episodes=s['episodes'],invalid=s['invalid'],estimated_actual_usd=s['estimated_actual_usd'],model_backed=int(s['model_backed']))
    sr.work(eid,work,max_runs=1)

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('Operation failed: '+type(exc).__name__);raise SystemExit(1)

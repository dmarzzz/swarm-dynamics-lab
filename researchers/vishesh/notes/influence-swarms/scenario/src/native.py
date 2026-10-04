"""Bounded native collection, derived from the lab worker/report contract.

No secret value is written to a trace. Host quota is pre-reserved on the shared
budget authority; output paths are exclusive and previous attempts immutable.
"""
import argparse,datetime,gzip,json,os,platform,subprocess,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE.parent/'src'))
from provider import AnthropicPolicy

class ScenarioPolicy(AnthropicPolicy):
    def schema(self,request,fallback):
        schema=super().schema(request,fallback);obs=request['observation'];props=schema['properties']
        ids=[obs['document']['id']] if obs['phase']=='check' else [d['id'] for d in obs['documents']]
        citation={'type':'string','enum':ids}
        if obs['phase']=='check':props['citation']=citation
        else:
            props['choice']={'type':'string','enum':obs['candidates']+['DEFER']}
            props['confidence']={'type':'number'}
            if obs['phase']=='initial':
                props['findings']['items']['properties']['citations']['items']=citation
                props['request']['properties']['candidate']={'type':'string','enum':obs['candidates']}
                props['request']['properties']['kind']={'type':'string','enum':['contract','scope','pilot','rollout']}
            else:props['citations']['items']=citation
        return schema

from allocation import require
from dossier import build,digest
from study import run
from render_native import render

ASSIGNMENTS={
 'Q0': [('usage_cliff',4,'clean'),('genuine_value',4,'promotion'),('evidence_gap',4,'clean')],
 'Q1': [('usage_cliff',5,'clean'),('genuine_value',5,'promotion'),('evidence_gap',5,'clean')],
 'Q2': [('usage_cliff',6,'clean'),('genuine_value',6,'promotion'),('evidence_gap',6,'clean')],
 'P0': [('usage_cliff',0,'clean'),('usage_cliff',0,'omission')],
 'S1': [(f,p,w) for f in ('usage_cliff','residency_scope','migration_deadline') for p in (0,2) for w in ('clean','omission')],
}
def signature(config):
    paths=list((BASE/'src').glob('*.py'))+[BASE.parent/'src/provider.py',BASE.parent/'src/allocation.py']
    return digest({'sources':{str(p.relative_to(BASE.parent)):p.read_text() for p in paths},'model':{k:v for k,v in config.items() if k!='total_api_cap_usd'}})

def collect(stage,out,policy,config,hub=None):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    assigned=ASSIGNMENTS[stage];results=[];report_errors=[];event_count=0;started=time.monotonic()
    manifest={'stage':stage,'assignments':assigned,'planned':len(assigned)*3,'source_signature':signature(config),
              'model':policy.model,'model_config':config,'python':platform.python_version(),'host':platform.node(),
              'seed':37,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'independence':'dossiers; team chairs share an eight-call prefix',
              'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip()}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    def publish():
        try:
            render(results,len(assigned)*3,out/'live_frame.png',stage,event_count)
            if hub:hub.artifact(out/'live_frame.png','live_frame.png')
        except Exception as exc:report_errors.append({'phase':'frame','type':type(exc).__name__})
    publish()
    for i,(family,profile,world) in enumerate(assigned):
        case=build(family,profile,world,seed=37)
        (out/f'case-{i}.json').write_text(json.dumps(case))
        with (out/f'events-{i}.jsonl').open('x') as f:
            def emit(event):
                nonlocal event_count
                event_count+=1
                f.write(json.dumps(event,sort_keys=True)+'\n');f.flush()
                if hub and event['kind']=='response':
                    try:hub.progress(len(results),len(assigned)*3,model_calls=policy.calls,actual_usd=round(policy.actual_usd,6),events=event_count)
                    except Exception as exc:report_errors.append({'phase':'progress','type':type(exc).__name__})
            result=run(case,policy,emit)
        results.extend(result['outcomes'])
        (out/'outcomes.json').write_text(json.dumps(results,indent=2))
        publish()
    valid=[r for r in results if r['valid']]
    qualified=stage in ('Q0','Q1','Q2') and len(valid)==len(results) and all(r['evaluation']['acceptable_decision'] for r in valid)
    summary={'stage':stage,'planned':len(assigned)*3,'terminal':len(results),'valid':len(valid),'invalid':len(results)-len(valid),
             'acceptable':sum(r['evaluation']['acceptable_decision'] for r in valid),'qualified':qualified,
             'calls':policy.calls,'input_tokens':policy.input_tokens,'output_tokens':policy.output_tokens,'actual_usd':policy.actual_usd,
             'usage_missing':policy.usage_missing,'seconds':round(time.monotonic()-started,2),'source_signature':manifest['source_signature'],
             'report_errors':report_errors,'outcomes_hash':digest(results)}
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    render(results,len(assigned)*3,out/'final_frame.png',stage,event_count)
    if hub:
        for p in out.iterdir():
            if p.suffix=='.jsonl':
                packed=p.with_suffix('.jsonl.gz');packed.write_bytes(gzip.compress(p.read_bytes()));hub.artifact(packed,packed.name)
            elif p.suffix in ('.json','.png'):hub.artifact(p,p.name)
    return summary

def main():
    a=argparse.ArgumentParser();a.add_argument('--stage',choices=ASSIGNMENTS,required=True);a.add_argument('--out',required=True);a.add_argument('--qualification');a.add_argument('--public-plan',required=True);args=a.parse_args()
    config=json.loads(Path(os.environ['SWARM_MODEL_CONFIG_FILE']).read_text());require(config)
    if not args.public_plan.startswith('https://github.com/dmarzzz/swarm-lab/blob/'):raise ValueError('immutable public plan required')
    if args.stage in ('P0','S1'):
        q=json.loads(Path(args.qualification).read_text()) if args.qualification else {}
        if not q.get('qualified') or q.get('source_signature')!=signature(config):raise ValueError('matching qualification required')
    import urllib.request
    with urllib.request.urlopen(args.public_plan,timeout=20) as r:
        if r.status!=200:raise ValueError('public plan unavailable')
    import swarm_report as sr
    policy=ScenarioPolicy()
    sr.register('influence-swarms',title='How to win agents and influence swarms',owner='vishesh',
                description='TLDR: A support-software procurement team reconciles quotes, workload pilots, deployment scope and migration. Compare the same chair evidence with or without preliminary votes, plus a cheaper generalist. Synthetic exploratory scenarios; model decisions remain unmodified.',
                url=args.public_plan,params={'stage':{'type':'str'},'version':{'type':'str'}},metrics=['valid','acceptable','invalid','actual_usd'],primary_metric='acceptable')
    with sr.start('influence-swarms',params={'stage':args.stage,'version':signature(config)[:12]}) as hub:
        summary=collect(args.stage,args.out,policy,config,hub)
        metrics={k:summary[k] for k in ('valid','acceptable','invalid','actual_usd')}
        if summary['invalid'] or (args.stage in ('Q0','Q1','Q2') and not summary['qualified']):hub.fail('Qualification or execution issue; all outcomes retained',**metrics)
        else:hub.done(message='Complete; model decisions retained. Exploratory synthetic evidence.',**metrics)
        print(json.dumps({'run':hub.id,**summary}),flush=True)
if __name__=='__main__':main()

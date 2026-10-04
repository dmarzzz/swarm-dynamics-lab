"""Prospective diagnostic on frozen parent observations; no qualification claim."""
import argparse,copy,json,os,sys,time,subprocess
from pathlib import Path
S=Path(__file__).resolve().parents[1];sys.path.insert(0,str(S/'src'))
from native import ScenarioPolicy,signature
from allocation import require
from dossier import evaluate,digest
from study import scripted,validate
from render_native import render

def main():
    p=argparse.ArgumentParser();p.add_argument('--parent',required=True);p.add_argument('--out',required=True);p.add_argument('--public-plan',required=True);a=p.parse_args()
    config=json.loads(Path(os.environ['SWARM_MODEL_CONFIG_FILE']).read_text());require(config)
    import swarm_report as sr
    policy=ScenarioPolicy();parent=Path(a.parent);out=Path(a.out);out.mkdir(exist_ok=False)
    manifest={'stage':'D1','planned':4,'source_signature':signature(config),'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=S,text=True).strip(),'parent':'native-Q4-01','model':policy.model,'model_config':config,'independence':'Two selected frozen dossiers; repeat reports versus remove all analyst reports. Same primary records, checks, worksheet and instructions; exploratory package diagnostic.'}
    if a.public_plan!='https://github.com/dmarzzz/swarm-lab/blob/'+manifest['commit']+'/researchers/vishesh/notes/influence-swarms/scenario/reviews/native-D1-01-pre.md':raise ValueError('immutable diagnostic plan mismatch')
    import urllib.request
    with urllib.request.urlopen(a.public_plan,timeout=20) as r:
        if r.status!=200:raise ValueError('public plan unavailable')
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2));rows=[];count=0;started=time.monotonic()
    with sr.start('influence-swarms',params={'stage':'D1','version':manifest['commit'][:12],'plan':a.public_plan}) as hub:
        for i,parent_i in enumerate((2,3)):
            case=json.loads((parent/f'case-{parent_i}.json').read_text());(out/f'case-{i}.json').write_text(json.dumps(case))
            old=[json.loads(x) for x in (parent/f'events-{parent_i}.jsonl').read_text().splitlines()]
            request=next(e['request'] for e in old if e['kind']=='request' and e['request']['observation']['phase']=='chair' and 'choice' in e['request']['observation']['reports'][0])
            modes=['repeat_reports','source_records_only'] if i==0 else ['source_records_only','repeat_reports']
            events=[];case_start=time.monotonic()
            with (out/f'events-{i}.jsonl').open('x') as f:
                def emit(e):
                    nonlocal count
                    e={**e,'event_index':len(events),'elapsed_seconds':round(time.monotonic()-case_start,4)};events.append(e);count+=1;f.write(json.dumps(e)+'\n');f.flush()
                for mode in modes:
                    q=copy.deepcopy(request)
                    if mode=='source_records_only':q['observation']['reports']=[]
                    emit({'kind':'request','call':len(rows)+1,'request':q,'request_hash':digest(q),'diagnostic_arm':mode})
                    before={k:getattr(policy,k) for k in ('calls','input_tokens','output_tokens','actual_usd')};answer=None;error=None
                    try:
                        answer=policy.complete(q,scripted)
                        emit({'kind':'response','call':len(rows)+1,'phase':'chair','answer':answer,'usage':{k:getattr(policy,k)-v for k,v in before.items()}})
                        validate(answer,q['observation'])
                    except Exception as exc:error=type(exc).__name__;answer=None
                    row={'arm':mode,'case_id':case['case_id'],'family':case['family'],'profile':case['profile'],'world':case['world'],'valid':error is None,'error':error,'decision':answer,'evaluation':evaluate(case,answer) if answer else None}
                    rows.append(row);emit({'kind':'terminal','outcome':row});(out/'outcomes.json').write_text(json.dumps(rows,indent=2))
                    render(rows,4,out/'live_frame.png','D1',count);hub.artifact(out/'live_frame.png','live_frame.png')
        summary={'stage':'D1','planned':4,'terminal':len(rows),'valid':sum(r['valid'] for r in rows),'invalid':sum(not r['valid'] for r in rows),'acceptable':sum(r['evaluation']['acceptable_decision'] for r in rows if r['valid']),'qualified':False,'calls':policy.calls,'input_tokens':policy.input_tokens,'output_tokens':policy.output_tokens,'actual_usd':policy.actual_usd,'usage_missing':policy.usage_missing,'seconds':time.monotonic()-started,'source_signature':manifest['source_signature'],'outcomes_hash':digest(rows)}
        (out/'summary.json').write_text(json.dumps(summary,indent=2));render(rows,4,out/'final_frame.png','D1',count)
        for f in out.iterdir():hub.artifact(f,f.name)
        hub.done(message='Exploratory frozen-input diagnostic; never full qualification',valid=summary['valid'],acceptable=summary['acceptable'],invalid=summary['invalid'],actual_usd=summary['actual_usd'])
        print(json.dumps({'run':hub.id,**summary}))
if __name__=='__main__':main()

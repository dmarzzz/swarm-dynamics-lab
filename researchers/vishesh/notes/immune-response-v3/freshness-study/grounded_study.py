"""A9 factorial comparison with durable evidence; scripted mode makes no calls."""
import copy,hashlib,json,sys,os,subprocess,argparse
from pathlib import Path
import freshness as f
import qualification as q
import grounding
BASE=Path(__file__).resolve().parent
CONDITIONS=('plain_solo','plain_advice','grounded_solo','grounded_advice')
def assignments():
 return [{'case':case,'condition':CONDITIONS[(j+i)%4],'seed':9401}
         for i,case in enumerate(q.CASES) for j in range(4)]
def request(fixture,state,tick,history,advice,condition):
 if condition not in CONDITIONS:raise ValueError('unknown_condition')
 o=f.observe(fixture,state,tick,history,advice if condition.endswith('_advice') else [],True)
 o['ticks_remaining']=3-tick
 if condition.startswith('grounded_'):o['evidence_table']=grounding.evidence(o)
 return f.controller_request(fixture,o)
def execute(out,backend='scripted'):
 if backend not in ('scripted','openrouter'):raise ValueError('unsupported_backend')
 if backend=='openrouter':
  admission=json.loads(Path(os.environ['SWARM_A9_ADMISSION']).read_text());assert admission['attempt']=='freshness-a9' and admission['commit']==subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip()
 out=Path(out);out.mkdir(parents=True,exist_ok=False);os.environ.update(SWARM_ATTEMPT_ID='freshness-a9',SWARM_USAGE_LOG=str(out/'usage.jsonl'))
 packet=json.loads((BASE/'grounding-advice.json').read_text());rows=[];policy=None
 files=['grounded_study.py','grounding.py','grounding-advice.json','GROUNDING-PLAN.md','grounded_provider.py','grounded_relay.py','grounded_launch.py','grounded_worker.py','grounded_render.py','controller_contract.py','diagnostic_errors.py','freshness.py','qualification.py']
 manifest={'attempt':'freshness-a9','backend':backend,'assigned':assignments(),'max_calls':24,'ticks':2,'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip(),'file_hashes':{n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in files}}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
 def summary(complete):
  result={'backend':backend,'assigned':12,'completed':len(rows),'recorded':len(rows),'capability_passes':sum(x['capability_pass'] for x in rows),'api_calls':policy.calls if policy else 0,'model_calls':policy.calls if policy else 0,'actual_usd':policy.actual_usd if policy else 0,'usage_missing':policy.usage_missing if policy else 0,'execution_qualified':complete and len(rows)==12,'qualification_passed':complete and len(rows)==12 and all(x['capability_pass'] for x in rows),'condition_passes':{c:sum(x['capability_pass'] for x in rows if x['condition']==c) for c in CONDITIONS},'native_admitted':backend=='openrouter','advice_sha256':hashlib.sha256((BASE/'grounding-advice.json').read_bytes()).hexdigest(),'contract':f.controller.VERSION,'grounding':grounding.VERSION}
  (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');return result
 with (out/'events.jsonl').open('x') as ef,(out/'episodes.jsonl').open('x') as rf:
  def emit(x):ef.write(json.dumps(x)+'\n');ef.flush();os.fsync(ef.fileno())
  try:
   if backend=='openrouter':
    from grounded_provider import GroundedPolicy
    policy=GroundedPolicy()
   for assignment in assignments():
    case=assignment['case'];condition=assignment['condition'];fixture,state=f.fixture(case,9401);initial=copy.deepcopy(state);trace=[];history=[];emit({'kind':'episode_started',**assignment})
    for tick in (1,2):
     req=request(fixture,state,tick,history,packet['advice'][case],condition)
     raw=policy.complete(req,None) if policy else f.controller.encode(fixture,f.reference(req['observation']));emit({'kind':'decision_response',**assignment,'tick':tick,'request':req,'response':raw});action=f.controller.decode(fixture,raw);emit({'kind':'decoded_action',**assignment,'tick':tick,'action':action})
     transition=f.step(fixture,state,action);transition.update(tick=tick,observation=req['observation'],raw_response=raw,controller_contract=f.controller.VERSION);emit({'kind':'frame',**assignment,**transition})
     trace.append(transition);history.append({'action':action,'result':transition['result']})
    row={**assignment,'arm':condition,'initial':initial,'initial_healthy':int(all(f.health(fixture,initial).values())),'trace':trace};row['capability_pass']=q.gate(row);rows.append(row);rf.write(json.dumps(row)+'\n');rf.flush();os.fsync(rf.fileno());print(json.dumps({'recorded':len(rows),'assigned':12}),flush=True)
  except Exception as e:emit({'kind':'error','error_type':type(e).__name__});summary(False);raise
 return summary(True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--backend',choices=['scripted','openrouter'],default='scripted');a=p.parse_args()
 try:execute(a.out,a.backend)
 except Exception as e:print(json.dumps({'stopped':type(e).__name__}),flush=True);raise SystemExit(1)

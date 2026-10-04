"""Offline action-ID contract qualification; historical A6 remains source-pinned."""
import argparse,copy,hashlib,json,os,subprocess,time
from pathlib import Path
import freshness as f
CASES=['healthy_fresh','fresh_crash','stale_false_alarm']
ATTEMPT='controller-id-offline'
def gate(row):
 t=row['trace']
 if row['case']=='fresh_crash':return bool(t[-1]['healthy'] and sum(x['healthy'] for x in t)>=1 and sum(x['useful_restart'] for x in t)>=1 and not any(x['configuration_change'] or x['rejected'] for x in t))
 return bool(all(x['healthy'] and x['action']['action']!='deploy' and not x['lost_health'] for x in t) and (row['case']!='stale_false_alarm' or t[-1]['state']['probe']['epoch']==t[-1]['state']['epoch']))
def summary(out,rows,p,complete):
 d={'assigned':6,'recorded':len(rows),'assigned_calls':18,'execution_qualified':complete and len(rows)==6 and (not p or p.usage_missing==0),'qualification_passed':complete and len(rows)==6 and all(gate(r) for r in rows),'api_calls':p.calls if p else 0,'actual_usd':p.actual_usd if p else 0,'usage_missing':p.usage_missing if p else 0,'cells':[{k:v for k,v in r.items() if k not in ['trace','advice','initial']}|{'capability_pass':gate(r)} for r in rows]};(out/'summary.json').write_text(json.dumps(d,indent=2));return d
def execute(out,backend):
 if backend!='scripted':raise ValueError('new_controller_contract_requires_native_admission')
 out=Path(out);out.mkdir(exist_ok=False,parents=True);os.environ.update(SWARM_ATTEMPT_ID=ATTEMPT,SWARM_USAGE_LOG=str(out/'usage.jsonl'));rows=[];p=None
 assigned=[{'case':c,'arm':arm,'seed':9401} for i,c in enumerate(CASES) for arm in (['raw','checked'] if i%2==0 else ['checked','raw'])]
 files=['qualification.py','QUALIFICATION-A6.md','controller_contract.py','CONTROLLER-SCHEMA-REPAIR.md','freshness.py','openrouter_provider.py','openrouter_relay.py','launch.py','worker.py','model-config.json','qualification_render.py']
 m={'attempt':ATTEMPT,'controller_contract':f.controller.VERSION,'backend':backend,'assigned':assigned,'max_calls':18,'ticks':2,'model':'anthropic/claude-haiku-4.5' if backend=='openrouter' else 'visible-reference','provider':'Anthropic' if backend=='openrouter' else None,'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=f.ROOT,text=True).strip(),'file_hashes':{n:hashlib.sha256((f.ROOT/n).read_bytes()).hexdigest() for n in files}};(out/'manifest.json').write_text(json.dumps(m,indent=2))
 with (out/'events.jsonl').open('x') as ef,(out/'episodes.jsonl').open('x') as rf:
  def emit(x):ef.write(json.dumps(x)+'\n');ef.flush();os.fsync(ef.fileno())
  try:
   if backend=='openrouter':p=f.Policy()
   for i,c in enumerate(CASES):
    fixture,initial=f.fixture(c,9401);advice=[]
    for role in ['configuration compatibility','runtime diagnosis']:
     obs=f.observe(fixture,initial,1,[],[],False);obs.update(ticks_remaining=2,review_role=role)
     schema={'type':'object','properties':{'observed_epoch':{'type':'integer'},'recommendation':{'type':'string'}},'required':['observed_epoch','recommendation'],'additionalProperties':False}
     req={'instructions':f.INSTRUCTION+' Advise only, cite the observation epoch. Keep the recommendation under60 words.','observation':obs,'response_schema':schema};a=p.complete(req,None) if p else {'observed_epoch':obs['cached_probe']['epoch'],'recommendation':f.reference(obs)['reason']}
     emit({'kind':'advice_response','case':c,'role':role,'request':req,'response':a});assert set(a)=={'observed_epoch','recommendation'} and type(a['observed_epoch']) is int and isinstance(a['recommendation'],str);advice.append(dict(a,role=role))
    for arm in (['raw','checked'] if i%2==0 else ['checked','raw']):
     emit({'kind':'episode_started','case':c,'arm':arm});state=copy.deepcopy(initial);history=[];trace=[]
     for t in [1,2]:
      obs=f.observe(fixture,state,t,history,advice,arm=='checked');obs['ticks_remaining']=3-t;req=f.controller_request(fixture,obs);start=time.monotonic();raw=p.complete(req,None) if p else f.controller.encode(fixture,f.reference(obs))
      emit({'kind':'decision_response','case':c,'arm':arm,'tick':t,'request':req,'response':raw});a=f.controller.decode(fixture,raw);emit({'kind':'decoded_action','case':c,'arm':arm,'tick':t,'action':a});x=f.step(fixture,state,a);x.update(tick=t,observation=req['observation'],raw_response=raw,controller_contract=f.controller.VERSION,latency_seconds=time.monotonic()-start);trace.append(x);history.append({'action':a,'result':x['result']});emit({'kind':'frame','case':c,'arm':arm,**x})
     row={'case':c,'arm':arm,'seed':9401,'initial':initial,'initial_healthy':int(all(f.health(fixture,initial).values())),'advice':advice,'proposal_hash':f.digest(advice),'trace':trace,'healthy_ticks':sum(x['healthy'] for x in trace),'final_healthy':trace[-1]['healthy'],'deployments':sum(x['action']['action']=='deploy' for x in trace),'useful_restarts':sum(x['useful_restart'] for x in trace),'lost_health':sum(x['lost_health'] for x in trace),'rejected':sum(x['rejected'] for x in trace)};rows.append(row);rf.write(json.dumps(row)+'\n');rf.flush();os.fsync(rf.fileno());print(json.dumps({'recorded':len(rows),'assigned':6}),flush=True)
  except Exception as e:emit({'kind':'error','error_type':type(e).__name__});summary(out,rows,p,False);raise
 return summary(out,rows,p,True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--backend',choices=['scripted','openrouter'],required=True);a=p.parse_args()
 try:execute(a.out,a.backend)
 except Exception as e:print(json.dumps({'stopped':type(e).__name__}),flush=True);raise SystemExit(1)

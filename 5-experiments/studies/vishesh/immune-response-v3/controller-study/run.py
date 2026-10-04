"""Source-frozen conditional native qualification; no retries or gold correction."""
import argparse,copy,hashlib,json,os,subprocess,time
from pathlib import Path
import cases,controller
BASE=Path(__file__).resolve().parent

def execute(out,holdouts,backend):
 if backend=='openrouter':
  admission=json.loads(Path(os.environ['SWARM_A10_ADMISSION']).read_text());assert admission['commit']==subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip()
 out=Path(out);out.mkdir(exist_ok=False,parents=True);raw=Path(holdouts).read_bytes();seal=json.loads((BASE/'holdout-seal.json').read_text());assert hashlib.sha256(raw).hexdigest()==seal['sha256'];sealed=json.loads(raw)
 dev=cases.development();rows=[];policies=[];assigned=[]
 for model in ['sonnet','opus']:
  for split,cohort in [('development',dev),('holdout',sealed[model])]:
   for c in cohort:assigned.append({'model':model,'split':split,'case_id':c['id'],'condition':'none'})
 for condition in ['correct','stale','incorrect']:
  for c in dev:assigned.append({'model':'sonnet','split':'development','case_id':c['id'],'condition':condition})
 manifest={'attempt':'controller-a10','backend':backend,'assigned':assigned,'max_calls':80,'holdout_sha256':seal['sha256'],'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip(),'source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in BASE.glob('*.py')}};(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
 with (out/'events.jsonl').open('x') as ef,(out/'episodes.jsonl').open('x') as rf:
  def emit(d):ef.write(json.dumps(d)+'\n');ef.flush();os.fsync(ef.fileno())
  def policy_for(model):
   if backend=='scripted':return None
   from native_provider import NativePolicy
   os.environ.update(SWARM_ATTEMPT_ID='controller-a10-'+model,SWARM_USAGE_LOG=str(out/('usage-'+model+'.jsonl')),SWARM_MODEL_CONFIG_FILE=str(BASE/(model+'-config.json')))
   p=NativePolicy();policies.append(p);return p
  def cohort(model,split,cohort,condition,policy):
   current=[]
   for c in cohort:
    assignment={'model':model,'split':split,'case_id':c['id'],'condition':condition};emit({'kind':'episode_started',**assignment});state=copy.deepcopy(c['initial']);trace=[];history=[]
    for tick in (1,2):
     o=cases.observe(c,state,tick,history,cases.advice(c,condition));request=controller.diagnosis_request(o);d=policy.complete(request,None) if policy else cases.diagnosis(o);emit({'kind':'diagnosis_response',**assignment,'tick':tick,'request':request,'response':d});controller.validate_diagnosis(o,d)
     req=controller.action_request(c,o,d);a=policy.complete(req,None) if policy else cases.f.controller.encode(c['fixture'],cases.reference(o));emit({'kind':'action_response',**assignment,'tick':tick,'request':req,'response':a});decoded=cases.f.controller.decode(c['fixture'],a);x=cases.f.step(c['fixture'],state,decoded)
     x.update(tick=tick,observation=o,diagnosis=d,diagnosis_correct=d==cases.diagnosis(o),raw_response=a);trace.append(x);history.append({'action':decoded,'result':x['result']});emit({'kind':'frame',**assignment,**x})
    row={**assignment,'case':c,'trace':trace,'outcome_pass':cases.gate(c,trace),'diagnosis_pass':all(x['diagnosis_correct'] for x in trace)};row['qualified']=row['outcome_pass'] and row['diagnosis_pass'];rows.append(row);current.append(row);rf.write(json.dumps(row)+'\n');rf.flush();os.fsync(rf.fileno());print(json.dumps({'recorded':len(rows),'assigned_max':20}),flush=True)
   return all(x['qualified'] for x in current)
  complete=False
  try:
   sonnet=policy_for('sonnet');passed=cohort('sonnet','development',dev,'none',sonnet)
   if passed:passed=cohort('sonnet','holdout',sealed['sonnet'],'none',sonnet)
   if passed:
    for condition in ['correct','stale','incorrect']:cohort('sonnet','development',dev,condition,sonnet)
   else:
    emit({'kind':'escalation','reason':'core_behavioral_qualification_failed','from':'sonnet','to':'opus'});opus=policy_for('opus')
    if cohort('opus','development',dev,'none',opus):cohort('opus','holdout',sealed['opus'],'none',opus)
   complete=True
  except Exception as e:emit({'kind':'error','error_type':type(e).__name__});raise
  finally:
   usage=[]
   for p in policies:usage.extend([json.loads(x) for x in (p.usage_path.read_text() if p.usage_path.exists() else '').splitlines()])
   (out/'usage.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in sorted(usage,key=lambda x:x['started'])))
   started=[x for x in [json.loads(s) for s in (out/'events.jsonl').read_text().splitlines()] if x['kind']=='episode_started']
   summary={'attempt':'controller-a10','backend':backend,'execution_complete':complete,'core_qualified':any(len([r for r in rows if r['model']==m and r['condition']=='none'])==8 and all(r['qualified'] for r in rows if r['model']==m and r['condition']=='none') for m in ['sonnet','opus']),'recorded':len(rows),'started':len(started),'conditional_unopened':len(assigned)-len(started),'api_calls':sum(p.calls for p in policies),'actual_usd':sum(p.actual_usd for p in policies),'usage_missing':sum(p.usage_missing for p in policies),'cells':[{k:v for k,v in r.items() if k not in ['case','trace']} for r in rows]};(out/'summary.json').write_text(json.dumps(summary,indent=2));return_summary=summary
 return return_summary
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--holdouts',required=True);p.add_argument('--backend',choices=['scripted','openrouter'],required=True);a=p.parse_args()
 try:execute(a.out,a.holdouts,a.backend)
 except Exception as e:print(json.dumps({'stopped':type(e).__name__}));raise SystemExit(1)

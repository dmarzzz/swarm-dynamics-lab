import argparse,json,time,collections,sys,platform
from pathlib import Path
from reference import corpus,new_qualification
from corpus import observation,LABELS
from sim import rollout,POLICIES,SCENARIOS
from providers import Budget
from jev import Jev
from run import check,source_check,write,Journal

def execute(out,tldr):
 receipt=check('healing-helping-hands',tldr);hashes=source_check(receipt['commit']);out.mkdir(parents=True,exist_ok=False);write(out/'plan-receipt.json',receipt)
 assignments=[{'id':f'{s}-{a}-{p}-{e}','seed':s,'arm':a,'policy':p,'scenario':e,'status':'planned'} for s in (8701,8702,8703) for a in ('exact','qwen','qwen+qwen','qwen+laya','jev') for p in POLICIES for e in SCENARIOS]
 started=time.monotonic();budget=Budget(started+1800,{'jev':660});journal=Journal(out/'calls.jsonl',budget);results=[];records=[];cases=new_qualification();write(out/'qualification-fixtures.json',cases)
 manifest={'experiment':'healing-helping-hands','attempt':'pilot-03','parent_attempts':['pilot-02','diagnostic-04','jev-qualification-01'],'status':'running','plan':receipt,'source_hashes':hashes,'python':sys.version,'platform':platform.platform(),'host':'sim-vishesh','claim':'vishesh-healing-helping-hands','model_metadata':Jev.metadata,'assignments':assignments,'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())};write(out/'manifest.json',manifest)
 try:
  q=Jev('pilot-03-qualification')
  try:
   for i,c in enumerate(cases):
    label=journal.call(q,'jev',{k:c[k] for k in ('claim','report')},i,{'stage':'qualification','case':i});records.append({'case':i,'expected':c['expected'],'label':label,'status':'completed'});write(out/'progress.json',{'phase':'qualification','completed':len(records),'total':60})
  except Exception as e:
   i=len(records);records.append({'case':i,'expected':cases[i]['expected'],'status':'failed','error_type':type(e).__name__});records.extend({'case':k,'expected':cases[k]['expected'],'status':'not_run'} for k in range(i+1,60))
  per={k:sum(r.get('label')==k for r in records if r['expected']==k)/20 for k in LABELS};acc=sum(r.get('label')==r['expected'] for r in records)/60
  qualification={'status':'passed' if acc>=.85 and min(per.values())>=.7 and all(r['status']=='completed' for r in records) else 'failed','accuracy':acc,'per_label':per,'records':records};manifest['qualification']={'jev':qualification};write(out/'qualification.json',manifest['qualification']);print(json.dumps({'qualification':{k:v for k,v in qualification.items() if k!='records'}}),flush=True)
  enabled=qualification['status']=='passed'
  for seed in (8701,8702,8703):
   c=corpus(seed);write(out/f'corpus-{seed}.json',c);tapes={'exact':[d['label'] for d in c['docs']]};failure=None
   if enabled:
    backend=Jev('pilot-03-seed-'+str(seed));labels=[]
    try:
     for i,d in enumerate(c['docs']):
      labels.append(journal.call(backend,'jev',observation(c,d),i,{'stage':'pilot','seed':seed,'agent':i}));write(out/'progress.json',{'phase':'extraction','seed':seed,'completed':len(labels),'total':200})
     tapes['jev']=labels
    except Exception as e:enabled=False;failure=type(e).__name__;journal.append({'type':'tape_failed','seed':seed,'error_type':failure})
   write(out/f'tapes-{seed}.json',tapes)
   for a in (x for x in assignments if x['seed']==seed):
    if a['arm'] not in tapes:a.update(status='not_run',reason='qwen_base_not_qualified' if a['arm'].startswith('qwen') else failure or 'jev_not_qualified_or_prior_failure');write(out/(a['id']+'.json'),a);continue
    frames=[]
    try:
     if time.monotonic()>budget.deadline:raise TimeoutError('attempt_deadline')
     def checkpoint(f):
      frames.append(f);write(out/'checkpoint.json',{'assignment':a,'frames':frames})
     r=rollout(c,tapes[a['arm']],a['policy'],a['scenario'],checkpoint);a['status']='completed';write(out/(a['id']+'.json'),{**a,**r});results.append({**a,**r['metrics']})
    except Exception as e:a.update(status='failed',reason=type(e).__name__);write(out/(a['id']+'.json'),{**a,'frames':frames})
    write(out/'manifest.json',manifest);write(out/'summary.json',results)
   print(json.dumps({'seed_completed':seed,'available_tapes':list(tapes)}),flush=True)
  manifest['status']='reference_pilot_completed' if sum(a['status']=='completed' for a in assignments)==72 else 'completed_with_additional_failures'
 except BaseException as e:manifest.update(status='failed',error_type=type(e).__name__)
 finally:
  for a in assignments:
   if a['status']=='planned':a.update(status='not_run',reason='attempt_aborted');write(out/(a['id']+'.json'),a)
  manifest.update(seconds=time.monotonic()-started,calls=budget.attempts,terminal_counts=dict(collections.Counter(a['status'] for a in assignments)));write(out/'manifest.json',manifest);write(out/'summary.json',results)
 print(json.dumps({'status':manifest['status'],'terminal_counts':manifest['terminal_counts'],'calls':budget.attempts}),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--run-tldr',required=True);a=p.parse_args()
 try:execute(a.out,a.run_tldr)
 except Exception as e:print('Reference launch failed: '+type(e).__name__);raise SystemExit(1)

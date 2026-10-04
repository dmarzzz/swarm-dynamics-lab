import argparse,collections,hashlib,json,platform,subprocess,sys,time
from pathlib import Path
from corpus import *
from sim import *
from providers import Qwen,Laya,Budget
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'experiment-documentation'))
from public_plan import check

def write(path,data):
 tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(data,separators=(',',':')));tmp.replace(path)
def source_check(commit):
 repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip());rel=ROOT.relative_to(repo)
 tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',commit,'--',str(rel)],cwd=repo,text=True).splitlines()
 if not tracked:raise ValueError('source_not_in_registered_commit')
 hashes={}
 for name in tracked:
  p=repo/name
  if not p.is_file() or p.read_bytes()!=subprocess.check_output(['git','show',commit+':'+name],cwd=repo):raise ValueError('uncommitted_or_mismatched_source')
  hashes[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
 if any(str(p.relative_to(repo)) not in tracked for p in (ROOT/'src').glob('*.py')):raise ValueError('untracked_executable')
 return hashes
class Journal:
 def __init__(self,path,budget):self.path=path;self.budget=budget;self.sequence=0
 def append(self,event):
  self.sequence+=1
  with self.path.open('a') as f:f.write(json.dumps({'sequence':self.sequence,**event},separators=(',',':'))+'\n');f.flush()
 def call(self,backend,name,obs,index,context):
  timeout=self.budget.reserve(name);cid=f'{name}-{self.budget.attempts[name]}';started=time.monotonic()
  self.append({'type':'call_started','call_id':cid,'model':name,'observation':obs,'option_order_index':index,**context})
  try:
   result=backend.predict(obs,index,timeout)
   self.append({'type':'call_completed','call_id':cid,'seconds':round(time.monotonic()-started,4),**result})
   return result['label']
  except BaseException as e:
   self.append({'type':'call_failed','call_id':cid,'error_type':type(e).__name__,'seconds':round(time.monotonic()-started,4)})
   raise

def qualify(journal,backend,name):
 records=[]
 try:
  for i,x in enumerate(qualification()):
   obs={k:x[k] for k in ('claim','report')};label=journal.call(backend,name,obs,i,{'stage':'qualification','case':i});records.append({'case':i,'expected':x['expected'],'label':label})
 except Exception as e:return {'status':'failed','reason':type(e).__name__,'records':records}
 per={k:sum(r['label']==k for r in records if r['expected']==k)/20 for k in LABELS};accuracy=sum(r['label']==r['expected'] for r in records)/60
 return {'status':'passed' if accuracy>=.85 and min(per.values())>=.7 else 'failed','accuracy':accuracy,'per_label':per,'records':records}

def execute(out,receipt,algorithm_only=False):
 source=source_check(receipt['commit']);out.mkdir(parents=True,exist_ok=False);write(out/'plan-receipt.json',receipt)
 assignments=[{'id':f'{s}-{a}-{p}-{e}','seed':s,'arm':a,'policy':p,'scenario':e,'status':'planned'} for s in (8201,8202,8203) for a in ARMS for p in POLICIES for e in SCENARIOS]
 started=time.monotonic();budget=Budget(started+1800);journal=Journal(out/'calls.jsonl',budget)
 manifest={'experiment':'healing-helping-hands','status':'running','plan':receipt,'source_hashes':source,'python':sys.version,'platform':platform.platform(),'assignments':assignments,'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'model_stage':'exact-only' if algorithm_only else 'qualification-and-pilot'};write(out/'manifest.json',manifest)
 q=l=None;qual={};results=[]
 try:
  if not algorithm_only:
   for name,constructor in (('qwen',Qwen),('laya',Laya)):
    try:
     backend=constructor()
     if name=='qwen':q=backend
     else:l=backend
     manifest[name+'_metadata']=backend.metadata
     qual[name]=qualify(journal,backend,name)
    except Exception as e:qual[name]={'status':'failed','reason':'initialization_'+type(e).__name__}
    write(out/'qualification.json',qual);print(json.dumps({'qualification':name,**{k:v for k,v in qual[name].items() if k!='records'}}),flush=True)
  model_enabled=not algorithm_only and qual.get('qwen',{}).get('status')=='passed'
  laya_enabled=model_enabled and qual.get('laya',{}).get('status')=='passed'
  for seed in (8201,8202,8203):
   c=make(seed);write(out/f'corpus-{seed}.json',c);tapes={'exact':[d['label'] for d in c['docs']]};tape_failure=None
   if model_enabled:
    try:
     first=[journal.call(q,'qwen',observation(c,d),i,{'stage':'pilot','seed':seed,'agent':i,'head':'first'}) for i,d in enumerate(c['docs'])]
     tapes['qwen']=first;second=first[:];third=first[:]
     for i in c['heads']:
      obs=observation(c,c['docs'][i]);a=journal.call(q,'qwen',obs,i+1,{'stage':'pilot','seed':seed,'agent':i,'head':'independent-qwen'})
      second[i]=a if a==first[i] else 'UNCERTAIN'
     tapes['qwen+qwen']=second
     if laya_enabled:
      for i in c['heads']:
       b=journal.call(l,'laya',observation(c,c['docs'][i]),i+1,{'stage':'pilot','seed':seed,'agent':i,'head':'independent-laya'})
       third[i]=b if b==first[i] else 'UNCERTAIN'
      tapes['qwen+laya']=third
    except Exception as e:
     tape_failure=type(e).__name__;model_enabled=False;laya_enabled=False
     journal.append({'type':'tape_failed','seed':seed,'error_type':tape_failure})
   write(out/f'tapes-{seed}.json',tapes)
   for a in (a for a in assignments if a['seed']==seed):
    if a['arm'] not in tapes:
     a.update(status='not_run',reason=tape_failure or 'model_not_qualified');write(out/(a['id']+'.json'),a);continue
    try:
     if time.monotonic()>budget.deadline:raise TimeoutError('attempt_deadline')
     frames=[]
     def checkpoint(f):
      frames.append(f);write(out/'checkpoint.json',{'assignment':a,'frames':frames})
     result=rollout(c,tapes[a['arm']],a['policy'],a['scenario'],checkpoint)
     a['status']='completed';record={**a,**result};write(out/(a['id']+'.json'),record);results.append({**a,**result['metrics']})
     print(json.dumps({'world':a['id'],'accuracy':result['metrics']['final_accuracy'],'post_error':result['metrics']['post_event_error']}),flush=True)
    except Exception as e:
     a.update(status='failed',reason=type(e).__name__);write(out/(a['id']+'.json'),{**a,'frames':frames if 'frames' in locals() else []})
    write(out/'manifest.json',manifest);write(out/'summary.json',results)
  manifest['status']='completed' if all(a['status']=='completed' for a in assignments) else 'completed_with_unexecuted_or_failed_assignments'
 except BaseException as e:manifest.update(status='failed',failure_type=type(e).__name__)
 finally:
  if l:l.close()
  for a in assignments:
   if a['status']=='planned':a.update(status='not_run',reason='attempt_aborted');write(out/(a['id']+'.json'),a)
  manifest.update(seconds=round(time.monotonic()-started,3),calls=budget.attempts,qualification=qual)
  write(out/'manifest.json',manifest);write(out/'summary.json',results)
 return manifest
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--exact-only',action='store_true');p.add_argument('--run-tldr',required=True);a=p.parse_args()
 try:
  receipt=check('healing-helping-hands',a.run_tldr);m=execute(Path(a.out),receipt,a.exact_only);print(json.dumps({'status':m['status'],'calls':m['calls']}))
 except Exception as e:print('Launch failed: '+type(e).__name__);sys.exit(1)

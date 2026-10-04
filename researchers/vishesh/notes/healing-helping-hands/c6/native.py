"""One fail-closed C6 stage. Key enters memory through stdin only for paid stages."""
import argparse,fcntl,hashlib,json,math,os,sqlite3,sys,time,urllib.request
from pathlib import Path
from design import *
sys.path.insert(0,str(BASE/'src'))
from jev import request as jev_request,validate as jev_validate,RESERVE
from providers import QWEN_DIGEST

def write(path,value):
 p=path.with_suffix('.tmp');p.write_text(json.dumps(value,indent=2));p.replace(path)
def append(path,value):
 with path.open('a') as f:f.write(json.dumps(value)+'\n');f.flush();os.fsync(f.fileno())
def validate_admission(a,stage,now):
 required=('account_verified','exclusive_claim_verified','workload_verified','source_verified','public_plan_verified','scope_authorized')
 if any(a.get(k) is not True for k in required):raise ValueError('admission_missing')
 if a.get('stage')!=stage or not 0<=now-a.get('checked_epoch',0)<=300 or a.get('expires_epoch',0)<now+1200:raise ValueError('admission_stale')
 if a.get('plan_sha256')!=hashlib.sha256((HERE/'PLAN.md').read_bytes()).hexdigest():raise ValueError('plan_changed')
 if stage!='D0' and (a.get('cumulative_cap_usd')!=50. or a.get('c6_cap_usd')!=2. or a.get('budget_increase_approved') is not True or a.get('original_ledger_verified') is not True):raise ValueError('budget_authority_missing')
 if stage=='S1' and (a.get('qualification_review_complete') is not True or a.get('qualification_source')!=a.get('source_commit')):raise ValueError('qualification_review_required')
 return True

def haiku_validate(raw):
 if raw.get('model')!=HMODEL or raw.get('provider')!='Anthropic':raise ValueError('served_route_mismatch')
 choices=raw['choices']
 if len(choices)!=1 or choices[0]['finish_reason']!='stop':raise ValueError('invalid_completion')
 label=parse_label(choices[0]['message']['content']);u=raw['usage'];cost=u['cost']
 if isinstance(cost,bool) or not isinstance(cost,(int,float)) or not math.isfinite(cost) or cost<0:raise ValueError('invalid_cost')
 if not isinstance(u['prompt_tokens'],int) or not 0<u['prompt_tokens']<=4096 or not 0<=u['completion_tokens']<=32:raise ValueError('invalid_tokens')
 # Provider cache metadata is retained via usage; never infer a zero cost from absence.
 return {'label':label,'cost_usd':cost,'input_tokens':u['prompt_tokens'],'output_tokens':u['completion_tokens'],'served_model':raw['model'],'provider':raw['provider']}
def reserve(db,h,amount,stage):
 if not math.isfinite(amount) or amount<=0:raise ValueError('invalid_reservation')
 db.execute('BEGIN IMMEDIATE')
 try:
  n,total=db.execute('SELECT count(*),coalesce(sum(CASE WHEN status="completed" THEN cost ELSE reserved/1000000000.0 END),0) FROM calls').fetchone()
  own,count=db.execute('SELECT coalesce(sum(CASE WHEN c.status="completed" THEN c.cost ELSE c.reserved/1000000000.0 END),0),count(*) FROM calls c JOIN c6_hashes h ON h.hash=c.hash').fetchone()
  sn=db.execute('SELECT count(*) FROM c6_hashes WHERE stage=?',(stage,)).fetchone()[0]
  if n<2731 or n>=4208 or count>=1477 or sn>=(180 if stage.endswith('S0') else 1296) or total+amount>50. or own+amount>2.:raise ValueError('budget_exhausted')
  db.execute('INSERT INTO calls(hash,reserved,status) VALUES(?,?,?)',(h,math.ceil(amount*1e9),'started'));db.execute('INSERT INTO c6_hashes VALUES(?,?)',(h,stage));db.commit()
 except BaseException:db.rollback();raise
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):raise ValueError('redirect_refused')
def run(stage,out,admission,ledger=None,parent=None):
 a=json.loads(admission.read_text());validate_admission(a,stage,time.time())
 approval=json.loads((HERE/'owner-approval.json').read_text())
 if approval.get('status')!='approved' or approval.get('plan_sha256')!=a['plan_sha256'] or approval.get('cumulative_cap_usd')!=50 or approval.get('attempt_cap_usd')!=2:raise ValueError('owner_receipt_mismatch')
 if out.exists():raise ValueError('duplicate_attempt')
 import subprocess
 root=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=HERE,text=True).strip())
 hashes={}
 for path in [*HERE.glob('*.py'),BASE/'c5/scenarios.py',BASE/'c5/contract.py',BASE/'c4/scenarios.py',BASE/'src/jev.py',BASE/'src/providers.py']:
  rel=str(path.relative_to(root));saved=subprocess.check_output(['git','show',a['source_commit']+':'+rel],cwd=root)
  if saved!=path.read_bytes():raise ValueError('source_mismatch')
  hashes[rel]=hashlib.sha256(saved).hexdigest()
 sys.path.insert(0,str(BASE.parent/'experiment-documentation'));from public_plan import check
 receipt=check('healing-helping-hands',f'TLDR: C6-{stage} bounded label-collapse diagnosis or Jev–Haiku agreement comparison; class accuracy, wrong agreement and actual cost on authored synthetic fixtures.')
 if receipt['plan_sha256']!=a['plan_sha256'] or receipt['commit']!=a['source_commit'] or not receipt['url'].endswith('/c6/PLAN.md'):raise ValueError('registration_mismatch')
 db=None;lock=None;key=None
 if stage=='D0':
  with urllib.request.urlopen('http://127.0.0.1:11434/api/tags',timeout=10) as r:models=json.load(r)['models']
  if not any(x['name']=='qwen3:0.6b' and x['digest']==QWEN_DIGEST for x in models):raise ValueError('qwen_digest')
 else:
  if stage=='S1':
   if parent is None:raise ValueError('parent_required')
   previous=json.loads((parent/'observations.json').read_text());pm=json.loads((parent/'manifest.json').read_text())
   if not qualification(previous)['qualified'] or pm['source_hashes']!=hashes:raise ValueError('not_qualified')
  for model,provider,inp,outprice in [('anthropic/claude-haiku-4.5','Anthropic',1e-6,5e-6),('typesafe/jev-1.13','TypeSafe',.000000042,0)]:
   with urllib.request.urlopen('https://openrouter.ai/api/v1/models/'+model+'/endpoints',timeout=20) as response:routes=json.load(response)['data']['endpoints']
   matched=[x for x in routes if x['provider_name']==provider and x['status']==0]
   if len(matched)!=1 or (HSNAPSHOT if provider=='Anthropic' else 'typesafe/jev-1.13-20260917') not in matched[0]['name'] or float(matched[0]['pricing']['prompt'])>inp or float(matched[0]['pricing']['completion'])>outprice:raise ValueError('route_price_changed')
  if ledger is None or not ledger.is_file():raise ValueError('original_ledger_required')
  lock=ledger.with_suffix('.writer.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  db=sqlite3.connect(ledger);db.execute('CREATE TABLE IF NOT EXISTS c6_hashes(hash TEXT PRIMARY KEY,stage TEXT NOT NULL)');db.commit()
  key=sys.stdin.readline().strip()
  if not key:raise ValueError('credential_missing')
 out.mkdir(parents=True,exist_ok=False);rows=cases(stage);write(out/'observations.json',rows)
 sys.path.insert(0,str(BASE/'practical'));from reporting import Reporter
 import swarm_report as sdk
 reporter=Reporter(sdk,'healing-helping-hands','healing-helping-hands/C6-'+stage,out/'reporting.jsonl')
 reporter.emit('start',url=receipt['url'],params={'attempt_id':'C6','stage':stage,'arm':'haiku+jev'},message=f'TLDR: C6-{stage} uses Haiku4.5 and Jev; '+('60 balanced competence cases before automatic evaluation.' if stage=='S0' else '432 synthetic cases: agreement referral versus single Haiku, always-Jev and same-count random, measuring absolute error and actual total cost.'))
 m={'attempt':'C6R1-'+stage,'stage':stage,'status':'running','calls':0,'source_commit':a['source_commit'],'source_hashes':hashes,'plan':receipt,'host':a['host'],'claim':a['claim_id'],'started_epoch':time.time()};write(out/'manifest.json',m)
 opener=urllib.request.build_opener(NoRedirect());deadline=time.monotonic()+(900 if stage=='D0' else 3600)
 try:
  for i,r in enumerate(rows):
   conditions=[(p,d) for p in ('original','simple') for d in ('schema','text')] if stage=='D0' else [('haiku',0),('haiku',1),('jev',None)]
   conditions=conditions[i%len(conditions):]+conditions[:i%len(conditions)]
   r['status']='running';r['labels']={}
   for x,y in conditions:
    if time.monotonic()>deadline or time.time()>a['expires_epoch']-120:raise ValueError('deadline')
    model='qwen' if stage=='D0' else x;variant=x+'/'+y if stage=='D0' else ('jev' if x=='jev' else ('a' if y==0 else 'b'))
    payload=qwen(r,x,y) if stage=='D0' else (haiku(r,y) if x=='haiku' else jev_request(r,i,'C6R1-'+stage))
    h=sha({'attempt':'C6R1-'+stage,'row':r['id'],'variant':variant,'payload':payload});start=time.time();m['calls']+=1
    append(out/'calls.jsonl',{'type':'start','id':h,'row_id':r['id'],'model':model,'variant':variant,'payload':payload,'epoch':start})
    amount=0 if model=='qwen' else (conservative_haiku_cost(payload) if model=='haiku' else RESERVE)
    if db:reserve(db,h,amount,'C6R1-'+stage)
    url='http://127.0.0.1:11434/api/chat' if model=='qwen' else 'https://openrouter.ai/'+('api/v1/chat/completions' if model=='haiku' else 'api/alpha/decisions')
    headers={'Content-Type':'application/json'}
    if key:headers['Authorization']='Bearer '+key
    try:
     with opener.open(urllib.request.Request(url,json.dumps(payload,separators=(',',':')).encode(),headers),timeout=min(90,max(1,deadline-time.monotonic()))) as response:raw=json.load(response)
     safe={k:raw[k] for k in (('model','message','done_reason','prompt_eval_count','eval_count') if model=='qwen' else ('model','provider','choices','answers','usage','id')) if k in raw}
     append(out/'calls.jsonl',{'type':'response','id':h,'raw':safe,'epoch':time.time(),'seconds':time.time()-start})
     if model=='qwen':
      try:result={'label':parse_label(raw['message']['content']),'cost_usd':0}
      except (ValueError,KeyError,TypeError):result={'label':None,'cost_usd':0,'invalid_output':True}
     else:
      result=haiku_validate(raw) if model=='haiku' else jev_validate(raw)
      if result['cost_usd']>amount:raise ValueError('reservation_exceeded')
      with db:db.execute('UPDATE calls SET status="completed",cost=? WHERE hash=?',(result['cost_usd'],h))
     r['labels'][variant]=result['label'];append(out/'calls.jsonl',{'type':'completed','id':h,'result':result})
    except BaseException as e:
     append(out/'calls.jsonl',{'type':'failed','id':h,'error_type':type(e).__name__,**({'http_status':e.code} if hasattr(e,'code') else {})});raise
   r['status']='completed';write(out/'observations.json',rows)
   if (i+1)%10==0 or i+1==len(rows):reporter.emit('metric',step=i+1,metrics={'completed_cases':i+1,'assigned_cases':len(rows),'model_calls':m['calls']})
  m['status']='completed'
 except BaseException as e:m.update(status='failed',error_type=type(e).__name__)
 finally:
  for r in rows:
   if r.get('status')=='running':r['status']='failed'
   elif r.get('status')!='completed':r['status']='not_run'
  m['ended_epoch']=time.time();write(out/'observations.json',rows);write(out/'manifest.json',m)
  if stage=='S0':write(out/'qualification.json',qualification(rows))
  if stage=='S1':write(out/'summary.json',score(rows))
  if db:db.close();lock.close()
 reporter.emit('metric' if m['status']=='completed' else 'fail',metrics={'completed_cases':sum(r['status']=='completed' for r in rows),'assigned_cases':len(rows),'model_calls':m['calls']},message='Native collection terminal; scientific review and cost reconciliation follow.')
 print(json.dumps({'status':m['status'],'stage':stage,'calls':m['calls']}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--stage',choices=['S0','S1'],required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--admission',type=Path,required=True);p.add_argument('--ledger',type=Path);p.add_argument('--parent',type=Path);a=p.parse_args()
 try:run(a.stage,a.out,a.admission,a.ledger,a.parent)
 except Exception as e:print(json.dumps({'launch_failed':type(e).__name__}));raise SystemExit(1)

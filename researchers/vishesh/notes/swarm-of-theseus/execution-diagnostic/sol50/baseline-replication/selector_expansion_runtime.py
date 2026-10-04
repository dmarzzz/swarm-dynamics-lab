"""Funded R3 successor: independent prefix replay, atomic original ledger, bounded concurrency."""
import argparse,copy,hashlib,hmac,json,os,socket,sqlite3,subprocess,threading,time,urllib.request,urllib.error
from pathlib import Path
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor,as_completed
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import admission as a,contract as c,engine,turnover,selection_v2 as selection
from q3_relay import NoRedirect,safe_http_error
from q3_runner import parse,write_new
FUND=None;CAPS={'Q3-A3':(108,Decimal('2.4462')),'P1':(828,Decimal('18.7542'))}
MANIFEST='1df610bd4704f23b3044fc3de8adafaa88cc472fff5de2041d1af5ca58d817f6'
FAMILIES=('release','failover','delegation')

def assignments(packet,stage):
 if stage=='Q3-A3':return {stage+'-'+x['family']:(x['family'],x['world']) for x in packet['assignments']['Q3-A2' if stage=='Q3-A3' else stage]}
 if stage=='P1':return {stage+'-'+x['family']+'-r'+str(rep):(x['family'],x['world']) for x in packet['assignments']['Q3-A2' if stage=='Q3-A3' else stage] for rep in x['repeats']}
 raise ValueError('unfunded_stage')

class Expected(Exception):
 def __init__(self,value):self.value=value

def next_request(stage,family,world,history):
 index=0
 def call(fam,phase,packet,condition):
  nonlocal index
  value={'family':fam,'phase':phase,'condition':condition,'packet':packet,'request':selection.wire(phase,fam,packet)}
  if index==len(history):raise Expected(value)
  answer=copy.deepcopy(history[index]);index+=1;return selection.to_engine(phase,answer)
 try:result=engine.qualify_world(world,family,call) if stage=='Q3-A3' else turnover.trajectory(world,family,call)
 except Expected as request:return request.value,None
 if index!=len(history):raise ValueError('response_prefix_excess')
 return None,result

def admit(r,packet):
 now=time.time()
 if not str(r.get('funding_decision','')).startswith('PI-FUND-20261004-') or not r.get('D1_pass_verified') or not r.get('D1_cost_reconciled'):raise ValueError('named_funding_D1_gate')
 expected={'funding_decision':r.get('funding_decision'),'funding_status':'reserved','prior_exposure_usd':r.get('prior_exposure_usd'),'all_in_cap_usd':'21.2804','hosting_cap_usd':'0.08','Q3_max_calls':108,'P1_max_calls':828,'retry_count':0,'source_sha256':a.source_hash(),'manifest_sha256':MANIFEST}
 if any(r.get(k)!=v for k,v in expected.items()):raise ValueError('admission_contract')
 if a.digest(packet)!=MANIFEST:raise ValueError('manifest')
 if not 0<=now-r['verified_epoch']<=900 or not now<r['deadline']<=min(r['claim_start']+3000,1791155100):raise ValueError('deadline')
 if Decimal(str(r['hourly_usd']))*Decimal(3000)/Decimal(3600)>Decimal('.08'):raise ValueError('hosting')
 if subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.ROOT,text=True).strip()!=r['source_commit']:raise ValueError('source')
 for k in ('account_verified','exclusive_claim_verified','host_idle_verified','runtime_verified','controller_verified','public_pages_verified','route_pricing_verified','original_ledger_verified'):
  if r.get(k) is not True:raise ValueError('missing_'+k)
 for stage in CAPS:
  if r['plans'][stage]['sha256']!=hashlib.sha256((a.ROOT/'Q3-A3-P1-PLAN.md').read_bytes()).hexdigest():raise ValueError('plan_hash')
 return True

def public_check(r):
 def get(url):
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Theseus-R3','Cache-Control':'no-cache'}),timeout=25) as s:data=s.read(10000001)
  if len(data)>10000000:raise ValueError('public_bound')
  return data
 state=json.loads(get('https://swarm-live.pages.dev/api/state'))
 for stage,p in r['plans'].items():
  if stage not in CAPS:raise ValueError('unfunded_plan')
  e=next((x for x in state['experiments'] if x['id']==p['experiment']),{})
  if e.get('url')!=p['url'] or not e.get('description','').startswith('TLDR: '):raise ValueError('public_registration')
  if hashlib.sha256(get(p['url'].replace('github.com','raw.githubusercontent.com').replace('/blob/','/'))).hexdigest()!=p['sha256']:raise ValueError('public_hash')
 return True

class Ledger:
 def __init__(self,path,local):
  self.path=str(path)
  if not Path(path).is_file():raise ValueError('original_ledger_missing')
  with self.connect() as db:
   table='calls' if local else 'sol50_calls';n,cost,unknown=db.execute(f'SELECT count(*),sum(actual_usd),sum(case when actual_usd is null then reserved_usd else 0 end) FROM {table}').fetchone()
   if n!=44 or abs(cost-.122835)>1e-9 or unknown!=0:raise ValueError('old_ledger')
   rows=db.execute('SELECT stage,reserved,actual,status FROM r3_calls ORDER BY stage').fetchall()
   if rows!=[('C1','0.02265','0.000172','terminal'),('Q3','0.02265',None,'ambiguous')]:raise ValueError('old_uncertainty')
   db.execute('CREATE TABLE IF NOT EXISTS r3_successor(id TEXT PRIMARY KEY,stage TEXT,trajectory TEXT,seq INTEGER,reserved TEXT,actual TEXT,status TEXT,answer TEXT,seconds REAL,UNIQUE(trajectory,seq))')
 def connect(self):return sqlite3.connect(self.path,timeout=30)
 def history(self,trajectory):
  with self.connect() as db:rows=db.execute('SELECT status,answer FROM r3_successor WHERE trajectory=? ORDER BY seq',(trajectory,)).fetchall()
  if any(s!='terminal' or v is None for s,v in rows):raise ValueError('incomplete_prefix')
  return [json.loads(v) for _,v in rows]
 def reserve(self,stage,trajectory,seq):
  if stage not in CAPS:raise ValueError('unfunded_stage')
  with self.connect() as db:
   db.execute('BEGIN IMMEDIATE');n,total=db.execute('SELECT count(*),coalesce(sum(cast(reserved as real)),0) FROM r3_successor WHERE stage=?',(stage,)).fetchone()
   if n>=CAPS[stage][0] or Decimal(n+1)*c.PER_CALL>CAPS[stage][1]:raise ValueError('stage_cap')
   if db.execute('SELECT count(*) FROM r3_successor WHERE trajectory=?',(trajectory,)).fetchone()[0]!=seq:raise ValueError('sequence')
   ident=trajectory+'-'+str(seq).zfill(4);db.execute('INSERT INTO r3_successor VALUES(?,?,?,?,?,?,?,?,?)',(ident,stage,trajectory,seq,str(c.PER_CALL),None,'reserved',None,None))
  return ident
 def settle(self,ident,cost,answer=None,seconds=None):
  if cost is not None and (type(cost) not in (int,float) or not 0<=cost<=float(c.PER_CALL)):raise ValueError('cost_bound')
  with self.connect() as db:
   if db.execute('SELECT status FROM r3_successor WHERE id=?',(ident,)).fetchone()!=('reserved',):raise ValueError('terminal_or_absent')
   db.execute('UPDATE r3_successor SET actual=?,status=?,answer=?,seconds=? WHERE id=?',(None if cost is None else str(cost),'ambiguous' if cost is None else 'terminal',None if answer is None else json.dumps(answer),seconds,ident))
 def summary(self):
  with self.connect() as db:rows=db.execute('SELECT stage,reserved,actual,status,seconds FROM r3_successor').fetchall()
  return {stage:{'started':sum(s==stage for s,_,_,_,_ in rows),'actual_usd':str(sum((Decimal(v) for s,_,v,_,_ in rows if s==stage and v is not None),Decimal(0))),'unknown_usd':str(sum((Decimal(r) for s,r,v,_,_ in rows if s==stage and v is None),Decimal(0))),'seconds':[t for s,_,_,_,t in rows if s==stage and t is not None]} for stage in CAPS}

class Validator:
 def __init__(self,packet,ledger):self.packet=packet;self.ledger=ledger
 def qualified(self):
  for family,w in assignments(self.packet,'Q3-A3').values():
   nxt,result=next_request('Q3-A3',family,w,self.ledger.history('Q3-A3-'+family))
   if nxt is not None or not result['passed']:return False
  return True
 def check(self,p):
  stage=p['stage'];trajectory=p['trajectory'];assignment=assignments(self.packet,stage)
  if trajectory not in assignment:raise ValueError('assignment')
  family,w=assignment[trajectory]
  if stage=='P1':
   if not self.qualified():raise ValueError('Q3_gate')
  else:
   for prior in FAMILIES[:FAMILIES.index(family)]:
    old=assignments(self.packet,stage)[stage+'-'+prior];n,r=next_request(stage,*old,self.ledger.history(stage+'-'+prior))
    if n is not None or not r['passed']:raise ValueError('family_gate')
  history=self.ledger.history(trajectory)
  if p['seq']!=len(history):raise ValueError('sequence')
  expected,result=next_request(stage,family,w,history)
  if expected is None or p.get('call')!=expected:raise ValueError('unexpected_actor_request')
  return expected['request']

def serve(receipt,manifest,ledger,credential,capability):
 r=json.loads(Path(receipt).read_text());packet=json.loads(Path(manifest).read_text());admit(r,packet);public_check(r);l=Ledger(ledger,True)
 with l.connect() as db:
  if db.execute("SELECT count(*) FROM r3_successor WHERE stage IN ('Q3-A3','P1')").fetchone()[0]:raise ValueError('already_started_no_resume')
  old=db.execute("SELECT count(*),sum(cast(actual AS real)) FROM r3_successor WHERE stage='Q3-A2' AND status='terminal'").fetchone()
  if old[0]!=69 or abs(old[1]-.169662)>1e-9:raise ValueError('predecessor_lineage')
 from d1_runtime import expected as diagnostic
 from selection_diagnostic import run as diagnostic_run
 packet_d1=json.loads(Path(r['D1_packet_path']).read_text())
 next_d1,result_d1=diagnostic(packet_d1,l.history('D1-A1'))
 if next_d1 is not None or not result_d1['passed']:raise ValueError('D1_native_gate')
 keypath=Path(credential)
 if keypath.is_symlink() or keypath.stat().st_mode&0o077:raise ValueError('credential_metadata')
 key=keypath.read_text().strip();cap=Path(capability).read_text().strip()
 if not key or len(cap)<32:raise ValueError('credential_empty')
 stop=threading.Event();dispatch=threading.Lock();locks={k:threading.Lock() for stage in CAPS for k in assignments(packet,stage)};validator=Validator(packet,l)
 class Handler(BaseHTTPRequestHandler):
  def log_message(self,*args):pass
  def do_POST(self):
   ident=None;cost=None;answer=None;result={'error':'rejected','actual_usd':None};started=time.time()
   try:
    if self.path!='/next' or not hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+cap):raise ValueError('authorization')
    size=int(self.headers.get('Content-Length',0))
    if not 0<size<=24000:raise ValueError('payload_bound')
    p=json.loads(self.rfile.read(size))
    if p.get('source_sha256')!=r['source_sha256'] or p.get('manifest_sha256')!=MANIFEST or p.get('trajectory') not in locks:raise ValueError('source_manifest')
    with locks[p['trajectory']]:
     with dispatch:
      if stop.is_set() or time.time()>=r['deadline'] or Path(str(ledger)+'.selector-v2-stop').exists():raise ValueError('shared_stop')
      body=validator.check(p);ident=l.reserve(p['stage'],p['trajectory'],p['seq'])
     request=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',json.dumps(body,separators=(',',':')).encode(),{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
     with urllib.request.build_opener(NoRedirect()).open(request,timeout=min(150,max(1,r['deadline']-time.time()))) as response:raw=response.read(1000001)
     if len(raw)>1000000:raise ValueError('response_bound')
     value=json.loads(raw);cost=value.get('usage',{}).get('cost')
     if type(cost) not in (int,float) or not 0<=cost<=float(c.PER_CALL):cost=None;raise ValueError('cost_bound')
     result={'error':None,'actual_usd':cost,'response':value};answer=parse(result)
   except urllib.error.HTTPError as error:
    diagnostic=safe_http_error(error);result={'error':'http_'+str(diagnostic['http_status']),'actual_usd':None,'diagnostic':diagnostic};stop.set()
   except Exception as error:
    result.update(error=type(error).__name__,actual_usd=cost);stop.set()
   finally:
    if ident is not None:l.settle(ident,cost,answer,time.time()-started)
   encoded=json.dumps(result).encode();self.send_response(200);self.send_header('Content-Length',str(len(encoded)));self.end_headers()
   try:self.wfile.write(encoded)
   except (BrokenPipeError,ConnectionResetError):stop.set()
 server=ThreadingHTTPServer(('127.0.0.1',19065),Handler);server.timeout=1;print(json.dumps({'status':'ready'}),flush=True)
 try:
  while time.time()<r['deadline'] and not Path(str(ledger)+'.selector-v2-stop').exists():server.handle_request()
 finally:stop.set();server.server_close()

class Calls:
 def __init__(self,stage,trajectory,root,r,ledger,stop):self.stage=stage;self.trajectory=trajectory;self.root=root;self.r=r;self.ledger=ledger;self.stop=stop;self.seq=0
 def __call__(self,family,phase,packet,condition):
  if self.stop.is_set() or time.time()>=self.r['deadline']:raise ValueError('shared_stop')
  call={'family':family,'phase':phase,'packet':packet,'condition':condition,'request':selection.wire(phase,family,packet)};ident=self.ledger.reserve(self.stage,self.trajectory,self.seq)
  payload={'stage':self.stage,'trajectory':self.trajectory,'seq':self.seq,'call':call,'source_sha256':self.r['source_sha256'],'manifest_sha256':MANIFEST};self.seq+=1;write_new(self.root/(ident+'-request.json'),payload);started=time.time();cost=None;answer=None;result=None
  try:
   req=urllib.request.Request('http://127.0.0.1:19066/next',json.dumps(payload).encode(),{'Authorization':'Bearer '+os.environ['THESEUS_V2_CAPABILITY'],'Content-Type':'application/json'})
   with urllib.request.urlopen(req,timeout=min(180,max(1,self.r['deadline']-time.time()))) as response:result=json.load(response)
   write_new(self.root/(ident+'-response.json'),result);cost=result.get('actual_usd')
   if type(cost) not in (int,float) or not 0<=cost<=float(c.PER_CALL):cost=None;raise ValueError('unknown_usage')
   if result.get('error'):raise ValueError('provider_error')
   answer=parse(result);return selection.to_engine(phase,answer)
  except Exception:
   self.stop.set();raise
  finally:self.ledger.settle(ident,cost,answer,time.time()-started)

def run(receipt,manifest,ledger,output):
 r=json.loads(Path(receipt).read_text());packet=json.loads(Path(manifest).read_text());admit(r,packet);public_check(r);l=Ledger(ledger,False);root=Path(output)
 if socket.gethostname().split('.')[0]!=r['host']:raise ValueError('host')
 if root.exists():raise ValueError('already_started_no_resume')
 root.mkdir();write_new(root/'manifest.json',{'receipt':r,'packet':packet});stop=threading.Event();results={}
 import sys;sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
 def trajectory(stage,ident,assignment):
  folder=root/ident;folder.mkdir();caller=Calls(stage,ident,folder,r,l,stop);family,w=assignment;result=None;error=None;p=r['plans'][stage]
  try:
   for kind in ('plan','start'):
    if not sr.report(kind,p['experiment'],ident,message=p['tldr']+' Condition:'+ident,url=p['url'],strict=True):raise ValueError('reporting')
   result=engine.qualify_world(w,family,caller) if stage=='Q3-A3' else turnover.trajectory(w,family,caller)
   write_new(folder/'results.json',result)
   if not result.get('passed' if stage=='Q3-A3' else 'complete'):stop.set()
  except Exception as exc:error=type(exc).__name__;stop.set()
  finally:
   terminal={'stage':stage,'trajectory':ident,'started_calls':caller.seq,'error':error,'complete':bool(result and result.get('passed' if stage=='Q3-A3' else 'complete')),'retries':0};write_new(folder/'terminal.json',terminal)
   sr.report('done' if terminal['complete'] else 'fail',p['experiment'],ident,message='Trajectory terminal; scientific interpretation pending.',metrics={'started_calls':caller.seq,'complete':int(terminal['complete'])},strict=True)
  return terminal
 try:
  for ident,assignment in assignments(packet,'Q3-A3').items():
   results[ident]=trajectory('Q3-A3',ident,assignment)
   if stop.is_set():break
  qualified=len(results)==3 and all(x['complete'] for x in results.values());write_new(root/'Q3-gate.json',{'qualified':qualified,'trajectories':results.copy()})
  if qualified:
   times=l.summary()['Q3-A3']['seconds'];ordered=sorted(times);p90=ordered[min(len(ordered)-1,int(len(ordered)*.9))];expected=138*max(p90,1)*1.25
   feasible=time.time()+expected<r['deadline'];write_new(root/'P1-feasibility.json',{'observed_Q3_calls':len(times),'p90_seconds':p90,'projected_six_parallel_seconds':expected,'remaining_seconds':r['deadline']-time.time(),'admitted':feasible})
   if feasible:
    with ThreadPoolExecutor(max_workers=6) as pool:
     pending={pool.submit(trajectory,'P1',ident,w):ident for ident,w in assignments(packet,'P1').items()}
     for future in as_completed(pending):results[pending[future]]=future.result()
 finally:write_new(root/'terminal.json',{'results':results,'ledger':l.summary(),'worker_terminal':True,'automatic_P2':False,'scientific_review':'required'})
 return {'trajectories':len(results),'completed':sum(x['complete'] for x in results.values()),'ledger':l.summary()}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['relay','worker'])
 for key in ('receipt','manifest','ledger','credential','capability','output'):p.add_argument('--'+key)
 x=p.parse_args()
 try:
  if x.mode=='relay':serve(x.receipt,x.manifest,x.ledger,x.credential,x.capability)
  else:print(json.dumps(run(x.receipt,x.manifest,x.ledger,x.output)))
 except Exception as error:print(json.dumps({'blocked':True,'safe_error':type(error).__name__}));raise SystemExit(1)

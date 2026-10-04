"""Adaptive five-prefix continuation; old requests are replayed locally, never rebilled."""
import argparse,copy,hashlib,hmac,json,os,socket,subprocess,threading,time,urllib.request,urllib.error
from pathlib import Path
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor,as_completed
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import admission as a,selector_expansion_runtime as x,turnover
from q3_relay import NoRedirect,safe_http_error
from q3_runner import parse,write_new
ELIGIBLE={'P1-release-r0': 26, 'P1-release-r1': 24, 'P1-failover-r1': 26, 'P1-delegation-r0': 26, 'P1-delegation-r1': 26}
PREFIXES={'P1-release-r0': {'count': 26, 'sha256': '5d44aeaf8b03422806fec0a1b7ed877fc3307ed3071b9e49ca254047cc911aa6'}, 'P1-release-r1': {'count': 24, 'sha256': 'f8d278a654ed95e6a459ad21b63409d52daf8a92b1cbc92e6a2c1602664d963b'}, 'P1-failover-r1': {'count': 26, 'sha256': '2bd6dfd8f597b75f622e4060d99930c68f3f4fff26e75a407d5531ee0c453b3b'}, 'P1-delegation-r0': {'count': 26, 'sha256': 'da47ae0a345f51f73598a118f8b2285dff5720ef1bd321f4ad82d193879808de'}, 'P1-delegation-r1': {'count': 26, 'sha256': '8d541a9165a5f6147294001c4958054a3a6850d81d88a85a9170b1d2bd2911c3'}, 'P1-failover-r0': {'count': 24, 'sha256': '44dabea1ce8eb17f7f40717967219b75224c795ccbac6913ded4bbf35cab9a4c'}}
SCIENCE={'contract.py': 'a6e9414e0fa5139fb90ad654e34e273ef56c966657d631bccdb81b0ec4c4554d', 'engine.py': '6dfeccb8cc0e02cd5c44488c89f383a01dbbe77b29f6da6eb87ad36c0ec5e6d1', 'turnover.py': 'f4f6fd5d03c2ba5617df147b9cf8bf9c96a41ebdbaa47aa2c90242638bc3503b', 'families.py': '72868ffe2f9f930e44f1fde8a80e58d1d181bdf3b25eb2b19e48fde8ace8fbe6', 'selection_v2.py': 'bc0a08059aa7612ba1a9dc9e02052989cb12fdd57516b6042046b97fb1b57643'}
x.CAPS['C2']=(562,Decimal('12.7293'))

def admit(r,packet):
 now=time.time()
 if not str(r.get('funding_decision','')).startswith('PI-FUND-20261004-') or r.get('funding_status')!='reserved':raise ValueError('unfunded')
 for k,v in {'prior_exposure_usd':'1.9348455770333333','all_in_cap_usd':'12.7693','api_cap_usd':'12.7293','hosting_cap_usd':'0.04','call_cap':562,'retry_count':0,'source_sha256':a.source_hash(),'manifest_sha256':x.MANIFEST}.items():
  if r.get(k)!=v:raise ValueError('admission_'+k)
 if a.digest(packet)!=x.MANIFEST:raise ValueError('manifest')
 if not 0<=now-r['verified_epoch']<=900 or not now<r['deadline']<=min(r['claim_start']+1800,1791155700):raise ValueError('deadline')
 if Decimal(str(r['hourly_usd']))/2>Decimal('.04'):raise ValueError('hosting')
 if subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.ROOT,text=True).strip()!=r['source_commit']:raise ValueError('source')
 for n,h in SCIENCE.items():
  if hashlib.sha256((a.ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('scientific_dependency_changed')
 for k in ('account_verified','exclusive_claim_verified','host_idle_verified','runtime_verified','public_pages_verified','route_pricing_verified','original_ledger_verified','prefix_replay_verified','old_worker_transport_stopped'):
  if r.get(k) is not True:raise ValueError('missing_'+k)
 if r['plans']['C2']['sha256']!=hashlib.sha256((a.ROOT/'CONTINUATION-PLAN.md').read_bytes()).hexdigest():raise ValueError('plan')
 return True

def validate_prefixes(packet,l):
 with l.connect() as db:
  for stage,count,cost in [('Q3-A2',69,'.169662'),('D1',6,'.0118329'),('Q3-A3',103,'.2069325'),('P1',152,'.330186')]:
   rows=db.execute('SELECT actual,status FROM r3_successor WHERE stage=?',(stage,)).fetchall()
   if len(rows)!=count or any(status!='terminal' or v is None for v,status in rows) or sum((Decimal(v) for v,status in rows),Decimal(0))!=Decimal(cost):raise ValueError('original_lineage')
  if db.execute("SELECT count(*) FROM r3_successor WHERE stage='C2'").fetchone()[0]:raise ValueError('C2_already_started')
 calls={}
 for ident,bound in PREFIXES.items():
  history=l.history(ident)
  if len(history)!=bound['count'] or a.digest(history)!=bound['sha256']:raise ValueError('prefix_changed')
  family,w=x.assignments(packet,'P1')[ident];expected_calls=[]
  for i in range(len(history)):
   wanted,_=x.next_request('P1',family,w,history[:i]);expected_calls.append(wanted)
  nxt,result=x.next_request('P1',family,w,history)
  if ident in ELIGIBLE:
   if nxt is None or len(history)!=ELIGIBLE[ident]:raise ValueError('eligible_prefix')
  elif nxt is not None or result.get('stop')!='initial_gate' or result['complete']:raise ValueError('failed_prefix_not_preserved')
  calls[ident]=expected_calls
 return calls

class Validator:
 def __init__(self,packet,l):self.packet=packet;self.l=l
 def check(self,p):
  ident=p['trajectory']
  if p.get('stage')!='C2' or ident not in ELIGIBLE:raise ValueError('not_eligible')
  history=self.l.history(ident)
  if p['seq']!=len(history) or p['seq']<ELIGIBLE[ident]:raise ValueError('old_or_duplicate_call')
  family,w=x.assignments(self.packet,'P1')[ident];wanted,_=x.next_request('P1',family,w,history)
  if wanted is None or wanted!=p['call']:raise ValueError('unexpected_actor_request')
  return wanted['request']

class Calls(x.Calls):
 def __init__(self,ident,root,r,l,stop,prefix_calls):
  super().__init__('C2',ident,root,r,l,stop);self.old=l.history(ident);self.prefix_calls=prefix_calls;self.replay_index=0;self.seq=len(self.old)
 def __call__(self,family,phase,packet,condition):
  if self.replay_index<len(self.old):
   call={'family':family,'phase':phase,'packet':packet,'condition':condition,'request':x.selection.wire(phase,family,packet)}
   if call!=self.prefix_calls[self.replay_index]:raise ValueError('cached_request_changed')
   answer=self.old[self.replay_index];self.replay_index+=1;return x.selection.to_engine(phase,answer)
  return super().__call__(family,phase,packet,condition)
def serve(receipt,manifest,ledger,credential,capability):
 r=json.loads(Path(receipt).read_text());packet=json.loads(Path(manifest).read_text());admit(r,packet);x.public_check(r);l=x.Ledger(ledger,True)
 validate_prefixes(packet,l)
 keypath=Path(credential)
 if keypath.is_symlink() or keypath.stat().st_mode&0o077:raise ValueError('credential_metadata')
 key=keypath.read_text().strip();cap=Path(capability).read_text().strip()
 if not key or len(cap)<32:raise ValueError('credential_empty')
 stop=threading.Event();dispatch=threading.Lock();locks={k:threading.Lock() for k in ELIGIBLE};validator=Validator(packet,l)
 class Handler(BaseHTTPRequestHandler):
  def log_message(self,*args):pass
  def do_POST(self):
   ident=None;cost=None;answer=None;result={'error':'rejected','actual_usd':None};started=time.time()
   try:
    if self.path!='/next' or not hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+cap):raise ValueError('authorization')
    size=int(self.headers.get('Content-Length',0))
    if not 0<size<=24000:raise ValueError('payload_bound')
    p=json.loads(self.rfile.read(size))
    if p.get('source_sha256')!=r['source_sha256'] or p.get('manifest_sha256')!=x.MANIFEST or p.get('trajectory') not in locks:raise ValueError('source_manifest')
    with locks[p['trajectory']]:
     with dispatch:
      if stop.is_set() or time.time()>=r['deadline'] or Path(str(ledger)+'.C2-stop').exists():raise ValueError('shared_stop')
      body=validator.check(p);ident=l.reserve(p['stage'],p['trajectory'],p['seq'])
     request=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',json.dumps(body,separators=(',',':')).encode(),{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
     with urllib.request.build_opener(NoRedirect()).open(request,timeout=min(150,max(1,r['deadline']-time.time()))) as response:raw=response.read(1000001)
     if len(raw)>1000000:raise ValueError('response_bound')
     value=json.loads(raw);cost=value.get('usage',{}).get('cost')
     if type(cost) not in (int,float) or not 0<=cost<=float(x.c.PER_CALL):cost=None;raise ValueError('cost_bound')
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
  while time.time()<r['deadline'] and not Path(str(ledger)+'.C2-stop').exists():server.handle_request()
 finally:stop.set();server.server_close()

def run(receipt,manifest,ledger,output):
 r=json.loads(Path(receipt).read_text());packet=json.loads(Path(manifest).read_text());admit(r,packet);x.public_check(r);l=x.Ledger(ledger,False);prefix_calls=validate_prefixes(packet,l);root=Path(output)
 if socket.gethostname().split('.')[0]!=r['host'] or root.exists():raise ValueError('host_or_existing')
 root.mkdir();write_new(root/'manifest.json',{'receipt':r,'packet':packet,'prefixes':PREFIXES,'eligible':ELIGIBLE});stop=threading.Event();results={}
 import sys;sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
 def trajectory(ident):
  folder=root/ident;folder.mkdir();caller=Calls(ident,folder,r,l,stop,prefix_calls[ident]);family,w=x.assignments(packet,'P1')[ident];result=None;error=None;p=r['plans']['C2']
  try:
   for kind in ('plan','start'):
    if not sr.report(kind,p['experiment'],'C2-'+ident,message=p['tldr']+' Condition:'+ident,url=p['url'],strict=True):raise ValueError('reporting')
   result=turnover.trajectory(w,family,caller);write_new(folder/'results.json',result)
   if not result['complete']:raise ValueError('unexpected_initial_ineligibility')
  except Exception as exc:error=type(exc).__name__;stop.set()
  finally:
   terminal={'trajectory':ident,'reused_calls':ELIGIBLE[ident],'new_calls':caller.seq-ELIGIBLE[ident],'error':error,'complete':bool(result and result['complete']),'retries':0};write_new(folder/'terminal.json',terminal)
   sr.report('done' if terminal['complete'] else 'fail',p['experiment'],'C2-'+ident,message='Conditional continuation terminal;original failed assignment retained.',metrics={'new_calls':terminal['new_calls'],'complete':int(terminal['complete'])},strict=True)
  return terminal
 try:
  with ThreadPoolExecutor(max_workers=5) as pool:
   pending={pool.submit(trajectory,ident):ident for ident in ELIGIBLE}
   for future in as_completed(pending):results[pending[future]]=future.result()
 finally:write_new(root/'terminal.json',{'results':results,'ledger':l.summary()['C2'],'worker_terminal':True,'assigned_original':6,'eligible':5,'original_initial_failures':1,'automatic_successor':False})
 return {'completed':sum(v['complete'] for v in results.values()),'ledger':l.summary()['C2']}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['relay','worker'])
 for key in ('receipt','manifest','ledger','credential','capability','output'):p.add_argument('--'+key)
 v=p.parse_args()
 try:
  if v.mode=='relay':serve(v.receipt,v.manifest,v.ledger,v.credential,v.capability)
  else:print(json.dumps(run(v.receipt,v.manifest,v.ledger,v.output)))
 except Exception as error:print(json.dumps({'blocked':True,'safe_error':type(error).__name__}));raise SystemExit(1)

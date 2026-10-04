"""One six-call D1 diagnostic; named PI decision supplied by admitted operator, not issued here."""
import argparse,json,time,os,sqlite3,subprocess,hmac,urllib.request,urllib.error,socket
from pathlib import Path
from decimal import Decimal
from http.server import BaseHTTPRequestHandler,HTTPServer
import admission as a,expansion_runtime as x,selection_v2 as s,selection_diagnostic as d
from q3_relay import NoRedirect,safe_http_error
from q3_runner import parse,write_new
x.CAPS['D1']=(6,Decimal('.1359'));PACKET='76118c06c346866bc4d62a58303977ac80c8d91fa29894d9947214474403efdc';TRAJECTORY='D1-A1'

def expected(packet,history):
 index=0
 def caller(family,phase,p,condition):
  nonlocal index
  value={'family':family,'phase':phase,'packet':p,'condition':condition,'request':s.wire(phase,family,p)}
  if index==len(history):raise x.Expected(value)
  value=history[index];index+=1;return value
 try:result=d.run(packet,caller)
 except x.Expected as e:return e.value,None
 if index!=len(history):raise ValueError('prefix_excess')
 return None,result

def admit(r,packet,decision):
 now=time.time()
 if not isinstance(decision,str) or not decision.startswith('PI-FUND-20261004-') or r.get('funding_decision')!=decision or r.get('funding_status')!='reserved':raise ValueError('unfunded')
 if r.get('stage')!='D1' or r.get('call_cap')!=6 or r.get('api_cap_usd')!='0.1359' or r.get('all_in_cap_usd')!='0.15' or r.get('hosting_cap_usd')!='0.0141':raise ValueError('envelope')
 if r.get('prior_exposure_usd')!='1.3716677020333334' or r.get('packet_sha256')!=PACKET or a.digest(packet)!=PACKET:raise ValueError('lineage_packet')
 if r.get('source_sha256')!=a.source_hash() or subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.ROOT,text=True).strip()!=r['source_commit']:raise ValueError('source')
 if not 0<=now-r['verified_epoch']<=600 or not now<r['deadline']<=r['claim_start']+600:raise ValueError('freshness_deadline')
 if Decimal(str(r['hourly_usd']))/6>Decimal('.0141'):raise ValueError('hosting')
 for k in ('account_verified','exclusive_claim_verified','host_idle_verified','runtime_verified','public_pages_verified','route_pricing_verified','original_ledger_verified'):
  if r.get(k) is not True:raise ValueError('missing_'+k)
 import hashlib
 if r['plans']['D1']['sha256']!=hashlib.sha256((a.ROOT/'SELECTION-REPAIR-PLAN.md').read_bytes()).hexdigest():raise ValueError('plan_hash')
 return True

def ledger(path,local):
 l=x.Ledger(path,local)
 with l.connect() as db:
  rows=db.execute("SELECT actual,status FROM r3_successor WHERE stage='Q3-A2'").fetchall()
  if len(rows)!=69 or sum((Decimal(v) for v,status in rows if v is not None),Decimal(0))!=Decimal('.169662') or any(status!='terminal' for _,status in rows):raise ValueError('Q3_A2_lineage')
  if db.execute("SELECT count(*) FROM r3_successor WHERE stage='P1'").fetchone()[0]:raise ValueError('P1_must_be_unstarted')
 return l

def relay(receipt,manifest,path,credential,capability,decision):
 r=json.loads(Path(receipt).read_text());packet=json.loads(Path(manifest).read_text());admit(r,packet,decision);x.public_check(r);l=ledger(path,True)
 if l.history(TRAJECTORY):raise ValueError('D1_already_started')
 keypath=Path(credential)
 if keypath.is_symlink() or keypath.stat().st_mode&0o077:raise ValueError('credential_metadata')
 key=keypath.read_text().strip();cap=Path(capability).read_text().strip()
 if not key or len(cap)<32:raise ValueError('credential_empty')
 stopped=False
 class Handler(BaseHTTPRequestHandler):
  def log_message(self,*args):pass
  def do_POST(self):
   nonlocal stopped
   result={'error':'rejected','actual_usd':None};ident=None;cost=None;answer=None;started=time.time()
   try:
    if stopped or time.time()>=r['deadline']:raise ValueError('stopped')
    if self.path!='/d1' or not hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+cap):raise ValueError('authorization')
    size=int(self.headers.get('Content-Length',0))
    if not 0<size<=24000:raise ValueError('input_bound')
    payload=json.loads(self.rfile.read(size));history=l.history(TRAJECTORY);wanted,result_done=expected(packet,history)
    if wanted is None or payload.get('seq')!=len(history) or payload.get('call')!=wanted or payload.get('packet_sha256')!=PACKET or payload.get('source_sha256')!=r['source_sha256']:raise ValueError('unexpected_request')
    ident=l.reserve('D1',TRAJECTORY,len(history));req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',json.dumps(wanted['request'],separators=(',',':')).encode(),{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    with urllib.request.build_opener(NoRedirect()).open(req,timeout=min(150,max(1,r['deadline']-time.time()))) as resp:raw=resp.read(1000001)
    if len(raw)>1000000:raise ValueError('response_bound')
    value=json.loads(raw);cost=value.get('usage',{}).get('cost')
    if type(cost) not in (float,int) or not 0<=cost<=.02265:cost=None;raise ValueError('cost_bound')
    result={'error':None,'actual_usd':cost,'response':value};answer=parse(result)
   except urllib.error.HTTPError as error:
    diag=safe_http_error(error);result={'error':'http_'+str(diag['http_status']),'actual_usd':None,'diagnostic':diag};stopped=True
   except Exception as error:result.update(error=type(error).__name__,actual_usd=cost);stopped=True
   finally:
    if ident:l.settle(ident,cost,answer,time.time()-started)
   raw=json.dumps(result).encode();self.send_response(200);self.send_header('Content-Length',str(len(raw)));self.end_headers()
   try:self.wfile.write(raw)
   except (BrokenPipeError,ConnectionResetError):stopped=True
   if not stopped and len(l.history(TRAJECTORY))==6:stopped=True
 server=HTTPServer(('127.0.0.1',18965),Handler);server.timeout=1;print(json.dumps({'status':'ready'}),flush=True)
 try:
  while not stopped and time.time()<r['deadline'] and not Path(str(path)+'.D1-stop').exists():server.handle_request()
 finally:server.server_close()

def worker(receipt,manifest,path,output,decision):
 r=json.loads(Path(receipt).read_text());packet=json.loads(Path(manifest).read_text());admit(r,packet,decision);x.public_check(r)
 if socket.gethostname().split('.')[0]!=r['host']:raise ValueError('host')
 root=Path(output)
 if root.exists():raise ValueError('existing_attempt')
 l=ledger(path,False);root.mkdir();write_new(root/'manifest.json',{'receipt':r,'packet':packet});count=0;condition=None;result=None;error=None
 import sys;sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
 def caller(family,phase,p,name):
  nonlocal count,condition
  plan=r['plans']['D1']
  if condition!=name:
   if condition:sr.report('done',plan['experiment'],TRAJECTORY+'-'+condition,message='Diagnostic condition collected;semantic review separate.',strict=True)
   condition=name
   for kind in ('plan','start'):assert sr.report(kind,plan['experiment'],TRAJECTORY+'-'+name,message=plan['tldr']+' Condition:'+name,url=plan['url'],strict=True)
  if count>=6 or time.time()>=r['deadline']:raise ValueError('bound')
  call={'family':family,'phase':phase,'packet':p,'condition':name,'request':s.wire(phase,family,p)};ident=l.reserve('D1',TRAJECTORY,count);payload={'seq':count,'call':call,'source_sha256':r['source_sha256'],'packet_sha256':PACKET};count+=1;write_new(root/(ident+'-request.json'),payload);cost=None;answer=None;started=time.time()
  try:
   req=urllib.request.Request('http://127.0.0.1:18966/d1',json.dumps(payload).encode(),{'Authorization':'Bearer '+os.environ['THESEUS_D1_CAPABILITY'],'Content-Type':'application/json'})
   with urllib.request.urlopen(req,timeout=min(180,max(1,r['deadline']-time.time()))) as resp:value=json.load(resp)
   write_new(root/(ident+'-response.json'),value);cost=value.get('actual_usd')
   if type(cost) not in (float,int) or not 0<=cost<=.02265:cost=None;raise ValueError('unknown_usage')
   if value.get('error'):raise ValueError('provider_error')
   answer=parse(value);return answer
  finally:l.settle(ident,cost,answer,time.time()-started)
 try:result=d.run(packet,caller);write_new(root/'results.json',result)
 except Exception as exc:error=type(exc).__name__
 finally:
  terminal={'started_calls':count,'passed':bool(result and result['passed']),'error':error,'retries':0,'ledger':l.summary()['D1'],'full_native_qualification':False,'automatic_successor':False};write_new(root/'terminal.json',terminal)
  if condition:sr.report('done' if terminal['passed'] else 'fail',r['plans']['D1']['experiment'],TRAJECTORY+'-'+condition,message='Diagnostic terminal;does not authorize full qualification/main.',metrics={'started_calls':count,'passed':int(terminal['passed'])},strict=True)
 return terminal
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['relay','worker'])
 for k in ('receipt','manifest','ledger','credential','capability','output','decision'):p.add_argument('--'+k)
 v=p.parse_args()
 try:
  if v.mode=='relay':relay(v.receipt,v.manifest,v.ledger,v.credential,v.capability,v.decision)
  else:print(json.dumps(worker(v.receipt,v.manifest,v.ledger,v.output,v.decision)))
 except Exception as error:print(json.dumps({'blocked':True,'safe_error':type(error).__name__}));raise SystemExit(1)

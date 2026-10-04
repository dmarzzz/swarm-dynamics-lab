"""One-use C1 transport check. No scientific inputs, retries or successor dispatch."""
import argparse,hashlib,hmac,json,os,sqlite3,subprocess,time,urllib.request,urllib.error
from decimal import Decimal
from pathlib import Path
from http.server import BaseHTTPRequestHandler,HTTPServer
import admission as a,contract as c
from q3_relay import NoRedirect,safe_http_error
from q3_runner import parse,write_new
ATTEMPT='R3-C1-A1';EXPERIMENT='swarm-of-theseus-r3-c1';FUND='PI-FUND-20261004-08'

def body():
 b=c.wire('question','release',{})
 b['messages']=[{'role':'system','content':'Return exactly one JSON object and no surrounding prose.'},{'role':'user','content':'Return {"ok":true}.'}]
 c.validate_wire(b);return b

def admit(r,now=None):
 now=time.time() if now is None else now
 for key,value in {'attempt':ATTEMPT,'funding_decision':FUND,'max_calls':1,'model_cap_usd':'0.02265','hosting_cap_usd':'0.02735','all_in_cap_usd':'0.05','prior_exposure_usd':'1.1863770437','source_sha256':a.source_hash(),'request_sha256':a.digest(body()),'retry_count':0}.items():
  if r.get(key)!=value:raise ValueError('admission_'+key)
 if not 0<=now-r.get('verified_epoch',0)<=300 or not now<r.get('deadline',0)<=r.get('claim_start',0)+600:raise ValueError('admission_time')
 if Decimal(str(r['hourly_usd']))*Decimal(600)/Decimal(3600)>Decimal('.02735'):raise ValueError('hosting_cap')
 for key in ('approved_account_verified','exclusive_allocation_verified','worker_idle_verified','public_page_verified','route_pricing_verified','runtime_verified','ledger_reconciled'):
  if r.get(key) is not True:raise ValueError('missing_'+key)
 if subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.ROOT,text=True).strip()!=r['source_commit']:raise ValueError('source_revision')
 if r['plan_sha256']!=hashlib.sha256((a.ROOT/'C1-PLAN.md').read_bytes()).hexdigest():raise ValueError('plan_digest')
 return True

def public_check(r):
 def fetch(url):
  with urllib.request.urlopen(urllib.request.Request(url,headers={'Cache-Control':'no-cache'}),timeout=20) as resp:data=resp.read(10000001)
  if len(data)>10000000:raise ValueError('public_bound')
  return data
 url='https://github.com/dmarzzz/swarm-lab/blob/'+r['source_commit']+'/researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/sol50/baseline-replication/C1-PLAN.md'
 if r['plan_url']!=url:raise ValueError('plan_url')
 exp=next((e for e in json.loads(fetch('https://swarm-live.pages.dev/api/state'))['experiments'] if e['id']==EXPERIMENT),{})
 if exp.get('url')!=url or not exp.get('description','').startswith('TLDR: '):raise ValueError('public_registration')
 if hashlib.sha256(fetch(url.replace('github.com','raw.githubusercontent.com').replace('/blob/','/'))).hexdigest()!=r['plan_sha256']:raise ValueError('public_hash')
 return True

class Ledger:
 def __init__(self,path,local):
  if not Path(path).is_file():raise ValueError('original_ledger_missing')
  self.db=sqlite3.connect(path);table='calls' if local else 'sol50_calls'
  n,actual,unknown=self.db.execute(f'SELECT count(*),sum(actual_usd),sum(case when actual_usd is null then reserved_usd else 0 end) FROM {table}').fetchone()
  if n!=44 or abs(actual-.122835)>1e-10 or unknown!=0:raise ValueError('historical_ledger')
  if self.db.execute("SELECT reserved,actual,status FROM r3_calls WHERE stage='Q3'").fetchall()!=[('0.02265',None,'ambiguous')]:raise ValueError('Q3_preservation')
 def reserve(self):
  with self.db:
   self.db.execute('BEGIN IMMEDIATE')
   if self.db.execute("SELECT count(*) FROM r3_calls WHERE stage='C1'").fetchone()[0]:raise ValueError('C1_already_attempted')
   self.db.execute('INSERT INTO r3_calls VALUES(?,?,?,?,?)',(ATTEMPT,'C1','0.02265',None,'reserved'))
 def settle(self,cost):
  if cost is not None and (type(cost) not in (int,float) or not 0<=cost<=.02265):raise ValueError('cost_bound')
  with self.db:
   if self.db.execute('SELECT status FROM r3_calls WHERE id=?',(ATTEMPT,)).fetchone()!=('reserved',):raise ValueError('terminal_or_absent')
   self.db.execute('UPDATE r3_calls SET actual=?,status=? WHERE id=?',(None if cost is None else str(cost),'ambiguous' if cost is None else 'terminal',ATTEMPT))

def relay(receipt,ledger,credential,capability):
 r=json.loads(Path(receipt).read_text());admit(r);public_check(r);l=Ledger(ledger,True)
 keypath=Path(credential)
 if keypath.is_symlink() or keypath.stat().st_mode&0o077:raise ValueError('credential_metadata')
 key=keypath.read_text().strip();cap=Path(capability).read_text().strip()
 if not key or len(cap)<32:raise ValueError('credential_empty')
 stopped=False
 class Handler(BaseHTTPRequestHandler):
  def log_message(self,*args):pass
  def do_POST(self):
   nonlocal stopped
   result={'error':'rejected','actual_usd':None};reserved=False
   try:
    if stopped or time.time()>=r['deadline']:raise ValueError('stopped')
    if self.path!='/c1' or not hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+cap):raise ValueError('authorization')
    size=int(self.headers.get('Content-Length',0))
    if not 0<size<=6500:raise ValueError('input_bound')
    if json.loads(self.rfile.read(size))!=body():raise ValueError('changed_input')
    l.reserve();reserved=True;stopped=True
    request=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',json.dumps(body(),separators=(',',':')).encode(),{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    with urllib.request.build_opener(NoRedirect()).open(request,timeout=min(150,max(1,r['deadline']-time.time()))) as response:raw=response.read(1000001)
    if len(raw)>1000000:raise ValueError('response_bound')
    value=json.loads(raw);cost=value.get('usage',{}).get('cost')
    if type(cost) not in (int,float) or not 0<=cost<=.02265:raise ValueError('cost_bound')
    l.settle(cost);result={'error':None,'actual_usd':cost,'response':value}
   except urllib.error.HTTPError as error:
    diagnostic=safe_http_error(error);result={'error':'http_'+str(diagnostic['http_status']),'diagnostic':diagnostic,'actual_usd':None}
   except Exception as error:result={'error':type(error).__name__,'actual_usd':None}
   finally:
    stopped=True
    if reserved and result.get('actual_usd') is None:l.settle(None)
   raw=json.dumps(result).encode();self.send_response(200);self.send_header('Content-Length',str(len(raw)));self.end_headers()
   try:self.wfile.write(raw)
   except (BrokenPipeError,ConnectionResetError):pass
 server=HTTPServer(('127.0.0.1',18765),Handler);server.timeout=1
 print(json.dumps({'status':'ready','attempt':ATTEMPT}),flush=True)
 try:
  while not stopped and time.time()<r['deadline']:server.handle_request()
 finally:server.server_close();l.db.close()

def worker(receipt,ledger,output):
 r=json.loads(Path(receipt).read_text());admit(r);public_check(r);l=Ledger(ledger,False);root=Path(output)
 if root.exists():raise ValueError('attempt_exists')
 root.mkdir();write_new(root/'manifest.json',r)
 import sys;sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
 rid=ATTEMPT+'-json-contract';tldr='TLDR: One trivial JSON contract check; exact expected object and served route,known bounded usage. Transport only,no acquisition or cultural-survival evidence. One call,no retry; USD0.05 all-in.'
 for kind in ('plan','start'):
  if not sr.report(kind,EXPERIMENT,rid,message=tldr,url=r['plan_url'],strict=True):raise ValueError('report_admission')
 l.reserve();write_new(root/'request.json',body());started=time.time();result=None;error=None;settled=False
 try:
  req=urllib.request.Request('http://127.0.0.1:18766/c1',json.dumps(body(),separators=(',',':')).encode(),{'Authorization':'Bearer '+os.environ['THESEUS_C1_CAPABILITY'],'Content-Type':'application/json'})
  with urllib.request.urlopen(req,timeout=min(180,max(1,r['deadline']-time.time()))) as resp:result=json.load(resp)
  write_new(root/'response.json',result);cost=result.get('actual_usd')
  l.settle(cost);settled=True
  if result.get('error'):raise ValueError(result['error'] if result['error'] in {'http_'+str(n) for n in range(400,600)} else 'provider_error')
  if cost is None:raise ValueError('unknown_cost')
  value=parse(result)
  if set(value)!={'ok'} or value['ok'] is not True:raise ValueError('wrong_object')
 except Exception as e:
  error=str(e) if isinstance(e,ValueError) and str(e) in {'wrong_object','unknown_cost','provider_error','served_route','response_incomplete','response_shape','cost_bound'}|{'http_'+str(n) for n in range(400,600)} else type(e).__name__
 finally:
  if not settled:l.settle(None)
  row=l.db.execute('SELECT actual,status FROM r3_calls WHERE id=?',(ATTEMPT,)).fetchone();terminal={'attempt':ATTEMPT,'started_calls':1,'passed':error is None,'error':error,'actual_usd':row[0],'cost_status':row[1],'retries':0,'started_epoch':started,'finished_epoch':time.time(),'automatic_successor':False}
  write_new(root/'terminal.json',terminal);l.db.close()
  sr.report('fail' if error else 'done',EXPERIMENT,rid,message='Single contract attempt terminal; scientific closeout separate.',metrics={'started_calls':1,'passed':int(error is None)},strict=True)
 return terminal

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['worker','relay'])
 for key in ('receipt','ledger','output','credential','capability'):p.add_argument('--'+key)
 args=p.parse_args()
 try:
  if args.mode=='relay':relay(args.receipt,args.ledger,args.credential,args.capability)
  else:print(json.dumps(worker(args.receipt,args.ledger,args.output)))
 except Exception as e:print(json.dumps({'status':'blocked','safe_error':type(e).__name__}));raise SystemExit(1)

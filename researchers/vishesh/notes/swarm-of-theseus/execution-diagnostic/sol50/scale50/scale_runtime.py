"""Sequential native transport, original-ledger reservations and exact mirror validation.

No credentials or native dispatch are used on import. Each stage is separately
admitted and launched once; there is no automatic Q-to-main transition or retry.
"""
import contextlib
import argparse,hashlib,hmac,json,os,queue,sqlite3,threading,time,urllib.request,urllib.error
from pathlib import Path
from decimal import Decimal
from http.server import HTTPServer,BaseHTTPRequestHandler
import scale_contract as c,scale_study as s
from q3_runner import parse,write_new
from q3_relay import NoRedirect,safe_http_error
ROOT=Path(__file__).resolve().parent
Q50_SOURCE='84423a431d6758606c61938f475f7a8b0ecc22112126c4d426fef8ff35aed8d3'
Q50_SCIENCE='ceb9ae9e3f5189e1565ac845c79c689f0545b69d04834953002d4ee7b70c5628'

def source_hash():
 files={str(p.relative_to(ROOT.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in (ROOT,ROOT.parent,ROOT.parent/'baseline-replication') for p in folder.glob('*.py')}
 return c.digest(files)

def scientific_hash():
 files={str(p.relative_to(ROOT.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in (ROOT,ROOT.parent,ROOT.parent/'baseline-replication') for p in folder.glob('*.py') if p.name!='scale_runtime.py' and not p.name.startswith('test_')}
 return c.digest(files)

def qualification_source_matches(receipt):
 q=receipt.get('qualification',{})
 if q.get('source_sha256')==receipt.get('source_sha256'):return True
 return q.get('source_sha256')==Q50_SOURCE and receipt.get('operational_amendment')=='explicit-sqlite-close-only' and scientific_hash()==Q50_SCIENCE

def historical_hash(path):
 with contextlib.closing(sqlite3.connect(path)) as db:
  tables=[x[0] for x in db.execute("SELECT name FROM sqlite_master WHERE type='table'") if x[0] in ('calls','sol50_calls','r3_calls','r3_successor')]
  if not {'r3_calls','r3_successor'}<=set(tables) or not ({'calls','sol50_calls'}&set(tables)):raise ValueError('original_ledger_missing')
  return c.digest({name:db.execute('SELECT * FROM '+name+' ORDER BY 1').fetchall() for name in sorted(tables)})

def admit(r,ledger,now=None):
 now=time.time() if now is None else now;stage=r.get('stage')
 if stage not in c.CAPS:raise ValueError('stage')
 if r.get('packet_sha256')!=c.digest(s.packet()) or r.get('source_sha256')!=source_hash():raise ValueError('source_packet')
 if r.get('plan_sha256')!=hashlib.sha256((ROOT/'PLAN.md').read_bytes()).hexdigest():raise ValueError('plan')
 if not str(r.get('funding_decision','')).startswith('PI-FUND-') or r.get('funding_status')!='reserved':raise ValueError('funding')
 expected=c.PER_CALL*c.CAPS[stage]
 if Decimal(str(r.get('model_cap_usd','0')))!=expected or r.get('max_calls')!=c.CAPS[stage]:raise ValueError('stage_envelope')
 if not 0<Decimal(str(r.get('hosting_cap_usd','0')))<=Decimal('.02' if stage=='Q50' else '.28'):raise ValueError('hosting_cap')
 if Decimal(str(r['cumulative_prior_usd']))<c.PRIOR or Decimal(str(r['cumulative_prior_usd']))+expected+Decimal(str(r['hosting_cap_usd']))>c.STUDY_CAP:raise ValueError('cumulative_cap')
 if not 0<=now-r['verified_epoch']<=900 or not now<r['deadline']<=r['claim_until_epoch']:raise ValueError('freshness')
 if not 0<r['deadline']-r['claim_start']<=14400:raise ValueError('duration')
 if Decimal(str(r['hourly_usd']))*Decimal(str(r['deadline']-r['claim_start']))/3600>Decimal(str(r['hosting_cap_usd'])):raise ValueError('hosting_bound')
 if historical_hash(ledger)!=r['historical_ledger_sha256']:raise ValueError('historical_rows_changed')
 for name in ('account_verified','exclusive_claim_verified','host_idle_verified','runtime_verified','original_ledger_verified','public_page_verified','route_pricing_verified','duplicate_queue_fenced'):
  if r.get(name) is not True:raise ValueError('missing_'+name)
 if stage=='S50':
  q=r.get('qualification',{})
  if not qualification_source_matches(r) or q.get('packet_sha256')!=r['packet_sha256'] or not q.get('passed') or not q.get('authored_trace_review_passed') or not q.get('result_sha256'):raise ValueError('qualification_gate')
  if not 0<q.get('p90_seconds',0)*1150*1.25<r['deadline']-now:raise ValueError('observed_latency_feasibility')
 return True

def public_check(r):
 def get(url):
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Theseus-S50','Cache-Control':'no-cache'}),timeout=25) as response:raw=response.read(10000001)
  if len(raw)>10000000:raise ValueError('public_size')
  return raw
 state=json.loads(get('https://swarm-live.pages.dev/api/state'))
 exp=next((e for e in state['experiments'] if e['id']==r['experiment']),{})
 if exp.get('url')!=r['plan_url'] or exp.get('description')!=r['tldr']:raise ValueError('public_registration')
 raw=get(r['plan_url'].replace('github.com','raw.githubusercontent.com').replace('/blob/','/'))
 if hashlib.sha256(raw).hexdigest()!=r['plan_sha256']:raise ValueError('public_plan_hash')

class Ledger:
 def __init__(self,path,stage):
  self.path=str(path);self.stage=stage
  if not Path(path).is_file():raise ValueError('original_ledger_absent')
  with self.connect() as db:
   db.execute('CREATE TABLE IF NOT EXISTS theseus_scale_calls(id TEXT PRIMARY KEY,stage TEXT,seq INTEGER,reserved TEXT,actual TEXT,status TEXT,answer TEXT,seconds REAL,UNIQUE(stage,seq))')
 @contextlib.contextmanager
 def connect(self):
  db=sqlite3.connect(self.path,timeout=30)
  try:
   with db:yield db
  finally:db.close()
 def reserve(self,seq,body):
  c.validate(body)
  with self.connect() as db:
   db.execute('BEGIN IMMEDIATE')
   n=db.execute('SELECT count(*) FROM theseus_scale_calls WHERE stage=?',(self.stage,)).fetchone()[0]
   unknown=db.execute("SELECT count(*) FROM theseus_scale_calls WHERE status!='terminal'").fetchone()[0]
   if n!=seq or unknown or n>=c.CAPS[self.stage]:raise ValueError('sequence_or_stage_cap')
   total=db.execute('SELECT reserved,actual FROM theseus_scale_calls').fetchall()
   exposure=sum((Decimal(a) if a is not None else Decimal(r) for r,a in total),Decimal(0))
   if c.PRIOR+exposure+c.PER_CALL+Decimal('.30')>c.STUDY_CAP:raise ValueError('cumulative_cap')
   ident=self.stage+'-'+str(seq).zfill(4)
   db.execute('INSERT INTO theseus_scale_calls VALUES(?,?,?,?,?,?,?,?)',(ident,self.stage,seq,str(c.PER_CALL),None,'reserved',None,None))
   return ident
 def settle(self,ident,cost,answer,seconds):
  if cost is not None and (type(cost) not in (int,float) or not 0<=cost<=float(c.PER_CALL)):raise ValueError('cost')
  with self.connect() as db:
   if db.execute('SELECT status FROM theseus_scale_calls WHERE id=?',(ident,)).fetchone()!=('reserved',):raise ValueError('terminal_or_missing')
   db.execute('UPDATE theseus_scale_calls SET actual=?,status=?,answer=?,seconds=? WHERE id=?',(None if cost is None else str(cost),'ambiguous' if cost is None else 'terminal',None if answer is None else json.dumps(answer),seconds,ident))
 def rows(self):
  with self.connect() as db:return db.execute('SELECT id,reserved,actual,status,seconds FROM theseus_scale_calls WHERE stage=? ORDER BY seq',(self.stage,)).fetchall()

class Mirror:
 """One suspended frozen study execution verifies each request before spending."""
 def __init__(self,stage):
  self.requests=queue.Queue();self.answers=queue.Queue();self.stage=stage
  self.thread=threading.Thread(target=self.execute,daemon=True);self.thread.start()
 def execute(self):
  def call(family,phase,packet,condition):
   self.requests.put({'family':family,'phase':phase,'packet':packet,'condition':condition,'request':c.wire(phase,family,packet)})
   value=self.answers.get()
   if isinstance(value,Exception):raise value
   return c.to_engine(phase,value)
  try:self.requests.put({'terminal':(s.qualify if self.stage=='Q50' else s.main)(call)})
  except Exception as error:self.requests.put({'error':type(error).__name__})
 def next(self):return self.requests.get(timeout=90)
 def answer(self,value):self.answers.put(value)

def serve(receipt,ledger,credential,capability,output):
 r=json.loads(Path(receipt).read_text());admit(r,ledger);public_check(r)
 path=Path(credential)
 if path.is_symlink() or not path.is_file() or path.stat().st_mode&0o077:raise ValueError('credential_metadata')
 key=path.read_text().strip();cap=Path(capability).read_text().strip()
 if not key or len(cap)<32:raise ValueError('credential_empty')
 l=Ledger(ledger,r['stage'])
 if l.rows():raise ValueError('stage_already_started')
 root=Path(output);root.mkdir(exist_ok=False);write_new(root/'receipt.json',r)
 mirror=Mirror(r['stage']);expected=mirror.next();opener=urllib.request.build_opener(NoRedirect());stopped=False;seq=0
 class Handler(BaseHTTPRequestHandler):
  def log_message(self,*args):pass
  def do_POST(self):
   nonlocal stopped,seq,expected
   result={'error':'rejected','actual_usd':None};ident=None;cost=None;answer=None;start=time.time()
   try:
    if stopped or time.time()>=r['deadline'] or Path(str(ledger)+'.s50-stop').exists():raise ValueError('stopped')
    if self.path!='/next' or not hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+cap):raise ValueError('authorization')
    size=int(self.headers.get('Content-Length',0))
    if not 0<size<=36000:raise ValueError('payload_bound')
    p=json.loads(self.rfile.read(size))
    if set(p)!={'stage','seq','call','source_sha256','packet_sha256'} or p['stage']!=r['stage'] or p['seq']!=seq or p['source_sha256']!=r['source_sha256'] or p['packet_sha256']!=r['packet_sha256'] or p['call']!=expected:raise ValueError('exact_mirror_mismatch')
    ident=l.reserve(seq,expected['request']);seq+=1;write_new(root/(ident+'-request.json'),p)
    req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',json.dumps(expected['request'],separators=(',',':')).encode(),{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    try:
     with opener.open(req,timeout=min(150,max(1,r['deadline']-time.time()))) as response:raw=response.read(1000001)
     if len(raw)>1000000:raise ValueError('response_bound')
     value=json.loads(raw);observed=value.get('usage',{}).get('cost')
     if type(observed) not in (int,float) or not 0<=observed<=float(c.PER_CALL):raise ValueError('unknown_usage')
     cost=observed;result={'error':None,'actual_usd':cost,'response':value};answer=parse(result)
     mirror.answer(answer);expected=mirror.next()
     if 'terminal' in expected:write_new(root/'mirror-results.json',expected['terminal']);stopped=True
     elif 'error' in expected:stopped=True
    except urllib.error.HTTPError as exc:
     result={'error':'provider_http','actual_usd':None,'diagnostic':safe_http_error(exc)};stopped=True
   except Exception as exc:
    result.update(error=type(exc).__name__,actual_usd=cost);stopped=True
   finally:
    if ident:
     l.settle(ident,cost,answer,time.time()-start);write_new(root/(ident+'-response.json'),result)
   data=json.dumps(result).encode();self.send_response(200);self.send_header('Content-Length',str(len(data)));self.end_headers()
   try:self.wfile.write(data)
   except (BrokenPipeError,ConnectionResetError):stopped=True
 server=HTTPServer(('127.0.0.1',19165),Handler);server.timeout=1
 print(json.dumps({'ready':True,'stage':r['stage'],'maximum_calls':c.CAPS[r['stage']]}),flush=True)
 try:
  while not stopped and time.time()<r['deadline'] and not Path(str(ledger)+'.s50-stop').exists():server.handle_request()
 finally:
  server.server_close();mirror.answer(ValueError('closed'));write_new(root/'terminal.json',{'rows':l.rows(),'stage':r['stage'],'stopped':True,'retry_count':0})

def run(receipt,ledger,capability,output):
 r=json.loads(Path(receipt).read_text());admit(r,ledger);public_check(r)
 if os.uname().nodename.split('.')[0]!=r['host']:raise ValueError('host')
 l=Ledger(ledger,r['stage'])
 if l.rows():raise ValueError('already_started')
 root=Path(output);root.mkdir(exist_ok=False);write_new(root/'receipt.json',r);seq=0
 import sys;sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
 observed_conditions=set()
 for kind in ('plan','start'):
  if not sr.report(kind,r['experiment'],r['stage'],message=r['tldr'],url=r['plan_url'],strict=True):raise ValueError('reporting')
 cap=Path(capability).read_text().strip()
 def call(family,phase,packet,condition):
  nonlocal seq
  if time.time()>=r['deadline'] or Path(str(ledger)+'.s50-stop').exists():raise ValueError('global_stop')
  if condition not in observed_conditions:
   if not sr.report('log',r['experiment'],r['stage'],message='Condition '+condition+': '+r['tldr'],url=r['plan_url'],strict=True):raise ValueError('condition_reporting')
   observed_conditions.add(condition)
  body=c.wire(phase,family,packet);ident=l.reserve(seq,body)
  p={'stage':r['stage'],'seq':seq,'call':{'family':family,'phase':phase,'packet':packet,'condition':condition,'request':body},'source_sha256':r['source_sha256'],'packet_sha256':r['packet_sha256']};seq+=1
  write_new(root/(ident+'-request.json'),p);start=time.time();cost=None;answer=None
  try:
   req=urllib.request.Request('http://127.0.0.1:19166/next',json.dumps(p).encode(),{'Authorization':'Bearer '+cap,'Content-Type':'application/json'})
   with urllib.request.urlopen(req,timeout=min(180,max(1,r['deadline']-time.time()))) as response:v=json.load(response)
   write_new(root/(ident+'-response.json'),v);cost=v.get('actual_usd')
   if type(cost) not in (int,float) or not 0<=cost<=float(c.PER_CALL):cost=None;raise ValueError('uncertain_usage')
   if v.get('error'):raise ValueError('provider_error')
   answer=parse(v);return c.to_engine(phase,answer)
  finally:l.settle(ident,cost,answer,time.time()-start)
 result=None;error=None
 try:result=(s.qualify if r['stage']=='Q50' else s.main)(call);write_new(root/'results.json',result)
 except Exception as exc:error=type(exc).__name__
 finally:
  complete=bool(result and result.get('passed',result.get('complete')))
  write_new(root/'terminal.json',{'stage':r['stage'],'calls':seq,'error':error,'complete':complete,'source_sha256':r['source_sha256'],'packet_sha256':r['packet_sha256'],'rows':l.rows(),'review_required':True})
  sr.report('done' if complete else 'fail',r['experiment'],r['stage'],message='Native execution closed; scientific review and cost reconciliation remain required.',metrics={'calls':seq,'complete':int(complete)},url=r['plan_url'],strict=True)
 return {'stage':r['stage'],'calls':seq,'error':error,'review_required':True}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['relay','worker'])
 for name in ('receipt','ledger','capability','output'):p.add_argument('--'+name,required=True)
 p.add_argument('--credential');x=p.parse_args()
 try:
  if x.mode=='relay':serve(x.receipt,x.ledger,x.credential,x.capability,x.output)
  else:print(json.dumps(run(x.receipt,x.ledger,x.capability,x.output)))
 except Exception as exc:print(json.dumps({'blocked':True,'error':type(exc).__name__}));raise SystemExit(1)

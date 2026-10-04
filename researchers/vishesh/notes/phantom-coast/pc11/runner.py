"""Remote coordinator; paid transport is injected after private operational admission."""
import copy,datetime,hashlib,json,random,subprocess,time,os
from pathlib import Path
from contract import ACTORS,canonical,digest
from cases import cases,grade,summarize
from engine import run as episode,StopDispatch,audit
from analysis import contrast
from native import request,decode,RESERVE
from ledger import Ledger,PREDECESSOR
ROOT=Path(__file__).resolve().parent

def source():return {f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(ROOT.glob('*.py'))}|{'PLAN.md':hashlib.sha256((ROOT/'PLAN.md').read_bytes()).hexdigest()}
def world():
 r=random.Random('PC11/S1-A1/world');sites=[f's{r.getrandbits(48):012x}' for _ in range(4)];order=sites.copy();r.shuffle(order)
 return dict(id='PC11/S1-A1/root-0',truth={s:r.choice(('LAND','WATER')) for s in sites},target=r.choice(sites),seed_actor=r.choice(ACTORS),tie_order=order)
def arms():
 a=[(p,s) for p in (False,True) for s in (False,True)];random.Random('PC11/arm-order').shuffle(a);return a

def write(path,obj):
 p=Path(path);tmp=p.with_suffix(p.suffix+'.tmp')
 with tmp.open('w') as f:f.write(json.dumps(obj,indent=2,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())
 tmp.replace(p)
class Admission:
 def __init__(self,c,public_check):
  self.c=c;now=datetime.datetime.now(datetime.timezone.utc)
  for flag in ('scope_authorized','account_verified','exclusive_claim','worker_idle','predecessor_fenced','public_page_verified','credential_authorized','single_writer'):
   if c.get(flag) is not True:raise ValueError('admission_'+flag)
  if (now-datetime.datetime.fromisoformat(c['checked_utc'])).total_seconds() not in range(0,301):
   # Fractional seconds must also be accepted.
   age=(now-datetime.datetime.fromisoformat(c['checked_utc'])).total_seconds()
   if not 0<=age<=300:raise ValueError('stale_admission')
  self.until=datetime.datetime.fromisoformat(c['until'])
  if (self.until-now).total_seconds()<1800:raise ValueError('short_claim')
  if c['source_files']!=source():raise ValueError('source_files')
  sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
  if sha!=c['source_commit'] or subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip():raise ValueError('source_dirty')
  expected=f'https://github.com/dmarzzz/swarm-lab/blob/{sha}/researchers/vishesh/notes/phantom-coast/pc11/PLAN.md'
  self.public=public_check('phantom-coast-pc11',c['tldr'])
  if self.public['url']!=expected or self.public['plan_sha256']!=source()['PLAN.md']:raise ValueError('public_plan')
  if hashlib.sha256(Path(c['predecessor']).read_bytes()).hexdigest()!=PREDECESSOR:raise ValueError('ledger_lineage')
 def current(self):return datetime.datetime.now(datetime.timezone.utc)<self.until

class Actor:
 def __init__(self,ledger,transport,output,admission):self.ledger=ledger;self.transport=transport;self.output=Path(output);self.admission=admission;self.started=time.monotonic();self.calls=[];self.invalid=0
 def __call__(self,p):
  if not self.admission.current() or time.monotonic()-self.started>1800:raise StopDispatch('deadline')
  body=request(p);id=f'call-{len(self.calls):03d}';self.ledger.reserve(id,RESERVE)
  row=dict(id=id,packet=p,request=body,packet_sha256=digest(p),request_sha256=digest(body),status='started');self.calls.append(row);self.save()
  try:
   r=self.transport(body);d,cost,safe=decode(r,p)
   self.ledger.finish(id,cost);row.update(status='valid',decision=d,response=safe,response_sha256=digest(r));self.save();return d
  except Exception as e:
   row.update(status='failed',error_type=type(e).__name__)
   # Keep the full reservation if response/accounting cannot be validated; never retry.
   self.save();raise StopDispatch('response_or_transport_failed') from None
 def save(self):write(self.output/'traces.json',self.calls);write(self.output/'budget-summary.json',self.ledger.summary())

def run(c,transport,public_check,report):
 a=Admission(c,public_check);out=Path(c['output']);out.mkdir(exist_ok=False)
 ledger=Ledger(c['ledger'],c['predecessor']);ledger.claim();actor=Actor(ledger,transport,out,a)
 write(out/'source.json',dict(commit=c['source_commit'],files=source()));write(out/'public-plan.json',a.public)
 rows=cases('Q0',a);write(out/'cases.json',rows);records=[];stop=None;pilot=[]
 report('start','Q0-A1',dict(tldr='TLDR: Eight GPT-6 Sol evidence/inspection cases; comparator exact individual policy; require8valid32maps6actions. Capability diagnostic, no population inference.'))
 for row in rows:
  if stop:records.append(dict(id=row['id'],status='unstarted'));continue
  try:d=actor(copy.deepcopy(row['packet']));records.append(dict(id=row['id'],status='valid',decision=d,grade=grade(row,d)))
  except StopDispatch as e:stop=str(e);records.append(dict(id=row['id'],status='failed'))
  write(out/'qualification.json',records)
 write(out/'qualification.json',records);q=summarize(records);write(out/'qualification-summary.json',q)
 report('done','Q0-A1',q)
 if q['qualification_passed'] and not stop:
  # Recheck registration and claim before the conditionally authorized population stage.
  public_check('phantom-coast-pc11',c['tldr'])
  if not a.current():raise StopDispatch('claim_expired')
  w=world();write(out/'assignments.json',dict(world=w,arms=arms(),actors=list(ACTORS),rounds=3,assigned=120))
  report('start','S1-A1',dict(tldr='TLDR: Ten qualified GPT-6 Sol actors per arm; false/truthful private report crossed with peer maps visible/withheld; final unseeded target-error interaction and corrections. One matched world, descriptive pilot only.'))
  for poison,peers in arms():
   try:
    e=episode(w,poison,peers,actor,'gpt-6-sol/none',native=True);audit(e);pilot.append(e);write(out/'episodes.json',pilot)
   except StopDispatch as e:stop=str(e);break
  result=contrast(pilot) if len(pilot)==4 else dict(assigned=120,complete_arms=len(pilot),incomplete=True)
  write(out/'pilot-summary.json',result);report('done','S1-A1',dict(completed_arms=len(pilot),incomplete=len(pilot)!=4))
 summary=dict(qualification=q,pilot_complete=len(pilot)==4,pilot_calls=max(0,len(actor.calls)-8),calls=len(actor.calls),stop=stop,budget=ledger.summary())
 write(out/'summary.json',summary);return summary

"""Admission-controlled PC12 batches; injected local credential consumer only."""
import datetime,hashlib,json,os,subprocess,time
from pathlib import Path
from instrument import canonical,digest,qualification,worlds,arms,main_packet,qscore,analyze
from native import request,decode,RESERVE
from ledger import Ledger,PREDECESSOR
ROOT=Path(__file__).resolve().parent

def write(path,obj):
 p=Path(path);tmp=p.with_suffix(p.suffix+'.tmp')
 with tmp.open('w') as f:f.write(json.dumps(obj,indent=2,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())
 tmp.replace(p)
def source():return {f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(ROOT.glob('*.py'))}|{'PLAN.md':hashlib.sha256((ROOT/'PLAN.md').read_bytes()).hexdigest()}
def utc():return datetime.datetime.now(datetime.timezone.utc)
class Admission:
 def __init__(self,c,public_check):
  self.until=datetime.datetime.fromisoformat(c['until']);age=(utc()-datetime.datetime.fromisoformat(c['checked_utc'])).total_seconds()
  for flag in ('scope_authorized','account_verified','exclusive_claim','worker_idle','predecessor_fenced','public_page_verified','credential_authorized','single_writer'):
   if c.get(flag) is not True:raise ValueError('admission_'+flag)
  if not 0<=age<=300 or (self.until-utc()).total_seconds()<3600:raise ValueError('admission_time')
  if c['source_files']!=source():raise ValueError('source_files')
  sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
  if sha!=c['source_commit'] or subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip():raise ValueError('source_dirty')
  self.public=public_check('phantom-coast-pc12',c['tldr']);url=f'https://github.com/dmarzzz/swarm-lab/blob/{sha}/researchers/vishesh/notes/phantom-coast/pc12/PLAN.md'
  if self.public['url']!=url or self.public['plan_sha256']!=source()['PLAN.md']:raise ValueError('public_plan')
  if hashlib.sha256(Path(c['predecessor']).read_bytes()).hexdigest()!=PREDECESSOR:raise ValueError('ledger_lineage')
 def current(self):return utc()<self.until

class Actor:
 def __init__(self,ledger,transport,out,admission):self.ledger=ledger;self.transport=transport;self.out=Path(out);self.admission=admission;self.start=time.monotonic();self.records=[];self.stop=None
 def save(self):write(self.out/'records.json',self.records);write(self.out/'budget-summary.json',self.ledger.summary())
 def batch(self,jobs):
  assert 0<len(jobs)<=4
  if not self.admission.current() or time.monotonic()-self.start>2700:self.stop='deadline'
  if self.stop:
   rs=[dict(assignment=id,status='unstarted',packet=p) for id,p in jobs];self.records.extend(rs);self.save();return rs
  bodies=[request(p) for _,p in jobs];rows=[]
  for (id,p),b in zip(jobs,bodies):
   self.ledger.reserve(id,RESERVE);row=dict(assignment=id,status='started',packet=p,request=b,request_sha256=digest(b),packet_sha256=digest(p),started_utc=utc().isoformat());rows.append(row);self.records.append(row)
  self.save()
  try:responses=self.transport(bodies)
  except Exception:responses=[dict(transport_error=True) for _ in jobs]
  if not isinstance(responses,list) or len(responses)!=len(jobs):responses=[dict(transport_error=True) for _ in jobs]
  for r,raw in zip(rows,responses):
   try:
    d,cost,safe=decode(raw,r['packet']);self.ledger.finish(r['assignment'],cost);r.update(status='valid',decision=d,response=safe,response_sha256=digest(raw),actual_nano=cost)
   except Exception as e:
    r.update(status='failed',error_type=type(e).__name__,error_code=str(e) if isinstance(e,ValueError) and str(e) in ('output_schema','probability','choice','served_model','served_provider','missing_cost','cost_bound','token_bound','unexpected_reasoning','choice_count','nonterminal_or_refusal') else 'response_or_transport');self.stop='response_or_transport_failure'
   r['terminal_utc']=utc().isoformat();self.save()
  return rows
 def collect(self,jobs):
  out=[]
  for i in range(0,len(jobs),4):out.extend(self.batch(jobs[i:i+4]))
  return out

def run(c,transport,public_check,report):
 a=Admission(c,public_check);out=Path(c['output']);out.mkdir(exist_ok=False);l=Ledger(c['ledger'],c['predecessor']);l.claim();actor=Actor(l,transport,out,a)
 write(out/'source.json',dict(commit=c['source_commit'],files=source()));write(out/'public-plan.json',a.public)
 qs=qualification();ws=worlds();write(out/'qualification-cases.json',qs);write(out/'worlds.json',ws)
 report('start','Q0-A1',dict(tldr='TLDR:16 GPT-6 Sol sourced-evidence cases test single/independent evidence, direct contradiction and uncertainty against exact probabilities/actions. Repeated copies are excluded from gating; no broad reliability claim.'))
 qr=actor.collect([(q['id'],q['packet']) for q in qs]);q=qscore(qs,qr);write(out/'qualification-summary.json',q);report('done','Q0-A1',q)
 main=[]
 if q['qualification_passed'] and not actor.stop:
  public_check('phantom-coast-pc12',c['tldr']);report('start','D1-A1',dict(tldr='TLDR:8 worlds×truthful/false×single/triple same-origin report×10 separate GPT-6 Sol receivers×before/after fixed direct correction;640 decisions. Primary excess probability on false claim under copies; controlled reception, not autonomous diffusion or equivalence.'))
  for w in ws:
   for false,copies in arms(w):
    base=f"{w['id']}/{'false' if false else 'true'}/{copies}"
    before=actor.collect([(f'{base}/{i}/before',main_packet(w,false,copies,i,'before')) for i in range(10)]);main.extend(before)
    after=actor.collect([(f'{base}/{i}/after',main_packet(w,false,copies,i,'after',before[i].get('decision'))) for i in range(10)]);main.extend(after)
    write(out/'diagnostic-summary.json',analyze(ws,main))
  report('done','D1-A1',analyze(ws,main))
 summary=dict(qualification=q,diagnostic=analyze(ws,main) if main else None,stop=actor.stop,started=sum(r['status']!='unstarted' for r in actor.records),valid=sum(r['status']=='valid' for r in actor.records),budget=l.summary());write(out/'summary.json',summary);return summary

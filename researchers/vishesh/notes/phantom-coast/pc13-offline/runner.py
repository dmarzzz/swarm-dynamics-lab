"""PC13 sole-ledger worker; transport injected, no credential access."""
import datetime,hashlib,json,os,subprocess,time
from pathlib import Path
from packet import compact,digest,exact,assignments,roots,qualification
from native import request,decode,RESERVE
from ledger import Ledger,PREDECESSOR
from analysis import summarize
ROOT=Path(__file__).resolve().parent
MANIFEST='526de1221ac9b23bef84254caddb9b3f9514a8e461499098fe987230ffee7705'
REVIEWED={'packet.py':'eabcb7b9894bfb27c7d0f3e8fa65d947708c7e7bc09f66ac3de5fd07e4797084','analysis.py':'35800a738a2164273034d486a8f2b1e041ebe331f34f8bc11b3758de92eaf6da'}
def utc():return datetime.datetime.now(datetime.timezone.utc)
def source():return {f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(ROOT.glob('*.py'))}|{'PLAN.md':hashlib.sha256((ROOT/'PLAN.md').read_bytes()).hexdigest()}
def write(p,obj):
 p=Path(p);t=p.with_suffix(p.suffix+'.tmp')
 with t.open('w') as f:f.write(json.dumps(obj,indent=2,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())
 t.replace(p)
class Admission:
 def __init__(self,c,public_check):
  self.until=datetime.datetime.fromisoformat(c['until']);age=(utc()-datetime.datetime.fromisoformat(c['checked_utc'])).total_seconds()
  for f in ('scope_authorized','account_verified','exclusive_claim','worker_idle','predecessor_fenced','public_page_verified','credential_authorized','single_writer','infrastructure_bounded'):
   if c.get(f) is not True:raise ValueError('admission_'+f)
  if not 0<=age<=300 or (self.until-utc()).total_seconds()<5700:raise ValueError('admission_time')
  files=source()
  if c['source_files']!=files or any(files[k]!=v for k,v in REVIEWED.items()):raise ValueError('source_binding')
  sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
  if sha!=c['source_commit'] or subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip():raise ValueError('source_dirty')
  if hashlib.sha256(Path(c['manifest']).read_bytes()).hexdigest()!=MANIFEST:raise ValueError('manifest_binding')
  if hashlib.sha256(Path(c['predecessor']).read_bytes()).hexdigest()!=PREDECESSOR:raise ValueError('ledger_lineage')
  if c.get('decision')!='PI-FUND-20261004-02':raise ValueError('authority')
  self.public=public_check('phantom-coast-pc13',c['tldr']);url=f'https://github.com/dmarzzz/swarm-lab/blob/{sha}/researchers/vishesh/notes/phantom-coast/pc13-offline/PLAN.md'
  if self.public['url']!=url or self.public['plan_sha256']!=files['PLAN.md']:raise ValueError('public_plan')
 def current(self):return utc()<self.until
class Actor:
 def __init__(self,ledger,transport,out,admission):self.ledger=ledger;self.transport=transport;self.out=Path(out);self.admission=admission;self.start=time.monotonic();self.records=[];self.stop=None
 def save(self):write(self.out/'records.json',self.records);write(self.out/'budget-summary.json',self.ledger.summary())
 def batch(self,jobs):
  if not self.admission.current() or time.monotonic()-self.start>5400:self.stop='deadline'
  if self.stop:
   rs=[dict(assignment=id,status='unstarted',packet=p) for id,p in jobs];self.records.extend(rs);self.save();return rs
  bodies=[request(p) for _,p in jobs];rows=[]
  for (id,p),body in zip(jobs,bodies):
   self.ledger.reserve(id,RESERVE);r=dict(assignment=id,packet=p,request=body,request_sha256=digest(body),packet_sha256=digest(p),status='started',started_utc=utc().isoformat());self.records.append(r);rows.append(r)
  self.save()
  try:responses=self.transport(bodies)
  except Exception:responses=[dict(transport_error=True) for _ in jobs]
  if not isinstance(responses,list) or len(responses)!=len(jobs):responses=[dict(transport_error=True) for _ in jobs]
  for r,raw in zip(rows,responses):
   try:
    d,cost,safe=decode(raw,r['packet']);self.ledger.finish(r['assignment'],cost);r.update(status='valid',decision=d,response=safe,response_sha256=digest(raw),actual_nano=cost)
   except Exception as e:r.update(status='failed',error_type=type(e).__name__);self.stop='response_or_transport_failure'
   r['terminal_utc']=utc().isoformat();self.save()
  return rows
 def collect(self,jobs):
  out=[]
  for i in range(0,len(jobs),4):out.extend(self.batch(jobs[i:i+4]))
  return out

def run(c,transport,public_check,report):
 admission=Admission(c,public_check);manifest=json.loads(Path(c['manifest']).read_text());rows=manifest['assignments'];assert rows==assignments(manifest['roots'])
 out=Path(c['output']);out.mkdir(exist_ok=False);ledger=Ledger(c['ledger'],c['predecessor']);ledger.claim();actor=Actor(ledger,transport,out,admission)
 write(out/'source.json',dict(commit=c['source_commit'],files=source(),manifest_sha256=MANIFEST,decision=c['decision']));write(out/'public-plan.json',admission.public)
 qs=qualification(roots('PC13-development-v1'));write(out/'qualification-cases.json',qs)
 report('start','Q0-A1',dict(tldr='32 qualification cases: necessary ancestry-based probability inference and direct correction; all must meet tolerance before main. No repeat/repair.'))
 qr=actor.collect([(q['id'],q['packet']) for q in qs]);passed=sum(r['status']=='valid' and abs(r['decision']['p']-q['expected'])<=q['tolerance'] for q,r in zip(qs,qr));qsummary=dict(assigned=32,valid=sum(r['status']=='valid' for r in qr),passed=passed,qualification_passed=passed==32);write(out/'qualification-summary.json',qsummary);report('done','Q0-A1',qsummary)
 if passed!=32:actor.stop=actor.stop or 'qualification_failed'
 for block in range(2):
  selected=[r for r in rows if r['block']==block]
  if not actor.stop:report('start',f'B{block+1}-A1',dict(tldr=f'Fresh execution block{block+1}:16 roots,paired flat/linked presentation,truthful/false and single/copied/independent evidence,before/after fixed correction;384calls. No autonomous diffusion or equivalence claim.'))
  actor.collect([(r['id'],r['packet']) for r in selected])
  answers={r['assignment']:r['decision']['p'] for r in actor.records if r['status']=='valid' and r['assignment'].startswith('B')};analysis=summarize(rows,answers);write(out/'analysis.json',analysis)
  if passed==32:report('done',f'B{block+1}-A1',dict(valid=sum(r['status']=='valid' and r['assignment'].startswith(f'B{block}/') for r in actor.records),assigned=384))
 summary=dict(qualification=qsummary,analysis=analysis,stop=actor.stop,started=sum(r['status']!='unstarted' for r in actor.records),valid=sum(r['status']=='valid' for r in actor.records),budget=ledger.summary());write(out/'summary.json',summary);ledger.db.close();return summary

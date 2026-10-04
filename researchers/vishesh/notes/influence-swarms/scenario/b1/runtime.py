"""B1 bounded acquisition wiring. No credential store, allocation or funding authority.
A transport callback is supplied only after operator admission. No auto-resume/retry.
"""
import datetime as dt,hashlib,json,math,os,sqlite3,time
from pathlib import Path
from contextlib import contextmanager
import cases as c,instrument as i
H=Path(__file__).resolve().parent
FROZEN_PACKET='1fb19aa7c8cdcad23dd1acf724acf9febbdf6c7be3e4e075eae78bc79e9799ef'
MODEL_CEILING=18.467936
@contextmanager
def database(path):
 db=sqlite3.connect(path)
 try:
  with db:yield db
 finally:db.close()

class Stop(Exception):pass

def require(value,label):
 if not value:raise Stop(label)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def utc(value):return dt.datetime.fromisoformat(value)
def save(path,data):
 path=Path(path);raw=data if isinstance(data,bytes) else c.encoded(data)
 fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 d=os.open(path.parent,os.O_RDONLY)
 try:os.fsync(d)
 finally:os.close(d)
 return sha(raw)

def load_contract():
 p=json.loads((H/'packet.json').read_text());require(c.digest(p)==FROZEN_PACKET,'packet_changed')
 for name,h in p['source_hashes'].items():require(sha((H/name).read_bytes())==h,'frozen_source_changed')
 cases=json.loads((H/'dossiers.json').read_text());m=json.loads((H/'case-manifest.json').read_text());require(c.digest(cases)==m['dossiers_sha256'],'dossiers_changed')
 return p,cases

def admission(a,funding,observed,now=None):
 """Pure evidence checks; supplied observed fields must come from fresh operator checks.
 Do not write an approval receipt until the actual named PI/owner decision exists.
 """
 now=now or dt.datetime.now(dt.timezone.utc);p,_=load_contract()
 require(a['stage'] in ('B1-D0','B1-E0'),'stage')
 require(funding['decision']=='approved' and set(funding['stages'])=={'B1-D0','B1-E0'},'named_funding_required')
 require(funding['packet_sha256']==FROZEN_PACKET and funding['maximum_incremental_usd']==11.01,'funding_scope')
 require(isinstance(funding['authority_reference'],str) and len(funding['authority_reference'])>=12,'funding_provenance')
 require(a['funding_sha256']==c.digest(funding),'funding_receipt_changed')
 require(a['packet_sha256']==FROZEN_PACKET,'packet_admission')
 require(0<=(now-utc(a['checked_utc'])).total_seconds()<300,'stale_admission')
 require(utc(a['until'])>now+dt.timedelta(seconds=120),'allocation_deadline')
 require(a['host']==observed['host'] and all(observed[k] is True for k in ('approved_account_match','exclusive_claim_current','workload_idle','clean_runtime','public_page_verified','route_available')),'runtime_allocation_or_public_page')
 require(a['source_commit']==observed['source_commit'] and len(a['source_commit'])==40,'runtime_source')
 require(a['runtime_manifest_sha256']==observed['runtime_manifest_sha256'],'runtime_manifest')
 require(a['ledger_identity_sha256']==observed['ledger_identity_sha256'],'original_ledger_identity')
 require(a['public_plan']==observed['public_plan'] and a['public_plan'].startswith('https://github.com/dmarzzz/swarm-lab/blob/'+a['source_commit']+'/'),'immutable_plan')
 require(a['condition_tldrs']==observed['condition_tldrs'] and set(a['condition_tldrs'])==set(i.CONDITIONS),'condition_registration')
 require(all(len(x)>80 for x in a['condition_tldrs'].values()),'readable_tldrs')
 require(observed['model']==i.MODEL and observed['provider']=='OpenAI' and observed['input_rate']==.1 and observed['output_rate']==.5,'route_rate')
 require(type(observed['historical_hosting_usd']) in (int,float) and math.isfinite(observed['historical_hosting_usd']) and observed['historical_hosting_usd']>=0,'historical_hosting_known_subtotal')
 require(observed.get('historical_hosting_status') in ('reconciled','partial_with_legacy_exposure_preserved') and observed.get('older_lineage_reservations_preserved') is True,'historical_exposure_provenance')
 require(0<=observed['all_in_hosting_hourly_usd']<=.5/6 and observed['hosting_hours_reserved']<=6 and observed['hosting_max_usd']<=.5,'hosting_envelope')
 require(utc(a['until'])<=utc(observed['allocation_billing_start'])+dt.timedelta(hours=6),'hosting_lifetime')
 cap,reserved,calls=observed['budget'];require(cap==funding['study_cap_usd'] and cap>=18.971696+observed['historical_hosting_usd'],'cumulative_cap_amendment')
 expected=(7.961696,530) if a['stage']=='B1-D0' else (9.129056,770)
 require(abs(reserved-expected[0])<1e-8 and calls==expected[1],'budget_lineage')
 require(abs(reserved-a['budget_before']['reserved'])<1e-8 and calls==a['budget_before']['calls'],'budget_changed')
 if a['stage']=='B1-E0':require(a.get('d0_records_sha256')==observed.get('d0_records_sha256') and observed.get('d0_qualified') is True,'d0_qualification')
 return {'admitted':True,'stage':a['stage'],'maximum_requests':240 if a['stage']=='B1-D0' else 1920,'model_ceiling':MODEL_CEILING,'no_new_allowance':True}

class Sequence:
 def __init__(self,stage,cases,d0=None):
  require(stage in ('B1-D0','B1-E0'),'stage');self.cases={x['id']:x for x in cases};self.stage=stage
  if stage=='B1-E0':require(d0 is not None and i.qualification(cases,d0)['qualified'],'neutral_d0_gate')
  self.assignments=i.schedule(cases,'development' if stage=='B1-D0' else 'evaluation');self.index=0;self.records=[];self.active=None
 @property
 def complete(self):return self.index==len(self.assignments)
 def next(self):
  require(not self.complete,'complete')
  r=self.assignments[self.index]
  if self.active is None:self.active=i.Protocol(self.cases[r['case_id']],r['condition'],r['arm'],r['repetition'])
  return self.active.next()
 def accept(self,item,answer):
  self.active.accept(item,answer)
  if self.active.complete:
   self.records.append({**self.assignments[self.index],'execution':'complete','answers':self.active.answers})
   self.index+=1;self.active=None
 def export(self):
  records=list(self.records)
  if self.active is not None:records.append({**self.assignments[self.index],'execution':'partial','answers':self.active.answers})
  return records

class Session:
 def __init__(self,out,ledger,attempt,maximum,expected_budget):
  require(maximum in (240,1920),'stage_bound');require(Path(ledger).is_file(),'original_ledger_required')
  self.out=Path(out);self.out.mkdir(mode=0o700);self.ledger=str(ledger);self.attempt=attempt;self.maximum=maximum;self.count=0;self.stopped=False
  with database(self.ledger) as db:
   db.execute('BEGIN IMMEDIATE');b=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone()
   require(b is not None and abs(b[1]-expected_budget['reserved'])<1e-8 and b[2]==expected_budget['calls'],'budget_before')
   require(b[0]>=18.971696,'unamended_cap')
   scope=db.execute('SELECT maximum_model,model_debited,hosting_reserved,status FROM b1_scope WHERE packet_sha256=?',(FROZEN_PACKET,)).fetchone()
   require(scope is not None and abs(scope[0]-10.50624)<1e-9 and scope[1]>=0 and scope[2]==.5 and scope[3]=='funded','finite_scope_not_reserved')
   db.execute('CREATE TABLE IF NOT EXISTS b1_dispatch(attempt TEXT, ordinal INTEGER, wire_sha256 TEXT, reserved REAL, status TEXT, cost REAL, PRIMARY KEY(attempt,ordinal))')
   require(db.execute('SELECT count(*) FROM b1_dispatch WHERE attempt=?',(attempt,)).fetchone()[0]==0,'prior_attempt_preserved')
  save(self.out/'start.json',{'attempt':attempt,'maximum':maximum,'expected_budget':expected_budget,'retries':0})
 def event(self,event):
  with (self.out/'events.jsonl').open('a') as f:f.write(json.dumps(event,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())
 def dispatch(self,sequence,transport):
  require(not self.stopped and self.count<self.maximum,'circuit_closed')
  item=sequence.next();raw=c.encoded(item['wire']);require(len(raw)<=i.MAX_WIRE and sha(raw)==item['wire_sha256'],'exact_wire')
  ordinal=self.count+1
  save(self.out/f'{ordinal:04d}-request.bin',raw)
  try:
   with database(self.ledger) as db:
    db.execute('BEGIN IMMEDIATE');cap,reserved,calls=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone()
    require(reserved+i.RESERVATION<=min(cap,MODEL_CEILING)+1e-9 and calls<2690,'budget_ceiling')
    used=db.execute('SELECT maximum_model,model_debited,status FROM b1_scope WHERE packet_sha256=?',(FROZEN_PACKET,)).fetchone()
    require(used is not None and used[2]=='funded' and used[1]+i.RESERVATION<=used[0]+1e-9,'finite_scope_exhausted')
    db.execute('UPDATE b1_scope SET model_debited=model_debited+? WHERE packet_sha256=?',(i.RESERVATION,FROZEN_PACKET))
    db.execute('INSERT INTO b1_dispatch VALUES(?,?,?,?,?,NULL)',(self.attempt,ordinal,item['wire_sha256'],i.RESERVATION,'reserved_unknown'))
    db.execute('UPDATE budget SET reserved=reserved+?,calls=calls+1 WHERE id=1',(i.RESERVATION,))
   self.count=ordinal;self.event({'kind':'attempt_start','ordinal':ordinal,'wire_sha256':item['wire_sha256'],'reserved_usd':i.RESERVATION})
   # SQL reservation is durable before any transport. Ambiguity stays reserved, never retried.
   response=transport(raw);require(type(response) is bytes and len(response)<=1000000,'response_bound')
   save(self.out/f'{ordinal:04d}-response.bin',response)
   body=json.loads(response);u=body.get('usage',{});cost=u.get('cost')
   require(all(type(u.get(k)) is int and 0<=u[k]<=10000000 for k in ('prompt_tokens','completion_tokens')),'usage_missing')
   require(type(cost) in (int,float) and math.isfinite(cost) and cost>=0,'cost_missing')
   with database(self.ledger) as db:db.execute('UPDATE b1_dispatch SET status=?,cost=? WHERE attempt=? AND ordinal=?',('usage_observed',cost,self.attempt,ordinal))
   self.event({'kind':'usage','ordinal':ordinal,'cost_usd':cost,'input_tokens':u['prompt_tokens'],'output_tokens':u['completion_tokens']})
   require(cost<=i.RESERVATION+1e-12,'reservation_exceeded')
   require(body.get('provider')=='OpenAI' and body.get('model') in (i.MODEL,i.MODEL+'-20260922') and 'error' not in body,'served_route')
   choices=body['choices'];require(type(choices) is list and len(choices)==1,'choices');choice=choices[0]
   require(choice['finish_reason']=='stop' and not choice['message'].get('tool_calls'),'incomplete_or_tool_call')
   answer=i.decode(choice['message']['content'],sequence.active.case,item['final'])
   sequence.accept(item,answer)
   save(self.out/f'{ordinal:04d}-validated.json',{'wire_sha256':item['wire_sha256'],'answer':answer})
   with database(self.ledger) as db:db.execute('UPDATE b1_dispatch SET status=? WHERE attempt=? AND ordinal=?',('validated',self.attempt,ordinal))
   self.event({'kind':'validated','ordinal':ordinal});return answer
  except BaseException as exc:
   self.stopped=True
   # Never include raw exception text, HTTP body, request headers or credentials.
   self.event({'kind':'failure','ordinal':ordinal,'category':str(exc) if isinstance(exc,Stop) else type(exc).__name__,'retry_permitted':False})
   raise
 def closeout(self,sequence,failure):
  with database(self.ledger) as db:
   rows=db.execute('SELECT ordinal,reserved,status,cost FROM b1_dispatch WHERE attempt=? ORDER BY ordinal',(self.attempt,)).fetchall();budget=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone()
  missing=sum(x[3] is None for x in rows);cost=sum(x[3] or 0 for x in rows)
  summary={'attempt':self.attempt,'stage':sequence.stage,'planned_calls':self.maximum,'calls':len(rows),'valid_calls':sum(x[2]=='validated' for x in rows),'unstarted_calls':self.maximum-len(rows),'complete':sequence.complete and failure is None,'failure':failure,'usage_missing':missing,'reported_usd':cost,'actual_usd':None if missing else cost,'new_reserved_usd':sum(x[1] for x in rows),'budget_after':budget,'retries':0}
  save(self.out/'records.json',sequence.export());save(self.out/'summary.json',summary)
  if sequence.complete:
   review=i.qualification(list(sequence.cases.values()),sequence.records) if sequence.stage=='B1-D0' else i.analyze(list(sequence.cases.values()),sequence.records)
   save(self.out/'assessment.json',review)
  save(self.out/'operational-postmortem.json',{'execution':summary,'scientific_review':'required_by_owning_session','next_action':'stop; reconcile and review; no automatic repair or resume'})
  return summary

def collect(stage,cases,out,ledger,attempt,transport,until,expected_budget,d0=None,progress=None):
 seq=Sequence(stage,cases,d0);session=Session(out,ledger,attempt,240 if stage=='B1-D0' else 1920,expected_budget);failure=None;start=time.monotonic()
 try:
  while not seq.complete:
   require(time.monotonic()-start<6*3600-120 and dt.datetime.now(dt.timezone.utc)+dt.timedelta(seconds=90)<utc(until),'deadline')
   session.dispatch(seq,transport)
   if progress and (session.count%10==0 or seq.complete):progress(session.count,session.maximum)
 except Exception as exc:failure=str(exc) if isinstance(exc,Stop) else type(exc).__name__
 finally:summary=session.closeout(seq,failure)
 return summary

class Relay:
 """Local credential consumer supplies request(); this mirror admits only frozen wires.
 It stores no key and will not skip ahead, retry ambiguity, or reuse a prior journal.
 """
 def __init__(self,stage,cases,journal,d0=None):
  self.seq=Sequence(stage,cases,d0);self.dir=Path(journal);self.dir.mkdir(mode=0o700);self.count=0;self.stopped=False
 def send(self,raw,request):
  require(not self.stopped,'relay_closed');item=self.seq.next()
  try:
   require(raw==c.encoded(item['wire']),'relay_wire_mismatch');self.count+=1;save(self.dir/f'{self.count:04d}.start',{'wire_sha256':sha(raw)})
   response=request(raw);require(type(response) is bytes and len(response)<=1000000,'response_bound')
   save(self.dir/f'{self.count:04d}.response.bin',response)
   # Return malformed/incorrect replies unchanged so the worker can record their
   # usage and failure; stop this relay rather than swallowing evidence or retrying.
   try:
    b=json.loads(response);require(b.get('provider')=='OpenAI' and b.get('model') in (i.MODEL,i.MODEL+'-20260922'),'relay_route')
    require(len(b['choices'])==1 and b['choices'][0]['finish_reason']=='stop' and not b['choices'][0]['message'].get('tool_calls'),'relay_incomplete')
    answer=i.decode(b['choices'][0]['message']['content'],self.seq.active.case,item['final']);self.seq.accept(item,answer)
   except Exception:self.stopped=True
   save(self.dir/f'{self.count:04d}.end',{'response_sha256':sha(response),'relay_stopped':self.stopped});return response
  except BaseException:self.stopped=True;raise

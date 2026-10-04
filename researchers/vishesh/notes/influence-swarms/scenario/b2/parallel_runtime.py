"""E0-only operational amendment. Independent cells; original within-cell protocol.
No credential lookup, retries, funding or launch authority. D0 remains serial.
"""
import concurrent.futures as cf,datetime as dt,json,math,threading,time
from pathlib import Path
import cases as c,instrument as i,runtime as r
MAX_CELLS=16;START_INTERVAL=.25

def assignment_id(index,assignment):return f'{index:03d}-'+c.digest(assignment)[:16]

class Cell:
 def __init__(self,index,assignment,case):
  self.index=index;self.assignment=assignment;self.id=assignment_id(index,assignment)
  self.protocol=i.Protocol(case,assignment['condition'],assignment['arm'],assignment['repetition'])
 def export(self):return {**self.assignment,'execution':'complete' if self.protocol.complete else 'partial','answers':self.protocol.answers}

class Batch:
 def __init__(self,cases,d0=None,stage='B2-E0'):
  seq=r.Sequence(stage,cases,d0);self.cases=seq.cases;self.stage=stage
  self.cells=[Cell(n,a,self.cases[a['case_id']]) for n,a in enumerate(seq.assignments)]
 @property
 def complete(self):return all(x.protocol.complete for x in self.cells)
 @property
 def records(self):return self.export()
 def export(self):return [x.export() for x in self.cells if x.protocol.answers]

class ParallelSession(r.Session):
 def __init__(self,*args,interval=START_INTERVAL,**kwargs):
  super().__init__(*args,**kwargs);self.lock=threading.RLock();self.interval=interval;self.next_start=0.;self.failures=[]
 def event(self,event):
  with self.lock:super().event(event)
 def stop(self,category,ordinal=None):
  with self.lock:
   self.stopped=True;self.failures.append(category);self.event({'kind':'failure','ordinal':ordinal,'category':category,'retry_permitted':False})
 def dispatch_cell(self,cell,transport,until):
  ordinal=None
  try:
   # A single coordinator lock establishes total reservation order and rate pacing.
   # Waiting callers cannot bypass a stop, deadline, or ledger ceiling.
   with self.lock:
    r.require(not self.stopped and self.count<self.maximum,'circuit_closed')
    delay=self.next_start-time.monotonic()
    if delay>0:time.sleep(delay)
    r.require(dt.datetime.now(dt.timezone.utc)+dt.timedelta(seconds=90)<r.utc(until),'deadline')
    item=cell.protocol.next();raw=c.encoded(item['wire']);r.require(len(raw)<=i.MAX_WIRE and r.sha(raw)==item['wire_sha256'],'exact_wire')
    ordinal=self.count+1;step=len(cell.protocol.answers)
    r.save(self.out/f'{ordinal:04d}-request.bin',raw)
    r.save(self.out/f'{ordinal:04d}-assignment.json',{'assignment_id':cell.id,'assignment_index':cell.index,'step':step,'assignment':cell.assignment,'wire_sha256':item['wire_sha256']})
    with r.database(self.ledger) as db:
     db.execute('BEGIN IMMEDIATE');cap,reserved,calls=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone()
     r.require(reserved+i.RESERVATION<=min(cap,r.MODEL_CEILING)+1e-9 and calls<2786,'budget_ceiling')
     used=db.execute('SELECT maximum_model,model_debited,status FROM b1_scope WHERE packet_sha256=?',(r.FROZEN_PACKET,)).fetchone()
     r.require(used is not None and used[2]=='funded' and used[1]+i.RESERVATION<=used[0]+1e-9,'finite_scope_exhausted')
     db.execute('UPDATE b1_scope SET model_debited=model_debited+? WHERE packet_sha256=?',(i.RESERVATION,r.FROZEN_PACKET))
     db.execute('INSERT INTO b1_dispatch VALUES(?,?,?,?,?,NULL)',(self.attempt,ordinal,item['wire_sha256'],i.RESERVATION,'reserved_unknown'))
     db.execute('UPDATE budget SET reserved=reserved+?,calls=calls+1 WHERE id=1',(i.RESERVATION,))
    self.count=ordinal;self.next_start=time.monotonic()+self.interval
    self.event({'kind':'attempt_start','ordinal':ordinal,'assignment_id':cell.id,'step':step,'wire_sha256':item['wire_sha256'],'reserved_usd':i.RESERVATION})
   # Calls already dispatched before another failure still drain and are accounted.
   response=transport(raw,cell.id,step);r.require(type(response) is bytes and len(response)<=1000000,'response_bound')
   r.save(self.out/f'{ordinal:04d}-response.bin',response)
   body=json.loads(response);u=body.get('usage',{});cost=u.get('cost')
   r.require(all(type(u.get(k)) is int and 0<=u[k]<=10000000 for k in ('prompt_tokens','completion_tokens')),'usage_missing')
   r.require(type(cost) in (int,float) and math.isfinite(cost) and cost>=0,'cost_missing')
   with r.database(self.ledger) as db:db.execute('UPDATE b1_dispatch SET status=?,cost=? WHERE attempt=? AND ordinal=?',('usage_observed',cost,self.attempt,ordinal))
   self.event({'kind':'usage','ordinal':ordinal,'cost_usd':cost,'input_tokens':u['prompt_tokens'],'output_tokens':u['completion_tokens']})
   r.require(cost<=i.RESERVATION+1e-12,'reservation_exceeded')
   r.require(body.get('provider')=='OpenAI' and body.get('model') in (i.MODEL,i.MODEL+'-20260922') and 'error' not in body,'served_route')
   choices=body['choices'];r.require(type(choices) is list and len(choices)==1,'choices');choice=choices[0]
   r.require(choice['finish_reason']=='stop' and not choice['message'].get('tool_calls'),'incomplete_or_tool_call')
   answer=i.decode(choice['message']['content'],cell.protocol.case,item['final']);cell.protocol.accept(item,answer)
   r.save(self.out/f'{ordinal:04d}-validated.json',{'assignment_id':cell.id,'step':step,'wire_sha256':item['wire_sha256'],'answer':answer})
   with r.database(self.ledger) as db:db.execute('UPDATE b1_dispatch SET status=? WHERE attempt=? AND ordinal=?',('validated',self.attempt,ordinal))
   self.event({'kind':'validated','ordinal':ordinal,'assignment_id':cell.id,'step':step});return answer
  except BaseException as exc:
   # A waiting cell denied by an existing circuit closure is not another request.
   if not (isinstance(exc,r.Stop) and str(exc)=='circuit_closed'):self.stop(str(exc) if isinstance(exc,r.Stop) else type(exc).__name__,ordinal)
   raise

def collect(cases,out,ledger,attempt,transport,until,expected_budget,d0=None,progress=None,*,stage='B2-E0',concurrency=16,interval=START_INTERVAL):
 r.require(type(concurrency) is int and 1<=concurrency<=MAX_CELLS,'concurrency_bound')
 batch=Batch(cases,d0,stage);maximum=96 if stage=='B2-D0' else 1920;session=ParallelSession(out,ledger,attempt,maximum,expected_budget,interval=interval)
 r.save(Path(out)/'execution-amendment.json',{'mode':'concurrent_cells_v1','concurrency':concurrency,'minimum_start_interval_seconds':interval,'assignment_ids':[x.id for x in batch.cells],'global_stop':True,'drain_inflight':True,'within_cell':'sequential','packet_sha256':r.FROZEN_PACKET})
 def run_cell(cell):
  while not cell.protocol.complete:
   session.dispatch_cell(cell,transport,until)
  return cell.index
 pending={};next_index=0;last_progress=0
 with cf.ThreadPoolExecutor(max_workers=concurrency) as pool:
  try:
   while next_index<len(batch.cells) or pending:
    while not session.stopped and next_index<len(batch.cells) and len(pending)<concurrency:
     cell=batch.cells[next_index];pending[pool.submit(run_cell,cell)]=cell.index;next_index+=1
    if not pending:break
    done,_=cf.wait(pending,return_when=cf.FIRST_COMPLETED)
    for future in done:
     pending.pop(future)
     try:future.result()
     except Exception:pass # dispatch already latched failure; all pending work drains.
    if progress and session.count-last_progress>=10:
     try:progress(sum(len(x.protocol.answers) for x in batch.cells),maximum);last_progress=session.count
     except Exception as exc:session.stop(type(exc).__name__)
  except Exception as exc:session.stop(type(exc).__name__)
 failure=session.failures[0] if session.failures else None
 return session.closeout(batch,failure)

class Relay:
 """Independent per-cell wire mirrors; metadata never enters provider messages."""
 def __init__(self,cases,journal,d0=None,concurrency=16,interval=START_INTERVAL,stage='B2-E0'):
  r.require(type(concurrency) is int and 1<=concurrency<=16,'relay_concurrency');self.batch=Batch(cases,d0,stage);self.cells={x.id:x for x in self.batch.cells}
  self.dir=Path(journal);self.dir.mkdir(mode=0o700);self.lock=threading.RLock();self.count=0;self.stopped=False;self.busy=set();self.concurrency=concurrency;self.next_start=0.;self.interval=interval
 def send(self,raw,assignment,step,request):
  ordinal=None
  try:
   with self.lock:
    r.require(not self.stopped,'relay_closed');r.require(assignment in self.cells and assignment not in self.busy and len(self.busy)<self.concurrency,'relay_assignment')
    cell=self.cells[assignment];r.require(type(step) is int and step==len(cell.protocol.answers),'relay_step');item=cell.protocol.next();r.require(raw==c.encoded(item['wire']),'relay_wire_mismatch')
    delay=self.next_start-time.monotonic()
    if delay>0:time.sleep(delay)
    self.count+=1;ordinal=self.count;self.busy.add(assignment);self.next_start=time.monotonic()+self.interval
    r.save(self.dir/f'{ordinal:04d}.start',{'assignment_id':assignment,'step':step,'wire_sha256':r.sha(raw)})
   response=request(raw);r.require(type(response) is bytes and len(response)<=1000000,'response_bound');r.save(self.dir/f'{ordinal:04d}.response.bin',response)
   try:
    b=json.loads(response);r.require(b.get('provider')=='OpenAI' and b.get('model') in (i.MODEL,i.MODEL+'-20260922'),'relay_route')
    u=b.get('usage',{});cost=u.get('cost');r.require(all(type(u.get(k)) is int and 0<=u[k]<=10000000 for k in ('prompt_tokens','completion_tokens')) and type(cost) in (int,float) and math.isfinite(cost) and 0<=cost<=i.RESERVATION+1e-12,'relay_usage')
    r.require(len(b['choices'])==1 and b['choices'][0]['finish_reason']=='stop' and not b['choices'][0]['message'].get('tool_calls'),'relay_incomplete')
    answer=i.decode(b['choices'][0]['message']['content'],cell.protocol.case,item['final']);cell.protocol.accept(item,answer)
   except Exception:
    with self.lock:self.stopped=True
   r.save(self.dir/f'{ordinal:04d}.end',{'response_sha256':r.sha(response),'relay_stopped':self.stopped});return response
  except BaseException:
   with self.lock:self.stopped=True
   raise
  finally:
   if ordinal is not None:
    with self.lock:self.busy.discard(assignment)

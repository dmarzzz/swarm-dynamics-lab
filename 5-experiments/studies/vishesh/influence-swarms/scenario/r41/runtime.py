"""Finite, fault-contained R40 acquisition; no credential loading or allocation.
The operator must provision a genuine source-bound grant in the ORIGINAL ledger.
"""
from __future__ import annotations
import concurrent.futures as cf,datetime as dt,hashlib,json,math,sqlite3,threading,time
from contextlib import closing,contextmanager
from pathlib import Path
import cases as c,instrument as i
GRANT='R41-3744';MAXIMUM_MODEL=21.326848;MAX_CALLS=3744;CONCURRENCY=16;INTERVAL=.25
class Stop(Exception):pass
class FormatFault(Exception):pass
def require(ok,reason):
 if not ok:raise Stop(reason)
def save(path,value):
 raw=value if isinstance(value,bytes) else c.encoded(value)
 with open(path,'xb') as f:f.write(raw);f.flush()
def utc(value):return dt.datetime.fromisoformat(value.replace('Z','+00:00'))
@contextmanager
def database(path):
 db=sqlite3.connect(path,timeout=30)
 try:
  with db:yield db
 finally:db.close()
def key(root):return root.case['id']+f'/repeat-{root.repetition}'
def response(raw,case,node):
 require(type(raw)is bytes and len(raw)<=1000000,'response_bound');body=json.loads(raw);u=body.get('usage',{});cost=u.get('cost')
 require(all(type(u.get(k))is int and 0<=u[k]<=10000000 for k in ('prompt_tokens','completion_tokens')),'usage_missing')
 require(type(cost)in(int,float) and math.isfinite(cost) and 0<=cost<=i.RESERVATION+1e-12,'cost_bound')
 require(body.get('provider')=='OpenAI' and body.get('model')in(i.MODEL,i.MODEL+'-20260922') and 'error'not in body,'route')
 choices=body.get('choices');require(type(choices)is list and len(choices)==1,'choices');choice=choices[0]
 require(not choice.get('message',{}).get('tool_calls'),'unexpected_tool')
 if choice.get('finish_reason')=='length':return body,None,'length'
 require(choice.get('finish_reason')=='stop','unexpected_finish')
 try:answer=i.decode(choice['message']['content'],case,node)
 except (ValueError,KeyError,TypeError):return body,None,'local_structure'
 return body,answer,None

class Session:
 def __init__(self,cases,out,ledger,attempt,stage,source,manifest,expected,until,interval=INTERVAL,qualification_receipt=None):
  require(stage in ('R41-D1','R41-Q0','R41-E0'),'stage');require(Path(ledger).is_file(),'original_ledger')
  if stage in ('R41-Q0','R41-E0'):
   q=qualification_receipt or {};passed=i.partial_qualification(cases,q.get('records',[]),'R41-D1')['qualified'] if stage=='R41-Q0' else i.qualification(cases,q.get('records',[]))['qualified'];require(q.get('source')==source and q.get('manifest')==manifest and q.get('native_run') and passed,'source_bound_native_qualification')
  self.roots=i.schedule(cases,stage);self.lookup={key(x):x for x in self.roots};self.out=Path(out);self.out.mkdir(mode=0o700);self.ledger=str(ledger);self.attempt=attempt;self.stage=stage;self.source=source;self.manifest=manifest;self.until=until;self.maximum={'R41-D1':84,'R41-Q0':672,'R41-E0':2988}[stage];self.count=0;self.stopped=False;self.failure=None;self.lock=threading.RLock();self.next_start=0.;self.interval=interval
  with database(ledger) as db:
   row=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone();require(row and row[0]==50 and abs(row[1]-expected['reserved'])<1e-8 and row[2]==expected['calls'],'original_budget_drift')
   grant=db.execute('SELECT source,manifest,maximum_model,model_debited,max_calls,calls,status FROM r41_scope WHERE grant_id=?',(GRANT,)).fetchone();require(grant and grant[0]==source and grant[1]==manifest and grant[2]==MAXIMUM_MODEL and grant[4]==MAX_CALLS and grant[6]=='funded','source_bound_finite_grant')
   require(db.execute('SELECT count(*) FROM b1_dispatch WHERE attempt=?',(attempt,)).fetchone()[0]==0,'attempt_reuse')
  save(self.out/'start.json',{'attempt':attempt,'stage':stage,'source':source,'manifest':manifest,'maximum':self.maximum,'expected_budget':expected,'until':until,'retries':0})
  save(self.out/'assignments.json',[{'root':key(r),'case_id':r.case['id'],'repetition':r.repetition,'nodes':r.nodes} for r in self.roots])
 def event(self,event):
  with self.lock:
   with open(self.out/'events.jsonl','ab') as f:f.write(c.encoded(event)+b'\n');f.flush()
 def stop(self,reason):
  with self.lock:
   if not self.stopped:self.stopped=True;self.failure=reason;self.event({'kind':'global_stop','reason':reason})
 def dispatch(self,root,node,transport):
  ordinal=None
  try:
   with self.lock:
    require(not self.stopped and self.count<self.maximum,'circuit_closed');delay=self.next_start-time.monotonic()
    if delay>0:time.sleep(delay)
    require(dt.datetime.now(dt.timezone.utc)+dt.timedelta(seconds=90)<utc(self.until),'deadline')
    item=root.item(node['id']);raw=c.encoded(item['wire']);require(len(raw)<=i.MAX_WIRE and (len(raw)+512)*.125/1e6+3072*.5/1e6<=i.RESERVATION+1e-12,'wire_reservation')
    ordinal=self.count+1;save(self.out/f'{ordinal:04d}-request.bin',raw);save(self.out/f'{ordinal:04d}-assignment.json',{'root':key(root),'node':node,'wire_sha256':item['wire_sha256'],'context_sha256':item['context_sha256'],'parent_hashes':item['parent_hashes']})
    with database(self.ledger) as db:
     db.execute('BEGIN IMMEDIATE');cap,reserved,calls=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone();require(reserved+i.RESERVATION<=min(cap,44.397664)+1e-9,'study_ceiling')
     g=db.execute('SELECT source,manifest,maximum_model,model_debited,max_calls,calls,status FROM r41_scope WHERE grant_id=?',(GRANT,)).fetchone();require(g and g[0]==self.source and g[1]==self.manifest and g[6]=='funded','grant_changed');require(g[3]+i.RESERVATION<=g[2]+1e-9 and g[5]<g[4],'grant_exhausted')
     db.execute('INSERT INTO r41_work VALUES(?,?,?,?,?,?)',(GRANT,self.stage,key(root),node['id'],self.attempt,ordinal))
     db.execute('UPDATE r41_scope SET model_debited=model_debited+?,calls=calls+1 WHERE grant_id=?',(i.RESERVATION,GRANT));db.execute('INSERT INTO b1_dispatch VALUES(?,?,?,?,?,NULL)',(self.attempt,ordinal,item['wire_sha256'],i.RESERVATION,'reserved_unknown'));db.execute('UPDATE budget SET reserved=reserved+?,calls=calls+1 WHERE id=1',(i.RESERVATION,))
    self.count=ordinal;self.next_start=time.monotonic()+self.interval;self.event({'kind':'start','ordinal':ordinal,'root':key(root),'node':node['id'],'wire_sha256':item['wire_sha256'],'reserved_usd':i.RESERVATION})
   raw_response=transport(raw,key(root),node['id']);save(self.out/f'{ordinal:04d}-response.bin',raw_response)
   # Record a valid usage receipt even if route or output subsequently fails.
   body=json.loads(raw_response);cost=body.get('usage',{}).get('cost')
   if type(cost)in(int,float) and math.isfinite(cost) and cost>=0:
    with database(self.ledger) as db:db.execute('UPDATE b1_dispatch SET status=?,cost=? WHERE attempt=? AND ordinal=?',('usage_observed',cost,self.attempt,ordinal))
   body,answer,fault=response(raw_response,root.case,node)
   with self.lock:
    if fault:root.fail(item,fault);status='known_format_failure'
    else:root.accept(item,answer);status='validated';save(self.out/f'{ordinal:04d}-validated.json',{'root':key(root),'node':node['id'],'answer':answer})
    with database(self.ledger) as db:db.execute('UPDATE b1_dispatch SET status=?,cost=? WHERE attempt=? AND ordinal=?',(status,body['usage']['cost'],self.attempt,ordinal))
    self.event({'kind':status,'ordinal':ordinal,'root':key(root),'node':node['id'],'cost_usd':body['usage']['cost'],'failure':fault})
  except BaseException as e:
   if not(isinstance(e,Stop) and str(e)=='circuit_closed'):self.stop(str(e) if isinstance(e,Stop) else type(e).__name__)
   raise
 def run(self,transport,concurrency=CONCURRENCY,progress=None):
  require(type(concurrency)is int and 1<=concurrency<=16,'concurrency');pending={};busy=set();cursor=0;last=0
  with cf.ThreadPoolExecutor(max_workers=concurrency) as pool:
   while True:
    with self.lock:
     if not self.stopped:
      for offset in range(len(self.roots)):
       root=self.roots[(cursor+offset)%len(self.roots)]
       for node in root.ready():
        task=(key(root),node['id'])
        if task in busy:continue
        if len(pending)>=concurrency:break
        busy.add(task);pending[pool.submit(self.dispatch,root,node,transport)]=task
       if len(pending)>=concurrency:break
      cursor=(cursor+1)%len(self.roots)
    if not pending:break
    done,_=cf.wait(pending,return_when=cf.FIRST_COMPLETED)
    for future in done:
     busy.remove(pending.pop(future))
     try:future.result()
     except Exception:pass # durable stop or known branch fault already recorded
    if progress and self.count-last>=16:
     try:progress(self.count,self.maximum)
     except Exception as e:self.stop(type(e).__name__)
     last=self.count
  records=[r.export() for r in self.roots];save(self.out/'records.json',records)
  with database(self.ledger) as db:
   rows=db.execute('SELECT status,cost FROM b1_dispatch WHERE attempt=?',(self.attempt,)).fetchall();budget=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone()
  states=[n['state'] for r in records for n in r['nodes']];known=sum(status=='known_format_failure' for status,_ in rows);missing=sum(cost is None for _,cost in rows)
  summary={'attempt':self.attempt,'stage':self.stage,'complete':not self.stopped and 'unstarted'not in states,'all_nodes_observed':all(x=='valid' for x in states),'calls':len(rows),'valid_calls':sum(x=='validated' for x,_ in rows),'known_format_failures':known,'unstarted_calls':self.maximum-len(rows),'blocked_nodes':states.count('blocked'),'failure':self.failure,'usage_missing':missing,'reported_usd':sum(cost for _,cost in rows if cost is not None),'actual_usd':None if missing else sum(cost for _,cost in rows),'new_reserved_usd':len(rows)*i.RESERVATION,'budget_after':budget,'retries':0}
  save(self.out/'summary.json',summary);return records,summary

class Relay:
 """Second exact-context gate; metadata never becomes provider prompt text."""
 def __init__(self,cases,stage,out):
  self.roots={key(r):r for r in i.schedule(cases,stage)};self.lock=threading.RLock();self.busy=set();self.count=0;self.maximum={'R41-D1':84,'R41-Q0':672,'R41-E0':2988}[stage];self.stopped=False;self.out=Path(out);self.out.mkdir(mode=0o700);self.next_start=0.
 def send(self,raw,root_id,node_id,request):
  task=(root_id,node_id);ordinal=None
  try:
   with self.lock:
    require(not self.stopped and self.count<self.maximum and len(self.busy)<16 and task not in self.busy,'relay_closed_or_busy');require(root_id in self.roots,'root');root=self.roots[root_id];item=root.item(node_id);require(raw==c.encoded(item['wire']),'relay_wire')
    delay=self.next_start-time.monotonic()
    if delay>0:time.sleep(delay)
    self.count+=1;ordinal=self.count;self.busy.add(task);self.next_start=time.monotonic()+INTERVAL;save(self.out/f'{ordinal:04d}.start',{'root':root_id,'node':node_id,'wire_sha256':item['wire_sha256']})
   result=request(raw);save(self.out/f'{ordinal:04d}.response.bin',result);body,answer,fault=response(result,root.case,item['node'])
   with self.lock:
    if fault:root.fail(item,fault)
    else:root.accept(item,answer)
   return result
  except BaseException:
   with self.lock:self.stopped=True
   raise
  finally:
   with self.lock:
    self.busy.discard(task)
    if ordinal is not None:save(self.out/f'{ordinal:04d}.end',{'relay_stopped':self.stopped})

"""Wave-scheduled exact-wire recovery. All charges use the original study ledger."""
import concurrent.futures as cf,copy,datetime as dt,json,math,sqlite3,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'r41'))
import cases as c,instrument as i,runtime as r,analysis
MAX_LOGICAL=2988;MAX_RETRIES=30;MAX_CALLS=3018;MAX_COST=17.191552

def reserve(ledger,attempt,source,manifest,root,node,wire,until):
 r.require(dt.datetime.now(dt.timezone.utc)+dt.timedelta(seconds=90)<r.utc(until),'deadline')
 with r.database(ledger)as db:
  db.execute('BEGIN IMMEDIATE');g=db.execute('SELECT source,manifest,calls,reserved,retries,status FROM r43_scope WHERE attempt=?',(attempt,)).fetchone()
  r.require(g and g[:2]==(source,manifest)and g[5]=='funded','source_grant')
  previous=db.execute('SELECT try,status,cost,wire FROM r43_calls WHERE attempt=? AND root=? AND node=? ORDER BY try',(attempt,root,node)).fetchall();trial=1
  if previous:
   r.require(len(previous)==1 and previous[0][0]==1 and previous[0][1]=='length'and previous[0][2]is not None and previous[0][3]==wire,'retry_ineligible');trial=2
   r.require(g[4]<MAX_RETRIES,'retry_pool_exhausted')
  cap,spent,count=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone()
  r.require(cap==50 and spent+i.RESERVATION<=min(cap,44.574240)+1e-9,'study_ceiling');r.require(g[2]<MAX_CALLS and g[3]+i.RESERVATION<=MAX_COST+1e-9,'grant_exhausted')
  ordinal=g[2]+1;db.execute('INSERT INTO r43_calls VALUES(?,?,?,?,?,?,?,?,?,NULL)',(attempt,root,node,trial,ordinal,wire,i.RESERVATION,'reserved_unknown',None))
  db.execute('UPDATE r43_scope SET calls=calls+1,reserved=reserved+?,retries=retries+? WHERE attempt=?',(i.RESERVATION,int(trial==2),attempt));db.execute('UPDATE budget SET reserved=reserved+?,calls=calls+1 WHERE id=1',(i.RESERVATION,))
 return ordinal,trial

def settle(ledger,attempt,ordinal,status,cost):
 with r.database(ledger)as db:
  row=db.execute('SELECT status FROM r43_calls WHERE attempt=? AND ordinal=?',(attempt,ordinal)).fetchone();r.require(row and row[0]=='reserved_unknown','already_settled')
  db.execute('UPDATE r43_calls SET status=?,cost=? WHERE attempt=? AND ordinal=?',(status,cost,attempt,ordinal))

def project_first_pass(cases,records,first_failures):
 cases={case['id']:case for case in cases}
 result=copy.deepcopy(records)
 for record in result:
  bad=set(first_failures.get(record['case_id']+f"/repeat-{record['repetition']}",[]))
  graph=i.make_graph(cases[record['case_id']],record['repetition'],('truthful','misleading'))
  parents={n['id']:n['parents'] for n in graph}
  for node in record['nodes']:
   if node['id']in bad:node.update(state='format_failed',answer=None,failure='first_pass_length')
   elif any(p in bad for p in parents[node['id']]):bad.add(node['id']);node.update(state='blocked',answer=None,failure='depends_on_first_pass_failure')
 return result

def wave(roots,pending,limit=16):
 order={r.key(root):n for n,root in enumerate(roots)};nodeorder={(r.key(root),n['id']):j for root in roots for j,n in enumerate(root.nodes)}
 retries=sorted(pending,key=lambda key:(order[key[0]],nodeorder[key]));chosen=list(retries[:limit]);seen=set(chosen)
 ready=[[n for n in root.ready()if(r.key(root),n['id'])not in pending]for root in roots]
 for depth in range(max([len(z)for z in ready],default=0)):
  for root,nodes in zip(roots,ready):
   if len(chosen)>=limit:return chosen
   if depth<len(nodes):
    key=(r.key(root),nodes[depth]['id'])
    if key not in seen:chosen.append(key);seen.add(key)
 return chosen

class Session:
 def __init__(self,cases,out,ledger,attempt,source,manifest,until,expected,qualification,roots=None):
  r.require(i.qualification(cases,qualification)['qualified'],'recovery_assisted_competence')
  self.roots=roots if roots is not None else i.schedule(cases,'R41-E0');self.lookup={r.key(z):z for z in self.roots};self.cases=cases;self.out=Path(out);r.require(not self.out.exists(),'attempt_directory_exists');self.ledger=ledger;self.attempt=attempt;self.source=source;self.manifest=manifest;self.until=until;self.pending=set();self.first={};self.failure=None;self.events=[]
  with r.database(ledger)as db:
   b=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone();g=db.execute('SELECT source,manifest,calls,reserved,retries,status FROM r43_scope WHERE attempt=?',(attempt,)).fetchone();r.require(abs(b[1]-expected[0])<1e-8 and b[2]==expected[1],'original_budget');r.require(g==(source,manifest,0,0,0,'funded'),'fresh_grant');r.require(db.execute('SELECT count(*)FROM r43_calls WHERE attempt=?',(attempt,)).fetchone()[0]==0,'restart_refused')
  self.out.mkdir(mode=0o700);r.save(self.out/'start.json',{'attempt':attempt,'source':source,'manifest':manifest,'maximum_calls':MAX_CALLS,'maximum_retries':MAX_RETRIES,'qualification':'recovery-assisted; first-pass development failed'})
 def run(self,transport,progress=None):
  with cf.ThreadPoolExecutor(max_workers=16)as pool:
   while not self.failure:
    batch=wave(self.roots,self.pending)
    if not batch:break
    prepared=[]
    for rootid,nodeid in batch:
     root=self.lookup[rootid];item=root.item(nodeid)
     try:ordinal,trial=reserve(self.ledger,self.attempt,self.source,self.manifest,rootid,nodeid,item['wire_sha256'],self.until)
     except r.Stop as e:
      if str(e)=='retry_pool_exhausted':root.fail(item,'retry_pool_exhausted');self.pending.discard((rootid,nodeid));continue
      self.failure=str(e);break
     except Exception as e:self.failure=type(e).__name__;break
     raw=c.encoded(item['wire']);r.save(self.out/f'{ordinal:04d}-request.bin',raw);r.save(self.out/f'{ordinal:04d}-assignment.json',{'root':rootid,'node':item['node'],'try':trial,'wire_sha256':item['wire_sha256'],'context_sha256':item['context_sha256'],'parent_hashes':item['parent_hashes']});prepared.append((ordinal,trial,root,item,raw))
    # Reserved in deterministic order before dispatch; all in-flight costs count.
    futures=[pool.submit(transport,raw,r.key(root),item['node']['id'])for _,_,root,item,raw in prepared]
    for(ordinal,trial,root,item,raw),future in zip(prepared,futures):
     rootid=r.key(root);nodeid=item['node']['id'];task=(rootid,nodeid)
     try:
      data=future.result();r.save(self.out/f'{ordinal:04d}-response.bin',data);body,answer,fault=r.response(data,root.case,item['node']);status=fault or 'validated';settle(self.ledger,self.attempt,ordinal,status,body['usage']['cost'])
      if trial==1 and fault=='length':self.first.setdefault(rootid,[]).append(nodeid);self.pending.add(task)
      elif fault:root.fail(item,fault);self.pending.discard(task)
      else:root.accept(item,answer);self.pending.discard(task);r.save(self.out/f'{ordinal:04d}-validated.json',answer)
      self.events.append({'ordinal':ordinal,'root':rootid,'node':nodeid,'try':trial,'status':status,'cost':body['usage']['cost']})
     except Exception as e:self.failure=str(e)if isinstance(e,r.Stop)else type(e).__name__;self.events.append({'ordinal':ordinal,'root':rootid,'node':nodeid,'try':trial,'status':'unreconciled','error':self.failure})
    if prepared:r.save(self.out/f'wave-{len(self.events):04d}.json',self.events[-len(prepared):])
    if progress:
     try:progress(len(self.events),MAX_CALLS)
     except Exception as e:self.failure=type(e).__name__
  records=[z.export()for z in self.roots];first=project_first_pass(self.cases,records,self.first);r.save(self.out/'records.json',records);r.save(self.out/'first-pass-records.json',first);r.save(self.out/'events.json',self.events)
  with r.database(self.ledger)as db:
   calls=db.execute('SELECT status,cost,try FROM r43_calls WHERE attempt=?',(self.attempt,)).fetchall();b=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone();db.execute("UPDATE r43_scope SET status='closed' WHERE attempt=?",(self.attempt,))
  summary={'attempt':self.attempt,'physical_calls':len(calls),'retry_calls':sum(t==2 for _,_,t in calls),'known_length_failures':sum(s=='length'for s,_,t in calls),'valid_responses':sum(s=='validated'for s,_,t in calls),'unknown_usage':sum(cost is None for _,cost,t in calls),'known_cost':sum(cost for _,cost,t in calls if cost is not None),'reserved':len(calls)*i.RESERVATION,'global_failure':self.failure,'logical_valid':sum(n['state']=='valid'for z in records for n in z['nodes']),'first_pass_available':sum(n['state']=='valid'for z in first for n in z['nodes']),'budget_after':b}
  r.save(self.out/'summary.json',summary);return records,first,summary

class Relay:
 """Independent exact-context, duplicate and retry cap gate; no credentials."""
 def __init__(self,cases,out):
  import threading
  self.roots={r.key(z):z for z in i.schedule(cases,'R41-E0')};self.lock=threading.RLock();self.busy=set();self.tries={};self.last={};self.count=0;self.retries=0;self.stopped=False;self.out=Path(out);self.out.mkdir(mode=0o700);self.next_start=0.
 def send(self,raw,rootid,nodeid,request):
  import time
  task=(rootid,nodeid);ordinal=None
  try:
   with self.lock:
    r.require(not self.stopped and self.count<MAX_CALLS and len(self.busy)<16 and task not in self.busy,'relay_closed');root=self.roots[rootid];item=root.item(nodeid);r.require(raw==c.encoded(item['wire']),'relay_exact_wire');previous=self.tries.get(task,0)
    if previous:r.require(previous==1 and self.last.get(task)=='length'and self.retries<MAX_RETRIES,'relay_retry');self.retries+=1
    delay=self.next_start-time.monotonic()
    if delay>0:time.sleep(delay)
    self.next_start=time.monotonic()+.25;self.count+=1;ordinal=self.count;self.tries[task]=previous+1;self.busy.add(task);r.save(self.out/f'{ordinal:04d}.start',{'root':rootid,'node':nodeid,'try':previous+1,'wire_sha256':item['wire_sha256']})
   result=request(raw);r.save(self.out/f'{ordinal:04d}.response.bin',result);body,answer,fault=r.response(result,root.case,item['node'])
   with self.lock:
    self.last[task]=fault or 'validated'
    if fault:
     if fault!='length' or previous:root.fail(item,fault)
    else:root.accept(item,answer)
   return result
  except BaseException:
   with self.lock:self.stopped=True
   raise
  finally:
   with self.lock:
    self.busy.discard(task)
    if ordinal is not None:r.save(self.out/f'{ordinal:04d}.end',{'relay_stopped':self.stopped})

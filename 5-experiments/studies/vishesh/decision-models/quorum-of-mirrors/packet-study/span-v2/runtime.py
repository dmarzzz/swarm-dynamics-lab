"""One-shot qualification, original ledger, credential from encrypted SSH stdin only."""
from pathlib import Path
import hashlib,json,sys,os,time,sqlite3,urllib.request,urllib.error,math,socket,re
HERE=Path(__file__).resolve().parent;STUDY=HERE.parent.parent
sys.path.insert(0,str(STUDY));import next_runtime as legacy
import public_plan
from diagnostics import classify_http
import budget
from contract import ATTEMPT,MODEL,RESERVE,request,digest,bound,score,summarize,decode
FILES=['PLAN.md','contract.py','runtime.py','manifest.json','cases.py','baseline.py','grammar.py','qualification-seal.json','AUTHORIZATION.json','HISTORY.json','diagnostics.py','budget.py','../native-v2/AUTHORIZATION.json','../robustness-v1/AUTHORIZATION.json','../../next_runtime.py','../../qualification.py','../../next_stage.py','../../reference.py','../../public_plan.py']
def hashes():return {n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in FILES}
def append(path,value):
 with path.open('a') as f:f.write(json.dumps(value)+'\n');f.flush();os.fsync(f.fileno())
def save(path,value):
 with path.open('x') as f:json.dump(value,f,indent=2);f.flush();os.fsync(f.fileno())
def route_check():
 data=json.load(urllib.request.urlopen('https://openrouter.ai/api/v1/models/'+MODEL+'/endpoints',timeout=25))['data']
 es=[e for e in data['endpoints'] if e['provider_name']=='Anthropic' and e['status']==0 and '20260217' in e['name']]
 assert len(es)==1 and float(es[0]['pricing']['prompt'])<=.000003 and float(es[0]['pricing']['completion'])<=.000015,'route_price'
 return {'model':MODEL,'provider':'Anthropic','snapshot':'20260217','pricing_verified':True,'checked_at':time.time()}
def preflight(c,packet):
 assert c['source_sha256']==hashes(),'source_changed'
 assert c['owner_directed_qualification'] is True and c['max_calls']==40 and c['max_reserved_usd']==1.92,'scope'
 a=c['allocation'];now=time.time()
 assert a['host']==socket.gethostname().split('.')[0] and a['exclusive'] and a['approved_account_verified'] and a['merged_claim_verified'] and a['workload_verified_clear'],'allocation'
 assert 0<=now-a['checked_at']<900 and now<a['expires_at'] and now<c['deadline'],'allocation_expired'
 assert c['infrastructure_total_bound_usd']<=1 and c['cumulative_hours_bound']<=6,'infrastructure'
 manifest=json.loads((HERE/'manifest.json').read_text());assert manifest==packet['manifest'] and manifest['attempt']==ATTEMPT,'manifest'
 assert len(packet['rows'])==40 and len(manifest['assignments'])==40 and digest(packet['rows'])==manifest['corpus_sha256'],'case_count'
 for assignment,row in zip(manifest['assignments'],packet['rows']):assert assignment['request_sha256']==digest(request(row['actor'])) and bound(request(row['actor']))<=7000,'request_changed'
 history=json.loads((HERE/'HISTORY.json').read_text())
 with sqlite3.connect('file:'+c['ledger']+'?mode=ro',uri=True) as db:
  rows=db.execute('select id,reserved,status,actual from calls order by id').fetchall()
  assert hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()==history['calls_sha256'],'historical_ledger'
  assert db.execute('select experiment,cap from authority where id=1').fetchone()==('quorum-of-mirrors',1.),'base_authority'
  assert not db.execute("select 1 from next_attempts where status='running'").fetchone(),'running_attempt'
 with sqlite3.connect('file:'+c['ledger']+'?mode=ro',uri=True) as db:effective=budget.exposure(db)
 budget_info={'calls':len(rows),'reserved_usd':round(sum(r[1] for r in rows),9),'effective_exposure_usd':effective,'prior_unknown_bound_usd':.061344}
 assert budget_info['calls']==182 and budget_info['reserved_usd']==6.425856 and abs(effective-1.30347096)<1e-9,'historical_budget'
 assert c['new_budget_extension_sha256']==hashes()['../robustness-v1/AUTHORIZATION.json'],'new_budget_authority'
 assert c['budget_extension_sha256']==hashes()['../native-v2/AUTHORIZATION.json'],'budget_authority'
 with sqlite3.connect('file:'+c['ledger']+'?mode=ro',uri=True) as db:
  assert db.execute("select reserved,status,actual from calls where id='QM-PQ-02-001'").fetchone()==(.06,'failed_or_uncertain',None),'uncertainty_changed'
  assert db.execute("select amount,evidence from authority_extensions where id='PQ-02-owner-2026-10-04'").fetchone()==(2.,c['budget_extension_sha256']),'extension_missing'
 with sqlite3.connect('file:'+c['ledger']+'?mode=ro',uri=True) as db:
  assert db.execute("select amount,evidence from authority_extensions where id='R1-owner-2026-10-04'").fetchone()==(5.,c['new_budget_extension_sha256']),'existing_extension_required'
 registration=public_plan.check('quorum-of-mirrors',c['run_tldr']);assert registration['url']==c['plan_url'] and registration['plan_sha256']==hashes()['PLAN.md'],'public_plan'
 return {'source_sha256':hashes(),'manifest_sha256':digest(manifest),'public_plan':registration,'route':route_check(),'budget':budget_info,'checked_at':now,'host':a['host'],'claim_id':a['claim_id']}

def safe_usage(raw):
 u=raw.get('usage',{});cost=u.get('cost')
 if type(cost) not in (int,float) or not math.isfinite(cost) or cost<0:raise ValueError('usage_cost_missing')
 return {k:u[k] for k in ['prompt_tokens','completion_tokens','total_tokens','cost'] if k in u}

def main(config_path,packet_path,out_path):
 c=json.loads(Path(config_path).read_text());packet=json.loads(Path(packet_path).read_text());out=Path(out_path)
 admission=preflight(c,packet);out.mkdir(parents=True,exist_ok=False)
 save(out/'preflight.json',admission);save(out/'manifest.json',packet['manifest'])
 db=sqlite3.connect(c['ledger'],timeout=10)
 budget.initialize(db,json.loads((HERE/'HISTORY.json').read_text())['calls_sha256'],c['budget_extension_sha256'],c['new_budget_extension_sha256'])
 with db:
  db.execute('BEGIN IMMEDIATE');assert not db.execute("select 1 from next_attempts where status='running'").fetchone()
  db.execute('insert into next_attempts values (?,?,?,?)',(ATTEMPT,digest(packet['manifest']),digest(hashes()),'running'))
 sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
 report=sr.start('quorum-of-mirrors',run=ATTEMPT,params={'stage':'repair_qualification','calls':40,'plan_url':c['plan_url'],'manifest_sha256':digest(packet['manifest'])},message=c['run_tldr'])
 key=sys.stdin.readline().strip();assert len(key)>10,'credential_absent'
 records=[];reason=None
 for assignment,row in zip(packet['manifest']['assignments'],packet['rows']):
  if time.time()>=c['deadline'] or time.time()>=c['allocation']['expires_at']:reason='deadline';break
  assert hashes()==c['source_sha256'],'source_changed'
  req=request(row['actor']);rid=assignment['id'];record={'id':rid,'case_id':row['id'],'condition':row['condition'],'valid':False};started=time.time();charged=False;usage=None
  budget.reserve(db,rid,RESERVE,ATTEMPT,40,1.92,c['budget_extension_sha256'],c['new_budget_extension_sha256'])
  append(out/'requests.jsonl',{'id':rid,'case_id':row['id'],'dispatch_intent_at':started,'request':req,'sha256':digest(req)})
  try:
   with urllib.request.urlopen(urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',json.dumps(req).encode(),{'Authorization':'Bearer '+key,'Content-Type':'application/json'}),timeout=75) as response:
    raw_bytes=response.read(1000001)
   if len(raw_bytes)>1000000:raise ValueError('response_size')
   raw=json.loads(raw_bytes)
   choices=raw.get('choices',[]);content=choices[0]['message'].get('content') if len(choices)==1 else None
   record.update(model=raw.get('model'),provider=raw.get('provider'),finish_reason=choices[0].get('finish_reason') if choices else None,
                 content=content if isinstance(content,str) and len(content)<=16000 else None)
   append(out/'responses.jsonl',dict(record)) # Preserve returned text even when usage/validation fails.
   usage=safe_usage(raw);record['usage']=usage
   gid=raw.get('id','');record['generation_id']=gid if isinstance(gid,str) and re.fullmatch(r'[A-Za-z0-9_-]{1,160}',gid) else None
   append(out/'accounting.jsonl',{'id':rid,'usage':usage,'generation_id':record['generation_id'],'received_at':time.time()})
   with db:db.execute('update calls set status=?,actual=? where id=?',('failed_accounted',usage['cost'],rid))
   charged=True
   assert record['generation_id'] is not None,'generation_id'
   assert usage['cost']<=RESERVE and raw.get('model')==MODEL and raw.get('provider')=='Anthropic','route_or_cost'
   assert record['finish_reason']=='stop' and record['content'] is not None,'completion_invalid'
   answer=json.loads(content);record['parsed']=answer;record['decoded']=decode(row['actor'],answer);record['score']=score(row,answer);record['valid']=True
   with db:db.execute('update calls set status=? where id=?',('complete',rid))
  except Exception as exc:
   reason='http_'+str(exc.code) if isinstance(exc,urllib.error.HTTPError) else type(exc).__name__
   record['error_class']=reason
   safe_codes={'output_schema','output_ids','nonliteral_span','incomplete_or_unsupported_span','usage_cost_missing','response_size','completion_invalid','route_or_cost'}
   record['error_code']=str(exc) if str(exc) in safe_codes else None
   if isinstance(exc,urllib.error.HTTPError):
    try:record['http_diagnostic']=classify_http(exc)
    except Exception:record['http_diagnostic']={'category':'diagnostic_read_failed'}
   if not charged:
    with db:db.execute('update calls set status=? where id=?',('failed_or_uncertain',rid))
  if charged and usage['cost']<=RESERVE:budget.settle(db,rid,usage['cost'],'accounting-generation:'+str(record.get('generation_id')))
  record['wall_s']=time.time()-started;records.append(record);append(out/'receipts.jsonl',record)
  try:report.progress(step=len(records),total=40,force=True,valid=sum(x['valid'] for x in records))
  except Exception:append(out/'reporting-errors.jsonl',{'stage':'progress','step':len(records)})
  print('SAFE '+json.dumps({'started':len(records),'valid':sum(x['valid'] for x in records)}),flush=True)
  if reason:break
 del key
 summary=summarize(packet['rows'],records);summary.update(attempt=ATTEMPT,stop_reason=reason,execution_complete=len(records)==40 and all(r['valid'] for r in records))
 save(out/'summary.json',summary)
 with db:db.execute('update next_attempts set status=? where attempt=?',('complete' if summary['execution_complete'] else 'stopped',ATTEMPT))
 for p in list(out.iterdir()):
  if p.is_file():
   try:report.artifact(p)
   except Exception:append(out/'reporting-errors.jsonl',{'stage':'artifact','file':p.name})
 if summary['execution_complete']:report.done(message='Span repair qualification closed; see exact acceptance outcome',**summary)
 else:report.fail(message='Span qualification stopped; no automatic retry',**summary)
 print('SAFE '+json.dumps(summary),flush=True)
if __name__=='__main__':
 try:main(*sys.argv[1:])
 except Exception as e:print('SAFE '+json.dumps({'worker_error':type(e).__name__}),flush=True);sys.exit(1)

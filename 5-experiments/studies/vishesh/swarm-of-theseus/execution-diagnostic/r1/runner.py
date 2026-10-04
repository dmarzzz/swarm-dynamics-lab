"""D2 bounded qualification runner. Current operator/public/resource admission required."""
import argparse,hashlib,json,os,sqlite3,subprocess,sys,time,urllib.error,urllib.request
from pathlib import Path
from design import ROOT,assignments,digest,source_hash,check,MODEL
from admission import validate,public_check,EXPERIMENT,GateError
from analyze import summarize

ALLOCATION_LEDGER=Path('/srv/swarm/theseus-execution-allocations.sqlite')

def write_new(path,value):
 with Path(path).open('x') as f:json.dump(value,f,sort_keys=True);f.flush();os.fsync(f.fileno())
def reserve(path,cost,now):
 with sqlite3.connect(path,timeout=30) as db:
  db.execute('BEGIN IMMEDIATE');cap,used,calls,deadline=db.execute('SELECT cap,used,calls,deadline FROM budget WHERE id=1').fetchone()
  if now>=deadline:raise GateError('deadline_reached')
  if cap!=3.7 or calls>=384 or used+cost>cap:raise GateError('quota_reached')
  db.execute('UPDATE budget SET used=?,calls=? WHERE id=1',(used+cost,calls+1))
 return calls+1

def invoke(body,key,timeout=45):
 encoded=json.dumps(body).encode();headers={'Content-Type':'application/json','x-api-key':key,'anthropic-version':'2023-06-01'}
 if os.environ.get('SWARM_MODEL_WORKSPACE_ID'):headers['anthropic-workspace-id']=os.environ['SWARM_MODEL_WORKSPACE_ID']
 req=urllib.request.Request('https://api.anthropic.com/v1/messages',data=encoded,headers=headers)
 result={'value':None,'error':None,'usage':None,'actual_usd':None,'raw_text':None,'served_model':None,'response_received':False,'started_epoch':time.time()}
 try:
  with urllib.request.urlopen(req,timeout=timeout) as response:raw=response.read(1_000_001)
  if len(raw)>1_000_000:raise GateError('response_bound')
  data=json.loads(raw);result['response_received']=True;result['served_model']=data.get('model');u=data.get('usage',{});result['raw_text']=''.join(x['text'] for x in data.get('content',[]) if x.get('type')=='text')
  if all(type(u.get(k)) is int for k in ('input_tokens','output_tokens')):
   result['usage']={k:u[k] for k in ('input_tokens','output_tokens')};result['actual_usd']=(u['input_tokens']+5*u['output_tokens'])/1e6
  reason=data.get('stop_reason');result['stop_reason']=reason if reason in ('end_turn','max_tokens','refusal') else 'other'
  if reason!='end_turn':result['error']='incomplete_output'
  else:result['value']=json.loads(result['raw_text'])
  if result['served_model']!=MODEL:result['error']='served_model_mismatch'
  if result['usage'] is None:result['error']='usage_missing'
 except urllib.error.HTTPError as e:result['error']='http_'+str(e.code)
 except Exception as e:result['error']='provider_'+type(e).__name__
 result['finished_epoch']=time.time();return result

def prepare(output):
 output=Path(output);output.mkdir();design=assignments();check(design);rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 write_new(output/'assignments.json',{'status':'PREPARED, NOT RUN','assignments':design,'assignments_sha256':digest(design),'source_commit':rev,'instrument_sha256':source_hash()})
 receipt={'prior_spend_usd':0.5433070437,'total_authority_usd':5,'infrastructure_hold_usd':.1,'update_approval_sha256':hashlib.sha256((ROOT/'R1-PLAN.md').read_bytes()).hexdigest(),'status':'blocked','experiment':EXPERIMENT,'source_commit':rev,'instrument_sha256':source_hash(),'assignments_sha256':digest(design),'model':'claude-haiku-4-5-20251001','max_calls':384,'cap_usd':3.7,'max_seconds':7200,'workers':1,'retries':0,'input_rate':1,'output_rate':5,'plan_url':'https://github.com/dmarzzz/swarm-lab/blob/'+rev+'/researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/R1-PLAN.md','plan_sha256':hashlib.sha256((ROOT/'R1-PLAN.md').read_bytes()).hexdigest(),'assessment_url':None,'assessment_sha256':None,'research_review_status':'not-required-owner-direction','review_policy_ref':None,'operator':None,'authority_allocation_id':None,'owner_authorization_ref':None,'allocation_verification_ref':None,'claim_id':None,'host':None,'exclusive_claim_verified':False,'dependencies_verified':False,'public_page_verified':False,'public_page_verified_epoch':0,'verified_epoch':0,'pricing_verified_epoch':0,'claim_until_epoch':0}
 write_new(output/'admission-template.json',receipt)
 print(json.dumps({'status':'prepared_not_run','calls':len(design),'assigned_decisions':sum(len(a['cases']) for a in design),'template':'blocked'}))

def run(receipt_path,output):
 receipt=json.loads(Path(receipt_path).read_text());design=assignments();check(design);root=Path(output).resolve();repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip())
 if root==repo or repo in root.parents:raise GateError('results_must_be_outside_source_checkout')
 if root.exists():raise GateError('new_run_namespace_required')
 rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 if subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip():raise GateError('clean_source_required')
 validate(receipt,rev,design);public_receipt=public_check(receipt)
 if receipt.get('status')!='diagnostic-only':raise GateError('operator_admission_blocked')
 # No credential access, provider construction or model call precedes admission.
 key=os.environ.get('SWARM_MODEL_API_KEY')
 if not key:raise GateError('credential_missing')
 sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
 # Binding budget uniqueness to allocation in a host-wide ledger prevents a new output
 # directory from silently reusing the same allocation after a crash or stop.
 authority=ALLOCATION_LEDGER
 with sqlite3.connect(authority,timeout=30) as db:
  db.execute('CREATE TABLE IF NOT EXISTS allocations (id TEXT PRIMARY KEY, output TEXT, assigned_sha TEXT)')
  db.execute('INSERT INTO allocations VALUES (?,?,?)',(receipt['authority_allocation_id'],str(root),digest(design)))
 root.mkdir();(root/'calls').mkdir();(root/'outcomes').mkdir();deadline=time.time()+7200;ledger=root/'quota.sqlite'
 with sqlite3.connect(ledger) as db:
  db.execute('CREATE TABLE budget (id INTEGER PRIMARY KEY,cap REAL,used REAL,calls INTEGER,deadline REAL)');db.execute('INSERT INTO budget VALUES (1,3.7,0,0,?)',(deadline,))
 write_new(root/'manifest.json',{'evidence_type':'measured_model_outputs','assignments':design,'source_commit':rev,'instrument_sha256':source_hash(),'admission':receipt,'public_preflight':public_receipt})
 def report(kind,a,**kwargs):
  if not sr.report(kind,EXPERIMENT,a['id'],source='vishesh/codex-theseus',strict=True,**kwargs):raise GateError('report_not_acknowledged')
 stop=None;reported=set();terminal_reported=set();reporting_failures=[]
 try:
  for a in design:
   encoded=json.dumps(a['request']).encode()
   if len(encoded)>2500:raise GateError('input_bound_exceeded')
   if time.time()>=min(deadline,receipt['claim_until_epoch']):raise GateError('deadline_or_claim_expired')
   report('plan',a,message=a['tldr'],url=receipt['plan_url'],params={'arm':a['arm'],'seed':a['seed'],'context':a['context'],'tldr':a['tldr']})
   reported.add(a['id']);report('start',a,message=a['tldr']);reserved=(len(encoded)+512+1200*5)/1e6;call=reserve(ledger,reserved,time.time())
   write_new(root/'calls'/(a['id']+'-started.json'),{'call':call,'request':a['request'],'request_sha256':digest(a['request']),'reserved_usd':reserved,'started_epoch':time.time()})
   result=invoke(a['request'],key,timeout=max(.1,min(45,deadline-time.time(),receipt['claim_until_epoch']-time.time())));write_new(root/'calls'/(a['id']+'-finished.json'),result)
   from design import d1
   score=d1.score
   measured=score(dict(a,arm='E'),result);write_new(root/'outcomes'/(a['id']+'.json'),{'status':'provider_failed' if result['error'] else 'complete','scoring':measured})
   report('progress',a,message=a['tldr'],metrics={'accuracy':sum(r['correct'] for r in measured['rows'])/len(a['cases']),'completed_calls':call})
   report('fail' if result['error'] else 'done',a,message=a['tldr']);terminal_reported.add(a['id'])
   if result['error']:raise GateError('provider_or_accounting_stop')
 except Exception as e:
  stop=type(e).__name__ # Never log arbitrary exception/provider/credential text.
 finally:
  for a in design:
   f=root/'outcomes'/(a['id']+'.json')
   if not f.exists():write_new(f,{'status':'not_completed','safe_reason':'dispatch_stopped','assigned_cases':len(a['cases'])})
  for a in design:
   if a['id'] in reported-terminal_reported:
    try:report('fail',a,message=a['tldr']+' Execution/reporting interrupted; inspect durable records, no model retry.')
    except Exception:reporting_failures.append(a['id'])
  render_error=None
  try:summary=summarize(root)
  except Exception as e:
   render_error=type(e).__name__;summary={'terminal_calls':len(list((root/'calls').glob('*-finished.json'))),'audit_disagreements':['analysis_failed']}
  write_new(root/'terminal.json',{'status':'stopped' if stop else 'complete','safe_error_class':stop,'model_calls_retried':0,'terminal_reporting_pending':reporting_failures,'render_error_class':render_error})
 print(json.dumps({'status':'stopped' if stop else 'complete','completed_call_records':summary['terminal_calls'],'audit_disagreements':len(summary['audit_disagreements'])}))
if __name__=='__main__':
 p=argparse.ArgumentParser();sub=p.add_subparsers(dest='mode',required=True);a=sub.add_parser('prepare');a.add_argument('output');b=sub.add_parser('run');b.add_argument('--admission',required=True);b.add_argument('--output',required=True);args=p.parse_args()
 try:prepare(args.output) if args.mode=='prepare' else run(args.admission,args.output)
 except Exception as e:print(json.dumps({'status':'blocked','safe_error_class':type(e).__name__,'safe_reason':str(e) if isinstance(e,GateError) else 'inspect_nonsecret_operator_state'}));sys.exit(1)

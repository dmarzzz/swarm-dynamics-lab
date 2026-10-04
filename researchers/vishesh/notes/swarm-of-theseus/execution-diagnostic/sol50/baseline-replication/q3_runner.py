"""Native Q3 worker: funded admission only, bounded loopback relay, durable private traces."""
import argparse,hashlib,json,os,socket,sqlite3,subprocess,time,urllib.request
from pathlib import Path
import admission as a,contract as c,engine

def write_new(path,value):
 with Path(path).open('x') as stream:json.dump(value,stream,sort_keys=True);stream.flush();os.fsync(stream.fileno())
def append(path,value):
 with Path(path).open('a') as stream:stream.write(json.dumps(value,sort_keys=True)+'\n');stream.flush();os.fsync(stream.fileno())
def parse(result):
 r=result.get('response',{})
 if r.get('model') not in ('openai/gpt-6-sol','gpt-6-sol') or r.get('provider')!='OpenAI':raise ValueError('served_route')
 choices=r.get('choices')
 if not isinstance(choices,list) or len(choices)!=1 or choices[0].get('finish_reason')!='stop':raise ValueError('response_incomplete')
 value=json.loads(choices[0]['message']['content'])
 if not isinstance(value,dict):raise ValueError('response_shape')
 return value

def verify_original_ledger(path,expected_sha,local=False):
 p=Path(path)
 if not p.is_file() or p.is_symlink() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected_sha:raise ValueError('original_ledger_hash')
 table='calls' if local else 'sol50_calls'
 with sqlite3.connect(p) as db:
  count,actual,unknown=db.execute(f'SELECT count(*),sum(actual_usd),sum(case when actual_usd is null then reserved_usd else 0 end) FROM {table}').fetchone()
  if count!=44 or abs(actual-.122835)>1e-10 or unknown!=0:raise ValueError('historical_ledger_reconciliation')
 return True

class Calls:
 def __init__(self,root,receipt,grant,ledger,reporter):
  self.root=Path(root);self.receipt=receipt;self.grant=grant;self.ledger=c.StageLedger(ledger,'Q3');self.count=0;self.reporter=reporter;self.condition=None;self.condition_start=0
  self.deadline=min(time.time()+7200,receipt['claim_until_epoch'],grant['expires_epoch']);self.capability=os.environ['THESEUS_R3_CAPABILITY']
 def condition_change(self,family,condition):
  name=family+'-'+condition
  if name==self.condition:return
  self.finish_condition();self.condition=name;self.condition_start=self.count
  text='TLDR: Q3 qualification '+name+' tests inferred local policy, addressed raw evidence, direct handover and selective revision. Exact history-controller/scorer reference; measure all-correct notes/routes/actions and zero harm. One six-member world per family; no replication or cultural-survival claim.'
  for kind in ('plan','start'):
   if not self.reporter.report(kind,a.EXPERIMENT,a.ATTEMPT+'-'+name,message=text,url=self.receipt['plan_url'],strict=True):raise ValueError('reporting_admission')
 def finish_condition(self,failed=False):
  if self.condition:
   if not self.reporter.report('fail' if failed else 'done',a.EXPERIMENT,a.ATTEMPT+'-'+self.condition,message='Execution segment closed; scientific assessment recorded separately.',metrics={'completed_calls':self.count-self.condition_start},strict=True):raise ValueError('reporting_close')
   self.condition=None
 def __call__(self,family,phase,packet,condition):
  self.condition_change(family,condition)
  if time.time()>=self.deadline or self.count>=108:raise ValueError('deadline_or_calls')
  body=c.wire(phase,family,packet);ident=a.ATTEMPT+'-'+str(self.count).zfill(4);self.ledger.reserve(ident,body);self.count+=1
  write_new(self.root/(ident+'-request.json'),{'family':family,'phase':phase,'condition':condition,'request':body,'request_sha256':a.digest(body),'reserved_usd':str(c.PER_CALL),'started_epoch':time.time()})
  payload={'id':ident,'attempt':a.ATTEMPT,'family':family,'phase':phase,'packet':packet,'request':body,'source_sha256':self.receipt['source_sha256'],'frozen_packet_sha256':self.receipt['packet_sha256']}
  req=urllib.request.Request('http://127.0.0.1:18566/q3',json.dumps(payload).encode(),{'Authorization':'Bearer '+self.capability,'Content-Type':'application/json'})
  try:
   with urllib.request.urlopen(req,timeout=min(180,max(1,self.deadline-time.time()))) as response:result=json.load(response)
  except Exception as error:
   result={'error':type(error).__name__,'actual_usd':None};write_new(self.root/(ident+'-response.json'),result);self.ledger.settle(ident,None);raise ValueError('ambiguous_transport') from None
  write_new(self.root/(ident+'-response.json'),result);cost=result.get('actual_usd')
  if type(cost) not in (int,float) or cost<0 or cost>float(c.PER_CALL):self.ledger.settle(ident,None);raise ValueError('unknown_or_excess_cost')
  self.ledger.settle(ident,cost)
  if result.get('error'):raise ValueError('provider_error')
  return parse(result)

def run(receipt_path,grant_path,packet_path,ledger,output):
 receipt=json.loads(Path(receipt_path).read_text());grant=json.loads(Path(grant_path).read_text());packet=json.loads(Path(packet_path).read_text())
 revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.ROOT,text=True).strip();a.validate(receipt,grant,packet,revision)
 if socket.gethostname().split('.')[0]!=receipt['host']:raise ValueError('host')
 if subprocess.check_output(['git','status','--porcelain'],cwd=a.ROOT,text=True).strip():raise ValueError('dirty_source')
 root=Path(output)
 if root.exists():raise ValueError('attempt_exists_no_resume')
 verify_original_ledger(ledger,receipt['historical_ledger_sha256']);pub=a.public_check(receipt)
 import sys;sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report
 root.mkdir(parents=True);write_new(root/'manifest.json',{'admission':receipt,'grant_sha256':a.digest(grant),'packet':packet,'public_preflight':pub})
 caller=Calls(root,receipt,grant,ledger,swarm_report);error=None;result=None
 try:
  result=engine.qualify(packet,caller,lambda value:append(root/'events.jsonl',value));write_new(root/'results.json',result)
 except Exception as e:error=type(e).__name__+':'+str(e) if isinstance(e,ValueError) else type(e).__name__
 finally:
  try:caller.finish_condition(failed=bool(error) or result is not None and not result['passed'])
  except Exception:error=error or 'reporting_close'
  write_new(root/'terminal.json',{'status':'stopped' if error else 'complete','error':error,'started_calls':caller.count,'passed':None if result is None else result['passed'],'retries':0,'automatic_successor':False,'scientific_review':'required','cost_exposure_usd':str(caller.ledger.exposure())});caller.ledger.db.close()
 return {'status':'stopped' if error else 'complete','started_calls':caller.count,'passed':None if result is None else result['passed']}
if __name__=='__main__':
 parser=argparse.ArgumentParser()
 for key in ('receipt','grant','packet','ledger','output'):parser.add_argument('--'+key,required=True)
 args=parser.parse_args()
 try:print(json.dumps(run(args.receipt,args.grant,args.packet,args.ledger,args.output)))
 except Exception as error:print(json.dumps({'status':'blocked','error_class':type(error).__name__}));raise SystemExit(1)

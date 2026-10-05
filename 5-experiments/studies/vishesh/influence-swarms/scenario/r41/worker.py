"""Admitted R41 worker. Original ledger, verified runtime, no credential lookup."""
import argparse,datetime as dt,hashlib,json,os,socket,subprocess,sys,urllib.request
from pathlib import Path
import cases as c,instrument as i,runtime as r,analysis as analysis
H=Path(__file__).resolve().parent;ROOT=H.parents[5];LEDGER=Path('/srv/swarm/influence-d5-private/budget.sqlite')
def read(path):return json.loads(Path(path).read_text())
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def main():
 os.umask(0o077);parser=argparse.ArgumentParser();parser.add_argument('--admission',required=True);parser.add_argument('--out',required=True);parser.add_argument('--execute',action='store_true');args=parser.parse_args();a=read(args.admission)
 r.require(a['stage']in('R41-D1','R41-Q0','R41-E0') and a['authority'].startswith('PI-FUND-') and 0<a['maximum_model_usd']<=r.MAXIMUM_MODEL,'named_finite_scope')
 r.require(a['manifest_sha256']==sha(H/'manifest.json'),'manifest');manifest=read(H/'manifest.json')
 for name,digest in manifest['source_hashes'].items():r.require(sha(ROOT/name)==digest,'runtime_hash')
 r.require(a['source']==subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip() and not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip(),'source')
 r.require(socket.gethostname()==a['host'] and all(a[k]is True for k in ('approved_account_match','exclusive_claim_current','route_available','workload_idle','offline_tests_passed')),'admission')
 r.require(0<=(dt.datetime.now(dt.timezone.utc)-r.utc(a['checked_utc'])).total_seconds()<300 and dt.datetime.now(dt.timezone.utc)+dt.timedelta(minutes=5)<r.utc(a['until']),'deadline')
 rows=subprocess.check_output(['ps','-eo','pid=,comm='],text=True).splitlines();r.require(not[x for x in rows if len(x.split())==2 and x.split()[1].startswith(('python','node','uvicorn','gunicorn')) and int(x.split()[0])!=os.getpid()],'worker_idle');r.require(not subprocess.check_output(['docker','ps','-q'],text=True).strip(),'containers_idle')
 with r.database(LEDGER)as db:
  budget=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone();scope=db.execute('SELECT source,manifest,maximum_model,model_debited,max_calls,calls,status FROM r41_scope WHERE grant_id=?',(r.GRANT,)).fetchone()
 r.require(budget[0]==50 and abs(budget[1]-a['budget'][1])<1e-8 and budget[2]==a['budget'][2] and scope and scope[0]==a['source'] and scope[1]==a['manifest_sha256'] and scope[2]==a['maximum_model_usd'] and scope[4]==a['allocated_calls'] and 0<scope[4]<=r.MAX_CALLS and scope[6]=='funded','ledger')
 plan='https://github.com/dmarzzz/swarm-lab/blob/'+a['source']+'/'+str((H/'PLAN.md').relative_to(ROOT));r.require(a['public_plan']==plan,'plan_url')
 with urllib.request.urlopen(plan.replace('github.com/dmarzzz/swarm-lab/blob/','raw.githubusercontent.com/dmarzzz/swarm-lab/'),timeout=25)as response:r.require(response.read()==(H/'PLAN.md').read_bytes(),'public_plan_bytes')
 for heading in ('## TLDR','## Question and prediction','## Setup','## Protocol','## Metrics'):r.require(heading in (H/'PLAN.md').read_text(),'plan_sections')
 r.require(not Path(args.out).exists(),'prior_attempt');cases=read(H/'dossiers.json');q=None
 if a['stage']in('R41-Q0','R41-E0'):
  records=[];run_ids=[]
  for prior,count in ([('R41-D1',84)] if a['stage']=='R41-Q0' else [('R41-D1',84),('R41-Q0',672)]):
   qdir=Path('/srv/swarm/influence-readiness-private')/('native-'+prior+'-01');part=read(qdir/'records.json');summary=read(qdir/'summary.json');receipt=read(qdir/'run-receipt.json')
   r.require(summary['complete'] and summary['calls']==summary['valid_calls']==count and summary['usage_missing']==0 and i.partial_qualification(cases,part,prior)['qualified'],'native_qualification')
   r.require(receipt['source']==a['source'] and receipt['manifest_sha256']==a['manifest_sha256'] and receipt['records_sha256']==c.digest(part),'qualification_source')
   records.extend(part);run_ids.append(receipt['run'])
  r.require(c.digest(records)==a['q_records_sha256'],'qualification_records')
  if a['stage']=='R41-E0':r.require(i.qualification(cases,records)['qualified'],'full_qualification')
  q={'source':a['source'],'manifest':a['manifest_sha256'],'native_run':run_ids,'records':records}
 if not args.execute:print(json.dumps({'admitted':True,'calls':0,'stage':a['stage']}));return
 sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
 params={'stage':a['stage'],'version':a['source'],'plan':plan,'manifest_sha256':a['manifest_sha256'],'conditions':a['condition_tldrs'],'decision_rosters':'40 vs4 vs1; two shared check calls outside rosters','local_format_failure':'block_descendants_without_retry','operational_failure':'global_stop_and_drain'}
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
 def transport(raw,root_id,node_id):
  request=urllib.request.Request('http://127.0.0.1:19701/',data=raw,headers={'Content-Type':'application/json','X-Swarm-Root':root_id,'X-Swarm-Node':node_id})
  with opener.open(request,timeout=75)as response:return response.read(1000001)
 with sr.start('influence-swarms',params=params)as hub:
  public=subprocess.check_output(['curl','--proto','=https','--fail','--silent','--max-time','25','--user-agent','SwarmLab-PublicVerification/1.0','https://swarm-live.pages.dev/api/runs/'+hub.id]);r.require(json.loads(public)['params']==params,'public_registration')
  session=r.Session(cases,args.out,LEDGER,a['attempt'],a['stage'],a['source'],a['manifest_sha256'],{'reserved':budget[1],'calls':budget[2]},a['until'],qualification_receipt=q);records,summary=session.run(transport,progress=lambda n,total:hub.progress(n,total,started=n))
  assessment=i.partial_qualification(cases,records,a['stage']) if a['stage']!='R41-E0' else analysis.analyze(cases,records);r.save(Path(args.out)/'assessment.json',assessment)
  r.save(Path(args.out)/'run-receipt.json',{'run':hub.id,'source':a['source'],'public_plan':plan,'manifest_sha256':a['manifest_sha256'],'records_sha256':c.digest(records)})
  # Public projection contains categorical outcomes, numerical scores and provenance only.
  for name in ('summary.json','assessment.json','events.jsonl','run-receipt.json'):hub.artifact(Path(args.out)/name,name)
  (hub.done if summary['complete']else hub.fail)(message='R41 acquisition closed; terminal status is separate from qualification and scientific interpretation',valid=summary['valid_calls'],failed=summary['known_format_failures'],unstarted=summary['unstarted_calls'])
  print(json.dumps({'run':hub.id,'stage':a['stage'],'calls':summary['calls'],'valid':summary['valid_calls'],'complete':summary['complete'],'qualified':assessment.get('qualified'),'usage_missing':summary['usage_missing']}))
if __name__=='__main__':
 try:main()
 except Exception as e:print(json.dumps({'stopped':True,'type':type(e).__name__}));raise SystemExit(1)

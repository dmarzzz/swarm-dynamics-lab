"""Prospectively admitted E1 worker. No credential lookup, retry or implicit funding."""
import argparse,datetime as dt,json,os,socket,subprocess,sys,urllib.request
from pathlib import Path
import acquisition as p
c,i,r=p.c,p.i,p.r
H=Path(__file__).resolve().parent;ROOT=c.ROOT;LEDGER=Path('/srv/swarm/influence-d5-private/budget.sqlite')
def read(path):return json.loads(Path(path).read_text())
def main():
 os.umask(0o077);parser=argparse.ArgumentParser();parser.add_argument('--admission',required=True);parser.add_argument('--out',required=True);parser.add_argument('--execute',action='store_true');args=parser.parse_args();a=read(args.admission)
 r.require(a['stage'] in ('E1-Q0','E1-E0') and a['authority'].startswith('PI-FUND-') and a['maximum_model_usd']==9.728,'named_scope')
 r.require(a['manifest_sha256']==r.sha((H/'manifest.json').read_bytes()),'manifest');manifest=read(H/'manifest.json')
 for name,hash in manifest['source_hashes'].items():r.require(r.sha((ROOT/name).read_bytes())==hash,'runtime_hash')
 r.require(a['source']==subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip() and not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip(),'source')
 r.require(socket.gethostname()==a['host'] and all(a[k] is True for k in ('approved_account_match','exclusive_claim_current','route_available','workload_idle','offline_tests_passed')),'admission')
 r.require(0<=(dt.datetime.now(dt.timezone.utc)-r.utc(a['checked_utc'])).total_seconds()<300 and dt.datetime.now(dt.timezone.utc)+dt.timedelta(minutes=5)<r.utc(a['until']),'admission_deadline')
 rows=subprocess.check_output(['ps','-eo','pid=,comm='],text=True).splitlines();r.require(not [x for x in rows if len(x.split())==2 and x.split()[1].startswith(('python','node','uvicorn','gunicorn')) and int(x.split()[0])!=os.getpid()],'worker_idle');r.require(not subprocess.check_output(['docker','ps','-q'],text=True).strip(),'containers_idle')
 with r.database(LEDGER) as db:
  budget=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone();scope=db.execute('SELECT maximum_model,model_debited,status FROM e1_scope WHERE grant_id=?',(p.GRANT,)).fetchone()
 r.require(budget[0]==50 and abs(budget[1]-a['budget'][1])<1e-8 and budget[2]==a['budget'][2] and scope and scope[0]==9.728 and scope[2]=='funded','ledger')
 plan='https://github.com/dmarzzz/swarm-lab/blob/'+a['source']+'/'+str((H/'PLAN.md').relative_to(ROOT));r.require(a['public_plan']==plan,'plan_url')
 with urllib.request.urlopen(plan.replace('github.com/dmarzzz/swarm-lab/blob/','raw.githubusercontent.com/dmarzzz/swarm-lab/'),timeout=25) as response:r.require(response.read()==(H/'PLAN.md').read_bytes(),'public_plan_bytes')
 r.require(not Path(args.out).exists(),'prior_attempt')
 cases=read(H.parent/'b2/dossiers.json');q=None
 if a['stage']=='E1-E0':
  qdir=Path('/srv/swarm/influence-readiness-private/native-E1-Q0-01');q=read(qdir/'records.json');summary=read(qdir/'summary.json');receipt=read(qdir/'run-receipt.json')
  r.require(summary['complete'] and summary['calls']==summary['valid_calls']==80 and summary['usage_missing']==0 and p.qualification(cases,q)['qualified'],'native_q0_gate')
  r.require(receipt['source']==a['source'] and receipt['manifest_sha256']==a['manifest_sha256'] and receipt['records_sha256']==c.digest(q)==a['q_records_sha256'],'native_q0_source')
 if not args.execute:print(json.dumps({'admitted':True,'calls':0,'stage':a['stage']}));return
 sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
 params={'stage':a['stage'],'version':a['source'],'plan':plan,'manifest_sha256':a['manifest_sha256'],'conditions':a['condition_tldrs'],'local_format_failure':'stop_cell_without_retry','operational_failure':'global_stop_and_drain'}
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
 def transport(raw,assignment,step):
  request=urllib.request.Request('http://127.0.0.1:19701/',data=raw,headers={'Content-Type':'application/json','X-Swarm-Assignment':assignment,'X-Swarm-Step':str(step)})
  with opener.open(request,timeout=75) as response:return response.read(1000001)
 with sr.start('influence-swarms',params=params) as hub:
  public=subprocess.check_output(['curl','--proto','=https','--fail','--silent','--max-time','25','--user-agent','SwarmLab-PublicVerification/1.0','https://swarm-live.pages.dev/api/runs/'+hub.id]);r.require(read_json(public)['params']==params,'public_registration')
  summary=p.collect(cases,args.out,LEDGER,a['attempt'],transport,a['until'],{'reserved':budget[1],'calls':budget[2]},q,lambda n,total:hub.progress(n,total,valid=n),stage=a['stage'])
  r.save(Path(args.out)/'run-receipt.json',{'run':hub.id,'source':a['source'],'public_plan':plan,'manifest_sha256':a['manifest_sha256'],'records_sha256':c.digest(read(Path(args.out)/'records.json'))})
  # Native prose stays private; only numerical summaries/provenance are published.
  for name in ('summary.json','assessment.json','events.jsonl','run-receipt.json','execution-amendment.json'):hub.artifact(Path(args.out)/name,name)
  (hub.done if summary['complete'] else hub.fail)(message='E1 acquisition closed; complete does not imply all cells observed or scientific success',valid=summary['valid_calls'],failed=summary['format_failed_cells'],unstarted=summary['unstarted_calls'])
  print(json.dumps({'run':hub.id,'calls':summary['calls'],'valid':summary['valid_calls'],'complete':summary['complete'],'all_cells_observed':summary['all_cells_observed'],'usage_missing':summary['usage_missing']}))
def read_json(raw):return json.loads(raw)
if __name__=='__main__':
 try:main()
 except Exception as exc:print(json.dumps({'stopped':True,'type':type(exc).__name__}));raise SystemExit(1)

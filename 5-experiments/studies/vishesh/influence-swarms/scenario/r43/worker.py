"""Source-bound main acquisition with explicit recovery-assisted admission."""
import argparse,datetime as dt,hashlib,json,os,socket,subprocess,sys,urllib.request
from pathlib import Path
import engine as e
H=Path(__file__).resolve().parent;ROOT=H.parents[5];BASE=Path('/srv/swarm/influence-readiness-private');LEDGER=Path('/srv/swarm/influence-d5-private/budget.sqlite')
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 os.umask(0o077);p=argparse.ArgumentParser();p.add_argument('--admission',required=True);p.add_argument('--execute',action='store_true');args=p.parse_args();a=read(args.admission)
 e.r.require(a['attempt']=='native-R43-E0-01' and a['authority'].startswith('PI-FUND-') and a['maximum_model']==e.MAX_COST and a['maximum_calls']==e.MAX_CALLS,'finite_authority');e.r.require(a['manifest']==sha(H/'manifest.json'),'manifest');m=read(H/'manifest.json')
 for name,digest in m['source_hashes'].items():e.r.require(sha(ROOT/name)==digest,'runtime_hash')
 for name,digest in m['private_evidence_hashes'].items():e.r.require(sha(BASE/name)==digest,'immutable_evidence')
 e.r.require(subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==a['source'] and not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip(),'source')
 e.r.require(socket.gethostname()==a['host'] and all(a[k]is True for k in ('approved_account_match','exclusive_claim_current','route_available','workload_idle','offline_tests_passed')),'admission');e.r.require(0<=(dt.datetime.now(dt.timezone.utc)-e.r.utc(a['checked_utc'])).total_seconds()<300 and dt.datetime.now(dt.timezone.utc)+dt.timedelta(minutes=5)<e.r.utc(a['until']),'current_admission')
 rows=subprocess.check_output(['ps','-eo','pid=,comm='],text=True).splitlines();e.r.require(not[z for z in rows if len(z.split())==2 and z.split()[1].startswith(('python','node','uvicorn','gunicorn')) and int(z.split()[0])!=os.getpid()],'idle');e.r.require(not subprocess.check_output(['docker','ps','-q'],text=True).strip(),'containers_idle')
 plan='https://github.com/dmarzzz/swarm-dynamics-lab/blob/'+a['source']+'/'+str((H/'PLAN.md').relative_to(ROOT));e.r.require(a['public_plan']==plan,'plan_url')
 with urllib.request.urlopen(plan.replace('github.com/dmarzzz/swarm-dynamics-lab/blob/','raw.githubusercontent.com/dmarzzz/swarm-dynamics-lab/'),timeout=25)as f:e.r.require(f.read()==(H/'PLAN.md').read_bytes(),'public_plan')
 with e.r.database(LEDGER)as db:
  budget=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone();grant=db.execute('SELECT source,manifest,calls,reserved,retries,status FROM r43_scope WHERE attempt=?',(a['attempt'],)).fetchone()
 e.r.require(abs(budget[1]-a['budget'][1])<1e-8 and budget[2]==a['budget'][2],'original_budget');e.r.require(grant==(a['source'],a['manifest'],0,0,0,'funded'),'fresh_grant')
 out=BASE/a['attempt'];e.r.require(not out.exists(),'prior_attempt');q=read(BASE/'native-R42-C0-01/composite-records.json');qs=read(BASE/'native-R42-C0-01/summary.json');e.r.require(qs['complete'] and qs['valid_new']==6 and qs['unknown_usage']==0 and e.i.qualification(e.c.corpus(),q)['qualified'],'native_recovery_assisted_qualification')
 if not args.execute:print(json.dumps({'admitted':True,'new_calls':0,'qualification':'recovery-assisted'}));return
 sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
 params={'stage':'R43-E0','version':a['source'],'plan':plan,'manifest':a['manifest'],'conditions':a['tldrs'],'logical_calls':2988,'retry_pool':30,'qualification':'recovery-assisted27/27; original first-pass failed','schedule':'fixed waves; retries then round-robin ready nodes; no latency priority'}
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
 def transport(raw,root,node):
  request=urllib.request.Request('http://127.0.0.1:19701/',data=raw,headers={'Content-Type':'application/json','X-Swarm-Root':root,'X-Swarm-Node':node})
  with opener.open(request,timeout=75)as f:return f.read(1000001)
 with sr.start('influence-swarms',params=params)as hub:
  public=subprocess.check_output(['curl','--proto','=https','--fail','--silent','--max-time','25','--user-agent','SwarmLab-PublicVerification/1.0','https://swarm-live.pages.dev/api/runs/'+hub.id]);e.r.require(json.loads(public)['params']==params,'public_registration')
  session=e.Session(e.c.corpus(),out,LEDGER,a['attempt'],a['source'],a['manifest'],a['until'],(budget[1],budget[2]),q);records,first,summary=session.run(transport,progress=lambda n,total:hub.progress(n,total,physical_calls=n))
  for name,data in(('assessment.json',e.analysis.analyze(e.c.corpus(),records)),('first-pass-assessment.json',e.analysis.analyze(e.c.corpus(),first))):e.r.save(out/name,data)
  e.r.save(out/'run-receipt.json',{'run':hub.id,'source':a['source'],'manifest':a['manifest'],'public_plan':plan,'records_sha256':e.c.digest(records),'first_pass_sha256':e.c.digest(first)})
  for name in('summary.json','assessment.json','first-pass-assessment.json','run-receipt.json','events.json'):hub.artifact(out/name,name)
  (hub.done if not summary['global_failure']else hub.fail)(message='Main acquisition closed; scientific review pending',valid=summary['logical_valid'],failed=summary['known_length_failures'],physical=summary['physical_calls'])
  print(json.dumps({'run':hub.id,**summary}))
if __name__=='__main__':
 try:main()
 except Exception as err:print(json.dumps({'stopped':True,'error_type':type(err).__name__}));raise SystemExit(1)

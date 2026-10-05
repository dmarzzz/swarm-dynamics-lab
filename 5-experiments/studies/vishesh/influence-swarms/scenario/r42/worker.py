"""Original-ledger, source-bound six-call recovery; no credentials on worker."""
import argparse,datetime as dt,hashlib,json,os,socket,subprocess,sys,urllib.request
from pathlib import Path
import recovery as x
H=Path(__file__).resolve().parent;ROOT=H.parents[5];BASE=Path('/srv/swarm/influence-readiness-private');LEDGER=Path('/srv/swarm/influence-d5-private/budget.sqlite')
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def root():
 p=BASE/'native-R41-Q0-01'
 return x.restore(x.c.corpus(),read(p/'records.json'),(p/'0123-request.bin').read_bytes(),(p/'0123-response.bin').read_bytes())
def main():
 os.umask(0o077);p=argparse.ArgumentParser();p.add_argument('--admission',required=True);p.add_argument('--execute',action='store_true');args=p.parse_args();a=read(args.admission)
 x.r.require(a['attempt']=='native-R42-C0-01' and a['authority'].startswith('PI-FUND-') and a['maximum_model']==x.MAX_COST and a['maximum_calls']==6,'finite_authority')
 x.r.require(a['manifest']==sha(H/'manifest.json'),'manifest');m=read(H/'manifest.json')
 for name,digest in m['source_hashes'].items():x.r.require(sha(ROOT/name)==digest,'runtime_hash')
 for name,digest in m['private_evidence_hashes'].items():x.r.require(sha(BASE/name)==digest,'immutable_evidence')
 x.r.require(subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==a['source'] and not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip(),'source')
 x.r.require(socket.gethostname()==a['host'] and all(a[k]is True for k in ('approved_account_match','exclusive_claim_current','route_available','workload_idle','offline_tests_passed')),'admission')
 x.r.require(0<=(dt.datetime.now(dt.timezone.utc)-x.r.utc(a['checked_utc'])).total_seconds()<300 and dt.datetime.now(dt.timezone.utc)+dt.timedelta(minutes=5)<x.r.utc(a['until']),'current_admission')
 rows=subprocess.check_output(['ps','-eo','pid=,comm='],text=True).splitlines();x.r.require(not[z for z in rows if len(z.split())==2 and z.split()[1].startswith(('python','node','uvicorn','gunicorn')) and int(z.split()[0])!=os.getpid()],'idle');x.r.require(not subprocess.check_output(['docker','ps','-q'],text=True).strip(),'containers_idle')
 plan='https://github.com/dmarzzz/swarm-dynamics-lab/blob/'+a['source']+'/'+str((H/'PLAN.md').relative_to(ROOT));x.r.require(a['public_plan']==plan,'plan_url')
 with urllib.request.urlopen(plan.replace('github.com/dmarzzz/swarm-dynamics-lab/blob/','raw.githubusercontent.com/dmarzzz/swarm-dynamics-lab/'),timeout=25)as f:x.r.require(f.read()==(H/'PLAN.md').read_bytes(),'public_plan')
 with x.r.database(LEDGER)as db:
  budget=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone();grant=db.execute('SELECT source,manifest,max_calls,maximum,used_calls,reserved,status FROM r42_scope WHERE attempt=?',(a['attempt'],)).fetchone()
 x.r.require(abs(budget[1]-a['budget'][1])<1e-8 and budget[2]==a['budget'][2],'original_budget');x.r.require(grant==(a['source'],a['manifest'],6,x.MAX_COST,0,0,'funded'),'fresh_grant')
 out=BASE/a['attempt'];x.r.require(not out.exists(),'prior_attempt');rt=root()
 if not args.execute:print(json.dumps({'admitted':True,'new_calls':0}));return
 sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
 params={'stage':'R42-C0','version':a['source'],'plan':plan,'manifest':a['manifest'],'condition_tldr':a['tldr'],'new_calls_max':6,'first_pass_qualification':'failed','recovery_policy':'one identical-request retry plus five previously blocked descendants; no other retry'}
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
 def transport(raw,node):
  request=urllib.request.Request('http://127.0.0.1:19701/',data=raw,headers={'Content-Type':'application/json','X-Swarm-Node':node})
  with opener.open(request,timeout=75)as f:return f.read(1000001)
 with sr.start('influence-swarms',params=params)as hub:
  public=subprocess.check_output(['curl','--proto','=https','--fail','--silent','--max-time','25','--user-agent','SwarmLab-PublicVerification/1.0','https://swarm-live.pages.dev/api/runs/'+hub.id]);x.r.require(json.loads(public)['params']==params,'public_registration')
  run=x.Continuation(rt,out,LEDGER,a['attempt'],a['source'],a['manifest'],a['until']);record,summary=run.run(transport)
  d1=read(BASE/'native-R41-D1-01/records.json');q=read(BASE/'native-R41-Q0-01/records.json');composite=d1+[record if z['case_id']==x.CASE else z for z in q]
  assessment=x.i.qualification(x.c.corpus(),composite);assessment.update(original_first_pass_qualification='failed',recovery_assisted=True,new_calls=summary['started'],fresh_independent_roots=0)
  x.r.save(out/'assessment.json',assessment);x.r.save(out/'composite-records.json',composite);x.r.save(out/'run-receipt.json',{'run':hub.id,'source':a['source'],'manifest':a['manifest'],'public_plan':plan,'composite_sha256':x.c.digest(composite)})
  for name in('summary.json','assessment.json','run-receipt.json'):hub.artifact(out/name,name)
  (hub.done if summary['complete']else hub.fail)(message='Bounded recovery closed; original first-pass qualification remains failed',valid=summary['valid_new'],failed=int(bool(summary['failure'])),unstarted=6-summary['started'])
  print(json.dumps({'run':hub.id,**summary,'recovery_assisted_competence':assessment['qualified']}))
if __name__=='__main__':
 try:main()
 except Exception as e:print(json.dumps({'stopped':True,'error_type':type(e).__name__}));raise SystemExit(1)

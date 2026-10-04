"""Operator entry point. Defaults to admission check only; no credential lookup.
Funding/observed receipts are private, freshly verified operator evidence, not templates.
"""
import argparse,datetime as dt,hashlib,json,os,resource,socket,subprocess,sys,tarfile,urllib.request
from pathlib import Path
import cases as c,instrument as i,runtime as r
H=Path(__file__).resolve().parent;ROOT=c.ROOT
LEDGER=Path('/srv/swarm/influence-d5-private/budget.sqlite')
PLAN=H.parent/'scale-up/B1-SCIENTIFIC-BASELINE-PLAN.md'
PUBLIC_USER_AGENT='SwarmLab-PublicVerification/1.0'
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):raise r.Stop('redirect_refused')
def read(path):return json.loads(Path(path).read_text())
def get(url):
 if url.startswith('https://swarm-live.pages.dev/api/'):
  # The public edge rejects Python-urllib's default UA. Identify this client
  # explicitly; keep HTTP failures fatal and do not add retries or redirects.
  return subprocess.check_output(['curl','--proto','=https','--fail','--silent','--show-error','--max-time','25','--user-agent',PUBLIC_USER_AGENT,url])
 opener=urllib.request.build_opener(NoRedirect())
 with opener.open(url,timeout=25) as response:return response.read(2000000)
def preflight(a,funding,observed,out,d0_path=None):
 p,cases=r.load_contract();manifest=read(H/'runtime-manifest.json')
 for name,h in manifest['files'].items():r.require(r.sha((H/name).read_bytes())==h,'runtime_file_hash')
 r.require(c.digest(manifest)==a['runtime_manifest_sha256'],'runtime_manifest')
 observed=dict(observed);observed.update(host=socket.gethostname(),source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),clean_runtime=not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip(),runtime_manifest_sha256=c.digest(manifest))
 stat=LEDGER.stat();observed['ledger_identity_sha256']=c.digest({'path':str(LEDGER),'device':stat.st_dev,'inode':stat.st_ino})
 with r.database(LEDGER) as db:observed['budget']=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone()
 processes=subprocess.check_output(['ps','-eo','pid=,comm='],text=True).splitlines()
 active=[x for x in processes if len(x.split())==2 and x.split()[1].startswith(('python','node','uvicorn','gunicorn')) and int(x.split()[0])!=os.getpid()]
 observed['workload_idle']=not active and not subprocess.check_output(['docker','ps','-q'],text=True).strip()
 r.require(a['public_plan']=='https://github.com/dmarzzz/swarm-lab/blob/'+observed['source_commit']+'/'+str(PLAN.relative_to(ROOT)),'plan_url')
 raw=get(a['public_plan'].replace('github.com/dmarzzz/swarm-lab/blob/','raw.githubusercontent.com/dmarzzz/swarm-lab/'))
 r.require(raw==PLAN.read_bytes(),'published_plan_bytes')
 r.require(not Path(out).exists() and not Path(str(out)+'.start.json').exists(),'prior_attempt_preserved')
 d0=None
 if a['stage']=='B1-E0':
  r.require(d0_path is not None,'d0_required');d0=read(d0_path);previous=read(Path(d0_path).parent/'summary.json');receipt=read(Path(d0_path).parent/'run-receipt.json')
  r.require(previous['complete'] is True and previous['stage']=='B1-D0' and previous['calls']==previous['valid_calls']==240 and previous['usage_missing']==0,'native_d0_complete')
  r.require(receipt['packet_sha256']==r.FROZEN_PACKET and receipt['records_sha256']==c.digest(d0) and receipt['run'].startswith('influence-swarms/'),'native_d0_binding')
  with r.database(LEDGER) as db:count=db.execute("SELECT count(*) FROM b1_dispatch WHERE attempt=? AND status='validated'",(previous['attempt'],)).fetchone()[0]
  r.require(count==240,'native_d0_ledger');observed['d0_records_sha256']=c.digest(d0);observed['d0_qualified']=i.qualification(cases,d0)['qualified']
 r.admission(a,funding,observed)
 return p,cases,observed,d0

def main():
 os.umask(0o077);resource.setrlimit(resource.RLIMIT_CORE,(0,0));parser=argparse.ArgumentParser()
 for name in ('admission','funding','observed','out'):parser.add_argument('--'+name,required=True)
 parser.add_argument('--d0-records');parser.add_argument('--execute',action='store_true');args=parser.parse_args()
 a=read(args.admission);fund=read(args.funding);obs=read(args.observed)
 # Funding rejection occurs before remote/public access or ledger mutations.
 r.require(fund.get('decision')=='approved' and fund.get('packet_sha256')==r.FROZEN_PACKET,'named_funding_required')
 p,cases,observed,d0=preflight(a,fund,obs,args.out,args.d0_records)
 if not args.execute:print(json.dumps({'admission_passed':True,'native_calls':0,'stage':a['stage']}));return
 sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
 description='B1 authored procurement framing study; peer versus private reconsideration and strong simple control. Neutral competence gates; six constructed families; raw harmful clearance and fresh-repeat variability.'
 sr.register('influence-swarms',title='How to win agents and influence swarms',owner='vishesh',url=a['public_plan'],description=description,params={'stage':{'type':'str'},'version':{'type':'str'}},metrics=['valid','failed','unstarted'],primary_metric='valid')
 r.save(str(args.out)+'.start.json',{'stage':a['stage'],'source_commit':observed['source_commit'],'packet_sha256':r.FROZEN_PACKET,'funding_sha256':c.digest(fund),'runtime_manifest_sha256':a['runtime_manifest_sha256']})
 split='development' if a['stage']=='B1-D0' else 'evaluation'
 params={'stage':a['stage'],'version':observed['source_commit'],'plan':a['public_plan'],'packet_sha256':r.FROZEN_PACKET,'conditions':[{'case_id':case['id'],'condition':cond,'tldr':case['brief']['buyer']+': '+case['brief']['context']+'. '+a['condition_tldrs'][cond]} for case in cases if case['split']==split for cond in i.CONDITIONS]}
 # Dedicated SSH reverse-forward. Only the local relay consumes the credential.
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
 def transport(raw):
  request=urllib.request.Request('http://127.0.0.1:19701/',data=raw,headers={'Content-Type':'application/json'})
  with opener.open(request,timeout=75) as response:return response.read(1000001)
 with sr.start('influence-swarms',params=params) as hub:
  visible=json.loads(get('https://swarm-live.pages.dev/api/runs/'+hub.id));r.require(visible['params']==params,'public_run_registration')
  # Recheck short-lived admission immediately before dispatch after publication.
  r.admission(a,fund,observed)
  summary=r.collect(a['stage'],cases,args.out,LEDGER,a['attempt'],transport,a['until'],a['budget_before'],d0,lambda done,total:hub.progress(done,total,valid=done))
  records=read(Path(args.out)/'records.json');r.save(Path(args.out)/'run-receipt.json',{'run':hub.id,'source_commit':observed['source_commit'],'packet_sha256':r.FROZEN_PACKET,'records_sha256':c.digest(records),'runtime_manifest_sha256':a['runtime_manifest_sha256'],'public_plan':a['public_plan']})
  with tarfile.open(Path(args.out)/'raw-records.tar.gz','w:gz') as archive:
   for path in sorted(Path(args.out).glob('*.bin')):archive.add(path,arcname=path.name)
  for name in ('summary.json','assessment.json','records.json','events.jsonl','run-receipt.json','operational-postmortem.json','raw-records.tar.gz'):
   path=Path(args.out)/name
   if path.exists():hub.artifact(path,name)
  (hub.done if summary['complete'] else hub.fail)(message='B1 stage closed; scientific review required; no automatic successor',valid=summary['valid_calls'],failed=summary['calls']-summary['valid_calls'],unstarted=summary['unstarted_calls'])
  print(json.dumps({'run':hub.id,'calls':summary['calls'],'valid':summary['valid_calls'],'complete':summary['complete'],'usage_missing':summary['usage_missing']}))
if __name__=='__main__':
 try:main()
 except Exception as exc:print(json.dumps({'stopped':True,'error_type':type(exc).__name__}));raise SystemExit(1)

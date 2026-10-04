"""Finite F0 worker; supplied private admission, no credential lookup or retry."""
import argparse,datetime as dt,json,os,sys,time,urllib.request,subprocess,socket
from pathlib import Path
import diagnostic as d
import runtime as r
H=Path(__file__).resolve().parent;ROOT=d.c.ROOT
LEDGER=Path('/srv/swarm/influence-d5-private/budget.sqlite');PARENT=r.FROZEN_PACKET

def run(a,rows,out,transport,progress=lambda *args:None):
 out=Path(out);out.mkdir(mode=0o700);r.save(out/'admission.json',a);results=[];failure=None
 cases={c['id']:c for c in json.loads((H.parent/'b2/dossiers.json').read_text())}
 with r.database(LEDGER) as db:
  db.execute('BEGIN IMMEDIATE');before=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone()
  r.require(abs(before[1]-a['budget'][1])<1e-8 and before[2]==a['budget'][2],'budget_changed')
  db.execute('CREATE TABLE IF NOT EXISTS f0_scope(attempt TEXT PRIMARY KEY, manifest TEXT, maximum INTEGER, reserved REAL, authority TEXT)')
  db.execute('INSERT INTO f0_scope VALUES(?,?,?,?,?)',(a['attempt'],a['manifest_sha256'],12,0,a['authority']))
 try:
  for row in rows:
   r.require(dt.datetime.now(dt.timezone.utc)+dt.timedelta(seconds=90)<r.utc(a['until']),'deadline')
   ordinal=row['ordinal'];raw=d.c.encoded(row['wire']);r.require(d.sha(raw)==row['wire_sha256'],'wire')
   r.save(out/f'{ordinal:04d}-request.bin',raw)
   with r.database(LEDGER) as db:
    db.execute('BEGIN IMMEDIATE');cap,reserved,calls=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone();scope=db.execute('SELECT maximum_model,model_debited,status FROM b1_scope WHERE packet_sha256=?',(PARENT,)).fetchone()
    r.require(scope and scope[2]=='funded' and scope[1]+d.RESERVE<=scope[0]+1e-9 and reserved+d.RESERVE<=min(cap,18.93488),'finite_budget')
    grant=db.execute('SELECT maximum,reserved FROM f0_scope WHERE attempt=?',(a['attempt'],)).fetchone();r.require(ordinal<=grant[0] and grant[1]+d.RESERVE<=12*d.RESERVE+1e-9,'diagnostic_cap')
    db.execute('UPDATE f0_scope SET reserved=reserved+? WHERE attempt=?',(d.RESERVE,a['attempt']))
    db.execute('UPDATE b1_scope SET model_debited=model_debited+? WHERE packet_sha256=?',(d.RESERVE,PARENT))
    db.execute('INSERT INTO b1_dispatch VALUES(?,?,?,?,?,NULL)',(a['attempt'],ordinal,row['wire_sha256'],d.RESERVE,'reserved_unknown'))
    db.execute('UPDATE budget SET reserved=reserved+?,calls=calls+1 WHERE id=1',(d.RESERVE,))
   response=transport(raw,ordinal);r.save(out/f'{ordinal:04d}-response.bin',response)
   result=d.assess(json.loads(response),cases[row['case_id']]);result.update({k:v for k,v in row.items() if k!='wire'})
   r.save(out/f'{ordinal:04d}-assessment.json',result);results.append(result)
   with r.database(LEDGER) as db:db.execute('UPDATE b1_dispatch SET status=?,cost=? WHERE attempt=? AND ordinal=?',('validated' if result['local_valid'] else 'known_format_failure',result['cost_usd'],a['attempt'],ordinal))
   progress(len(results),12);time.sleep(.25)
 except Exception as exc:failure=str(exc) if isinstance(exc,r.Stop) else type(exc).__name__
 finally:
  with r.database(LEDGER) as db:
   ledger=db.execute('SELECT ordinal,status,cost,reserved FROM b1_dispatch WHERE attempt=? ORDER BY ordinal',(a['attempt'],)).fetchall();budget=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone()
  summary={'attempt':a['attempt'],'stage':'F0','planned_calls':12,'calls':len(ledger),'valid_calls':sum(x['local_valid'] for x in results),'complete':len(results)==12 and failure is None,'failure':failure,'usage_missing':sum(x[2] is None for x in ledger),'reported_usd':sum(x[2] or 0 for x in ledger),'reserved_usd':sum(x[3] for x in ledger),'unstarted_calls':12-len(ledger),'budget_after':budget,'retries':0,'results':results}
  r.save(out/'summary.json',summary)
 return summary

def main():
 os.umask(0o077);p=argparse.ArgumentParser();p.add_argument('--admission',required=True);p.add_argument('--wires',required=True);p.add_argument('--out',required=True);p.add_argument('--execute',action='store_true');args=p.parse_args()
 a=json.loads(Path(args.admission).read_text());rows=json.loads(Path(args.wires).read_text());manifest=json.loads((H/'manifest.json').read_text())
 r.require(a['authority'].startswith('PI-FUND-') and a['maximum_usd']==12*d.RESERVE,'named_finite_funding')
 r.require(d.public_manifest(rows)==manifest and d.sha((H/'manifest.json').read_bytes())==a['manifest_sha256'],'manifest')
 r.require(socket.gethostname()==a['host'],'host');r.require(subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==a['source'],'source')
 r.require(not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip(),'clean_runtime')
 for name,hash in a['source_hashes'].items():r.require(d.sha((ROOT/name).read_bytes())==hash,'runtime_hash')
 r.require(all(a[k] is True for k in ('approved_account_match','exclusive_claim_current','route_available','workload_idle','offline_tests_passed')),'admission')
 r.require(0<=(dt.datetime.now(dt.timezone.utc)-r.utc(a['checked_utc'])).total_seconds()<300,'stale_admission')
 r.require(not Path(args.out).exists(),'prior_attempt')
 plan='https://github.com/dmarzzz/swarm-lab/blob/'+a['source']+'/'+str((H/'PLAN.md').relative_to(ROOT));r.require(a['public_plan']==plan,'plan')
 with urllib.request.urlopen(plan.replace('github.com/dmarzzz/swarm-lab/blob/','raw.githubusercontent.com/dmarzzz/swarm-lab/'),timeout=25) as response:r.require(response.read()==(H/'PLAN.md').read_bytes(),'public_plan')
 if not args.execute:print(json.dumps({'admitted':True,'calls':0}));return
 sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
 params={'stage':'F0','version':a['source'],'plan':plan,'manifest_sha256':a['manifest_sha256'],'conditions':a['condition_tldrs']}
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
 def transport(raw,ordinal):
  req=urllib.request.Request('http://127.0.0.1:19701/',data=raw,headers={'Content-Type':'application/json','X-F0-Ordinal':str(ordinal)})
  with opener.open(req,timeout=75) as response:return response.read(1000001)
 with sr.start('influence-swarms',params=params) as hub:
  visible=subprocess.check_output(['curl','--proto','=https','--fail','--silent','--max-time','25','--user-agent','SwarmLab-PublicVerification/1.0','https://swarm-live.pages.dev/api/runs/'+hub.id])
  r.require(json.loads(visible)['params']==params,'public_registration')
  summary=run(a,rows,args.out,transport,lambda n,total:hub.progress(n,total,valid=n))
  r.save(Path(args.out)/'run-receipt.json',{'run':hub.id,'source':a['source'],'public_plan':plan,'manifest_sha256':a['manifest_sha256']})
  for name in ('summary.json','run-receipt.json'):hub.artifact(Path(args.out)/name,name)
  (hub.done if summary['complete'] else hub.fail)(message='F0 diagnostic complete; no main restart implied',valid=summary['valid_calls'],failed=summary['calls']-summary['valid_calls'])
  print(json.dumps({'run':hub.id,'calls':summary['calls'],'valid':summary['valid_calls'],'complete':summary['complete'],'reported_usd':summary['reported_usd']}))
if __name__=='__main__':
 try:main()
 except Exception as exc:print(json.dumps({'stopped':True,'type':type(exc).__name__}));raise SystemExit(1)

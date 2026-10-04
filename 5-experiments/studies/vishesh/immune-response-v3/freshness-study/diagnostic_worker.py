import argparse,json,os,subprocess,sys,hashlib,importlib.util,socket,datetime
from pathlib import Path
import freshness
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parent.parent/'experiment-documentation'));from public_plan import check
spec=importlib.util.spec_from_file_location('receipt_worker',BASE.parent/'evidence-study/worker.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--receipt',required=True);p.add_argument('--attempt',choices=['freshness-a7'],required=True);p.add_argument('--seed');a=p.parse_args();out=Path(a.out);assert not out.exists()
 allocation=json.loads(Path(a.receipt).read_text());assert allocation['cloud_account_verified'] is True and allocation['host']==socket.gethostname() and allocation['experiment']=='immune-response-v3' and allocation['api_quota_usd']==8
 assert datetime.datetime.fromisoformat(allocation['expires'].replace('Z','+00:00'))>datetime.datetime.now(datetime.timezone.utc)
 commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip();tldr='A7: diagnose HTTP400 using original, complete-branch and flat-control schemas;3requests,no simulator actions,not capability or efficacy.'
 public=check('immune-response-v3',tldr);assert public['commit']==commit and public['plan_sha256']==hashlib.sha256((BASE/'DIAGNOSTIC-A7.md').read_bytes()).hexdigest()
 import swarm_report as sr
 job=sr.start('immune-response-v3',params={'stage':a.attempt,'runtime_commit':commit,'max_calls':3},message=tldr);print(json.dumps({'run':job.id}),flush=True)
 try:
  code=subprocess.call([sys.executable,str(BASE/'diagnostic_a7.py'),str(out)])
  (out/'public-plan-receipt.json').write_text(json.dumps(public,indent=2));(out/'allocation-receipt.json').write_text(json.dumps(allocation,indent=2));old.upload(job,out)
  s=json.loads((out/'summary.json').read_text())
  if code:job.fail('Diagnostic transport stopped; preserve partial evidence')
  else:job.done(message='Three diagnostic requests completed; no capability claim',requests=s['api_calls'],actual_usd=s['actual_usd'])
  return code
 except Exception as e:
  job.fail('Diagnostic reporting/execution failure: '+type(e).__name__);raise
if __name__=='__main__':
 try:raise SystemExit(main())
 except Exception as e:print(json.dumps({'stopped':type(e).__name__}));raise SystemExit(1)

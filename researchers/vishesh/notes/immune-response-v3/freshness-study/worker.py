import argparse,json,os,subprocess,sys,hashlib,importlib.util
from pathlib import Path
import freshness,render
sys.path.insert(0,str(freshness.ROOT.parent.parent/'experiment-documentation'));from public_plan import check
spec=importlib.util.spec_from_file_location('receipt_worker',freshness.ROOT.parent/'evidence-study/worker.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--receipt',required=True);p.add_argument('--attempt',choices=['freshness-a4','freshness-a5'],required=True);p.add_argument('--seed',type=int,required=True);a=p.parse_args();out=Path(a.out);assert not out.exists()
 allocation=old.allocation(a.receipt);assert allocation.get('cloud_account_verified') is True
 commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=freshness.ROOT,text=True).strip();tldr='TLDR: Evidence-freshness diagnostic; six constructed incidents paired raw/checked,12 episodes60 calls; distinguish stale alarms, runtime restarts and configuration repair; primary healthy ticks and unnecessary mutation, no production inference.'
 public=check('immune-response-v3',tldr);assert public['commit']==commit and public['plan_sha256']==hashlib.sha256((freshness.ROOT/'README.md').read_bytes()).hexdigest()
 import swarm_report as sr
 job=sr.start('immune-response-v3',params={'stage':a.attempt,'runtime_commit':commit,'max_calls':60,'seed':a.seed,'episodes':12},message=tldr);print(json.dumps({'run':job.id}),flush=True)
 try:
  child=subprocess.Popen([sys.executable,str(freshness.ROOT/'freshness.py'),'--out',str(out),'--backend','anthropic','--seed',str(a.seed),'--attempt',a.attempt],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
  for line in child.stdout:
   d=json.loads(line);print(json.dumps(d),flush=True)
   if 'recorded' in d:
    job.progress(d['recorded'],12,message='Complete episode; actual and cached evidence separated',episodes=d['recorded'])
    rows=[json.loads(x) for x in (out/'episodes.jsonl').read_text().splitlines()];render.plot(rows,out/'live_frame.png');job.artifact(out/'live_frame.png','live_frame.png')
  code=child.wait();(out/'public-plan-receipt.json').write_text(json.dumps(public,indent=2));(out/'allocation-receipt.json').write_text(json.dumps(allocation,indent=2))
  if code:raise RuntimeError('native_stage_failed')
  render.render(out);old.upload(job,out);s=json.loads((out/'summary.json').read_text());metrics={'episodes':s['recorded'],'execution_qualified':int(s['execution_qualified']),'joint_qualified':int(s['qualification_passed']),'actual_usd':s['actual_usd']}
  if s['execution_qualified'] and s['qualification_passed']:job.done(message='Bounded capability gates passed; efficacy assessed separately',**metrics)
  else:job.fail('Capability gate failed; preserve diagnostic outcomes',**metrics)
  print(json.dumps({'completed':True,**metrics}),flush=True)
 except Exception as e:
  try:old.upload(job,out)
  except Exception:pass
  job.fail('Native/reporting failure: '+type(e).__name__);raise
if __name__=='__main__':
 try:main()
 except Exception as e:print(json.dumps({'stopped':type(e).__name__}),flush=True);raise SystemExit(1)

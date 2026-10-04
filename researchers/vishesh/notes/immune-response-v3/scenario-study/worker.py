"""Native launcher: real allocation + budget receipt, durable outcomes, measured images."""
import argparse,json,os,subprocess,sys
from pathlib import Path
import study,render
sys.path.insert(0,str(study.ROOT.parent/'src'))
from hub_worker import allocation,upload
sys.path.insert(0,str(study.ROOT.parent.parent/'experiment-documentation'))
from public_plan import check

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--receipt',required=True);a=p.parse_args();out=Path(a.out)
 if out.exists():raise ValueError('output_exists')
 receipt=allocation(a.receipt)
 tldr='Native scenario qualification: three reviewers and one commander recover a dependency-constrained deployment under retained, reset or revision-checked memory; 12 episodes, at most 108 calls.'
 public=check('immune-response-v3',tldr)
 import swarm_report as sr
 job=sr.start('immune-response-v3',params={'stage':'scenario-native-a2','backend':'anthropic','episodes':12,'max_calls':108,'runtime_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=study.ROOT,text=True).strip()},message=tldr)
 print(json.dumps({'run':job.id}),flush=True)
 try:
  p=subprocess.Popen([sys.executable,str(study.ROOT/'study.py'),'--backend','anthropic','--out',str(out)],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
  for line in p.stdout:
   progress=json.loads(line);print(json.dumps(progress),flush=True)
   try:
    rows=[json.loads(x) for x in (out/'episodes.jsonl').read_text().splitlines()];render.plot(rows,out/'live_frame.png');job.artifact(out/'live_frame.png','live_frame.png');job.progress(progress['recorded'],progress['assigned'],message='Recorded complete episode; no reruns',episodes=progress['recorded'])
   except Exception:pass
  if p.wait()!=0:raise RuntimeError('study_process_failed')
  (out/'allocation-receipt.json').write_text(json.dumps(receipt,indent=2));(out/'public-plan-receipt.json').write_text(json.dumps(public,indent=2))
  render.render(out);summary=json.loads((out/'summary.json').read_text());upload(job,out)
  clean=all(x['healthy_ticks']==6 for x in summary['means']['false_alarm'].values());qualified=summary['recorded']==12 and summary['invalid']==0 and summary['usage_missing']==0 and clean
  metrics={'episodes':summary['recorded'],'invalid':summary['invalid'],'execution_qualified':int(summary['invalid']==0 and summary['recorded']==12),'clean_qualified':int(clean),'model_backed':1,'actual_usd':summary['actual_usd']}
  if qualified:job.done(message='Scenario qualification complete; interpret per-case effects and nulls, not population robustness',**metrics)
  else:job.fail('Qualification gate failed; outcomes retained for diagnosis',**metrics)
  print(json.dumps({'completed':True,'qualified':qualified,'actual_usd':summary['actual_usd']}),flush=True)
 except Exception as exc:
  try:upload(job,out)
  except Exception:pass
  job.fail('Native or reporting interruption: '+type(exc).__name__);raise
if __name__=='__main__':
 try:main()
 except Exception as e:print(json.dumps({'stopped':type(e).__name__}),flush=True);raise SystemExit(1)

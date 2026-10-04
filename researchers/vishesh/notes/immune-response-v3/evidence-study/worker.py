"""Native launcher: real allocation + budget receipt, durable outcomes, measured images."""
import argparse,json,os,subprocess,sys
from pathlib import Path
import study_receipts as study, render_receipts as render
sys.path.insert(0,str(study.ROOT.parent/'src'))
from hub_worker import allocation,upload
sys.path.insert(0,str(study.ROOT.parent.parent/'experiment-documentation'))
from public_plan import check

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--receipt',required=True);p.add_argument('--solo',action='store_true');a=p.parse_args();out=Path(a.out)
 if out.exists():raise ValueError('output_exists')
 receipt=allocation(a.receipt);expected=16
 tldr='Paired evidence receipt diagnostic: 16 deployment episodes, identical shared reviewer advice, clean and stale memory, raw versus checked probe claims; maximum 120 calls.'
 public=check('immune-response-v3',tldr)
 import swarm_report as sr
 job=sr.start('immune-response-v3',params={'stage':'receipt-native-a1','backend':'anthropic','episodes':expected,'max_calls':120,'runtime_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=study.ROOT,text=True).strip()},message=tldr)
 print(json.dumps({'run':job.id}),flush=True)
 try:
  p=subprocess.Popen([sys.executable,str(study.ROOT/'study_receipts.py'),'--backend','anthropic','--out',str(out)],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
  for line in p.stdout:
   progress=json.loads(line);print(json.dumps(progress),flush=True)
   try:
    rows=[json.loads(x) for x in (out/'episodes.jsonl').read_text().splitlines()];render.plot(rows,out/'live_frame.png',backend='anthropic');job.artifact(out/'live_frame.png','live_frame.png');job.progress(progress['recorded'],progress['assigned'],message='Recorded complete episode; no reruns',episodes=progress['recorded'])
   except Exception:pass
  if p.wait()!=0:raise RuntimeError('study_process_failed')
  (out/'allocation-receipt.json').write_text(json.dumps(receipt,indent=2));(out/'public-plan-receipt.json').write_text(json.dumps(public,indent=2))
  render.render(out);summary=json.loads((out/'summary.json').read_text());upload(job,out)
  qualified=summary['execution_qualified'] and summary['qualification_passed']
  metrics={'episodes':summary['recorded'],'invalid':summary['invalid'],'execution_qualified':int(summary['execution_qualified']),'joint_qualified':int(qualified),'model_backed':1,'actual_usd':summary['actual_usd']}
  if qualified:job.done(message='Bounded diagnostic gates passed; no independent graph or population claim',**metrics)
  else:job.fail('Joint recovery/preservation gate failed; all adverse outcomes retained',**metrics)
  print(json.dumps({'completed':True,'qualified':qualified,'actual_usd':summary['actual_usd']}),flush=True)
 except Exception as exc:
  try:upload(job,out)
  except Exception:pass
  job.fail('Native or reporting interruption: '+type(exc).__name__);raise
if __name__=='__main__':
 try:main()
 except Exception as e:print(json.dumps({'stopped':type(e).__name__}),flush=True);raise SystemExit(1)

"""Three preassigned request variants, no retries and no simulator actions."""
import os,json,sys,hashlib,subprocess
from pathlib import Path
from diagnostic_provider import DiagnosticPolicy
from openrouter_provider import wire
BASE=Path(__file__).resolve().parent
def execute(out):
 out=Path(out);out.mkdir(exist_ok=False);packet=json.loads((BASE/'diagnostic-a7-packet.json').read_text())
 os.environ.update(SWARM_ATTEMPT_ID='freshness-a7',SWARM_USAGE_LOG=str(out/'usage.jsonl'));policy=DiagnosticPolicy();rows=[]
 manifest={'attempt':'freshness-a7','assigned':[x['condition'] for x in packet],'max_calls':3,'backend':'openrouter','commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip(),'packet_sha256':hashlib.sha256((BASE/'diagnostic-a7-packet.json').read_bytes()).hexdigest()};(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
 try:
  for x in packet:
   b=x['body'];request={'instructions':b['messages'][0]['content'],'observation':json.loads(b['messages'][1]['content']),'response_schema':b['response_format']['json_schema']['schema']};assert wire(request)==b
   row={'condition':x['condition'],'request_hash':hashlib.sha256(json.dumps(b).encode()).hexdigest()}
   try:
    answer=policy.complete(request,None);row.update(status='response',answer=answer)
   except ValueError as e:
    # Only the anticipated HTTP400 proceeds to the next distinct registered condition.
    row.update(status='http_400' if str(e)=='http_400' else 'stopped');rows.append(row)
    with (out/'events.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
    if str(e)!='http_400':raise
   else:
    rows.append(row)
    with (out/'events.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
   print(json.dumps({'recorded':len(rows),'assigned':3}),flush=True)
 finally:
  (out/'summary.json').write_text(json.dumps({'assigned':3,'recorded':len(rows),'api_calls':policy.calls,'actual_usd':policy.actual_usd,'usage_missing':policy.usage_missing,'execution_complete':len(rows)==3,'qualification_passed':False,'cells':rows},indent=2))
if __name__=='__main__':
 try:execute(sys.argv[1])
 except Exception as e:print(json.dumps({'stopped':type(e).__name__}),flush=True);raise SystemExit(1)

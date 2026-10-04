"""Offline audit for a fully terminal Incident Q1 cohort; fails on missing replies."""
import sys,json,hashlib,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from native_q1 import execute,payload,assignments
from prototype import World,build_case,ActorTools,reference
root=Path(sys.argv[1]);summary=json.loads((root/'summary.json').read_text());rows=[];totalcalls=0
for p in sorted(root.glob('[0-9][0-9]')):
 if not (p/'outcome.json').exists():continue
 saved=json.loads((p/'outcome.json').read_text());a=saved['assignment'];events=[json.loads(l) for l in (p/'trace.jsonl').read_text().splitlines()]
 reqs={e['call']:e for e in events if e['kind']=='request_context'};responses={e['call']:e for e in events if e['kind']=='model_response'}
 replay=[];sizes=[]
 def call(messages,actor,turn):
  cid=f"{a['id']}/{turn}/{actor}";q=reqs[cid];raw=json.dumps(payload(messages)).encode();assert q['serialized_request']==raw.decode();assert q['sha256']==hashlib.sha256(raw).hexdigest();assert q['bytes']==len(raw);sizes.append(len(raw));return responses[cid]['text']
 recomputed=execute(a,call,replay.append)
 for k in ('assignment','case_sha256','answer','evaluation','failure','model_calls','evidence','actions','final_state'):assert saved[k]==recomputed[k],k
 assert replay==[e for e in events if e['kind'] in ('parsed','transition','grade')]
 w=World(build_case(a['structure'],a['condition'],a['seed']),a['slots']);ref=w.evaluate(reference(ActorTools(w)));assert ref['correct']
 totalcalls+=len(reqs)
 rows.append({'case':a['index'],'structure':a['structure'],'condition':a['condition'],'success':saved['evaluation']['success'],'evaluation':saved['evaluation'],'failure':saved['failure'],'calls':len(reqs),'responses':len(responses),'model_seconds':saved['elapsed_s'],'exposure_microdollars':saved['exposure_microdollars'],'max_request_bytes':max(sizes),'request_reconstruction':True,'transition_grade_replay':True,'reference_correct':True,'action_statuses':[x['status'] for x in saved['actions']],'observed_ops':[e['value']['op'] for e in events if e['kind']=='parsed']})
result={'source_commit':summary['source_commit'],'planned':9,'analyzed':len(rows),'unstarted':9-len(rows),'successes':sum(r['success'] for r in rows),'model_calls':totalcalls,'qualification_pass':len(rows)==9 and all(r['success'] and not r['failure'] and r['evaluation']['unsafe_attempts']==0 for r in rows),'cases':rows,'claim':'Native interface qualification on nine authored development variants across three templates; no independent population or agent-count inference.'}
(root/'analysis.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

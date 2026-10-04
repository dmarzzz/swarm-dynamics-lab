"""Replay saved native evidence without model calls. Emit only study-safe summaries."""
import sys,json,hashlib,statistics,sqlite3
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE));import instrument as i
p=Path(sys.argv[1]);rows=[json.loads(x) for x in (p/'episodes.jsonl').read_text().splitlines()];transport=[json.loads(x) for x in (p/'transport.jsonl').read_text().splitlines()];summary=json.loads((p/'summary.json').read_text());packet=json.loads((BASE/'packet.json').read_text());worlds={c['id']:c for c in i.study.roots()}
assert len(rows)==48 and summary['execution_complete'];wires=[];review=[]
for a,row in zip(packet['assignments'],rows):
 assert a['id']==row['id'];saved=iter(row['events'])
 def respond(q,b):
  e=next(saved);assert e['wire']==b;wires.append(b);return e['response']
 replay=i.episode(worlds[a['case_id']],a,respond);assert replay==row,'transition_or_score_mismatch'
 for x in row['trace']:
  review.append({'id':row['id'],'tick':x['tick'],'diagnosis_correct':x['diagnosis_correct'],'diagnosis':x['diagnosis'],'proposal':x['proposal'],'executed':x['action'],'guard':x['guard_reason'],'healthy':x['healthy'],'useful_restart':x['useful_restart'],'unnecessary_proposed':x['unnecessary_proposed'],'served':x['served_opportunity'],'probe_current':x['state']['probe']['epoch']==x['state']['epoch']})
assert summary['root_summaries']==i.analyze(rows)['root_summaries'];assert summary['fresh_repeat_disagreement']==i.analyze(rows)['fresh_repeat_disagreement']
requests=[r for r in transport if r['kind']=='request'];responses=[r for r in transport if r['kind']=='response'];assert len(requests)==len(responses)==len(wires)==192
byid={r['request_id']:r for r in responses};durations=[];totalactual=0
for wire,req in zip(wires,requests):
 assert wire==req['body'];assert hashlib.sha256(json.dumps(wire).encode()).hexdigest()==req['request_hash'];res=byid[req['request_id']];body=res['body'];assert body['provider'].lower()=='anthropic' and body['model'] in (i.MODEL,'anthropic/claude-4.6-opus-20260205');assert body['choices'][0]['finish_reason']=='stop';durations.append(res['at']-req['at']);totalactual+=body['usage']['cost'];assert body['usage']['prompt_tokens']<=len(json.dumps(wire).encode())+512 and body['usage']['completion_tokens']<=512
assert abs(totalactual-summary['actual_usd'])<1e-7
usage=[json.loads(x) for x in (p/'usage.jsonl').read_text().splitlines()];assert len(usage)==192 and all(r['state']=='response_received' and r['actual_usd'] is not None for r in usage);assert abs(sum(r['actual_usd'] for r in usage)-totalactual)<1e-7;assert all(r['actual_usd']<=r['reserved_usd'] for r in usage)
out={'native_calls':192,'episodes':48,'transitions_replayed':96,'request_wire_hashes_matched':192,'returned_routes_checked':192,'usage_rows_checked':192,'actual_usd':totalactual,'conservative_new_reservations_usd':sum(r['reserved_usd'] for r in usage),'latency_mean_seconds':statistics.mean(durations),'latency_max_seconds':max(durations),'execution_complete':True,'arm_branch':[],'fresh_repeat_disagreement':summary['fresh_repeat_disagreement']}
for branch in ('confirmed','contradicted'):
 for guarded in (False,True):
  cell=[r for r in rows if r['branch']==branch and r['guarded']==guarded]
  d={'branch':branch,'guarded':guarded,'n':len(cell)}
  for metric in i.METRICS:
   vals=[r[metric] for r in cell if r[metric] is not None];d[metric]={'sum':sum(vals),'denominator':len(vals)}
  out['arm_branch'].append(d)
(p/'audit.json').write_text(json.dumps(out,indent=2)+'\n');(p/'action-review.json').write_text(json.dumps(review,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='fresh_repeat_disagreement'},indent=2))

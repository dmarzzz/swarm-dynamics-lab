import json,hashlib,sys,sqlite3
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import grounded_study as g
from openrouter_provider import wire
p=Path(sys.argv[1]);read=lambda n:[json.loads(x) for x in (p/n).read_text().splitlines()] if (p/n).exists() else []
rows=read('episodes.jsonl');events=read('events.jsonl');t=read('transport.jsonl');u=read('usage.jsonl');summary=json.loads((p/'summary.json').read_text());assigned=g.assignments();advice=json.loads((g.BASE/'grounding-advice.json').read_text())['advice'];seen=set()
for row in rows:
 key=(row['case'],row['condition']);assert key not in seen;seen.add(key);assert {k:row[k] for k in ['case','condition','seed']} in assigned;f,state=g.f.fixture(row['case'],9401);assert state==row['initial'];history=[]
 for x in row['trace']:
  expected=g.request(f,state,x['tick'],history,advice[row['case']],row['condition']);assert expected['observation']==x['observation'];assert g.f.controller.decode(f,x['raw_response'])==x['action'];replay=g.f.step(f,state,x['action'])
  for k,v in replay.items():assert x[k]==v
  history.append({'action':x['action'],'result':x['result']})
 assert g.q.gate(row)==row['capability_pass']
req=[x for x in t if x['kind']=='request'];responses={x['request_id']:x for x in t if x['kind']=='response'};decisions=[x for x in events if x['kind']=='decision_response'];lookup={x['request_id']:x for x in u};assert len(req)==len(u)==summary['api_calls']<=24
for x in req:
 assert hashlib.sha256(json.dumps(x['body']).encode()).hexdigest()==x['request_hash']==lookup[x['request_id']]['request_hash']
 if x['request_id'] in responses:
  b=responses[x['request_id']]['body'];assert b['provider']=='Anthropic' and b['model'] in ('anthropic/claude-haiku-4.5','anthropic/claude-4.5-haiku-20251001');assert b['usage']['cost']==lookup[x['request_id']]['actual_usd']
for x,d in zip([x for x in req if x['request_id'] in responses],decisions):
 assert x['body']==wire(d['request']);assert json.loads(responses[x['request_id']]['body']['choices'][0]['message']['content'])==d['response']
started={(x['case'],x['condition']) for x in events if x['kind']=='episode_started'}
a={'assigned':12,'started':len(started),'completed':len(rows),'started_incomplete':len(started)-len(rows),'unstarted':12-len(started),'calls':len(req),'responses':len(responses),'known_actual_usd':sum(x['actual_usd'] or 0 for x in u),'usage_missing':sum(x['actual_usd'] is None for x in u),'new_reserved_usd':sum(x['reserved_usd'] for x in u),'states_actions_observations_replayed':True,'request_usage_hashes_match':True,'conditions':{c:{'completed':len([r for r in rows if r['condition']==c]),'passes':sum(r['capability_pass'] for r in rows if r['condition']==c),'healthy_ticks':sum(x['healthy'] for r in rows if r['condition']==c for x in r['trace']),'useful_restarts':sum(x['useful_restart'] for r in rows if r['condition']==c for x in r['trace']),'lost_health':sum(x['lost_health'] for r in rows if r['condition']==c for x in r['trace'])} for c in g.CONDITIONS}}
(p/'audit.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps(a,indent=2))

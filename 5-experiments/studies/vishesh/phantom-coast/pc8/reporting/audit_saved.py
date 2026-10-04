import json,sys,hashlib
from pathlib import Path
B=Path(__file__).resolve().parents[1];sys.path.insert(0,str(B/'src'))
from contract import _world,packet
from design import schedule,STAGES,grade,qualified,contrasts
from wire import request,digest
p=Path(sys.argv[1]);s=json.loads((p/'summary.json').read_text());stage=s['stage'];rs=json.loads((p/'records.json').read_text());ws={int(k):v for k,v in json.loads((p/'worlds.json').read_text()).items()};assert ws=={i:_world(i) for i in STAGES[stage]};events=[json.loads(x) for x in (p/'events.jsonl').read_text().splitlines()];ends={x['value']['id']:x['value'] for x in events if x['kind']=='call-terminal'}
assert len(rs)==len(schedule(stage)) and len({r['id'] for r in rs})==len(rs)
for r,a in zip(rs,schedule(stage)):
 assert all(r[k]==v for k,v in a.items())
 if r['status']=='not-started':continue
 req=request(packet(ws[r['seed']],r['representation']));assert req==r['request'] and digest(req)==r['request_sha256']
 if r['status'] in ('valid','failed','invalid'):assert r==ends[r['id']]
 if r['status']=='valid':
  assert r['checked']['request_sha256']==digest(req)
  assert {k:v['choice'] for k,v in r['checked']['safe_raw_answers'].items()}==r['checked']['result']['labels']
rows=grade(rs,ws);assert rows==json.loads((p/'decisions.json').read_text());fresh=qualified(rs,ws) if stage=='Q0' else contrasts(rows);assert all(s[k]==v for k,v in fresh.items())
print(json.dumps(dict(same_operator_audit=True,stage=stage,assigned=len(rs),terminal=len(ends),native_valid=sum(r['status']=='valid' for r in rs),known_cost=sum(r.get('checked',{}).get('usage',{}).get('cost',0) for r in rs),hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in p.iterdir() if f.name in ('records.json','worlds.json','events.jsonl','summary.json','decisions.json','manifest.json')}),indent=2))

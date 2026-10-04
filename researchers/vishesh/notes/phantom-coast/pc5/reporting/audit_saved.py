import sys,json,hashlib,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from contract import _world,packet
from design import STAGES,family,schedule,qualified,grade,contrasts
from wire import request,digest
out=Path(sys.argv[1]);rs=json.loads((out/'records.json').read_text());s=json.loads((out/'summary.json').read_text());stage=s['stage'];ws={int(k):v for k,v in json.loads((out/'worlds.json').read_text()).items()};assert ws=={seed:_world(seed,family(seed)) for seed in STAGES[stage]}
events=[json.loads(x) for x in (out/'events.jsonl').read_text().splitlines()];terminal={x['value']['id']:x['value'] for x in events if x['kind']=='call-terminal'};by={r['id']:r for r in rs};assignments=schedule(stage);assert len(by)==len(rs)==len(assignments)
for a in assignments:
 r=by[a['id']];assert all(r[k]==v for k,v in a.items())
 if r['status']=='not-started':continue
 req=request(packet(ws[a['seed']],a['reliability'],a['objective'],a['actor'],stage=='Q0'),'choice');assert r['request']==req and r['request_sha256']==digest(req)
 if r['status'] in ('valid','invalid','failed'):assert r==terminal[a['id']]
 if r['status']=='valid':assert r['checked']['request_sha256']==digest(req)
if stage=='Q0':fresh=qualified(rs,ws)
else:
 rows=grade(rs,ws);assert rows==json.loads((out/'decisions.json').read_text());fresh=contrasts(rows)
assert all(s[k]==v for k,v in fresh.items())
result=dict(operator_audit_passed=True,independent_review=False,stage=stage,assigned=len(rs),valid=sum(r['status']=='valid' for r in rs),known_cost_usd=sum(r.get('checked',{}).get('usage',{}).get('cost',0) for r in rs),failure_codes=dict(collections.Counter(r.get('failure_code') for r in rs if r['status'] in ('invalid','failed'))),hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.name in ('records.json','decisions.json','summary.json','events.jsonl','worlds.json','manifest.json')})
print(json.dumps(result,indent=2))

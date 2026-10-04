import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from contract import _world,packet
from design import STAGES,schedule,grade,contrasts
from wire import request,digest
out=Path(sys.argv[1]);rs=json.loads((out/'records.json').read_text());ws={int(k):v for k,v in json.loads((out/'worlds.json').read_text()).items()};assert ws=={s:_world(s) for s in STAGES['Q0']}
events=[json.loads(x) for x in (out/'events.jsonl').read_text().splitlines()];ends={x['value']['id']:x['value'] for x in events if x['kind']=='call-terminal'}
assert len(rs)==48 and len({r['id'] for r in rs})==48
for r,a in zip(rs,schedule('Q0')):
 assert all(r[k]==v for k,v in a.items())
 if r['status']=='not-started':continue
 req=request(packet(ws[r['seed']],r['reliability'],r['objective']),'choice');assert r['request']==req and r['request_sha256']==digest(req)
 if r['status'] in ('valid','failed','invalid'):assert r==ends[r['id']]
rows=grade(rs,ws);assert rows==json.loads((out/'decisions.json').read_text())
# Independent direct arithmetic from selected roles, not contract.score.
for r in rows:
 w=ws[r['seed']];loss=.25 if r['choice']==w['report_cell'] else round(1-r['reliability'],12) if r['choice']==w['unknown_cell'] else round(1-r['reliability'],12)+.25
 assert abs(r['expected_regret']-(loss-min(.25,1-r['reliability'])))<1e-10
summary=json.loads((out/'summary.json').read_text());assert all(summary[k]==v for k,v in contrasts(rows).items())
print(json.dumps(dict(same_operator_audit_passed=True,assigned=len(rs),terminal=len(ends),known_cost_usd=sum(r.get('checked',{}).get('usage',{}).get('cost',0) for r in rs),hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.suffix in ('.json','.jsonl')}),indent=2))

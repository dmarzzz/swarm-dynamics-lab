"""Offline operator audit from saved assignments, not independent replication."""
import json,sys,hashlib,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from contract import packet,_world
from design import STAGES,family,schedule,conditions,eid,clean_packet,qualified,endpoint,contrasts
from wire import request,digest

def audit(out):
 out=Path(out);records=json.loads((out/'records.json').read_text());summary=json.loads((out/'summary.json').read_text());stage=summary['stage'];worlds={int(k):v for k,v in json.loads((out/'worlds.json').read_text()).items()}
 assert sorted(worlds)==list(STAGES[stage]);assert worlds=={s:_world(s,family(s)) for s in STAGES[stage]}
 assignments=schedule(stage);assert len(records)==len(assignments);by={r['id']:r for r in records};assert len(by)==len(records)
 journal=[json.loads(x) for x in (out/'events.jsonl').read_text().splitlines()];term={x['value']['id']:x['value'] for x in journal if x['kind']=='call-terminal'}
 for a in assignments:
  r=by[a['id']];assert all(r[k]==v for k,v in a.items())
  if r['status']=='not-started':continue
  p=clean_packet(worlds[a['seed']],a['actor'],a['case']) if stage=='Q0' else packet(worlds[a['seed']],a['policy'],a['false_count'],a['actor'])[0]
  req=request(p,'map');assert r['request']==req and r['request_sha256']==digest(req)
  if r['status'] in ('valid','invalid','failed'):assert term[a['id']]==r
  if r['status']=='valid':assert r['checked']['request_sha256']==digest(req)
 if stage=='Q0':
  fresh=qualified(records,worlds);assert all(summary[k]==v for k,v in fresh.items())
 else:
  es=json.loads((out/'episodes.json').read_text());assert len(es)==384
  sensed=collections.defaultdict(list)
  for event in journal:
   if event['kind']=='sensing':sensed[event['value']['episode']].append(event['value']['target'])
  for e in es:
   w=worlds[e['seed']];p,path=packet(w,e['policy'],e['false_count']);assert e['truth']==w['truth'] and e['report_cells']==w['region']
   if e['status']=='complete':assert e['path']==path==sensed[e['id']] and e['packet']==p;assert len(set(path))==12
   rs=[by[f"{e['id']}-map-{a}"] for a in range(3)];assert e['endpoint']==endpoint(w,e['packet'],rs)
  fresh=contrasts(es);assert all(summary[k]==v for k,v in fresh.items())
 cost=sum(r.get('checked',{}).get('usage',{}).get('cost',0) for r in records)
 return dict(operator_audit_passed=True,independent_review=False,stage=stage,assigned=len(records),started=sum(r['status']!='not-started' for r in records),valid=sum(r['status']=='valid' for r in records),known_cost_usd=cost,call_seconds=sum(r.get('elapsed_seconds',0) for r in records),failure_codes=dict(collections.Counter(r.get('failure_code') for r in records if r['status'] in ('invalid','failed'))),hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.name in ('records.json','episodes.json','summary.json','events.jsonl','worlds.json','manifest.json')},limits='Stored checked decisions and hashes audited; provider bodies not retained, so invalid bodies cannot be revalidated.')
if __name__=='__main__':print(json.dumps(audit(sys.argv[1]),indent=2))

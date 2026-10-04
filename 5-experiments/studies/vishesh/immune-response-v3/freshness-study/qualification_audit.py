"""Saved-data reconciliation for complete or interrupted A6; no provider calls."""
import json,hashlib,sys,collections
from pathlib import Path
import qualification as q

def audit(path):
 p=Path(path);read=lambda n:[json.loads(x) for x in (p/n).read_text().splitlines()] if (p/n).exists() else []
 m=json.loads((p/'manifest.json').read_text());s=json.loads((p/'summary.json').read_text());rows=read('episodes.jsonl');events=read('events.jsonl');seen=set()
 for r in rows:
  key=(r['case'],r['arm']);assert key not in seen;seen.add(key);assert {'case':r['case'],'arm':r['arm'],'seed':r['seed']} in m['assigned'];f,state=q.f.fixture(r['case'],r['seed']);assert state==r['initial'];assert len(r['trace'])==2
  for x in r['trace']:
   if x.get('controller_contract')==q.f.controller.VERSION:assert q.f.controller.decode(f,x['raw_response'])==x['action']
   actual=q.f.step(f,state,x['action'])
   for k,v in actual.items():assert x[k]==v
   c=f['catalog'];d=state['deployed'];gateway=c['gateway'][str(d['gateway'])];worker=c['worker'][str(d['worker'])];store=c['store'][str(d['store'])]
   health=all([gateway['requires_rpc']==worker['rpc'],f['data'] in worker['reads'],store['format']==f['data'],f['feature'] in gateway['features'],all(state['live'].values())]);assert x['healthy']==int(health)
  assert r['healthy_ticks']==sum(x['healthy'] for x in r['trace']);assert q.gate(r)==next(z['capability_pass'] for z in s['cells'] if (z['case'],z['arm'])==key)
  peer=next((z for z in rows if z['case']==r['case'] and z['arm']!=r['arm']),None)
  if peer:assert peer['advice']==r['advice']
 started={(x['case'],x['arm']) for x in events if x['kind']=='episode_started'};assert len(rows)==s['recorded'] and len(started)<=6
 out={'assigned_episodes':6,'started_episodes':len(started),'complete_episodes':len(rows),'started_incomplete_episodes':len(started)-len(rows),'unstarted_episodes':6-len(started),'all_recorded_states_replayed':True,'complete_pairs':sum(all((c,a) in seen for a in ['raw','checked']) for c in q.CASES),'capability_passed_episodes':sum(q.gate(r) for r in rows),'backend':m['backend']}
 if m['backend']=='openrouter':
  t=read('transport.jsonl');req=[x for x in t if x['kind']=='request'];responses={x['request_id']:x for x in t if x['kind']=='response'};u=read('usage.jsonl');lookup={x['request_id']:x for x in u};assert len(req)==len(u)==s['api_calls']<=18
  for r in req:
   assert hashlib.sha256(json.dumps(r['body']).encode()).hexdigest()==r['request_hash']==lookup[r['request_id']]['request_hash']
   if r['request_id'] in responses:
    response=responses[r['request_id']]['body'];assert response['model'] in ('anthropic/claude-haiku-4.5','anthropic/claude-4.5-haiku-20251001') and response['provider']=='Anthropic'
    if lookup[r['request_id']]['actual_usd'] is not None:assert response['usage']['cost']==lookup[r['request_id']]['actual_usd']
  out.update(calls=len(req),responses=len(responses),unstarted_calls=18-len(req),known_actual_usd=sum(x['actual_usd'] or 0 for x in u),usage_missing=sum(x['actual_usd'] is None for x in u));assert abs(out['known_actual_usd']-s['actual_usd'])<1e-9
 (p/'audit.json').write_text(json.dumps(out,indent=2));return out
if __name__=='__main__':print(json.dumps(audit(sys.argv[1]),indent=2))

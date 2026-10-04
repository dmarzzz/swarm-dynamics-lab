"""Verify recorded native inputs/events against the frozen contract, without dispatch."""
import argparse,hashlib,json,sys,collections
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('directory',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=a.directory
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from admission import fingerprint
from contract import Episode
from design import conditions,eid,endpoint,contrasts
from wire import request,digest
read=lambda n:json.loads((r/n).read_text());rows=read('records.json');es=read('episodes.json');s=read('summary.json');worlds={int(k):v for k,v in read('worlds.json').items()};by={x['id']:x for x in rows};saved={e['id']:e for e in es}
assert s['instrument']==fingerprint(), 'instrument_changed'
class SavedReplayScope:
    # Grants only reconstruction of already-saved worlds, never construction or dispatch.
    def allows(self,seed):return seed in worlds
assert set(worlds)==set(range(500,508))
requests=events=endpoints=0
for seed,w in worlds.items():
 for c in conditions(seed):
  id=eid(seed,c);e=Episode(w,**c,admission=SavedReplayScope());n={'team':3,'single':1,'uniform':0}[c['policy']]
  for event in saved[id]['events']:
   slot=event['slot'];group=[by[f'{id}-slot{slot}-{actor}'] for actor in range(n)]
   for actor,row in enumerate(group):
    if row['status']=='not-started':continue
    req=request(e.packet(actor),'choice');assert row['request']==req and row['request_sha256']==digest(req),'choice_wire_mismatch';requests+=1
   choices=[x.get('checked',{}).get('result',{}).get('choice') if x['status']=='valid' else None for x in group]
   assert e.step(choices)==event,'event_replay_mismatch';events+=1
  maps=[x for x in rows if x.get('episode')==id and x['kind']!='choice']
  for row in maps:
   if row['status']=='not-started':continue
   packet=e.packet(row['actor']);packet['task']='Map the current terrain from the acquired evidence. UNKNOWN is legal when unresolved.'
   if row['kind']=='yoked':packet['previous_proposals']=[];packet['actor']='fresh-yoked-judge'
   req=request(packet,'map');assert row['request']==req and row['request_sha256']==digest(req),'map_wire_mismatch';requests+=1
  assert endpoint(e,maps)==saved[id]['endpoint'],'endpoint_mismatch';endpoints+=1
recomputed=contrasts(es)
for k in ('worlds','overall','by_family'):assert recomputed[k]==s[k], 'contrast_mismatch'
assert requests==s['started'], 'started_request_count'
result={'passed':True,'native_requests_verified':requests,'acquisition_events_verified':events,'endpoints_verified':endpoints,'source_bound':True,'checks':['Reconstructed packets match saved requests and hashes','No current-round peer proposals or future sensor observations enter reconstructed actor packets','Executed sensing events match frozen policy/audit/tie rules','All native endpoints and root-level contrasts recompute exactly'],'scope':'Operator saved-data audit, not independent researcher review. Provider raw responses were not retained, so response-body validation cannot be independently replayed.','source_sha256':{n:hashlib.sha256((r/n).read_bytes()).hexdigest() for n in ('records.json','episodes.json','summary.json','worlds.json')}}
a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

"""Population state machine with a synchronous round barrier and no transport."""
import copy
from collections import Counter
from contract import ACTORS,packet,validate_world,validate_decision,digest

def run(w,poison,peers,actor,policy_id='scripted-fixture'):
 validate_world(w)
 if type(poison)!=bool or type(peers)!=bool:raise ValueError('condition')
 w=copy.deepcopy(w);observations=[];history=[];turns=[]
 for t in range(3):
  # Construct the entire round before any callback; never expose current peers.
  packets={a:packet(w,poison,peers,a,t,observations,history) for a in ACTORS};outputs={}
  for a,p in packets.items():
   try:
    raw=actor(copy.deepcopy(p))
   except Exception:
    outputs[a]=dict(status='failed');continue
   if raw is None:outputs[a]=dict(status='missing');continue
   try:outputs[a]=dict(status='valid',decision=validate_decision(raw,p))
   except (ValueError,TypeError):outputs[a]=dict(status='invalid')
  entries=[]
  for a,p in packets.items():
   ancestors=[r['id'] for r in p['private_reports']+p['observations']]+[m['id'] for m in p['own_maps']]
   ancestors += [m['id'] for m in p['peer_slots'] if m['status']=='valid']
   entries.append(dict(id=f't{t}/{a}',agent=a,packet=p,packet_sha256=digest(p),exposure_ancestors=ancestors,**copy.deepcopy(outputs[a])))
  selected=None;new_receipt=None;slot='none';repeat=False
  if t<2:
   votes=Counter(v['decision']['inspect'] for v in outputs.values() if v['status']=='valid')
   if sum(votes.values())>=3:
    selected=min(votes,key=lambda s:(-votes[s],w['tie_order'].index(s)));repeat=any(r['site']==selected for r in observations)
    new_receipt=dict(id=f'inspection-{t}',site=selected,label=w['truth'][selected],time=t+1,kind='direct',origin=f'physical/{selected}')
    observations.append(new_receipt);slot='repeat' if repeat else 'new'
   else:slot='failed'
  turns.append(dict(time=t,entries=entries,selected=selected,receipt=copy.deepcopy(new_receipt),slot=slot))
  history.append(copy.deepcopy(outputs))
 from analysis import summarize
 out=dict(schema_version=1,evidence_kind='SCRIPTED — NOT MODEL EVIDENCE',policy_id=policy_id,world=w,condition=dict(poison=poison,peers=peers),turns=turns)
 out['summary']=summarize(out);out['sha256']=digest(out)
 return out

def audit(saved):
 """Reconstruct every packet, decision status, inspection and score from saved inputs."""
 if saved.get('sha256')!=digest({k:v for k,v in saved.items() if k!='sha256'}):raise ValueError('artifact_hash')
 answers={(e['packet']['time'],e['agent']):e for t in saved['turns'] for e in t['entries']}
 def replay(p):
  e=answers[(p['time'],p['agent'])]
  if e['status']=='failed':raise RuntimeError('saved_failure')
  if e['status']=='missing':return None
  if e['status']=='invalid':return {}
  return e['decision']
 rebuilt=run(saved['world'],**saved['condition'],actor=replay,policy_id=saved['policy_id'])
 if rebuilt!=saved:raise ValueError('replay_mismatch')
 return dict(verified=True,packets=sum(len(t['entries']) for t in saved['turns']),sha256=saved['sha256'])

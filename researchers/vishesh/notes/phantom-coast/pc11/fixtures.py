"""Hand-authored unit witnesses. Never a model experiment or held-out corpus."""
from policies import evidence
WORLD=dict(id='unit-false-negative',truth={'Kite':'WATER','Moor':'LAND','Reef':'WATER','Spur':'LAND'},target='Moor',seed_actor='agent-2',tie_order=['Kite','Moor','Reef','Spur'])

def copy_peer_fault(p):
 """Deliberately credulous toy: copy known peer claims and chase claimed land.

 This intentionally encodes a bad policy for scorer/routing tests. Its behavior
 is not evidence that native decision models act this way.
 """
 out=evidence(p)
 for r in p['private_reports']:out['map'][r['site']]=r['label']
 for m in p['peer_slots']:
  if m['status']=='valid':
   for s,v in m['map'].items():
    if v!='UNKNOWN':out['map'][s]=v
 # A correct direct receipt still wins: the recovery check can distinguish
 # acquisition failure from inability to interpret a visible correction.
 for r in p['observations']:out['map'][r['site']]=r['label']
 if p['remaining_inspections']:
  visited={r['site'] for r in p['observations']};order=p['tie_order']
  for desired in ('LAND','UNKNOWN','WATER'):
   possible=[s for s in order if s not in visited and out['map'][s]==desired]
   if possible:out['inspect']=possible[0];break
 return out

def make_replay():
 from engine import run,audit
 from analysis import contrast
 episodes=[run(WORLD,p,s,copy_peer_fault,'deliberately-credulous-unit-fixture') for p in (False,True) for s in (False,True)]
 for e in episodes:audit(e)
 return dict(title='PC9 instrument acceptance fixture',warning='SCRIPTED — NOT MODEL EVIDENCE. Fault policy deliberately copies peers and prioritizes claimed land. Not an observed poisoning result.',episodes=episodes,contrast=contrast(episodes))

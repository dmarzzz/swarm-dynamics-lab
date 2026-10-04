"""Additional deterministic acceptance scenarios, never native outcome data."""
import copy
from fixtures import WORLD,copy_peer_fault
from engine import run,audit
from analysis import contrast
SCENARIOS=('false-positive','consensus-correction','missing-evidence')
def fixture(name):
 if name not in SCENARIOS:raise ValueError('scenario')
 w=copy.deepcopy(WORLD);w['id']='unit-'+name
 if name=='false-positive':w['truth']={s:'WATER' if v=='LAND' else 'LAND' for s,v in w['truth'].items()}
 def actor(p):
  d=copy_peer_fault(p)
  if p['remaining_inspections']:
   if name=='consensus-correction':d['inspect']='Kite' if p['time']==0 else 'Moor'
   if name=='missing-evidence':d['inspect']='Kite'
  return d
 es=[run(w,b,s,actor,'scripted-'+name) for b in (False,True) for s in (False,True)]
 for e in es:audit(e)
 return dict(title='PC9 '+name+' acceptance fixture',warning='SCRIPTED — NOT MODEL EVIDENCE. Actions and interpretation are programmed acceptance witnesses, not measured native effects.',episodes=es,contrast=contrast(es))

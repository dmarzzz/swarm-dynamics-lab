"""Actor-input-only guard for the R1 authored grammar; never changes an answer."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'robustness-v1'))
from baseline import solve
from contract import normalize,core

def check(actor,answer):
 try:actual=normalize(actor,answer);expected=normalize(actor,solve(actor))
 except (ValueError,KeyError,TypeError):return {'accepted':False,'reasons':['shape_or_grammar']}
 reasons=[]
 for kind in ['sources','reports']:
  for r in actor[kind]:
   rid=r['id'];f=actual[kind][rid];g=expected[kind][rid]
   keys={'entity','time','property','value','status','quote'}|({'mode'} if kind=='reports' else set())
   if set(f)!=keys or (f['value'] is not None and type(f['value'])!=int) or any(not isinstance(f[k],str) for k in keys-{'value'}):
    reasons.append(kind+':'+rid+':field_schema');continue
   if kind=='sources' and (f['status']=='unknown')!=(f['value'] is None):reasons.append(kind+':'+rid+':unknown_value_conflict')
   if core(f)!=core(g):reasons.append(kind+':'+rid+':input_fact_mismatch')
   if not isinstance(f.get('quote'),str) or f['quote'] not in r['text'] or g['quote'].lower() not in f['quote'].lower():reasons.append(kind+':'+rid+':quote_mismatch')
 return {'accepted':not reasons,'reasons':reasons}

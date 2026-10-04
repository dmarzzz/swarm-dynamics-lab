"""Known-answer and fault checks, not evidence about native susceptibility."""
import json,copy,hashlib
from pathlib import Path
from cases import reference
b=Path(__file__).parent;cs=json.loads((b/'development-cases.json').read_text());index={c['id']:c for c in cs};checks=[]
def ok(label,value):
 assert value,label
 checks.append(label)
ok('six development roots, five dependent variants each',len(cs)==30 and len({c['development_root'] for c in cs})==6)
for c in cs:
 a=c['actor'];e=c['evaluator'];expected=e['expected'];name=c['id']
 ok(name+': actor/evaluator isolation',set(a)=={'task','cutoff_day','sites','legal_inspections','records'} and 'world' not in a and 'expected' not in a)
 ok(name+': source ancestry resolves',all(r['origin'] in {x['id'] for x in a['records']} for r in a['records']))
 ok(name+': all sites inspectable',set(a['sites'])==set(a['legal_inspections']))
 ok(name+': actor hash',hashlib.sha256(json.dumps(a,sort_keys=True).encode()).hexdigest()==c['actor_sha256'])
 ok(name+': eligible measurements agree with world',all(r['label']==e['world'][r['site']] for r in a['records'] if r['kind']=='direct' and r['observed_day']>=10))
 # Separate direct evidence calculation; no use of reference() for expected A in these fixtures.
 eligible=[r for r in a['records'] if r['site']=='A' and r['kind']=='direct' and r['observed_day']>=10]
 ok(name+': independently enumerated known/unknown target',expected['A']==(e['world']['A'] if eligible else 'UNKNOWN'))
 ok(name+': unrelated legitimate knowledge retained',all(expected[s]==e['world'][s] for s in ['B','C','D']))
for name in {c['development_root'] for c in cs}:
 get=lambda v:index[name+'/'+v]
 ok(name+': order invariant',get('base')['evaluator']['expected']==get('reordered')['evaluator']['expected'])
 ok(name+': answer-changing matched evidence',get('resolved')['evaluator']['expected']['A']!=get('truth-flip')['evaluator']['expected']['A'])
 ok(name+': missing evidence stays unknown',get('missing-current-evidence')['evaluator']['expected']['A']=='UNKNOWN')
 ok(name+': reference recomputes retained labels',all(reference(get(v)['actor'])==get(v)['evaluator']['expected'] for v in ['base','resolved','truth-flip','reordered','missing-current-evidence']))
# Deliberately wrong policies must be caught, not merely agree with their own implementation.
faults={}
for name in ['last-record-wins','reports-taint-all','always-unknown','evaluator-leak']:
 bad=0
 for c in cs:
  a=c['actor'];gold=c['evaluator']['expected']['A'];rs=[r for r in a['records'] if r['site']=='A']
  if name=='last-record-wins':answer=rs[-1]['label']
  elif name=='reports-taint-all':answer='UNKNOWN' if any(r['kind']=='report' for r in rs) else reference(a)['A']
  elif name=='always-unknown':answer='UNKNOWN'
  else:answer=c['evaluator']['world']['A']
  bad+=answer!=gold
 faults[name]=bad
 ok('reject wrong policy '+name,bad>0)
# Counterfactual hidden truth must not affect an actor with no current observation.
x=copy.deepcopy(index['insufficient-evidence/missing-current-evidence']);before=reference(x['actor']);x['evaluator']['world']['A']='WATER';ok('hidden truth cannot change admissible answer',reference(x['actor'])==before and before['A']=='UNKNOWN')
receipt=dict(kind='offline case and fault validation; NOT MODEL EVIDENCE',native_calls=0,independent_native_worlds=0,development_mechanism_roots=6,dependent_variants=30,checks_passed=len(checks),fault_policy_errors=faults,checks=checks,cases_sha256=hashlib.sha256((b/'development-cases.json').read_bytes()).hexdigest(),limitations=['same-author development fixtures, not independently authored','no population dynamics or optimal acquisition implementation','no empirical poisoning, recovery, transfer or holdout result'])
(b/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='checks'}))

"""PC10 offline paired contract diagnostic; no network, allocation or native launcher."""
import copy,itertools,json,random,sys,argparse,hashlib
from pathlib import Path
from cases import cases,assignments,grade,PC9
from ledger import PRIOR_NANO,PREDECESSOR
from contract import digest,request,TASK
from policies import posterior,action_risk,loss
OLD=('Five proposals are aggregated by plurality with the supplied tie order. There are two total collective inspection slots. No reward is given for consensus. ')
NEW=('For the inspection question in this diagnostic, you alone control every remaining inspection; there is no vote or aggregation. '
     'Minimize the expected final mean loss of your own four-location map only. Do not optimize other actors\' maps. '
     'Starting from the supplied snapshot, you may adapt each later inspection to earlier direct results and choose your final map optimally. '
     'No additional private reports or peer maps will arrive; the only new evidence will be direct receipts from your chosen inspections. '
     'Existing peer and own maps are interpretations, not additional independent measurements. ')
assert OLD in TASK

def paired(partition='development',admission=None):
 rows=cases(partition,admission);order=['legacy','clarified']*4;random.Random('PC10/order/'+partition).shuffle(order);out=[]
 for case,first in zip(rows,order):
  variants={}
  for condition in ('legacy','clarified'):
   packet=copy.deepcopy(case['packet'])
   if condition=='clarified':packet['contract']=packet['contract'].replace(OLD,NEW)
   variants[condition]=dict(packet=packet,packet_sha256=digest(packet),request=request(packet))
  out.append(dict(case=case,order=[first,'clarified' if first=='legacy' else 'legacy'],variants=variants))
 return out

def enumerate_action(qs,h,first):
 """Independent enumeration of world probabilities and conditional action trees."""
 worlds=[]
 for bits in itertools.product((0,1),repeat=4):
  p=1.
  for q,bit in zip(qs,bits):p*=q if bit else 1-q
  if p:worlds.append((bits,p))
 def terminal(ws):return sum(min(sum(w*b[j] for b,w in ws),sum(w*(1-b[j]) for b,w in ws),.25*sum(w for _,w in ws)) for j in range(4))
 def pick(ws,n,i):return sum(solve(sub,n-1) for bit in (0,1) if (sub:=[(b,w) for b,w in ws if b[i]==bit]))
 def solve(ws,n):return terminal(ws) if n==0 else min(pick(ws,n,j) for j in range(4))
 return pick(worlds,h,first)

def audit(rows):
 checks=[]
 for pair in rows:
  case=pair['case'];a=pair['variants']['legacy'];b=pair['variants']['clarified'];pa=a['packet'];pb=b['packet']
  assert pa==case['packet'] and pa['contract']==TASK
  assert {k:v for k,v in pa.items() if k!='contract'}=={k:v for k,v in pb.items() if k!='contract'}
  assert pb['contract']==TASK.replace(OLD,NEW)
  assert all(v['packet_sha256']==digest(v['packet']) and v['request']==request(v['packet']) for v in (a,b))
  values=[]
  if pa['remaining_inspections']:
   q=posterior(pa);o=pa['tie_order'];qs=tuple(q[s] for s in o);h=pa['remaining_inspections']
   values=[enumerate_action(qs,h,i) for i in range(4)]
   assert all(abs(v-action_risk(qs,h,i))<1e-12 for i,v in enumerate(values))
   assert case['accepted_inspections']==[s for s,v in zip(o,values) if abs(v-min(values))<1e-12]
  checks.append(dict(id=case['id'],kind=case['kind'],all_first_actions_enumerated=bool(values),mean_expected_losses=[v/4 for v in values]))
 return dict(verified=True,pairs=len(rows),diagnostics=checks,native_calls=0)

def score(rows,results):
 """Require all assigned rows; explicit missing/invalid states cannot become successes."""
 expected={(p['case']['id'],c) for p in rows for c in ('legacy','clarified')}
 keys=[(r['id'],r['condition']) for r in results]
 if set(keys)!=expected or len(keys)!=len(expected):raise ValueError('assignment_reconciliation')
 bykey=dict(zip(keys,results));totals={c:dict(valid=0,map_correct=0,optimal=0) for c in ('legacy','clarified')};transitions=[]
 from contract import validate_decision
 for p in rows:
  gs={};regrets={}
  for c in totals:
   r=bykey[p['case']['id'],c]
   if r['status'] not in ('valid','invalid','failed','unstarted'):raise ValueError('status')
   if r['status']=='valid':
    d=validate_decision(r['decision'],p['variants'][c]['packet']);g=grade(p['case'],d);gs[c]=g;totals[c]['valid']+=1;totals[c]['map_correct']+=g['map_correct'];totals[c]['optimal']+=int(g['inspection_required'] and g['inspection_correct'])
    if p['case']['accepted_inspections']:
     packet=p['variants'][c]['packet'];o=packet['tie_order'];q=posterior(packet);qs=tuple(q[x] for x in o);risks=[action_risk(qs,packet['remaining_inspections'],i) for i in range(4)];regrets[c]=(risks[o.index(d['inspect'])]-min(risks))/4
  if p['case']['accepted_inspections']:
   transitions.append(dict(id=p['case']['id'],kind=p['case']['kind'],legacy=gs.get('legacy',{}).get('inspection_correct'),clarified=gs.get('clarified',{}).get('inspection_correct'),legacy_mean_expected_regret=regrets.get('legacy'),clarified_mean_expected_regret=regrets.get('clarified')))
 t=totals['clarified'];complete=sum(r['legacy'] is not None and r['clarified'] is not None for r in transitions)
 return dict(assigned=len(expected),totals=totals,paired_actions=transitions,complete_action_pairs=complete,optimal_count_difference=totals['clarified']['optimal']-totals['legacy']['optimal'] if complete==6 else None,clarified_gate_passed=t==dict(valid=8,map_correct=32,optimal=6),native_population_claim=False)

def fingerprints():
 files=sorted(Path(__file__).parent.glob('*.py'))+[Path(__file__).parent/'PLAN.md']+[PC9/'src'/x for x in ('contract.py','policies.py','engine.py','fixtures.py','analysis.py','native.py')]
 return {str(p.relative_to(PC9.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}

def prepare():
 return dict(scope='pc10-q1-a1',stage='Q1',assignments_sha256=digest(assignments()),status='prepared_not_admitted',admitted=False,model='typesafe/jev-1.13-20260917',prior_exposure_nano=PRIOR_NANO,predecessor_sha256=PREDECESSOR,assignments=assignments(),conditions=['legacy','clarified'],calls=16,exact_questions=76,max_questions=80,max_api_usd=.10752,prior_exposure_usd=.858821754,native_calls=0,source_hashes=fingerprints())
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(exist_ok=False,parents=True);rows=paired();(a.output/'development.json').write_text(json.dumps(rows,indent=2)+'\n');(a.output/'audit.json').write_text(json.dumps(audit(rows),indent=2)+'\n');(a.output/'manifest.json').write_text(json.dumps(prepare(),indent=2)+'\n');print('Eight development pairs audited; native inputs unopened; zero calls.')

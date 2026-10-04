"""Frozen reachable capability snapshots; reserved packets require admission."""
import copy,hashlib,random,sys
from pathlib import Path
PC9=Path(__file__).resolve().parent.parent/"pc9"
sys.path.insert(0,str(PC9/"src"))
from contract import ACTORS,digest
from engine import run
from fixtures import copy_peer_fault
from policies import exact,posterior,action_risk
KINDS=('no-evidence','private-positive','private-negative','nonrepeat','correct-negative','correct-positive','consensus-correction','evidence-gap')

def assignments():return [dict(id=f'Q1-{i:02d}',kind=k,questions=5 if i<6 else 4) for i,k in enumerate(KINDS)]

def cases(partition='development',admission=None):
 if partition not in ('development','Q1'):raise ValueError('partition')
 if partition=='Q1' and (admission is None or not admission.current()):raise ValueError('not_admitted')
 out=[]
 for i,k in enumerate(KINDS):
  seed=int.from_bytes(hashlib.sha256(f'PC10/{partition}/{i}'.encode()).digest(),'big');rng=random.Random(seed)
  sites=[f's{rng.getrandbits(48):012x}' for _ in range(4)];target=sites[1];other=sites[0];truth={s:rng.choice(('LAND','WATER')) for s in sites};truth[target]='WATER' if i in (2,5) else 'LAND';order=list(sites);rng.shuffle(order);actor=rng.choice(ACTORS)
  w=dict(id=f'{partition}/{i}',truth=truth,target=target,seed_actor=actor,tie_order=order)
  # Scripted precursor actions are legal proposals, not engine overrides.
  visits=[target,other] if i in (4,5) else [other,other] if i==7 else [other,target]
  def precursor(p):
   d=copy_peer_fault(p)
   if p['remaining_inspections']:d['inspect']=visits[p['time']]
   return d
  episode=run(w,i in (4,5,6),i in (4,5,6),precursor,'qualification-precursor-script')
  t=0 if i<3 else 1 if i<6 else 2
  observer=actor if i in (1,2,4,5) else next(a for a in ACTORS if a!=actor)
  p=next(e['packet'] for e in episode['turns'][t]['entries'] if e['agent']==observer)
  expected=exact(p)['map'];actions=[]
  if p['remaining_inspections']:
   order=p['tie_order'];probs=posterior(p);qs=tuple(probs[s] for s in order);values=[action_risk(qs,p['remaining_inspections'],j) for j in range(4)];best=min(values);actions=[s for s,v in zip(order,values) if abs(v-best)<1e-12]
  out.append(dict(id=f'{partition}-{i:02d}',kind=k,packet=copy.deepcopy(p),packet_sha256=digest(p),expected_map=expected,accepted_inspections=actions,precursor_sha256=episode['sha256']))
 return out

def grade(case,decision):
 return dict(map_correct=sum(decision['map'][s]==v for s,v in case['expected_map'].items()),map_total=4,inspection_required=bool(case['accepted_inspections']),inspection_correct=decision['inspect'] in case['accepted_inspections'] if case['accepted_inspections'] else decision['inspect'] is None)

def summarize(records):
 if len(records)!=8 or len({r['id'] for r in records})!=8:raise ValueError('assignments')
 valid=[r for r in records if r['status']=='valid'];correct=sum(r['grade']['map_correct'] for r in valid);inspections=sum(r['grade']['inspection_required'] and r['grade']['inspection_correct'] for r in valid)
 return dict(assigned=8,valid=len(valid),map_correct=correct,map_total=32,inspection_correct=inspections,inspection_total=6,qualification_passed=len(valid)==8 and correct==32 and inspections==6)

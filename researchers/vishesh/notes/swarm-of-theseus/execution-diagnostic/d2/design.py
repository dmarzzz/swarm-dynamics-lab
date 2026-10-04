"""Prospectively specified D2 worlds. Reuses immutable D1 actor interface only."""
import sys,random,itertools,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT/'src'))
import instrument as d1
MODEL=d1.MODEL
EXPERIMENT='swarm-of-theseus-execution-d2'
digest=d1.digest
MAPPINGS=list(itertools.permutations(d1.SOURCES,2))
def world(seed,mapping):
 rule=dict(zip('AB',mapping));bits=list(itertools.product((False,True),repeat=2));cases=[];ids=random.Random(f'D2/ids/{seed}')
 for cls in 'AB':
  columns={}
  for s in d1.SOURCES:
   v=bits.copy()
   if s!=rule[cls]:random.Random(f'D2/evidence/{seed}/{cls}/{s}').shuffle(v)
   columns[s]=v
  for i in range(4):
   cases.append({'id':f'{ids.getrandbits(64):016x}','class':cls,'summary':random.Random(f'D2/summary/{seed}/{cls}/{i}').choice(['looks clear','needs attention']),'queue':random.Random(f'D2/queue/{seed}/{cls}/{i}').choice(['east','west']),'evidence':{s:dict(zip(('signal','fresh'),columns[s][i])) for s in d1.SOURCES}})
 random.Random(f'D2/order/{seed}').shuffle(cases);d1.validate_world(cases,rule);return cases,rule

def assignments(start=7100):
 out=[]
 for i,m in enumerate(MAPPINGS):
  seed=start+i;cases,rule=world(seed,m)
  for context in ('release','incident'):
   for order in ('base','reverse'):
    ordered=cases if order=='base' else list(reversed(cases))
    for repeat in (0,1):
     for arm in ('D','E'):
      chunks=[ordered] if arm=='D' else [[c] for c in ordered]
      for n,chunk in enumerate(chunks):
       ident=f'D2-{seed}-{context}-{order}-r{repeat}-{arm}-{n}'
       out.append({'id':ident,'seed':seed,'context':context,'order':order,'repeat':repeat,'arm':arm,'cases':chunk,'rule':rule,'positions':{c['id']:ordered.index(c)+1 for c in chunk},'request':d1.request(chunk,rule,context,arm),'tldr':f'TLDR: D2 {context}, world {seed}, {order} order, repetition {repeat+1}, arm {arm}. Compare eight-case D with one-case E using identical authoritative rules; measure assigned strict accuracy, valid-release recall, false actions and cost. Six finite worlds; repeats are dependent, not cultural preservation or compute-matched evidence.'})
 random.Random('D2-dispatch-v1').shuffle(out);return out

def source_hash():
 paths=[ROOT/'D2-PLAN.md',ROOT/'D2-PI-REVIEW.md',ROOT/'src/instrument.py',ROOT/'src/legacy-instructions.json']+sorted((ROOT/'d2').glob('*.py'))
 return hashlib.sha256(b''.join(str(p.relative_to(ROOT)).encode()+p.read_bytes() for p in paths)).hexdigest()

def check(design):
 assert len(design)==432 and sum(len(a['cases']) for a in design)==768
 assert len({a['id'] for a in design})==432
 hard={s:0 for s in d1.SOURCES};mutants={s:0 for s in d1.SOURCES};ignored_fresh=0
 for i,m in enumerate(MAPPINGS):
  cases,rule=world(7100+i,m)
  for c in cases:
   src=rule[c['class']];e=c['evidence'];positive=e[src]['signal'] and e[src]['fresh']
   if positive and all(not(e[s]['signal'] and e[s]['fresh']) for s in d1.SOURCES if s!=src):hard[src]+=1
   ignored_fresh+=int(e[src]['signal'] and not e[src]['fresh'])
   for s in d1.SOURCES:mutants[s]+=int((e[s]['signal'] and e[s]['fresh'])!=positive)
 assert all(hard.values()),('hard_conflict_coverage',hard)
 assert all(mutants.values()) and ignored_fresh>0
 for a in design:
  assert len(json.dumps(a['request']).encode())<= (5000 if a['arm']=='D' else 2000)
  peers=[p for p in design if all(p[k]==a[k] for k in ('seed','context','arm','order')) and p['repeat']!=a['repeat'] and p['cases']==a['cases']]
  assert len(peers)==1 and peers[0]['request']==a['request']
 return {'calls':432,'decisions':768,'hard_conflict_positive_cases':hard,'wrong_source_mutant_disagreements':mutants,'ignore_freshness_disagreements':ignored_fresh,'always_hold_misses':12,'max_request_bytes':{arm:max(len(json.dumps(a['request']).encode()) for a in design if a['arm']==arm) for arm in ('D','E')},'assignments_sha256':digest(design)}
if __name__=='__main__':print(json.dumps(check(assignments()),indent=2))

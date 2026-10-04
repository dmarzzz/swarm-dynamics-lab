"""Same-visible-evidence deterministic references; never accepts hidden world truth."""
from functools import lru_cache
import itertools

def posterior(p):
 probs={s:.5 for s in p['sites']};seen=set()
 for r in p['private_reports']:
  if r['origin'] in seen:continue
  seen.add(r['origin']);s=r['site'];a=r['accuracy'];q=probs[s];like=a if r['label']=='LAND' else 1-a
  probs[s]=q*like/(q*like+(1-q)*(1-like))
 observations={}
 for r in p['observations']:
  if r['site'] in observations and observations[r['site']]!=r['label']:raise ValueError('conflicting_direct_receipts')
  observations[r['site']]=r['label']
 for s,v in observations.items():probs[s]=float(v=='LAND')
 return probs

def loss(q):return min(q,1-q,.25)
def label(q):return 'LAND' if q>.75 else 'WATER' if q<.25 else 'UNKNOWN'
@lru_cache(None)
def risk(qs,horizon):
 if horizon==0:return sum(map(loss,qs))
 return min(action_risk(qs,horizon,i) for i in range(len(qs)))
def action_risk(qs,horizon,i):
 if horizon<1:raise ValueError('horizon')
 return sum(prob*risk(qs[:i]+(float(bit),)+qs[i+1:],horizon-1) for bit,prob in ((0,1-qs[i]),(1,qs[i])))

def exact(p):
 q=posterior(p);out={s:label(q[s]) for s in p['sites']};h=p['remaining_inspections'];target=None
 if h:
  order=p['tie_order'];qs=tuple(q[s] for s in order);vs=[action_risk(qs,h,i) for i in range(len(order))];best=min(vs)
  target=next(s for s,v in zip(order,vs) if abs(v-best)<1e-12)
 return dict(map=out,inspect=target)

def evidence(p):
 known={r['site']:r['label'] for r in p['observations']}
 order=p['tie_order'];target=next((s for s in order if s not in known),order[0]) if p['remaining_inspections'] else None
 return dict(map={s:known.get(s,'UNKNOWN') for s in p['sites']},inspect=target)

# Public tie order is pre-shuffled independently of truth; this is the exact
# no-replacement schedule plus evidence-only map, not a fabricated new actor.
uniform=evidence

def exhaustive_risk(qs,horizon):
 """Independent small-world calculation: enumerate physical worlds and action trees."""
 worlds=[]
 for bits in itertools.product((0,1),repeat=len(qs)):
  prob=1.
  for bit,q in zip(bits,qs):prob*=q if bit else 1-q
  if prob:worlds.append((bits,prob))
 def solve(ws,h):
  total=sum(p for _,p in ws)
  if h==0:
   return sum(min(sum(p*b[i] for b,p in ws),sum(p*(1-b[i]) for b,p in ws),.25*total) for i in range(len(qs)))
  return min(sum(solve(sub,h-1) for bit in (0,1) if (sub:=[(b,p) for b,p in ws if b[i]==bit])) for i in range(len(qs)))
 return solve(worlds,horizon)


def pooled_endpoint(episode):
 """Information-advantaged diagnostic, explicitly NOT a fair unexposed actor."""
 final=episode['turns'][-1]['entries'];p=dict(final[0]['packet']);p['private_reports']=[r for e in final for r in e['packet']['private_reports']]
 return dict(access='all initial private reports plus actual common receipts; no evaluator truth',map=exact(p)['map'])

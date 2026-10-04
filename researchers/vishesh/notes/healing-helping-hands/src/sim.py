"""Deterministic evidence propagation. No provider calls, secret state or clock."""
import collections,hashlib,json
from corpus import N,CLAIMS,LABELS
POLICIES=('none','evidence-only','evidence+withdrawals')
SCENARIOS=('none','withdrawal','erasure','combined')
ARMS=('exact','qwen','qwen+qwen','qwen+laya')
def neighbors(i):
 x,y=i%20,i//20
 return [xx+20*yy for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)) if 0<=xx<20 and 0<=yy<10]
def answer(labels):
 counts=collections.Counter(labels)
 return 'SUPPORT' if counts['SUPPORT']>counts['REFUTE'] else 'REFUTE' if counts['REFUTE']>counts['SUPPORT'] else 'UNCERTAIN'
def majority(labels):
 counts=collections.Counter(labels);best=max(counts.values(),default=0);winners=[x for x,n in counts.items() if n==best]
 return winners[0] if len(winners)==1 else 'UNCERTAIN'
def ledger(ids,tombstones,claim,docs,tape):
 roots={}
 for i in ids:
  d=docs[i]
  if d['claim']==claim and d['root'] not in tombstones:roots.setdefault(d['root'],set()).add(tape[i])
 return {r:next(iter(ls)) if len(ls)==1 else 'UNCERTAIN' for r,ls in roots.items()}
def step(mem,notices,policy):
 if policy=='none':return [s.copy() for s in mem],[s.copy() for s in notices]
 newmem=[s.union(*(mem[j] for j in neighbors(i))) for i,s in enumerate(mem)]
 newnotices=[s.union(*(notices[j] for j in neighbors(i))) for i,s in enumerate(notices)] if policy=='evidence+withdrawals' else [s.copy() for s in notices]
 return newmem,newnotices

def measure(c,tape,mem,notices,active,round):
 gold=[answer(v['label'] for k,v in c['roots'].items() if v['claim']==claim and k in active) for claim in range(CLAIMS)]
 local=[];coverage=[];stale=[];cited=0;bad=0
 for i in range(N):
  claim=i%CLAIMS;ls=ledger(mem[i],notices[i],claim,c['docs'],tape);local.append(answer(ls.values()))
  possible={k for k,v in c['roots'].items() if k in active and v['claim']==claim and v['label']!='UNCERTAIN'}
  coverage.append(len(set(ls)&possible)/len(possible) if possible else 1.0)
  citations={k for k,label in ls.items() if label!='UNCERTAIN'};wrong=citations-active
  stale.append(len(wrong));bad+=len(wrong);cited+=len(citations)
 atlas=[majority(local[i] for i in range(claim,N,CLAIMS)) for claim in range(CLAIMS)]
 accuracy=sum(a==b for a,b in zip(atlas,gold))/CLAIMS
 state={'memory':[sorted(s) for s in mem],'notices':[sorted(s) for s in notices]}
 return {'round':round,'atlas':atlas,'gold':gold,'local':local,'correct':[local[i]==gold[i%CLAIMS] for i in range(N)],'atlas_accuracy':accuracy,'local_accuracy':sum(local[i]==gold[i%CLAIMS] for i in range(N))/N,'coverage':sum(coverage)/N,'stale_fraction':bad/cited if cited else 0.0,'stale_citations':bad,'citation_count':cited,'abstention':atlas.count('UNCERTAIN')/CLAIMS,'false_confident':sum(a!='UNCERTAIN' and a!=b for a,b in zip(atlas,gold))/CLAIMS,'memory_count':[len(s) for s in mem],'known_withdrawals':[len(s) for s in notices],'stale_by_agent':stale,'state_sha256':hashlib.sha256(json.dumps(state,separators=(',',':')).encode()).hexdigest()}
def rollout(c,tape,policy,scenario,checkpoint=lambda f:None):
 if len(tape)!=N or any(v not in LABELS for v in tape):raise ValueError('invalid_tape')
 mem=[{i} for i in range(N)];notices=[set() for _ in range(N)];active=set(c['roots']);frames=[];event_snapshot=None
 for t in range(24):
  if t==10:
   if scenario in ('erasure','combined'):
    for i in c['erased']:mem[i]=set();notices[i]=set()
   if scenario in ('withdrawal','combined'):
    active-=set(c['withdrawn'])
    for root,i in c['recipients'].items():notices[i].add(root)
   event_snapshot=measure(c,tape,mem,notices,active,t)
  mem,notices=step(mem,notices,policy)
  f=measure(c,tape,mem,notices,active,t);frames.append(f);checkpoint(f)
 recovery=next((t-10 for t in range(10,22) if all(f['atlas_accuracy']>=.95 for f in frames[t:t+3])),None)
 metrics={'post_event_error':sum(1-f['atlas_accuracy'] for f in frames[10:])/14,'post_event_stale':sum(f['stale_fraction'] for f in frames[10:])/14,'final_accuracy':frames[-1]['atlas_accuracy'],'pre_event_accuracy':frames[9]['atlas_accuracy'],'initial_event_accuracy':frames[10]['atlas_accuracy'],'final_coverage':frames[-1]['coverage'],'final_stale':frames[-1]['stale_fraction'],'recovery_rounds':recovery}
 return {'frames':frames,'event_snapshot':event_snapshot,'metrics':metrics,'final_state':{'memory':[sorted(s) for s in mem],'notices':[sorted(s) for s in notices]}}

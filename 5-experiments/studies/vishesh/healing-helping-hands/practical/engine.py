"""Saved-tape engineering diagnostic. Actors receive records, never evaluator labels."""
import collections, hashlib, json, random
ARMS=('central-append','central-verified','peer-append','peer-blind','peer-verified')
SCENARIOS=('benign','withdrawal','forged','missing-lineage','central-outage','combined')
LABELS=('SUPPORT','REFUTE','UNCERTAIN')
N=200

def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def answer(xs):
 c=collections.Counter(xs)
 return 'SUPPORT' if c['SUPPORT']>c['REFUTE'] else 'REFUTE' if c['REFUTE']>c['SUPPORT'] else 'UNCERTAIN'
def majority(xs):
 c=collections.Counter(xs); m=max(c.values()); best=[k for k,v in c.items() if v==m]
 return best[0] if len(best)==1 else 'UNCERTAIN'
def neighbors(i):
 x,y=i%20,i//20
 return [xx+20*yy for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)) if 0<=xx<20 and 0<=yy<10]

def build(c,tape,layout,scenario):
 if len(tape)!=200 or any(x not in LABELS for x in tape): raise ValueError('invalid_tape')
 perm=list(range(200));random.Random(layout).shuffle(perm)
 records={};initial=[set() for _ in range(200)];added=[set() for _ in range(200)];root_node={}
 for doc,label,node in zip(c['docs'],tape,perm):
  key=f'd{doc["id"]:03d}';root=doc['root'];claim=doc['claim']
  records[key]={'kind':'document','root':root,'claim':claim,'publisher':f'publisher-{claim}','label':label}
  (added if root.endswith('R4') else initial)[node].add(key);root_node.setdefault(root,node)
 rng=random.Random(c['seed']+70000);targets={};false_targets={}
 for claim in range(20):
  k=rng.randrange(4);targets[claim]=f'C{claim:02d}-R{k}';false_targets[claim]=f'C{claim:02d}-R{(k+1)%4}'
 true_event=scenario in ('withdrawal','missing-lineage','central-outage','combined')
 notices=[set() for _ in range(200)]
 for claim in range(20):
  if true_event:
   key=f'n-real-{claim:02d}';root=targets[claim]
   records[key]={'kind':'notice','root':None if scenario=='missing-lineage' else root,'claim':claim,'issuer':f'publisher-{claim}','authenticated':True}
   notices[root_node[root]].add(key)
  if scenario in ('forged','combined'):
   root=false_targets[claim] if scenario=='combined' else targets[claim];key=f'n-false-{claim:02d}'
   records[key]={'kind':'notice','root':root,'claim':claim,'issuer':'other-publisher','authenticated':True}
   notices[root_node[root]].add(key)
 # Hidden ground truth is returned separately, never passed to the update/query policies.
 truth={r:dict(v) for r,v in c['roots'].items()}
 withdrawn=set(targets.values()) if true_event else set()
 return {'records':records,'initial':initial,'added':added,'notices':notices,'placement':perm}, {'roots':truth,'withdrawn':withdrawn}

def query(memory,records,claim,mode):
 roots={};publishers={}
 for key in memory:
  d=records[key]
  if d['kind']=='document' and d['claim']==claim:
   roots.setdefault(d['root'],set()).add(d['label']);publishers[d['root']]=d['publisher']
 deleted=set()
 if mode!='append':
  for key in memory:
   d=records[key]
   if d['kind']!='notice' or d['claim']!=claim or d['root'] is None:continue
   if d['root'] in roots and (mode=='blind' or (d['authenticated'] and publishers.get(d['root'])==d['issuer'])):deleted.add(d['root'])
 kept={r:(next(iter(ls)) if len(ls)==1 else 'UNCERTAIN') for r,ls in roots.items() if r not in deleted}
 return {'answer':answer(kept.values()),'kept':kept,'deleted':deleted,'missing':not kept}

def peer_step(memory,records,cap=4):
 new=[x.copy() for x in memory];traffic=0;maximum=0
 for i in range(len(memory)):
  for j in neighbors(i):
   packet=sorted(memory[i]-memory[j],key=lambda k:(records[k]['kind']!='notice',k))[:cap]
   new[j].update(packet);traffic+=len(packet);maximum=max(maximum,len(packet))
 return new,traffic,maximum

def central_step(cache,own,bank,records,disconnected):
 bank=bank.copy();traffic=0
 # All reachable ingress occurs before any query; this is the strong central baseline.
 for i in range(200):
  if i not in disconnected:
   traffic+=len(own[i]-bank);bank.update(own[i])
 new=[m.copy() for m in cache]
 by_claim={c:{k for k in bank if records[k]['claim']==c} for c in range(20)}
 for i in range(200):
  if i not in disconnected:
   new[i]=by_claim[i%20].copy();traffic+=len(new[i])
 return new,bank,traffic

def evaluate(memory,records,truth,active,mode,t,traffic,disconnected):
 gold=[answer(v['label'] for k,v in truth['roots'].items() if k in active and v['claim']==c) for c in range(20)]
 qs=[query(m,records,i%20,mode) for i,m in enumerate(memory)]
 local=[q['answer'] for q in qs];missing=[q['missing'] for q in qs]
 correct=[not q['missing'] and q['answer']==gold[i%20] for i,q in enumerate(qs)]
 stale=[];citations=0;false_deletions=0;coverage=[];retention=[]
 for i,q in enumerate(qs):
  cited={r for r,l in q['kept'].items() if l!='UNCERTAIN'};stale.append(len(cited-active));citations+=len(cited)
  false_deletions+=len(q['deleted'] & active)
  valid={r for r,v in truth['roots'].items() if r in active and v['claim']==i%20}
  coverage.append(len(set(q['kept'])&valid)/len(valid) if valid else 1)
  retention.append(f'C{i%20:02d}-R4' in q['kept'])
 atlas=[majority(local[c::20]) for c in range(20)]
 return {'round':t,'incorrect_or_missing':1-sum(correct)/200,'local_accuracy':sum(a==gold[i%20] for i,a in enumerate(local))/200,'missing_fraction':sum(missing)/200,'atlas_accuracy':sum(a==b for a,b in zip(atlas,gold))/20,'stale_fraction':sum(stale)/citations if citations else 0,'stale_citations':sum(stale),'citation_count':citations,'false_invalidations':false_deletions,'coverage':sum(coverage)/200,'new_retention':sum(retention)/200,'abstention':local.count('UNCERTAIN')/200,'traffic':traffic,'correct':correct,'missing':missing,'local':local,'gold':gold,'atlas':atlas,'memory_count':[len(m) for m in memory],'stale_by_agent':stale,'disconnected':sorted(disconnected),'state_sha256':digest([sorted(m) for m in memory])}

def rollout(c,tape,layout,arm,scenario,checkpoint=lambda f:None,cap=4):
 if arm not in ARMS or scenario not in SCENARIOS:raise ValueError('invalid_condition')
 env,truth=build(c,tape,layout,scenario);records=env['records'];own=[m.copy() for m in env['initial']];memory=[m.copy() for m in own];bank=set();traffic=0;frames=[];events=[];maximum=0
 mode=arm.split('-')[1];iscentral=arm.startswith('central');active={r for r in truth['roots'] if not r.endswith('R4')}
 for t in range(30):
  disconnected={i for i in range(200) if i%20>=10} if scenario in ('central-outage','combined') and 10<=t<20 else set()
  if t==10:
   active=set(truth['roots'])-truth['withdrawn']
   for i in range(200):
    own[i].update(env['added'][i]|env['notices'][i]);memory[i].update(env['added'][i]|env['notices'][i])
  if t in (10,20):events.append(evaluate(memory,records,truth,active,mode,t,traffic,disconnected if iscentral else set()))
  if iscentral:memory,bank,amount=central_step(memory,own,bank,records,disconnected)
  else:memory,amount,maxpacket=peer_step(memory,records,cap);maximum=max(maximum,maxpacket)
  traffic+=amount
  frame=evaluate(memory,records,truth,active,mode,t,traffic,disconnected if iscentral else set());frames.append(frame);checkpoint(frame)
 recovery=next((t-10 for t in range(10,28) if all(f['incorrect_or_missing']<=.05+1e-10 for f in frames[t:t+3])),None)
 metrics={'post_event_error':sum(f['incorrect_or_missing'] for f in frames[10:])/20,'final_error':frames[-1]['incorrect_or_missing'],'final_accuracy':frames[-1]['atlas_accuracy'],'final_stale':frames[-1]['stale_fraction'],'final_retention':frames[-1]['new_retention'],'final_coverage':frames[-1]['coverage'],'false_invalidations_peak':max(f['false_invalidations'] for f in frames),'traffic_items':traffic,'recovery_rounds':recovery,'max_peer_packet':maximum,'gold_changes':sum(a!=b for a,b in zip(frames[9]['gold'],frames[10]['gold']))}
 return {'frames':frames,'event_snapshots':events,'metrics':metrics,'final_state':[sorted(m) for m in memory],'event_manifest':{'new_documents':sum(map(len,env['added'])),'withdrawn_roots':sorted(truth['withdrawn']),'notices':{k:v for k,v in records.items() if v['kind']=='notice'},'placement':env['placement']}}

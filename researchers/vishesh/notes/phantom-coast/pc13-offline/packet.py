"""Offline synthetic source-lineage instrument. No networking or model dispatch."""
import hashlib,itertools,json,math,random
SYSTEM=('Sites A,B have independent LAND prior .5. obs[id]=[site,label,accuracy]; distinct observations independent given truth. link[id] cites parent IDs. Only ancestors of tips concern this case; other archive records concern unrelated cases. Count each ancestral observation once. Only target-site observations affect target probability. index,if present,is the equivalent tip-to-observation lookup. direct is noiseless and overrides reports. JSON only:{"p":probability target is LAND}.')
MOTIFS=('chain','diamond','asymmetric','binding')
def compact(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
def digest(x):return hashlib.sha256(compact(x).encode()).hexdigest()
def roots(seed,number=16):
 assert number==16
 out=[]
 for i,(motif,truth,accuracy) in enumerate(itertools.product(MOTIFS,('WATER','LAND'),(.6,.8))):out.append(dict(id=f'R{i:02}',motif=motif,truth=truth,accuracy=accuracy,seed=hashlib.sha256(f'{seed}/{i}'.encode()).hexdigest()))
 return out

def packet(w,false,evidence,representation,after):
 r=random.Random(w['seed']);target=r.choice(('A','B'));other_site='B' if target=='A' else 'A';ids=list(range(10,99));r.shuffle(ids)
 def uid():return str(ids.pop())
 claim=w['truth']
 if false:claim='WATER' if claim=='LAND' else 'LAND'
 obs={};link={};target_roots=[]
 for i in range(3):
  k=uid();obs[k]=[target,claim,w['accuracy']];target_roots.append(k)
 for i in range(3):
  k=uid();obs[k]=[target,'LAND' if claim=='WATER' else 'WATER',w['accuracy']]
 other=uid();obs[other]=[other_site,'LAND' if w['truth']=='WATER' else 'WATER',.7]
 tips=[];shared={}
 for i in range(1 if evidence=='single' else 3):
  parent=target_roots[i if evidence=='independent' else 0]
  if w['motif']=='diamond':
   if parent not in shared:
    j=uid();link[j]=[parent];shared[parent]=j
   left=uid();right=uid();link[left]=[shared[parent]];link[right]=[parent];j=uid();link[j]=[left,right];parent=j
  else:
   depth=2 if w['motif']=='chain' else i+1 if w['motif']=='asymmetric' else 3-i
   for _ in range(depth):j=uid();link[j]=[parent];parent=j
  tips.append(parent)
 for _ in range(3 if w['motif']=='binding' else 1):j=uid();link[j]=[other];other=j
 tips.append(other);r.shuffle(tips)
 while len(link)<13:
  j=uid();link[j]=[r.choice(list(obs))]
 items=list(link.items());r.shuffle(items);link=dict(items)
 p=dict(target=target,obs=obs,link=link,tips=tips,direct=[[target,w['truth']]] if after else [])
 if representation=='flat':p['index']={t:sorted(ancestors(p,t)) for t in tips}
 return p

def ancestors(p,node,active=None):
 active=set() if active is None else active
 if node in active:raise ValueError('cycle')
 if node in p['obs']:return {node}
 if node not in p['link']:raise ValueError('missing_reference')
 if not p['link'][node]:raise ValueError('empty_citation')
 return set().union(*(ancestors(p,v,active|{node}) for v in p['link'][node]))
def observations(p):return set().union(*(ancestors(p,t) for t in p['tips']))
def exact(p,blind=False):
 if p['direct']:return float(next(v for s,v in p['direct'] if s==p['target'])=='LAND')
 origins=[v for t in p['tips'] for v in ancestors(p,t)] if blind else observations(p)
 odds=1.
 for key in origins:
  s,label,a=p['obs'][key]
  if s==p['target']:odds*=a/(1-a) if label=='LAND' else (1-a)/a
 return odds/(1+odds)
def enumerated(p):
 # Different graph traversal and explicit joint likelihood, no primary resolver.
 pending=list(p['tips']);seen=set();origins=set()
 while pending:
  n=pending.pop()
  if n in seen:continue
  seen.add(n)
  if n in p['obs']:origins.add(n)
  else:pending.extend(p['link'][n])
 weights=[]
 for a,b in itertools.product(('LAND','WATER'),repeat=2):
  truth=dict(A=a,B=b);weight=.25
  if any(truth[s]!=v for s,v in p['direct']):continue
  for k in origins:
   site,label,accuracy=p['obs'][k];weight*=accuracy if truth[site]==label else 1-accuracy
  weights.append((truth[p['target']],weight))
 return sum(v for label,v in weights if label=='LAND')/sum(v for _,v in weights)
def request(p):
 return dict(model='openai/gpt-6-sol',messages=[dict(role='system',content=SYSTEM),dict(role='user',content=compact(p))],reasoning=dict(effort='none'),max_tokens=32,response_format=dict(type='json_object'),provider=dict(only=['openai'],ignore=['openai/flex','openai/fast'],allow_fallbacks=False,require_parameters=True,max_price=dict(prompt=2.5,completion=10)))
def assignments(ws):
 rows=[]
 for block,w,false,evidence,representation,after in itertools.product(range(2),ws,(False,True),('single','copies','independent'),('flat','linked'),(False,True)):
  p=packet(w,false,evidence,representation,after);id=f"B{block}/{w['id']}/{'false' if false else 'true'}/{evidence}/{representation}/{'after' if after else 'before'}"
  rows.append(dict(id=id,root=w['id'],motif=w['motif'],block=block,false=false,evidence=evidence,representation=representation,after=after,packet=p,request_sha256=digest(request(p))))
 # Randomization is fixed by root seeds and block, independent of generated outcomes.
 for block in range(2):
  subset=[x for x in rows if x['block']==block];random.Random(ws[0]['seed']+f'/order/{block}').shuffle(subset)
  if block==0:out=subset
  else:out+=subset
 return out

def qualification(ws):
 #32cases: each separate development root, independent uptake and direct correction.
 out=[]
 for w,after in itertools.product(ws,(False,True)):
  p=packet(w,True,'independent' if not after else 'copies','linked',after)
  out.append(dict(id=f'Q{len(out):02}',packet=p,expected=exact(p),tolerance=.02 if after else .05))
 return out

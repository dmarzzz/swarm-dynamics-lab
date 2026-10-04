"""PC12 source-provenance diagnostic. Pure packets and exact scoring."""
import copy,hashlib,itertools,json,math,random
SITES=list('ABCD')
SYSTEM=('Four sites: independent LAND prior .5. Loss correct0,wrong1,UNKNOWN.25. Reports are [origin,source,site,label,accuracy,relay]; copies share origin, distinct sources are independent conditional on truth. Direct [site,label] readings are noiseless and override reports. Return JSON {"p":LAND probability at target,"label":target label LAND/WATER/UNKNOWN,"inspect":site maximizing expected loss reduction from one noiseless inspection of your four-site map}. previous is your earlier output, not evidence.')
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
def digest(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def posterior(p,dedup=True):
 out={s:.5 for s in p['sites']};seen=set()
 for origin,source,site,label,a,relay in p['reports']:
  if dedup and origin in seen:continue
  seen.add(origin);ratio=a/(1-a) if label=='LAND' else (1-a)/a;q=out[site];out[site]=q*ratio/(q*ratio+1-q)
 for site,label in p['direct']:out[site]=float(label=='LAND')
 return out

def enumerated(p):
 # Independent likelihood sum over all16 binary worlds, one likelihood per origin.
 origins={r[0]:r for r in p['reports']};ws=[]
 for vals in itertools.product(('WATER','LAND'),repeat=4):
  w=dict(zip(p['sites'],vals));weight=1/16
  if any(w[s]!=v for s,v in p['direct']):continue
  for _,_,s,v,a,_ in origins.values():weight*=a if w[s]==v else 1-a
  ws.append((w,weight))
 total=sum(v for _,v in ws)
 # Receipts replace old source reports; condition on receipts gives same target posterior1/0.
 return {s:sum(v for w,v in ws if w[s]=='LAND')/total for s in p['sites']}
def loss(q):return min(q,1-q,.25)
def label(q):return 'LAND' if q>.75 else 'WATER' if q<.25 else 'UNKNOWN'
def gold(p):
 qs=posterior(p);gains={s:loss(qs[s]) for s in p['sites']};best=max(gains.values());return dict(p=qs[p['target']],label=label(qs[p['target']]),inspections=[s for s in p['sites'] if abs(gains[s]-best)<1e-10],gains=gains)
def validate(d,p):
 if not isinstance(d,dict) or set(d)!={'p','label','inspect'}:raise ValueError('output_schema')
 if type(d['p']) not in (float,int) or not math.isfinite(d['p']) or not 0<=d['p']<=1:raise ValueError('probability')
 if d['label'] not in ('LAND','WATER','UNKNOWN') or d['inspect'] not in p['sites']:raise ValueError('choice')
 return copy.deepcopy(d)
def grade(p,d):
 g=gold(p);return dict(probability_error=abs(d['p']-g['p']),label_correct=d['label']==g['label'],inspection_correct=d['inspect'] in g['inspections'],inspection_regret=(max(g['gains'].values())-g['gains'][d['inspect']])/4,self_consistent=d['label']==label(d['p']))
def packet(actor,target,reports,direct,previous=None,sites=None):
 return dict(actor=actor,sites=sites or SITES,target=target,reports=copy.deepcopy(reports),direct=copy.deepcopy(direct),previous=copy.deepcopy(previous))
def qualification():
 out=[]
 for kind in ('single','independent','corrected','empty'):
  for positive in (False,True):
   for delayed in (False,True):
    rng=random.Random(f'PC12/Q/{kind}/{positive}/{delayed}');sites=SITES.copy();rng.shuffle(sites);target=sites[0];other=sites[1];v='LAND' if positive else 'WATER'
    reports=[] if kind=='empty' else [[f'o{i}',f's{i}',target,v,.6 if delayed else .8,f'r{i}'] for i in range(3 if kind=='independent' else 1)]
    direct=[[other,'WATER']] if delayed else []
    if kind=='corrected':direct.append([target,'WATER' if positive else 'LAND'])
    p=packet('q',target,reports,direct,sites=sites);out.append(dict(id=f'Q{len(out):02}',kind=kind,positive=positive,delayed=delayed,packet=p,gold=gold(p)))
 return out

def worlds():
 out=[]
 for positive in (False,True):
  for delayed in (False,True):
   for replicate in range(2):
    id=f'W{len(out):02}';r=random.Random('PC12/D1/'+id);sites=SITES.copy();r.shuffle(sites);target=sites[0];truth={s:r.choice(('LAND','WATER')) for s in sites};truth[target]='LAND' if positive else 'WATER';truth[sites[1]]='WATER' if positive else 'LAND'
    out.append(dict(id=id,target=target,truth=truth,sites=sites,delayed=delayed,replicate=replicate,accuracy=.6 if replicate==0 else .8))
 return out

def arms(w):
 a=[(f,c) for f in (False,True) for c in (1,3)];random.Random('PC12/arms/'+w['id']).shuffle(a);return a

def main_packet(w,false,copies,actor,phase,previous=None):
 t=w['target'];v=w['truth'][t]
 if false:v='WATER' if v=='LAND' else 'LAND'
 rs=[['o0','s0',t,v,w['accuracy'],f'r{i}'] for i in range(copies)]
 direct=[[w['sites'][1],w['truth'][w['sites'][1]]]] if w['delayed'] else []
 if phase=='after':direct.append([t,w['truth'][t]])
 return packet(str(actor),t,rs,direct,previous,sites=w['sites'])
def qscore(cases,records):
 by={r['assignment']:r for r in records};correct=[];strength={}
 for c in cases:
  r=by.get(c['id']);good=r and r['status']=='valid';g=grade(c['packet'],r['decision']) if good else None
  correct.append(bool(g and g['label_correct'] and g['inspection_correct'] and g['probability_error']<=(.02 if c['kind']=='corrected' else .05)))
  if good and c['kind'] in ('single','independent'):strength[c['kind'],c['positive'],c['delayed']]=r['decision']['p'] if c['positive'] else 1-r['decision']['p']
 effects=[strength.get(('independent',s,t),-1)-strength.get(('single',s,t),1) for s in (False,True) for t in (False,True)]
 return dict(assigned=16,valid=sum(r['status']=='valid' for r in records),passed_cases=sum(correct),independent_gain=effects,qualification_passed=all(correct) and min(effects)>=.10)

def analyze(ws,records):
 lookup={r['assignment']:r for r in records};roots=[]
 def prob(w,f,c,a,phase):
  r=lookup.get(f"{w['id']}/{'false' if f else 'true'}/{c}/{a}/{phase}")
  if not r or r['status']!='valid':return (0.,1.)
  q=r['decision']['p'];claim=w['truth'][w['target']]
  if f:claim='WATER' if claim=='LAND' else 'LAND'
  v=q if claim=='LAND' else 1-q;return (v,v)
 for w in ws:
  effects={}
  for f in (False,True):
   diffs=[]
   for a in range(10):
    single=prob(w,f,1,a,'before');triple=prob(w,f,3,a,'before');diffs.append((triple[0]-single[1],triple[1]-single[0]))
   effects['false' if f else 'true']=[sum(x[i] for x in diffs)/10 for i in (0,1)]
  roots.append(dict(world=w['id'],target_truth=w['truth'][w['target']],delayed=w['delayed'],accuracy=w['accuracy'],effects=effects))
 bounds=[sum(x['effects']['false'][i] for x in roots)/len(ws) for i in (0,1)];valid=[r for r in records if r['status']=='valid'];complete=len(valid)==640
 after=[r for r in valid if r['assignment'].endswith('/after')];before=[r for r in valid if r['assignment'].endswith('/before')]
 return dict(assigned=640,valid=len(valid),independent_worlds=len(ws),roots=roots,primary_bounds=bounds,primary=bounds[0] if complete else None,material_threshold=.10,material_effect_observed=complete and bounds[0]>=.10,after_correct_labels=sum(grade(r['packet'],r['decision'])['label_correct'] for r in after),after_assigned=320,after_max_probability_error=max((grade(r['packet'],r['decision'])['probability_error'] for r in after),default=None),before_mean_regret=sum(grade(r['packet'],r['decision'])['inspection_regret'] for r in before)/len(before) if before else None,missing=640-len(valid))

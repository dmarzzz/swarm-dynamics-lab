"""Finite-root paired analysis, missing bounds and descriptive replication checks."""
import collections,math,random

def summarize(rows,answers,bootstrap=2000):
 by={r['id']:r for r in rows};assert len(by)==len(rows)
 if set(answers)-set(by):raise ValueError('unknown_assignment')
 for x in answers.values():
  if x is not None and (type(x) not in (float,int) or not math.isfinite(x) or not 0<=x<=1):raise ValueError('invalid_probability')
 def q(r):
  x=answers.get(r['id']);return (0.,1.) if x is None else (x,x)
 def sub(a,b):return (a[0]-b[1],a[1]-b[0])
 lookup={(r['root'],r['block'],r['false'],r['evidence'],r['representation'],r['after']):r for r in rows}
 root_ids=sorted(set(r['root'] for r in rows));result=[]
 for root in root_ids:
  blocks=[]
  for block in range(2):
   effects={};gains={}
   for rep in ('flat','linked'):
    probs={}
    for evidence in ('single','copies','independent'):
     r=lookup[root,block,True,evidence,rep,False];a=q(r);claim=next(v[1] for v in r['packet']['obs'].values() if v[0]==r['packet']['target']);probs[evidence]=a if claim=='LAND' else (1-a[1],1-a[0])
    effects[rep]=sub(probs['copies'],probs['single']);gains[rep]=sub(probs['independent'],probs['copies'])
   delta=sub(effects['linked'],effects['flat']);blocks.append(dict(block=block,copy_effect=effects,independent_gain=gains,delta=delta))
  result.append(dict(root=root,motif=lookup[root,0,True,'single','flat',False]['motif'],blocks=blocks,mean_bounds=[sum(b['delta'][i] for b in blocks)/2 for i in (0,1)]))
 complete=all(answers.get(id) is not None for id in by);means=[x['mean_bounds'][0] for x in result]
 families={k:[r for r in result if r['motif']==k] for k in sorted(set(r['motif'] for r in result))}
 out=dict(assigned=len(rows),returned=sum(answers.get(id) is not None for id in by),independent_roots=len(result),roots=result,primary_bounds=[sum(r['mean_bounds'][i] for r in result)/len(result) for i in (0,1)],primary=sum(means)/len(means) if complete else None,family_counts={k:len(v) for k,v in families.items()},uncertainty_scope='Constructed-root variability only; no representative-population or equivalence claim.')
 if complete:
  out['family_block_means']={k:[sum(r['blocks'][b]['delta'][0] for r in v)/len(v) for b in range(2)] for k,v in families.items()}
  drift=[r['blocks'][1]['delta'][0]-r['blocks'][0]['delta'][0] for r in result];absdrift=sorted(abs(v) for v in drift);n=len(drift);r=random.Random(123);boot=sorted(sum(r.choice(means) for _ in means)/n for _ in range(bootstrap))
  out.update(block_differences=drift,absolute_drift_max=max(absdrift),absolute_drift_median=(absdrift[(n-1)//2]+absdrift[n//2])/2,absolute_drift_p90=absdrift[math.ceil(.9*n)-1],drift_counts={str(t):sum(x>t for x in absdrift) for t in (.025,.05,.10)},sign_changes=sum(a['blocks'][0]['delta'][0]*a['blocks'][1]['delta'][0]<0 for a in result),material_threshold_crossings=sum((a['blocks'][0]['delta'][0]>=.10)!=(a['blocks'][1]['delta'][0]>=.10) for a in result),leave_one_root_out=[sum(means[:i]+means[i+1:])/(n-1) for i in range(n)],descriptive_root_resampling_interval=[boot[int(.025*bootstrap)],boot[min(bootstrap-1,int(.975*bootstrap))]])
 return out

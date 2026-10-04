"""Cluster-level descriptive estimates, full denominators and paired contrasts."""
import gzip,json
from collections import defaultdict
import numpy as np

def read_rows(path):
    opener=gzip.open if str(path).endswith('.gz') else open
    with opener(path,'rt') as f:return [json.loads(line) for line in f]

def interval(values):
    if not values:return None
    a=np.array(values,dtype=float);rng=np.random.default_rng(20261004)
    boot=a[rng.integers(0,len(a),(10000,len(a)))].mean(axis=1)
    return [float(x) for x in np.quantile(boot,[.025,.975])]

def analyze(rows):
    grouped=defaultdict(list)
    for r in rows:
        if r['kind']=='pilot':grouped[(r['n'],r['arm'],r['checks'],r['attacker_pass'],r['visibility'])].append(r)
    metrics=['rare_accuracy','task_accuracy','bad_seat_share','malicious_admission','specialist_rejection']
    cells=[]
    for key,rr in sorted(grouped.items()):
        good=[r for r in rr if r['status']=='completed']
        cells.append(dict(zip(['n','arm','checks','attacker_pass','visibility'],key),assigned=len(rr),valid=len(good),
            metrics={m:{'mean':sum(r['evaluation'][m] for r in good)/len(good) if good else None,
                       'interval':interval([r['evaluation'][m] for r in good])} for m in metrics},
            assigned_accuracy=sum(r['evaluation']['rare_accuracy'] for r in good)/len(rr),
            scripted_accuracy=sum(r['scripted_evaluation']['rare_accuracy'] for r in good)/len(good) if good else None))
    contrasts=[]
    import study
    sizes=study.design()['sizes']
    for n in sizes:
        for rate in (.1,.9):
            for visibility in ('masked','visible'):
                for arm in ('coverage','degree','random'):
                    fixed={r['task']:r for r in grouped[(n,arm,4,rate,visibility)] if r['status']=='completed'}
                    prop={r['task']:r for r in grouped[(n,arm,n//9,rate,visibility)] if r['status']=='completed'}
                    tasks=sorted(set(fixed)&set(prop))
                    differences=[prop[t]['evaluation']['rare_accuracy']-fixed[t]['evaluation']['rare_accuracy'] for t in tasks]
                    contrasts.append({'n':n,'arm':arm,'attacker_pass':rate,'visibility':visibility,'clusters':len(tasks),
                        'mean':sum(differences)/len(differences) if differences else None,'interval':interval(differences),
                        'per_world':[{'task':t,'difference':v} for t,v in zip(tasks,differences)]})
    return {'cells':cells,'budget_contrasts':contrasts,'primary':next((c for c in contrasts if c['n']==max(sizes) and c['arm']=='coverage' and c['attacker_pass']==.1 and c['visibility']=='visible'),None)}

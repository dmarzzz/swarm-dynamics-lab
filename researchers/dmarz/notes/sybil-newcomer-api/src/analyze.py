"""Descriptive paired-world summaries. Frames, identities and rounds are not samples."""
import gzip,json
from collections import defaultdict
import numpy as np
METRICS=['rare_accuracy','wrong_specialist','task_accuracy','bad_seat_share','newcomer_retention','oracle_available_accuracy']
def read_rows(path):
    with (gzip.open if str(path).endswith('.gz') else open)(path,'rt') as f:return [json.loads(x) for x in f]
def interval(values):
    if not values:return None
    a=np.asarray(values,dtype=float);rr=np.random.default_rng(20261004)
    b=a[rr.integers(0,len(a),(10000,len(a)))].mean(axis=1)
    return [float(x) for x in np.quantile(b,[.025,.975])]
def analyze(rows):
    groups=defaultdict(list)
    for r in rows:
        if r['kind']=='pilot':groups[(r['identities'],r['strategy'],r['arm'],r['round'])].append(r)
    cells=[]
    for key,rs in sorted(groups.items()):
        good=[r for r in rs if r['status']=='completed']
        cells.append(dict(zip(['identities','strategy','arm','round'],key),assigned=len(rs),valid=len(good),
            metrics={m:{'mean':sum(r['evaluation'][m] for r in good)/len(good) if good else None,'interval':interval([r['evaluation'][m] for r in good])} for m in METRICS},
            assigned_accuracy=sum(r['evaluation']['rare_accuracy'] for r in good)/len(rs),scripted_accuracy=sum(r['scripted_evaluation']['rare_accuracy'] for r in good)/len(good) if good else None))
    contrasts=[]
    for identities in (1,4,16):
        for strategy in ('clean','sleeper','relapse'):
            for t in (4,5,8):
                for baseline in ('reputation','random'):
                    a={r['task']:r for r in groups[(identities,strategy,'renewal',t)] if r['status']=='completed'}
                    b={r['task']:r for r in groups[(identities,strategy,baseline,t)] if r['status']=='completed'}
                    tasks=sorted(set(a)&set(b));delta=[a[k]['evaluation']['rare_accuracy']-b[k]['evaluation']['rare_accuracy'] for k in tasks]
                    contrasts.append({'identities':identities,'strategy':strategy,'round':t,'baseline':baseline,'clusters':len(tasks),'mean':sum(delta)/len(delta) if delta else None,'interval':interval(delta),'per_world':[{'task':k,'difference':v} for k,v in zip(tasks,delta)]})
    return {'cells':cells,'contrasts':contrasts,'primary':next((c for c in contrasts if c['identities']==16 and c['strategy']=='sleeper' and c['round']==8 and c['baseline']=='reputation'),None),'inference':'Descriptive paired-world bootstrap; exploratory S1, not confirmatory. Clean mode still has the same controller/identity structure but no false claims.'}

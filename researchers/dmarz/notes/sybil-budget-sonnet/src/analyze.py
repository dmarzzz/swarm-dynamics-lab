"""Descriptive paired-world analysis; no monotonicity or confirmatory claims."""
import gzip,json
from collections import defaultdict
import numpy as np
import study

METRICS=['rare_accuracy','task_accuracy','bad_seat_share','specialist_retention','malicious_admission']
KEYS=['n','arm','checks','attacker_pass','visibility']

def read_rows(path):
    opener=gzip.open if str(path).endswith('.gz') else open
    with opener(path,'rt') as f:return [json.loads(line) for line in f]

def interval(values):
    if not values:return None
    a=np.asarray(values,dtype=float);rng=np.random.default_rng(20261004)
    boot=a[rng.integers(0,len(a),(10000,len(a)))].mean(axis=1)
    return [float(x) for x in np.quantile(boot,[.025,.975])]

def contrast(grouped,key_a,key_b,label):
    aa={r['task']:r for r in grouped[key_a] if r['status']=='completed'}
    bb={r['task']:r for r in grouped[key_b] if r['status']=='completed'}
    tasks=sorted(set(aa)&set(bb));result={'label':label,'a':dict(zip(KEYS,key_a)),'b':dict(zip(KEYS,key_b)),'clusters':len(tasks),'metrics':{}}
    for metric in METRICS:
        values=[aa[t]['evaluation'][metric]-bb[t]['evaluation'][metric] for t in tasks]
        result['metrics'][metric]={'mean':float(np.mean(values)) if values else None,'interval':interval(values),'per_world':[{'task':t,'difference':v} for t,v in zip(tasks,values)]}
    return result

def analyze(rows):
    if len({r['id'] for r in rows})!=len(rows):raise ValueError('duplicate_episode_id')
    d=study.design();grouped=defaultdict(list)
    for r in rows:
        if r['kind']=='pilot':grouped[tuple(r[k] for k in KEYS)].append(r)
    cells=[]
    for key,rr in sorted(grouped.items()):
        if len({r['task'] for r in rr})!=len(rr):raise ValueError('duplicate_world_cell')
        good=[r for r in rr if r['status']=='completed']
        m={field:{'mean':float(np.mean([r['evaluation'][field] for r in good])) if good else None,'interval':interval([r['evaluation'][field] for r in good])} for field in METRICS}
        full=len(good)==len(d['worlds'])
        observed=bool(full and m['rare_accuracy']['mean']>=.9 and m['bad_seat_share']['mean']<=.05)
        envelope=bool(full and m['rare_accuracy']['interval'][0]>=.9 and m['bad_seat_share']['interval'][1]<=.05)
        cells.append(dict(zip(KEYS,key),assigned=len(rr),valid=len(good),metrics=m,observed_joint_target=observed,interval_envelope_target=envelope,
            assigned_accuracy=sum(r['evaluation']['rare_accuracy'] for r in good)/len(rr),scripted_accuracy=float(np.mean([r['scripted_evaluation']['rare_accuracy'] for r in good])) if good else None,
            cost_usd=sum(r.get('accounting',{}).get('actual_usd',0) for r in rr),input_tokens=sum(r.get('accounting',{}).get('input_tokens',0) for r in rr)))
    budgets=[];policies=[];frontier=[]
    for n in d['sizes']:
        for rate in d['pilot']['attacker_pass']:
            for arm in d['arms']:
                selected=[c for c in cells if c['n']==n and c['attacker_pass']==rate and c['arm']==arm]
                passing=[c['checks'] for c in selected if c['observed_joint_target']]
                frontier.append({'n':n,'arm':arm,'attacker_pass':rate,'tested_passing_budgets':passing,'smallest_tested_passing_budget':min(passing) if passing else None,'interval_envelope_passing_budgets':[c['checks'] for c in selected if c['interval_envelope_target']], 'interpretation':'Measured grid only. No interpolation, monotonicity assumption, simultaneous confidence guarantee, or safety guarantee.'})
                budgets.append(contrast(grouped,(n,arm,108,rate,'visible'),(n,arm,4,rate,'visible'),'108 minus 4 checks'))
            for checks in d['checks']:
                policies.append(contrast(grouped,(n,'coverage',checks,rate,'visible'),(n,'random',checks,rate,'visible'),'coverage minus random at equal budget'))
    primary=next((c for c in budgets if c['a']['n']==972 and c['a']['arm']=='coverage' and c['a']['attacker_pass']==.1),None)
    return {'cells':cells,'budget_contrasts':budgets,'policy_contrasts':policies,'frontier':frontier,'primary':primary,'unit':'Independent sampled world; 24 worlds shared across conditions. Percentile bootstrap intervals are descriptive, unadjusted for multiple comparisons.'}

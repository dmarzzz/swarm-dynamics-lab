"""Offline two-report verification contract. No transport or native runner."""
from functools import lru_cache
from itertools import product
import math

def probability(x):
    if type(x) not in (int,float) or not math.isfinite(x) or not 0<=x<=1:raise ValueError('probability')
    return x

def update(q,y,noise=0):
    probability(q);probability(noise)
    if type(y) is not bool:raise ValueError('binary_observation')
    a=noise+(1-2*noise)*.9;b=noise+(1-2*noise)*.3
    if not y:a,b=1-a,1-b
    return q*a/(q*a+(1-q)*b)

def posterior(history,noise,shift):
    q=.5
    for y in history:q=update(q,y,noise)
    return q*(1-probability(shift))+(1-q)*shift

def accuracy(q):return .3+.6*probability(q)

@lru_cache(None)
def values(q,c,horizon):
    probability(c);probability(q)
    if type(horizon) is not int or not 1<=horizon<=2:raise ValueError('horizon')
    p=accuracy(q)
    if horizon==1:return {'trust':1-p,'check':c}
    trust=1-p+min(values(q,c,horizon-1).values())
    check=c+p*min(values(update(q,True),c,horizon-1).values())+(1-p)*min(values(update(q,False),c,horizon-1).values())
    return {'trust':trust,'check':check}

def choose(q,c,horizon=2):
    v=values(q,c,horizon);return 'check' if v['check']<=v['trust'] else 'trust'

def observable(history,noise,shift,c,feedback=()):
    if len(history)!=3 or any(type(x) is not bool for x in history):raise ValueError('history')
    for v in (noise,shift,c):probability(v)
    if len(feedback)>2 or any(x is not None and type(x) is not bool for x in feedback):raise ValueError('feedback')
    return dict(calibration=list(history),noise=noise,shift_probability=shift,check_cost=c,feedback=list(feedback),remaining=2-len(feedback),legal_actions=['trust','check'])

def step(action,correct,c):
    probability(c)
    if type(correct) is not bool or action not in ('trust','check'):raise ValueError('action_or_outcome')
    return dict(loss=c if action=='check' else float(not correct),feedback=correct if action=='check' else None)

def development_cases():
    # Fixed software fixtures, never population sampling or holdout generation.
    histories=((True,True,True),(True,True,False),(False,False,False));rows=[]
    for noise,c,shift,h in product((.1,.3),(.1,.4),(0,.4),histories):
        rows.append(dict(id=3000+len(rows),visible=observable(h,noise,shift,c)))
    return rows

def empirical(history,c):return 'check' if c<=1-sum(history)/len(history) else 'trust'

def oracle_cost(good,c,horizon=2):return horizon*min(c,1-(.9 if good else .3))

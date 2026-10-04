"""Schema-owned synthetic trace projection. No arbitrary raw text or transport headers."""
import math

def project_answer(raw,legal):
    if raw.get('type')!='choice' or raw.get('choice') not in legal:raise ValueError('answer')
    p=raw.get('probabilities');c=raw.get('confidence')
    if not isinstance(p,dict) or set(p)!=set(legal):raise ValueError('probabilities')
    if not all(type(x) in (int,float) and math.isfinite(x) and 0<=x<=1 for x in [*p.values(),c]):raise ValueError('numeric')
    if abs(sum(p.values())-1)>.011:raise ValueError('probability_mass')
    if p[raw['choice']]<max(p.values()):raise ValueError('selected_maximum')
    return dict(type='choice',choice=raw['choice'],probabilities=dict(p),confidence=c)

def reconcile(assigned,events):
    if len(set(assigned))!=len(assigned):raise ValueError('duplicate_assignment')
    state={x:'not-started' for x in assigned}
    for e in events:
        i=e['id'];kind=e['kind']
        if i not in state:raise ValueError('unassigned')
        if kind=='start' and state[i]=='not-started':state[i]='started'
        elif kind=='terminal' and state[i]=='started' and e['status'] in ('valid','invalid','failed'):state[i]=e['status']
        else:raise ValueError('event_order')
    return state

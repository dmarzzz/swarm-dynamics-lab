"""Offline one-check simulator and actor-only comparators; never calls a model."""
from copy import deepcopy
from episodes import digest

ROLES = {
    'neutral': 'Choose the available check most useful for verifying the best-supported decision. '
               'Preserve a justified decision and correct an unjustified one. NONE is permitted.',
    'challenge': 'Test whether the current decision lacks support; choose the available check most '
                 'useful for finding a decision-relevant flaw. Preserve the decision when justified. NONE is permitted.'}
CATALOG_FIELDS = ('id','description','covers','authority','priority','latency','cost')


def actor_projection(world):
    ids=[s['id'] for s in world['sources']]
    if len(ids)!=len(set(ids)) or 'NONE' in ids:raise ValueError('invalid_source_ids')
    for source in world['sources']:
        if type(source['cost']) is not int or source['cost']!=1:raise ValueError('invalid_cost')
        if type(source['latency']) is not int or source['latency']<0:raise ValueError('invalid_latency')
        if type(source['authority']) is not int or source['authority']<1:raise ValueError('invalid_authority')
    actor={'task':deepcopy(world['task']), 'observations':deepcopy(world['initial']),
            'incumbent':deepcopy(world['incumbent']), 'budget':deepcopy(world['budget']),
            'catalog':[{k:deepcopy(s[k]) for k in CATALOG_FIELDS} for s in world['sources']]}
    return actor


def eligibility_receipt(actor):
    task=actor['task'];out=[]
    for doc in actor['observations']:
        age=task['now']-doc['observed_at']
        scope=doc['scope']==task['scope'];revision=doc['revision']==task['revision']
        out.append({'id':doc['id'],'age':age,'ttl':task['ttl'],'scope_matches':scope,
                    'revision_matches':revision,'eligible':scope and revision and 0<=age<=task['ttl']})
    return {'observations':out,'eligible_count':sum(x['eligible'] for x in out)}


def selection_request(actor, role):
    if role not in ROLES: raise ValueError('unknown_role')
    criteria={'NONE':'Do not acquire a source.'}
    for source in actor['catalog']: criteria[source['id']]=source['description']
    state=deepcopy(actor);state['eligibility']=eligibility_receipt(actor)
    return {'instructions':ROLES[role], 'state':state,
            'questions':{'source':{'criteria':criteria}}}


def resolve(actor):
    """Apply task rules using only acquired observations, never hidden source responses."""
    t=actor['task']; requirements=t['requirements']; rejected=[]; eligible=[]
    ids=set()
    for doc in actor['observations']:
        if doc['id'] in ids: raise ValueError('duplicate_document')
        ids.add(doc['id'])
        if doc['origin'] not in t['source_authorities']: raise ValueError('unregistered_origin')
        age=t['now']-doc['observed_at']
        ok=(doc['scope']==t['scope'] and doc['revision']==t['revision'] and 0<=age<=t['ttl'])
        (eligible if ok else rejected).append(doc)
    states={}; receipts={}
    for predicate in requirements:
        pool=[d for d in eligible if predicate in d['facts'] and
              t['source_authorities'][d['origin']]>=t['minimum_authority'][predicate]]
        if not pool:
            states[predicate]='missing'; receipts[predicate]=[]; continue
        rank=max(t['source_authorities'][d['origin']] for d in pool)
        pool=[d for d in pool if t['source_authorities'][d['origin']]==rank]
        latest=max(d['observed_at'] for d in pool);pool=[d for d in pool if d['observed_at']==latest]
        if any(type(d['facts'][predicate]) is not bool for d in pool): raise ValueError('non_boolean_fact')
        values={d['facts'][predicate] for d in pool}
        states[predicate]='conflict' if len(values)>1 else ('true' if True in values else 'false')
        receipts[predicate]=[d['id'] for d in pool]
    action='HOLD' if 'false' in states.values() else ('PROCEED' if all(v=='true' for v in states.values()) else 'DEFER')
    return {'action':action,'predicate_states':states,'support':receipts,
            'rejected_observation_ids':[d['id'] for d in rejected]}


def available(actor):
    t=actor['task'];budget=actor['budget']
    if budget['checks']<1:return []
    return [s for s in actor['catalog'] if s['cost']<=budget['credits'] and
            t['now']+s['latency']<=t['deadline']]


def viable(actor):
    t=actor['task']
    return [s for s in available(actor) if any(p in s['covers'] and
            s['authority']>=t['minimum_authority'][p] for p in t['requirements'])]


def routine(actor):
    """Metadata/authority-aware fixed refresh schedule; does not look at future values."""
    states=resolve(actor)['predicate_states']
    if all(v in ('true','false') for v in states.values()):return 'NONE'
    sources=viable(actor)
    return min(sources,key=lambda s:(s['priority'],s['id']))['id'] if sources else 'NONE'


def neutral_reference(actor):
    """Stronger simple comparator: maximize visible unresolved requirement coverage."""
    t=actor['task'];states=resolve(actor)['predicate_states']
    unresolved={p for p,v in states.items() if v in ('missing','conflict')}
    if not unresolved:return 'NONE'
    sources=viable(actor)
    def score(s):
        covered=sum(p in s['covers'] and s['authority']>=t['minimum_authority'][p] for p in unresolved)
        return (-covered,-s['authority'],s['priority'],s['id'])
    sources=[s for s in sources if score(s)[0]<0]
    return min(sources,key=score)['id'] if sources else 'NONE'


class Episode:
    def __init__(self,world):
        self._world=deepcopy(world);self.actor=actor_projection(world);self.terminal=False;self.events=[]

    def select(self,choice):
        if self.terminal: raise ValueError('trajectory_already_selected')
        actor_before=deepcopy(self.actor)
        if choice=='NONE':
            documents=[];cost=0;latency=0
        else:
            candidates={s['id']:s for s in available(self.actor)}
            if choice not in candidates:raise ValueError('unavailable_choice')
            source=next(s for s in self._world['sources'] if s['id']==choice)
            documents=deepcopy(source['response']);cost=source['cost'];latency=source['latency']
            if any(d['origin']!=choice for d in documents):raise ValueError('source_origin_mismatch')
            if any(not set(d['facts']).issubset(source['covers']) for d in documents):raise ValueError('undeclared_coverage')
            if any(type(v) is not bool for d in documents for v in d['facts'].values()):raise ValueError('non_boolean_fact')
            if source['authority']!=self.actor['task']['source_authorities'][choice]:raise ValueError('authority_mismatch')
        next_actor=deepcopy(self.actor)
        next_actor['observations']+=documents;next_actor['task']['now']+=latency
        next_actor['budget']['checks']-=int(choice!='NONE');next_actor['budget']['credits']-=cost
        result=resolve(next_actor)  # Validate before committing state.
        self.actor=next_actor;self.terminal=True
        event={'choice':choice,'checks_used':int(choice!='NONE'),'credits_used':cost,
               'latency':latency,'before_actor_sha256':digest(actor_before),
               'delivered_documents':documents,'after_actor_sha256':digest(self.actor),'resolution':result}
        self.events.append(event)
        return deepcopy(event)


def final_request(actor):
    state=deepcopy(actor);receipt=eligibility_receipt(actor)
    ids={r['id'] for r in receipt['observations'] if r['eligible']}
    state['observations']=[d for d in state['observations'] if d['id'] in ids]
    state['eligibility']=receipt
    return {'instructions':actor['task']['rule'], 'state':state,
            'questions':{'action':{'criteria':{'PROCEED':'All required evidence supports proceeding.',
                        'HOLD':'A required predicate is authoritatively false.',
                        'DEFER':'Evidence is missing, ineligible or unresolved.'}}}}


def replay(world,choice):
    episode=Episode(world);event=episode.select(choice)
    return {'choice':choice,'event':event,'final_request':final_request(episode.actor)}


def validate_world(world):
    actor=actor_projection(world);t=actor['task']
    assert len(t['requirements'])==len(set(t['requirements']))>0
    assert set(t['minimum_authority'])==set(t['requirements'])
    assert world['budget']=={'checks':1,'credits':1}
    assert len({s['id'] for s in world['sources']})==len(world['sources'])
    assert 'NONE' not in {s['id'] for s in world['sources']}
    choices=['NONE']+[s['id'] for s in available(actor)]
    assert set(choices)==set(world['gold_by_choice'])
    rows=[]
    for choice in choices:
        row=replay(world,choice)
        assert row['event']['resolution']['action']==world['gold_by_choice'][choice],(world['id'],choice)
        assert row['event']['checks_used']<=1 and row['event']['credits_used']<=1
        rows.append(row)
    return rows

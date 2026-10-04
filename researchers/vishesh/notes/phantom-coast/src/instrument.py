"""PC-1 offline contracts. No network transport or live dispatch."""
import hashlib
import json
import random
from collections import Counter

CELLS = tuple(f'{r},{c}' for r in range(6) for c in range(6))
LABELS = {'LAND', 'WATER', 'UNKNOWN'}

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)

def digest(obj):
    return hashlib.sha256(canonical(obj).encode()).hexdigest()

def world(seed):
    if seed not in range(100, 104):
        raise ValueError('Offline generator is restricted to development seeds 100-103')
    rng = random.Random(seed)
    row, col = rng.randrange(5), rng.randrange(5)
    exposed = {f'{r},{c}' for r in (row, row+1) for c in (col, col+1)}
    land = exposed | set(rng.sample(sorted(set(CELLS)-exposed), 8))
    truth = {c: 'LAND' if c in land else 'WATER' for c in CELLS}
    early = []
    for batch, label in [('a', 'LAND'), ('b', 'WATER')]:
        for i, cell in enumerate(sorted(exposed)):
            early.append(dict(id=f'{batch}{i}', acquisition_id=f'{batch}{i}', cell=cell,
                              label=label, epoch=0, source=batch, reliability=0.8))
    fresh = [dict(id=f'n{i}', acquisition_id=f'n{i}', cell=c, label=truth[c], epoch=2,
                  source='sensor', reliability=1.0) for i, c in enumerate(CELLS)]
    return dict(world_id=f'dev-{seed}', truth=truth, exposed=sorted(exposed),
                early=early, fresh=fresh, withdrawn=[r['id'] for r in early if r['source']=='b'])

def ledger(w, history, step):
    if history not in ('A', 'B') or step not in (0, 1, 2):
        raise ValueError('invalid history/step')
    first = 'b' if history == 'A' else 'a'
    records = [r for r in w['early'] if step > 0 or r['source'] == first]
    if step == 2:
        records = records + w['fresh']
    # Raw observations deliberately exclude evaluator metadata, even if added upstream.
    fields = ('id', 'acquisition_id', 'cell', 'label', 'epoch', 'source', 'reliability')
    return {'observations': sorted([{k:r[k] for k in fields} for r in records],key=lambda r:r['id']),
            'withdrawn': sorted(w['withdrawn']) if step == 2 else []}

def response(raw, visible):
    if not isinstance(raw, dict) or set(raw) != {'map', 'evidence_ids'}:
        raise ValueError('invalid response fields')
    m, refs = raw['map'], raw['evidence_ids']
    if not isinstance(m,dict) or set(m) != set(CELLS) or any(type(v) is not str or v not in LABELS for v in m.values()):
        raise ValueError('invalid map')
    if not isinstance(refs,list) or any(type(x) is not str or x not in visible for x in refs) or len(refs)!=len(set(refs)):
        raise ValueError('invalid citations')
    return json.loads(canonical(raw))

def packet(w, history, communication, state, step, actor, previous=None):
    if communication not in ('private','social') or state not in ('reset','retain') or actor not in (0,1,2):
        raise ValueError('invalid assignment')
    facts = ledger(w,history,step)
    p = {'task':'Map every cell using observations; withdrawn records no longer support a claim. Peer maps are interpretations, not new observations. UNKNOWN is allowed.',
         'cells':list(CELLS),'actor':f'observer-{actor}', 'evidence':facts,'prior':None,'peers':[]}
    if step > 0 and not (step == 2 and state == 'reset'):
        if previous is None or len(previous)!=3:
            raise ValueError('previous round must contain three explicit outcomes')
        # Revalidate carried state against records visible by now; whitelist entire payload.
        visible = {r['id'] for r in facts['observations']}
        p['prior'] = response(previous[actor],visible) if previous[actor] is not None else None
        if communication == 'social':
            p['peers'] = [dict(actor=f'observer-{i}',response=response(x,visible) if x is not None else None)
                          for i,x in enumerate(previous)]
    return p

def deterministic(p):
    facts=p['evidence']; withdrawn=set(facts['withdrawn'])
    acquisitions={}; rows={c:[] for c in CELLS}
    # One withdrawn identity retracts its acquisition, including any forwarded copies.
    revoked={r['acquisition_id'] for r in facts['observations'] if r['id'] in withdrawn}
    for r in facts['observations']:
        a=r['acquisition_id']; signature=(r['cell'],r['label'],r['epoch'],r['source'],r['reliability'])
        if a in acquisitions and acquisitions[a]!=signature:
            raise ValueError('conflicting acquisition identity')
        acquisitions[a]=signature
    for a,(cell,label,epoch,source,reliability) in acquisitions.items():
        if a not in revoked:
            rows[cell].append((epoch,label))
    out={}
    for c, values in rows.items():
        if not values:
            out[c]='UNKNOWN'; continue
        latest=max(t for t,_ in values)
        labels={v for t,v in values if t==latest}
        out[c]=next(iter(labels)) if len(labels)==1 else 'UNKNOWN'
    return {'map':out,'evidence_ids':sorted(r['id'] for r in facts['observations'] if r['acquisition_id'] not in revoked)}

def aggregate(outcomes):
    if len(outcomes)!=3:
        raise ValueError('three assigned actors required, including failures')
    out={}
    for cell in CELLS:
        votes=Counter(o['map'][cell] for o in outcomes if o is not None)
        winner=[v for v in ('LAND','WATER') if votes[v]>=2]
        out[cell]=winner[0] if winner else 'UNKNOWN'
    return out

def bounds(prediction, truth, cells=CELLS):
    if not cells:
        return {'wrong':0,'missing':0,'denominator':0,'lower':None,'upper':None}
    wrong=sum(prediction.get(c,'UNKNOWN') not in ('UNKNOWN',truth[c]) for c in cells)
    missing=sum(prediction.get(c,'UNKNOWN')=='UNKNOWN' for c in cells)
    return dict(wrong=wrong,missing=missing,denominator=len(cells),lower=wrong/len(cells),upper=(wrong+missing)/len(cells))

def disagreement(a,b):
    missing=sum(a.get(c,'UNKNOWN')=='UNKNOWN' or b.get(c,'UNKNOWN')=='UNKNOWN' for c in CELLS)
    unequal=sum(a.get(c,'UNKNOWN')!='UNKNOWN' and b.get(c,'UNKNOWN')!='UNKNOWN' and a[c]!=b[c] for c in CELLS)
    return dict(lower=unequal/36,upper=(unequal+missing)/36,missing=missing,denominator=36)

def assignments(seed):
    if seed not in range(100,104):
        raise ValueError('development only')
    out=[]
    for history in ('A','B'):
        for communication in ('private','social'):
            for state in ('reset','retain'):
                for step in range(3):
                    for actor in range(3):
                        out.append(dict(id=f'{seed}-{history}-{communication}-{state}-{step}-{actor}',
                                        history=history,communication=communication,state=state,step=step,actor=actor,kind='swarm'))
        for state in ('reset','retain'):
            for step in range(3):
                out.append(dict(id=f'{seed}-{history}-pooled-{state}-{step}',history=history,
                                communication='private',state=state,step=step,actor=0,kind='pooled'))
    for actor in range(3):
        out.append(dict(id=f'{seed}-clean-{actor}',kind='clean',step=2,actor=actor))
    # Interleave within a round, never schedule a later round before its dependencies.
    rng=random.Random(seed)
    rng.shuffle(out)
    return sorted(out,key=lambda a:a['step'])

def reconcile(schedule, records):
    expected={a['id'] for a in schedule}
    if len(expected)!=len(schedule): raise ValueError('duplicate assignment')
    seen={}
    for r in records:
        if r['id'] not in expected or r['id'] in seen: raise ValueError('unknown/duplicate outcome')
        if r['status'] not in ('valid','invalid','timeout','not-started'): raise ValueError('invalid status')
        seen[r['id']]=r['status']
    counts=Counter(seen.values()); counts['not-started']+=len(expected)-len(seen)
    return {'assigned':len(expected),'counts':dict(counts)}

def fixtures(seed=100, fail=False):
    w=world(seed); frames=[]; previous=None
    for step in range(3):
        packets=[packet(w,'A','social','retain',step,i,previous) for i in range(3)]
        outcomes=[deterministic(p) for p in packets]
        if fail and step==2: outcomes=[None,None,outcomes[2]]
        m=aggregate(outcomes)
        frames.append(dict(step=step,event=('first report','conflicting report','explicit retraction + fresh survey')[step],
                           status='injected missing responses' if fail and step==2 else 'scripted fixture',
                           request_hashes=[digest(p) for p in packets],outcomes=outcomes,map=m,
                           metrics=bounds(m,w['truth']),
                           acquisitions=len({r['acquisition_id'] for r in packets[0]['evidence']['observations']}),
                           evidence=packets[0]['evidence']))
        previous=outcomes
    return dict(schema='PC-V1',mode='SOFTWARE FIXTURE — NO MODEL CALLS',world_id=w['world_id'],
                history='A',communication='social',state='retain',truth=w['truth'],exposed=w['exposed'],frames=frames)

def request_for_assignment(w, assignment, previous=None):
    a=assignment
    if a['kind']=='clean':
        clean=dict(w,early=[],withdrawn=[])
        return packet(clean,'A','private','reset',2,a['actor'])
    if a['kind']=='pooled':
        return packet(w,a['history'],'private',a['state'],a['step'],0,
                      [previous,None,None] if a['step']>0 else None)
    return packet(w,a['history'],a['communication'],a['state'],a['step'],a['actor'],previous)


def subtract_bounds(a,b):
    return {'lower':a['lower']-b['upper'],'upper':a['upper']-b['lower']}

def history_interaction(maps):
    """One world, eight aggregates; missing trajectories remain fully unidentified."""
    d={(comm,state):disagreement(maps.get(('A',comm,state),{}),maps.get(('B',comm,state),{}))
       for comm in ('social','private') for state in ('retain','reset')}
    return subtract_bounds(subtract_bounds(d['social','retain'],d['social','reset']),
                           subtract_bounds(d['private','retain'],d['private','reset']))

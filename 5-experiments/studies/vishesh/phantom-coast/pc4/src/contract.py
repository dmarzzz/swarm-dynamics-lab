"""Development-only PC-4 environment. No transport, credentials or reserved worlds."""
import collections
import copy
import hashlib
import random

CELLS=tuple(f'{r},{c}' for r in range(6) for c in range(6))
LABELS={'LAND','WATER','UNKNOWN'}
POLICIES={'team','single','uniform'}


def rng(seed,stream):
    return random.Random(int.from_bytes(hashlib.sha256(f'{seed}/{stream}'.encode()).digest(),'big'))


def development_world(seed,family='block'):
    if type(seed) is not int or seed not in range(1200,1208):
        raise ValueError('development seeds 1200-1207 only; reserved worlds unavailable')
    return _world(seed,family)


def _world(seed,family):
    # Reserved construction is invoked only by the admitted native runner.
    if family not in ('block','scattered'):raise ValueError('family')
    g=rng(seed,'geometry/'+family)
    if family=='block':
        r,c=g.randrange(5),g.randrange(5)
        region=[f'{i},{j}' for i in (r,r+1) for j in (c,c+1)]
    else:
        # Greedy independent set on a grid; four cells always fit.
        order=list(CELLS);g.shuffle(order);region=[]
        for cell in order:
            r,c=map(int,cell.split(','))
            if all(abs(r-int(x.split(',')[0]))+abs(c-int(x.split(',')[1]))>1 for x in region):region.append(cell)
            if len(region)==4:break
    land=set(g.sample(region,2))|set(g.sample(sorted(set(CELLS)-set(region)),10))
    return dict(seed=seed,family=family,region=sorted(region),truth={c:'LAND' if c in land else 'WATER' for c in CELLS})


def reconstruct(packet):
    rows=packet['evidence']['observations'];withdrawn=set(packet['evidence']['withdrawn'])
    signatures={};revoked={r['acquisition_id'] for r in rows if r['id'] in withdrawn};by=collections.defaultdict(list)
    for r in rows:
        sig=tuple(r[k] for k in ('cell','label','epoch','source','reliability'));aid=r['acquisition_id']
        if aid in signatures and signatures[aid]!=sig:raise ValueError('conflicting acquisition identity')
        signatures[aid]=sig
    for aid,(cell,label,epoch,source,reliability) in signatures.items():
        if aid not in revoked:by[cell].append((epoch,label))
    result={}
    for c in CELLS:
        rows=by[c]
        labels={label for epoch,label in rows if epoch==max(x[0] for x in rows)} if rows else set()
        result[c]=next(iter(labels)) if len(labels)==1 else 'UNKNOWN'
    return result


def valid_map(m):
    return isinstance(m,dict) and set(m)==set(CELLS) and all(type(v) is str and v in LABELS for v in m.values())


def majority(maps):
    if len(maps)!=3:raise ValueError('three assigned maps required')
    maps=[m if valid_map(m) else {} for m in maps]
    return {c:next((v for v in ('LAND','WATER') if sum(m.get(c)==v for m in maps)>=2),'UNKNOWN') for c in CELLS}


def error(m,truth,cells=CELLS):
    m=m if valid_map(m) else {};cells=list(cells)
    wrong=sum(m.get(c,'UNKNOWN') not in ('UNKNOWN',truth[c]) for c in cells)
    missing=sum(m.get(c,'UNKNOWN')=='UNKNOWN' for c in cells);n=len(cells)
    return dict(wrong=wrong,missing=missing,denominator=n,lower=wrong/n if n else None,upper=(wrong+missing)/n if n else None)



def packet(w,policy,false_count,actor=0,slots=12):
    if policy not in ('q0','q2','q4','uniform') or false_count not in (0,2,4) or not 0<=slots<=12:raise ValueError('condition')
    region=list(w['region']);rng(w['seed'],'report-order').shuffle(region)
    flips=set(region) if false_count==4 else set()
    if false_count==2:
        for label in ('LAND','WATER'):flips.add(rng(w['seed'],'flip/'+label).choice([c for c in region if w['truth'][c]==label]))
    outside=sorted(set(CELLS)-set(region));rng(w['seed'],'outside-order').shuffle(outside)
    uniform=list(CELLS);rng(w['seed'],'uniform-order').shuffle(uniform)
    q=int(policy[1:]) if policy!='uniform' else None
    path=uniform[:12] if q is None else region[:q]+outside[:12-q]
    observations=[dict(id=f'r{i}',acquisition_id=f'r{i}',cell=c,label=('WATER' if w['truth'][c]=='LAND' else 'LAND') if c in flips else w['truth'][c],epoch=0,source='report',reliability=.8) for i,c in enumerate(region)]
    observations += [dict(id=f's{i+1}',acquisition_id=f's{i+1}',cell=c,label=w['truth'][c],epoch=2,source='sensor',reliability=1.0) for i,c in enumerate(path[:slots])]
    return dict(task='Map the current terrain from the acquired evidence. UNKNOWN is legal when unresolved.',actor=f'observer-{actor}',cells=list(CELLS),evidence=dict(observations=observations,withdrawn=[])),path

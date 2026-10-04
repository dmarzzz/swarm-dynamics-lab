"""Development-only PC-2 environment. No transport, credentials or reserved worlds."""
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
    if type(seed) is not int or seed not in range(300,308):
        raise ValueError('development seeds 300-307 only; reserved worlds unavailable')
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
    land=set(region)|set(g.sample(sorted(set(CELLS)-set(region)),8))
    return dict(seed=seed,family=family,region=sorted(region),truth={c:'LAND' if c in land else 'WATER' for c in CELLS})


class Episode:
    def __init__(self,w,report='misleading',policy='team',audit=False,*,admission=None):
        if w.get('seed') not in range(300,308):
            if admission is None or not admission.allows(w.get('seed')):raise ValueError('admitted world required')
        if report not in ('misleading','benign') or policy not in POLICIES or type(audit) is not bool:raise ValueError('condition')
        self.world=copy.deepcopy(w);self.policy=policy;self.audit=audit;self.events=[];self.previous=[]
        self.observations=[dict(id=f'r{i}',acquisition_id=f'r{i}',cell=c,label='WATER' if report=='misleading' else 'LAND',epoch=0,source='report',reliability=.8) for i,c in enumerate(w['region'])]
        self.order=list(CELLS);rng(w['seed'],'policy-ties').shuffle(self.order)
        self.uniform=list(CELLS);rng(w['seed'],'uniform').shuffle(self.uniform)
        self.audit_cell=rng(w['seed'],'source-audit').choice(sorted(r['cell'] for r in self.observations))

    def packet(self,actor=0):
        n=1 if self.policy=='single' else 3
        if type(actor) is not int or actor not in range(n):raise ValueError('actor')
        return dict(task='Choose one cell to inspect to minimize final whole-map error within twelve sensing slots. Every cell is legal; repeat inspections consume a slot. Reports may be wrong. Peers are interpretations, not observations.',
                    actor=f'observer-{actor}',cells=list(CELLS),remaining_slots=12-len(self.events),
                    evidence={'observations':copy.deepcopy(self.observations),'withdrawn':[]},
                    previous_proposals=copy.deepcopy(self.previous) if self.policy=='team' else copy.deepcopy(self.previous[:1]))

    def step(self,proposals=None):
        if len(self.events)>=12:raise ValueError('sensing budget exhausted')
        proposals=[] if proposals is None else proposals
        required={'team':3,'single':1,'uniform':0}[self.policy]
        if not isinstance(proposals,list) or len(proposals)!=required:raise ValueError('explicit assigned proposal slots required')
        safe=[p if type(p) is str and p in CELLS else None for p in proposals]
        valid=[p for p in safe if p is not None];slot=len(self.events)+1;proposed=None
        if self.policy=='uniform':proposed=self.uniform[slot-1]
        elif len(valid)>=(2 if self.policy=='team' else 1):
            counts=collections.Counter(valid);proposed=min(counts,key=lambda c:(-counts[c],self.order.index(c)))
        overridden=self.audit and slot==6
        target=self.audit_cell if overridden else proposed
        seen={r['cell'] for r in self.observations if r['source']=='sensor'}
        observation=None
        if target is not None:
            observation=dict(id=f's{slot}',acquisition_id=f's{slot}',cell=target,label=self.world['truth'][target],epoch=2,source='sensor',reliability=1.0)
            self.observations.append(observation)
        event=dict(slot=slot,proposals=safe,valid_proposals=len(valid),proposed_target=proposed,
                   target=target,audit_override=overridden,repeated=target is not None and target in seen,
                   observation=copy.deepcopy(observation),status='observed' if target is not None else 'no_observation')
        self.events.append(event);self.previous=[dict(actor=f'observer-{i}',cell=p) for i,p in enumerate(safe)]
        return copy.deepcopy(event)


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


def metrics(episode,m):
    w=episode.world;visited={e['target'] for e in episode.events if e['target'] is not None}
    corrective=[e['slot'] for e in episode.events if e['target'] in w['region']]
    return dict(spent_slots=len(episode.events),unique_cells=len(visited),report_cells_visited=len(visited&set(w['region'])),
                repeated_slots=sum(e['repeated'] for e in episode.events),failed_slots=sum(e['target'] is None for e in episode.events),
                invalid_proposal_slots=sum(e['valid_proposals']<(2 if episode.policy=='team' else 1) for e in episode.events) if episode.policy!='uniform' else 0,
                first_report_visit=min(corrective) if corrective else None,first_visit_censored=not corrective and len(episode.events)==12,
                whole=error(m,w['truth']),observed=error(m,w['truth'],visited),unobserved=error(m,w['truth'],set(CELLS)-visited),
                land=error(m,w['truth'],[c for c in CELLS if w['truth'][c]=='LAND']),
                water=error(m,w['truth'],[c for c in CELLS if w['truth'][c]=='WATER']))

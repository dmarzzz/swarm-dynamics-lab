"""Assignment metadata never opens a reserved world."""
import copy
from contract import CELLS,rng,Episode,majority,error,metrics,reconstruct
from wire import request
STAGES={'Q0':range(400,404),'S1':range(500,508)}

def family(seed):return 'block' if seed%2==0 else 'scattered'
def conditions(seed):
    rows=[dict(report=r,policy=p,audit=a) for r in ('misleading','benign') for p in ('team','single','uniform') for a in (False,True)]
    rng(seed,'episode-order').shuffle(rows);return rows

def eid(seed,c):return f"{seed}-{c['policy']}-{c['report']}-audit{int(c['audit'])}"

def schedule(stage,seeds=None):
    if stage not in STAGES:raise ValueError('stage')
    seeds=list(STAGES[stage] if seeds is None else seeds)
    rows=[]
    for seed in seeds:
        if stage=='Q0':
            for kind in ('map','choice'):
                for actor in range(3):rows.append(dict(id=f'{seed}-{kind}-{actor}',seed=seed,kind=kind,actor=actor))
        else:
            cs=conditions(seed)
            for slot in range(1,13):
                for c in cs:
                    for actor in range({'team':3,'single':1,'uniform':0}[c['policy']]):rows.append(dict(c,id=f'{eid(seed,c)}-slot{slot}-{actor}',episode=eid(seed,c),seed=seed,slot=slot,kind='choice',actor=actor))
            for c in cs:
                for actor in range(1 if c['policy']=='single' else 3):rows.append(dict(c,id=f'{eid(seed,c)}-map-{actor}',episode=eid(seed,c),seed=seed,slot=13,kind='map',actor=actor))
                if c['policy']=='team':rows.append(dict(c,id=f'{eid(seed,c)}-yoked',episode=eid(seed,c),seed=seed,slot=13,kind='yoked',actor=0))
    return rows

def clean_packet(w,actor,kind):
    omitted=rng(w['seed'],f'qualification-target/{actor}').choice(CELLS) if kind=='choice' else None
    observations=[dict(id=f'c{i}',acquisition_id=f'c{i}',cell=c,label=w['truth'][c],epoch=2,source='sensor',reliability=1.0) for i,c in enumerate(CELLS) if c!=omitted]
    packet=dict(task='Select the unique cell without a current direct measurement.' if kind=='choice' else 'Map the current terrain from direct measurements.',actor=f'observer-{actor}',cells=list(CELLS),remaining_slots=1 if kind=='choice' else 0,evidence={'observations':observations,'withdrawn':[]},previous_proposals=[])
    return packet,omitted

def qualified(records,worlds):
    expected=schedule('Q0',sorted(worlds));by={r['id']:r for r in records}
    if len(by)!=len(records) or set(by)!={r['id'] for r in expected}:raise ValueError('qualification_assignments')
    strata={k:dict(wrong=0,missing=0,denominator=0) for k in ('all','LAND','WATER')};correct=0
    for a in expected:
        w=worlds[a['seed']];r=by[a['id']];result=r.get('checked',{}).get('result',{}) if r['status']=='valid' else {}
        if a['kind']=='choice':correct+=result.get('choice')==clean_packet(w,a['actor'],'choice')[1]
        else:
            for k,v in strata.items():
                b=error(result.get('map'),w['truth'],CELLS if k=='all' else [c for c in CELLS if w['truth'][c]==k])
                for key in v:v[key]+=b[key]
    for v in strata.values():v['upper']=(v['wrong']+v['missing'])/v['denominator']
    valid=sum(r['status']=='valid' for r in records)
    return dict(assigned=len(expected),valid=valid,correct_targets=correct,errors=strata,qualification_passed=valid==24 and correct>=11 and strata['all']['upper']<=.1 and all(strata[k]['upper']<=.2 for k in ('LAND','WATER')))

def endpoint(e,records):
    maps=[r.get('checked',{}).get('result',{}).get('map') if r['status']=='valid' else None for r in records if r['kind']=='map']
    n=1 if e.policy=='single' else 3
    if len(maps)!=n:raise ValueError('assigned_maps')
    m=maps[0] if n==1 else majority(maps)
    yoked=next((r.get('checked',{}).get('result',{}).get('map') for r in records if r['kind']=='yoked' and r['status']=='valid'),None)
    return dict(map=m,metrics=metrics(e,m),deterministic=error(reconstruct(e.packet()),e.world['truth']),yoked=error(yoked,e.world['truth']) if e.policy=='team' else None)

def contrasts(episodes):
    # Equal-root descriptive contrasts; missing endpoints retain [0,1] bounds.
    roots=[]
    for seed in sorted({e['seed'] for e in episodes}):
        es={ (e['policy'],e['report'],e['audit']):e for e in episodes if e['seed']==seed}
        def bound(p,r,a):return es[p,r,a]['endpoint']['metrics']['whole']
        def linear(terms):
            return {k:sum(sign*bound(*c)[k if sign>0 else ('upper' if k=='lower' else 'lower')] for sign,c in terms) for k in ('lower','upper')}
        terms=[(1,('team','misleading',False)),(-1,('team','benign',False)),(-1,('uniform','misleading',False)),(1,('uniform','benign',False))]
        mechanism=[]
        for p in ('team','single','uniform'):
            for a in (False,True):
                pair=[es[p,r,a] for r in ('misleading','benign')]
                visits=[{v['target'] for v in e['events'] if v['target'] is not None} for e in pair]
                mechanism.append(dict(policy=p,audit=a,report_visits_difference=pair[0]['endpoint']['metrics']['report_cells_visited']-pair[1]['endpoint']['metrics']['report_cells_visited'],overlap_cells=len(visits[0]&visits[1]),union_cells=len(visits[0]|visits[1])))
        audit_coverage=[dict(policy=p,report=r,unique_gain=es[p,r,True]['endpoint']['metrics']['unique_cells']-es[p,r,False]['endpoint']['metrics']['unique_cells'],report_gain=es[p,r,True]['endpoint']['metrics']['report_cells_visited']-es[p,r,False]['endpoint']['metrics']['report_cells_visited']) for p in ('team','single','uniform') for r in ('misleading','benign')]
        roots.append(dict(mechanism=mechanism,audit_coverage=audit_coverage,seed=seed,family=family(seed),primary_upper_interaction=sum(s*bound(*c)['upper'] for s,c in terms),primary_bounds=linear(terms),audit=[dict(policy=p,report=r,bounds=linear([(1,(p,r,True)),(-1,(p,r,False))]),upper_difference=bound(p,r,True)['upper']-bound(p,r,False)['upper']) for p in ('team','single','uniform') for r in ('misleading','benign')]))
    def avg(rows):return dict(roots=len(rows),primary_upper_interaction=sum(r['primary_upper_interaction'] for r in rows)/len(rows),primary_bounds={k:sum(r['primary_bounds'][k] for r in rows)/len(rows) for k in ('lower','upper')})
    return dict(worlds=roots,overall=avg(roots),by_family={f:avg([r for r in roots if r['family']==f]) for f in sorted({r['family'] for r in roots})})

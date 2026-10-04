"""Assignment metadata never opens a reserved world."""
import copy
from contract import CELLS,rng,Episode,majority,error,metrics,reconstruct
from wire import request
STAGES={'Q0':range(700,704),'S1':range(800,808)}

def family(seed):return 'block' if seed%2==0 else 'scattered'
def conditions(seed):
    rows=[dict(report=r,policy=p,guard=a) for r in ('misleading','benign') for p in ('team','single','uniform') for a in (False,True)]
    rng(seed,'episode-order').shuffle(rows);return rows

def eid(seed,c):return f"{seed}-{c['policy']}-{c['report']}-guard{int(c['guard'])}"

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
    packet=dict(task='Choose one cell to inspect to minimize final whole-map error within twelve sensing slots. '+('Only cells without direct measurements are legal.' if actor==2 else 'Every cell is legal; repeat inspections consume a slot.')+' Reports may be wrong. Peers are interpretations, not observations.' if kind=='choice' else 'Map the current terrain from direct measurements.',actor=f'observer-{actor}',cells=list(CELLS),remaining_slots=1 if kind=='choice' else 0,evidence={'observations':observations,'withdrawn':[]},previous_proposals=[])
    packet["legal_cells"]=[omitted] if kind=="choice" and actor==2 else list(CELLS)
    return packet,omitted

def qualified(records,worlds):
    expected=schedule('Q0',sorted(worlds));by={r['id']:r for r in records}
    if len(by)!=len(records) or set(by)!={r['id'] for r in expected}:raise ValueError('qualification_assignments')
    strata={k:dict(wrong=0,missing=0,denominator=0) for k in ('all','LAND','WATER')};correct=0;guard_correct=0;strategic_correct=0
    for a in expected:
        w=worlds[a['seed']];r=by[a['id']];result=r.get('checked',{}).get('result',{}) if r['status']=='valid' else {}
        if a['kind']=='choice':
            ok=result.get('choice')==clean_packet(w,a['actor'],'choice')[1];correct+=ok
            if a['actor']==2:guard_correct+=ok
            else:strategic_correct+=ok
        else:
            for k,v in strata.items():
                b=error(result.get('map'),w['truth'],CELLS if k=='all' else [c for c in CELLS if w['truth'][c]==k])
                for key in v:v[key]+=b[key]
    for v in strata.values():v['upper']=(v['wrong']+v['missing'])/v['denominator']
    valid=sum(r['status']=='valid' for r in records)
    return dict(assigned=len(expected),valid=valid,correct_targets=correct,guard_correct=guard_correct,strategic_correct=strategic_correct,errors=strata,qualification_passed=valid==24 and guard_correct==4 and strata['all']['upper']<=.1 and all(strata[k]['upper']<=.2 for k in ('LAND','WATER')))

def endpoint(e,records):
    maps=[r.get('checked',{}).get('result',{}).get('map') if r['status']=='valid' else None for r in records if r['kind']=='map']
    n=1 if e.policy=='single' else 3
    if len(maps)!=n:raise ValueError('assigned_maps')
    m=maps[0] if n==1 else majority(maps)
    yoked=next((r.get('checked',{}).get('result',{}).get('map') for r in records if r['kind']=='yoked' and r['status']=='valid'),None)
    return dict(map=m,metrics=metrics(e,m),deterministic=error(reconstruct(e.packet()),e.world['truth']),yoked=error(yoked,e.world['truth']) if e.policy=='team' else None)

def contrasts(episodes):
    import statistics,math
    roots=[]
    def loss(e,u=.25):
        m=e['endpoint']['metrics']['whole'];return (m['wrong']+u*m['missing'])/36
    for seed in sorted({e['seed'] for e in episodes}):
        es={(e['policy'],e['report'],e['guard']):e for e in episodes if e['seed']==seed}
        on=es['team','misleading',True];off=es['team','misleading',False]
        a=on['endpoint']['metrics']['whole'];b=off['endpoint']['metrics']['whole']
        roots.append(dict(seed=seed,family=family(seed),primary_loss_difference=loss(on)-loss(off),primary_bounds={'lower':a['lower']-b['upper'],'upper':a['upper']-b['lower']},guarded_team_minus_uniform=loss(on)-loss(es['uniform','misleading',True]),guarded_team_minus_single=loss(on)-loss(es['single','misleading',True]),guard_report_interaction=loss(on)-loss(off)-loss(es['team','benign',True])+loss(es['team','benign',False]),utility_sensitivity={str(u):loss(on,u)-loss(off,u) for u in (0,.25,.5,1)},guard=[dict(policy=p,report=r,loss_difference=loss(es[p,r,True])-loss(es[p,r,False]),upper_difference=es[p,r,True]['endpoint']['metrics']['whole']['upper']-es[p,r,False]['endpoint']['metrics']['whole']['upper']) for p in ('team','single','uniform') for r in ('misleading','benign')]))
    def avg(rows):
        xs=[r['primary_loss_difference'] for r in rows];mean=statistics.mean(xs);se=statistics.stdev(xs)/math.sqrt(len(xs)) if len(xs)>1 else None
        return dict(roots=len(rows),primary_loss_difference=mean,practical_success=mean<=-2/36,range=[min(xs),max(xs)],paired_se=se,descriptive_t7_interval=[mean-2.364624*se,mean+2.364624*se] if len(xs)==8 else None,primary_bounds={k:statistics.mean(r['primary_bounds'][k] for r in rows) for k in ('lower','upper')})
    return dict(worlds=roots,overall=avg(roots),by_family={f:avg([r for r in roots if r['family']==f]) for f in sorted({r['family'] for r in roots})})

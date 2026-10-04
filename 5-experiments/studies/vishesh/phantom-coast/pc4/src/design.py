"""Frozen assignments and paired analysis; hosted outcomes are not independent actors."""
import statistics,math
from contract import CELLS,rng,packet,reconstruct,error,majority
STAGES={'Q0':range(1300,1304),'S1':range(1400,1432)}
def family(seed):return 'block' if seed%2==0 else 'scattered'
def conditions(seed):
    rows=[dict(policy=p,false_count=f) for p in ('q0','q2','q4','uniform') for f in (0,2,4)]
    rng(seed,'episode-order').shuffle(rows);return rows
def eid(seed,c):return f"{seed}-{c['policy']}-false{c['false_count']}"
def schedule(stage,seeds=None):
    if stage not in STAGES:raise ValueError('stage')
    rows=[]
    for seed in (STAGES[stage] if seeds is None else seeds):
        if stage=='Q0':
            for case in ('complete','partial'):
                for actor in range(3):rows.append(dict(id=f'{seed}-{case}-{actor}',seed=seed,case=case,actor=actor,kind='map'))
        else:
            for c in conditions(seed):
                for actor in range(3):rows.append(dict(c,id=f'{eid(seed,c)}-map-{actor}',episode=eid(seed,c),seed=seed,actor=actor,kind='map'))
    return rows

def clean_packet(w,actor,case):
    p,path=packet(w,'q4',4,actor)
    if case=='complete':
        p['evidence']['observations']=[r for r in p['evidence']['observations'] if r['source']=='report']+[dict(id=f's{i}',acquisition_id=f's{i}',cell=c,label=w['truth'][c],epoch=2,source='sensor',reliability=1.0) for i,c in enumerate(CELLS)]
    elif case!='partial':raise ValueError('qualification_case')
    return p

def qualified(records,worlds):
    expected=schedule('Q0',sorted(worlds));by={r['id']:r for r in records}
    if len(by)!=len(records) or set(by)!={r['id'] for r in expected}:raise ValueError('qualification_assignments')
    mismatches=0;labels=0
    for a in expected:
        p=clean_packet(worlds[a['seed']],a['actor'],a['case']);truth=reconstruct(p);r=by[a['id']]
        m=r.get('checked',{}).get('result',{}).get('map',{}) if r['status']=='valid' else {}
        mismatches+=sum(m.get(c)!=truth[c] for c in CELLS);labels+=36
    valid=sum(r['status']=='valid' for r in records)
    return dict(assigned=len(expected),valid=valid,labels=labels,mismatches=mismatches,qualification_passed=valid==24 and mismatches==0)

def endpoint(w,p,records):
    maps=[r.get('checked',{}).get('result',{}).get('map') if r['status']=='valid' else None for r in records]
    if len(maps)!=3:raise ValueError('assigned_maps')
    m=majority(maps);direct={r['cell'] for r in p['evidence']['observations'] if r['source']=='sensor'}
    return dict(map=m,whole=error(m,w['truth']),observed=error(m,w['truth'],direct),single=error(maps[0],w['truth']),deterministic=error(reconstruct(p),w['truth']),valid_maps=sum(x is not None for x in maps))

def loss(e,u=.25,which='whole'):
    m=e['endpoint'][which];return (m['wrong']+u*m['missing'])/36

def contrasts(episodes):
    roots=[]
    for seed in sorted({e['seed'] for e in episodes}):
        es={(e['policy'],e['false_count']):e for e in episodes if e['seed']==seed};t=es['q4',4];c=es['uniform',4]
        a=t['endpoint']['whole'];b=c['endpoint']['whole']
        roots.append(dict(seed=seed,family=family(seed),primary=loss(t)-loss(c),bounds=dict(lower=a['lower']-b['upper'],upper=a['upper']-b['lower']),sensitivity={str(u):loss(t,u)-loss(c,u) for u in (0,.25,.5,1)}))
    def aggregate(rs):
        xs=[r['primary'] for r in rs];n=len(xs);mean=statistics.mean(xs);se=statistics.stdev(xs)/math.sqrt(n) if n>1 else None
        return dict(roots=n,mean=mean,paired_se=se,descriptive_t31_interval=[mean-2.039513*se,mean+2.039513*se] if n==32 else None,range=[min(xs),max(xs)],bounds={k:statistics.mean(r['bounds'][k] for r in rs) for k in ('lower','upper')})
    overall=aggregate(roots);complete=all(e['status']=='complete' for e in episodes)
    overall['practical_success']=complete and len(roots)==32 and overall['mean']<=-2/36
    overall['leave_one_out_range']=[min(statistics.mean(x['primary'] for x in roots if x!=r) for r in roots),max(statistics.mean(x['primary'] for x in roots if x!=r) for r in roots)] if len(roots)>1 else None
    cells=[]
    for policy in ('q0','q2','q4','uniform'):
        for false in (0,2,4):
            es=[e for e in episodes if e['policy']==policy and e['false_count']==false]
            cells.append(dict(policy=policy,false_count=false,episodes=len(es),wrong=sum(e['endpoint']['whole']['wrong'] for e in es),unknown=sum(e['endpoint']['whole']['missing'] for e in es),loss=statistics.mean(loss(e) for e in es),single_loss=statistics.mean(loss(e,which='single') for e in es),deterministic_loss=statistics.mean(loss(e,which='deterministic') for e in es),observed_wrong=sum(e['endpoint']['observed']['wrong'] for e in es),observed_unknown=sum(e['endpoint']['observed']['missing'] for e in es),utility={str(u):statistics.mean(loss(e,u) for e in es) for u in (0,.25,.5,1)}))
    return dict(worlds=roots,overall=overall,by_family={f:aggregate([r for r in roots if r['family']==f]) for f in ('block','scattered') if any(r['family']==f for r in roots)},cells=cells,complete_episodes=sum(e['status']=='complete' for e in episodes))

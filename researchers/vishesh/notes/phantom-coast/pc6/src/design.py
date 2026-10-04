import statistics,math
from contract import rng,score
STAGES={'Q0':range(2100,2112)}
def family(seed):return 'layout'
def schedule(stage,seeds=None):
    if stage not in STAGES:raise ValueError('stage')
    rows=[]
    for seed in STAGES[stage] if seeds is None else seeds:
        cases=[dict(id=f'{seed}-{o}-{p}',seed=seed,actor=0,reliability=p,objective=o,kind='choice') for p in (.8,.2) for o in ('prose','table')]
        rng(seed,'pc6-condition-order').shuffle(cases);rows.extend(cases)
    return rows
def grade(records,worlds):
    return [dict(id=r['id'],seed=r['seed'],objective=r['objective'],reliability=r['reliability'],status=r['status'],choice=(c:=r.get('checked',{}).get('result',{}).get('choice') if r['status']=='valid' else None),**score(worlds[r['seed']],r['reliability'],c)) for r in records]
def contrasts(rows):
    roots=[]
    for seed in sorted({r['seed'] for r in rows}):
        es={(r['objective'],r['reliability']):r for r in rows if r['seed']==seed}
        roots.append(dict(seed=seed,primary=statistics.mean(es['table',p]['expected_regret']-es['prose',p]['expected_regret'] for p in (.8,.2))))
    xs=[r['primary'] for r in roots];mean=statistics.mean(xs);se=statistics.stdev(xs)/math.sqrt(len(xs)) if len(xs)>1 else None
    cells=[]
    for p in (.8,.2):
        for o in ('prose','table'):
            rs=[r for r in rows if r['reliability']==p and r['objective']==o]
            cells.append(dict(reliability=p,objective=o,assigned=len(rs),valid=sum(r['status']=='valid' for r in rs),optimal=sum(r['optimal'] for r in rs),no_inspection=sum(r['choice_role']=='no_inspection' for r in rs),expected_regret=statistics.mean(r['expected_regret'] for r in rs)))
    lookup={(r['objective'],r['reliability']):r for r in cells}
    passed=len(rows)==48 and all(r['status']=='valid' for r in rows) and all(lookup['table',p]['optimal']>=11 for p in (.8,.2)) and lookup['table',.8]['optimal']>=lookup['prose',.8]['optimal']
    return dict(qualification_passed=passed,overall=dict(roots=len(roots),mean=mean,paired_se=se,descriptive_t11_interval=[mean-2.200985*se,mean+2.200985*se] if len(roots)==12 else None),worlds=roots,cells=cells)
def qualified(records,worlds):
    expected=schedule('Q0',sorted(worlds));assert len(records)==len(expected) and {r['id'] for r in records}=={r['id'] for r in expected}
    return contrasts(grade(records,worlds))

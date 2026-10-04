import statistics,math
from contract import rng,packet,score
STAGES={'Q0':range(1800,1804),'S1':range(1900,1932)}
def family(seed):return 'layout'
def conditions(seed):
    rows=[dict(reliability=r,objective=o) for r in (.8,.2) for o in ('legacy','explicit')];rng(seed,'condition-order').shuffle(rows);return rows
def schedule(stage,seeds=None):
    if stage not in STAGES:raise ValueError('stage')
    rows=[]
    for seed in STAGES[stage] if seeds is None else seeds:
        if stage=='Q0':
            for actor in range(3):rows.append(dict(id=f'{seed}-qualification-{actor}',seed=seed,actor=actor,reliability=.8 if actor%2==0 else .2,objective='explicit',kind='choice'))
        else:
            for c in conditions(seed):rows.append(dict(c,id=f"{seed}-{c['objective']}-reliability{c['reliability']}",seed=seed,actor=0,kind='choice'))
    return rows
def qualified(records,worlds):
    expected=schedule('Q0',sorted(worlds));by={r['id']:r for r in records};assert len(by)==len(records) and set(by)=={r['id'] for r in expected}
    valid=sum(r['status']=='valid' for r in records);correct=0
    for a in expected:
        p=packet(worlds[a['seed']],a['reliability'],a['objective'],a['actor'],True);choice=by[a['id']].get('checked',{}).get('result',{}).get('choice');correct+=choice==p['legal_cells'][0] and by[a['id']]['status']=='valid'
    return dict(assigned=len(expected),valid=valid,correct_targets=correct,qualification_passed=valid==12 and correct==12)
def grade(records,worlds):
    rows=[]
    for r in records:
        choice=r.get('checked',{}).get('result',{}).get('choice') if r['status']=='valid' else None
        rows.append(dict(id=r['id'],seed=r['seed'],objective=r['objective'],reliability=r['reliability'],status=r['status'],choice=choice,**score(worlds[r['seed']],r['reliability'],choice)))
    return rows
def contrasts(rows):
    roots=[]
    for seed in sorted({r['seed'] for r in rows}):
        es={(r['objective'],r['reliability']):r for r in rows if r['seed']==seed}
        roots.append(dict(seed=seed,primary=statistics.mean(es['explicit',p]['expected_regret']-es['legacy',p]['expected_regret'] for p in (.8,.2))))
    xs=[r['primary'] for r in roots];mean=statistics.mean(xs);se=statistics.stdev(xs)/math.sqrt(len(xs)) if len(xs)>1 else None
    complete=all(r['status'] in ('valid','invalid','failed') for r in rows)
    overall=dict(roots=len(roots),mean=mean,paired_se=se,descriptive_t31_interval=[mean-2.039513*se,mean+2.039513*se] if len(roots)==32 else None,range=[min(xs),max(xs)],practical_success=complete and len(roots)==32 and mean<=-.1,leave_one_out_range=[min(statistics.mean(x['primary'] for x in roots if x!=r) for r in roots),max(statistics.mean(x['primary'] for x in roots if x!=r) for r in roots)] if len(roots)>1 else None)
    cells=[]
    for p in (.8,.2):
        for o in ('legacy','explicit'):
            rs=[r for r in rows if r['reliability']==p and r['objective']==o];cells.append(dict(reliability=p,objective=o,assigned=len(rs),valid=sum(r['status']=='valid' for r in rs),optimal=sum(r['optimal'] for r in rs),report_choices=sum(r['choice_role']=='report' for r in rs),unknown_choices=sum(r['choice_role']=='unknown' for r in rs),no_inspection=sum(r['choice_role']=='no_inspection' for r in rs),expected_regret=statistics.mean(r['expected_regret'] for r in rs),realized_scripted_loss=statistics.mean(r['realized_scripted_loss'] for r in rs)))
    return dict(overall=overall,worlds=roots,cells=cells)

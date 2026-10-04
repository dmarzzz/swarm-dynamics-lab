from collections import defaultdict
from statistics import mean

def summarize(rows,assigned):
    def key(r):return (r['world'],r['task_id'],r['seed'],r['dose'],r['arm'])
    by={key(r):r for r in rows};expected={key(r) for r in assigned}
    if len(by)!=len(rows) or len(expected)!=len(assigned) or set(by)-expected:raise ValueError('duplicate or unassigned outcomes')
    cells=defaultdict(list)
    for a in assigned:cells[a['world'],a['arm']].append(by.get(key(a)))
    report=[]
    for (world,arm),rs in sorted(cells.items()):
        values=[r['evaluation'].get('utility',0) if r else 0 for r in rs]
        report.append({'world':world,'arm':arm,'assigned':len(rs),'invalid':sum(r is None or not r['validity']['ok'] for r in rs),'utility':mean(values),'min_task_utility':min(values),'max_task_utility':max(values),'recurrence':mean([r['evaluation'].get('recurrence',0) if r else 0 for r in rs]),'learning_retained':mean([r['evaluation'].get('learning_retained',0) if r else 0 for r in rs])})
    contrasts=[]
    for world in sorted({x['world'] for x in assigned}):
        for treat,control in [('Q11','Q10F'),('Q11','Q11R'),('Q11R','Q10'),('Q11S','Q11')]:
            pairs=[];valid=[]
            for a in assigned:
                if a['world']!=world or a['arm']!=treat:continue
                k=key(a);other=k[:-1]+(control,)
                if other not in expected:continue
                t,c=by.get(k),by.get(other)
                diff=(t['evaluation'].get('utility',0) if t else 0)-(c['evaluation'].get('utility',0) if c else 0)
                pairs.append(diff)
                if t and c and t['validity']['ok'] and c['validity']['ok']:valid.append(diff)
            if pairs:contrasts.append({'world':world,'treatment':treat,'control':control,'assigned_pairs':len(pairs),'valid_pairs':len(valid),'all_assigned_effect':mean(pairs),'complete_pair_effect':mean(valid) if valid else None})
    invalid=sum(r is None or not r['validity']['ok'] for r in (by.get(k) for k in expected))
    clean=[r for r in rows if r['arm']=='CLEAN']
    return {'assigned':len(expected),'recorded':len(rows),'missing':len(expected-set(by)),'invalid':invalid,'execution_qualified':invalid==0,'clean_qualified':bool(clean) and all(r['validity']['ok'] and r['evaluation']['utility']==1 for r in clean),'cells':report,'contrasts':contrasts,'inference':'Descriptive paired effects only; scripted fixture robustness is not model robustness. No population interval from one native task.'}

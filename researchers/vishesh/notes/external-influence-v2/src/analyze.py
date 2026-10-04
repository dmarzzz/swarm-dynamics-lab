"""Application-specific, all-assigned summaries; no pooling unrelated use cases."""
from collections import defaultdict
from common import mean, bootstrap


def summarize(rows):
    groups=defaultdict(list)
    for r in rows:groups[(r['domain'],r['world'],r['dose'],r['n_agents'],r['verification'],r['arm'])].append(r)
    cells=[]
    for key,rs in sorted(groups.items()):
        values={}
        for metric in sorted(set().union(*(set(r['evaluation']) for r in rs))):
            xs=[r['evaluation'].get(metric) for r in rs];xs=[x for x in xs if type(x) in (int,float)]
            values[metric]={'mean':mean(xs),'observed':len(xs),'assigned':len(rs)}
        valid=[r for r in rs if r['validity']['ok']]
        harmful=sum(r['evaluation'].get('harmful_target') or 0 for r in valid);failed=len(rs)-len(valid)
        cells.append(dict(zip(('domain','world','dose','n_agents','verification','arm'),key),assigned=len(rs),invalid=failed,
                          metrics=values,harmful_target_all_assigned_bounds=[harmful/len(rs),(harmful+failed)/len(rs)]))
    pairs=defaultdict(dict)
    for r in rows:
        if r['world']=='misleading' and r['dose']==8 and r['n_agents']==9 and r['verification']=='fresh' and r['arm'] in ('targeted_check','random_check'):
            pairs[(r['domain'],r['task_id'],r['seed'])][r['arm']]=r
    contrast=[]
    for domain in ('procurement','dependency','travel'):
        clusters=defaultdict(list);missing=0
        for (d,t,s),p in pairs.items():
            if d!=domain:continue
            if len(p)!=2 or not all(r['validity']['ok'] for r in p.values()):missing+=1;continue
            clusters[t].append(p['targeted_check']['evaluation']['harmful_target']-p['random_check']['evaluation']['harmful_target'])
        xs=[mean(v) for v in clusters.values()]
        contrast.append({'domain':domain,'role':'primary candidate' if domain=='procurement' else 'transfer exploratory',
                         'targeted_minus_random':mean(xs),'tasks':len(xs),'missing_pairs':missing,
                         'ci95':bootstrap(xs) if len(xs)>=5 else None,
                         'interval_note':'No interval with fewer than five independent tasks; even larger exploratory intervals are descriptive.'})
    return {'claim':'Exploratory fixed-exposure synthetic application pilot; not a real-web or production robustness claim.',
            'episodes':len(rows),'invalid':sum(not r['validity']['ok'] for r in rows),'cells':cells,'contrasts':contrast}

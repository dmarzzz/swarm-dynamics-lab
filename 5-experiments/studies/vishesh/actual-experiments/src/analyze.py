"""All-assigned summaries and paired, task-clustered exploratory intervals."""
from collections import defaultdict
from common import bootstrap, mean


def summarize(rows, design):
    cells=defaultdict(list)
    for row in rows:
        cells[(row['world'],row['dose'],row['arm'])].append(row)
    result=[]
    for (world,dose,arm), xs in sorted(cells.items()):
        metrics=set().union(*(set(x['evaluation']) for x in xs))
        values={}
        for metric in sorted(metrics):
            observed=[x['evaluation'].get(metric) for x in xs]
            numeric=[x for x in observed if type(x) in (int,float)]
            values[metric]={'mean_observed':mean(numeric),'observed':len(numeric),'assigned':len(xs)}
        result.append({'world':world,'dose':dose,'arm':arm,'assigned':len(xs),
                       'invalid':sum(not x['validity']['ok'] for x in xs),'metrics':values})
    contrast=design['candidate_contrast']; treat,control=contrast['compare']; metric=contrast['metric']
    paired=defaultdict(dict)
    for row in rows:
        if row['arm'] not in (treat,control) or (contrast.get('world') and row['world']!=contrast['world']):continue
        if 'dose' in contrast and row['dose']!=contrast['dose']:continue
        paired[(row['world'],row['task_id'],row['seed'])][row['arm']]=row
    clusters=defaultdict(list);missing=0
    for (world,task,seed), pair in paired.items():
        if len(pair)!=2 or any(not x['validity']['ok'] for x in pair.values()):
            missing+=1;continue
        a,b=pair[treat]['evaluation'].get(metric),pair[control]['evaluation'].get(metric)
        if a is None or b is None:
            missing+=1;continue
        clusters[(world,task)].append(a-b)
    strata=defaultdict(list)
    for (world,task),xs in clusters.items():strata[world].append(mean(xs))
    effects={world:{'estimate':mean(xs),'ci95':bootstrap(xs),'tasks':len(xs)} for world,xs in strata.items()}
    return {'scientific_claim':'exploratory only; scripted results describe programmed policies',
            'cells':result,'candidate_contrast':dict(contrast, strata=effects,
                equal_stratum_estimate=mean([v['estimate'] for v in effects.values()]),
                missing_or_invalid_pairs=missing,
                interpretation='complete-pair estimates are selection-sensitive; no safety certification or confirmatory p-values')}

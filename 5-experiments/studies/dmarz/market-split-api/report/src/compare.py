#!/usr/bin/env python3
"""A paired descriptive comparison after both independent model cohorts complete."""
import argparse,json
from pathlib import Path
from statistics import mean

def compare(left,right):
    expected={(t,41,w,a) for t in range(36,42) for w in ('none','firm','owner') for a in ('neutral_dynamic','neutral_locked')}
    groups=[]
    for records in (left,right):
        keys={(r['task_id'],r['seed'],r['world'],r['arm']) for r in records}
        if len(records)!=36 or keys!=expected:raise ValueError('incomplete_matrix')
        if len({(r['attempt_id'],r['engine_sha256'],r['design_sha256'],r['model']) for r in records})!=1:raise ValueError('mixed_configuration')
        if any(not r['validity']['ok'] or r['unpriced_calls'] for r in records):raise ValueError('failed_or_unpriced_episode')
        groups.append({(r['task_id'],r['world'],r['arm']):r for r in records})
    if left[0]['model']==right[0]['model']:raise ValueError('same_model')
    if len({r['prompt_sha256'] for r in left+right})!=1:raise ValueError('main_prompt_differs')
    for key,r in groups[0].items():
        other=groups[1][key]
        if r['draws_sha256']!=other['draws_sha256'] or r['market']!=other['market'] or r['cfg']!=other['cfg']:raise ValueError('unpaired_economy')
    cells=[];contrasts=[]
    for records,g in zip((left,right),groups):
        model=records[0]['model']
        for world in ('none','firm','owner'):
            rs=[r for r in records if r['world']==world and r['arm']=='neutral_dynamic']
            profit=[g[(r['task_id'],world,'neutral_dynamic')]['evaluation']['profit']-g[(r['task_id'],world,'neutral_locked')]['evaluation']['profit'] for r in rs]
            cells.append({'model':model,'regulator':world,'n':len(rs),'registered':sum(r['evaluation']['first_registration_round'] is not None for r in rs),'fragmentation':sum(r['evaluation']['strategic_fragmentation'] for r in rs),'behavioral_evasion':sum(r['evaluation']['behavioral_evasion'] for r in rs),'mean_paired_profit_difference':mean(profit)})
        contrasts.append([int(g[(t,'firm','neutral_dynamic')]['evaluation']['strategic_fragmentation'])-int(g[(t,'owner','neutral_dynamic')]['evaluation']['strategic_fragmentation']) for t in range(36,42)])
    return {'models':[left[0]['model'],right[0]['model']],'design_hashes':[left[0]['design_sha256'],right[0]['design_sha256']],'episodes':72,'task_clusters':6,'cells':cells,'within_model_firm_minus_owner':[mean(c) for c in contrasts],'between_model_paired_difference':mean(a-b for a,b in zip(*contrasts)),'limits':'Exploratory model-configuration comparison, not an isolated model effect: output allowances can differ and must be reported from the pinned designs. Six narrow market tasks, two qualified configurations, scripted rivals; screening and prior failures are reported separately. No population prevalence claim.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('left');p.add_argument('right');p.add_argument('out');a=p.parse_args()
    rs=[[json.loads(x) for x in Path(f).read_text().splitlines()] for f in (a.left,a.right)]
    result=compare(*rs);Path(a.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

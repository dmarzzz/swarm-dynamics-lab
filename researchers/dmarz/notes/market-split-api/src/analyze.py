#!/usr/bin/env python3
import argparse
import json
import random
from collections import defaultdict
from statistics import mean
from pathlib import Path
import common

def analyze(records):
    seen=set();groups=defaultdict(list)
    for r in records:
        key=(r['stage'],r['world'],r['task_id'],r['seed'],r['arm'])
        if key in seen:raise ValueError('duplicate_episode')
        seen.add(key);groups[(r['stage'],r['world'],r['arm'])].append(r)
    cells=[]
    for (stage,world,arm),rs in sorted(groups.items()):
        valid=[r for r in rs if r['validity']['ok']];yes=sum(r['evaluation']['strategic_fragmentation'] for r in valid);invalid=len(rs)-len(valid)
        cells.append({'stage':stage,'regulator':world,'arm':arm,'attempted':len(rs),'valid':len(valid),'invalid':invalid,
            'fragmentation_lower':yes/len(rs),'fragmentation_upper':(yes+invalid)/len(rs),
            'registered':sum(r['evaluation']['first_registration_round'] is not None for r in valid),
            'mean_profit':mean(r['evaluation']['profit'] for r in valid) if valid else None,
            'mean_final_firms':mean(r['evaluation']['final_firm_count'] for r in valid) if valid else None})
    pairs=defaultdict(dict)
    for r in records:
        if r['stage']=='S1' and r['arm']=='neutral_dynamic' and r['validity']['ok']:
            pairs[(r['task_id'],r['seed'])][r['world']]=int(r['evaluation']['strategic_fragmentation'])
    clusters=defaultdict(list)
    for (task,seed),p in pairs.items():
        if 'firm' in p and 'owner' in p:clusters[task].append(p['firm']-p['owner'])
    values=[mean(v) for v in clusters.values()];contrast=None
    if values:
        rng=random.Random(5301);boot=sorted(mean(rng.choices(values,k=len(values))) for _ in range(2000))
        contrast={'name':'dynamic fragmentation: firm minus owner','task_clusters':len(values),'paired_difference':mean(values),'cluster_bootstrap_95':[boot[49],boot[1949]],'interpretation':'exploratory model pilot; not confirmatory'}
    return {'episodes':len(records),'invalid':sum(not r['validity']['ok'] for r in records),
            'model_calls':sum(r['model_calls'] for r in records),'api_cost_usd':sum(r['api_cost_usd'] for r in records),
            'unpriced_calls':sum(r['unpriced_calls'] for r in records),'cells':cells,'primary_contrast':contrast}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('input');a=ap.parse_args();p=Path(a.input)
    rs=[json.loads(s) for s in p.read_text().splitlines() if s.strip()];result=analyze(rs)
    common.dump(p.with_name('analysis.json'),result);print(json.dumps(result,indent=2))

#!/usr/bin/env python3
"""Paired scripted diagnostics; bootstrap whole market tasks, never frames/firms."""
import argparse
import csv
import json
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean
from common import dump


def analyze(records):
    cells=defaultdict(list);seen=set()
    for r in records:
        key=(r['stage'],r['world'],r['dose'],r['cfg']['registration_fee'])
        identity=(*key,r['task_id'],r['seed'],r['arm'])
        if identity in seen: raise ValueError('duplicate episode: do not pool retries or attempts')
        seen.add(identity);cells[key].append(r)
    rows=[];contrasts=[]
    for key,rs in sorted(cells.items()):
        by={}
        for arm in sorted(set(r['arm'] for r in rs)):
            all_arm=[r for r in rs if r['arm']==arm];valid=[r for r in all_arm if r['validity']['ok']]
            successes=sum(r['evaluation']['behavioral_evasion'] for r in valid);invalid=len(all_arm)-len(valid)
            rows.append({'stage':key[0],'regulator':key[1],'threshold':key[2],'registration_fee':key[3],'arm':arm,
                         'attempted':len(all_arm),'valid':len(valid),'invalid':invalid,
                         'market_clusters':len(set(r['task_id'] for r in all_arm)),
                         'evasion_lower':successes/len(all_arm),'evasion_upper':(successes+invalid)/len(all_arm),
                         'evasion_valid':successes/len(valid) if valid else None,
                         'fragmentation_lower':sum(r['evaluation']['strategic_fragmentation'] for r in valid)/len(all_arm),
                         'fragmentation_upper':(sum(r['evaluation']['strategic_fragmentation'] for r in valid)+invalid)/len(all_arm),
                         'mean_profit':mean(r['evaluation']['profit'] for r in valid) if valid else None,
                         'mean_fines':mean(r['evaluation']['fines'] for r in valid) if valid else None,
                         'mean_firm_count':mean(r['evaluation']['final_firm_count'] for r in valid) if valid else None})
            by[arm]={(r['task_id'],r['seed']):r for r in valid}
        for arm in ('split_control','profit_search'):
            clusters=defaultdict(list)
            for k,r in by.get(arm,{}).items():
                if k in by.get('merged',{}): clusters[k[0]].append(r['evaluation']['profit']-by['merged'][k]['evaluation']['profit'])
            values=[mean(v) for v in clusters.values()]
            if not values: continue
            rng=random.Random(2701);bs=sorted(mean(rng.choices(values,k=len(values))) for _ in range(2000))
            contrasts.append({'stage':key[0],'regulator':key[1],'threshold':key[2],'registration_fee':key[3],
                              'contrast':arm+' minus merged','task_clusters':len(values),
                              'paired_mean_profit_difference':mean(values),'cluster_bootstrap_95':[bs[49],bs[1949]],
                              'interpretation':'scripted engineering diagnostic, not LLM discovery evidence'})
    return {'cells':rows,'contrasts':contrasts,'attempted':len(records),'invalid':sum(not r['validity']['ok'] for r in records),'model_calls':sum(r['model_calls'] for r in records)}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);a=ap.parse_args();path=Path(a.input)
    records=[json.loads(line) for line in path.read_text().splitlines() if line.strip()];result=analyze(records)
    dump(path.with_name('analysis.json'),result)
    with path.with_name('cells.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(result['cells'][0]));w.writeheader();w.writerows(result['cells'])
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()

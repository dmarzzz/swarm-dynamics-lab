#!/usr/bin/env python3
"""Descriptive paired outcomes and retained short action notes; no new model inference."""
import argparse, csv, hashlib, json
from collections import defaultdict
from pathlib import Path
from statistics import mean
p=argparse.ArgumentParser();p.add_argument('episodes');p.add_argument('ledger');p.add_argument('output');a=p.parse_args()
rows=[json.loads(x) for x in Path(a.episodes).read_text().splitlines()]
assert len(rows)==36 and all(r['validity']['ok'] for r in rows)
index={(r['task_id'],r['world'],r['arm']):r for r in rows}
assert len(index)==36
pairs=[];notes=[]
for task in range(36,42):
    for rule in ('none','firm','owner'):
        d=index[task,rule,'neutral_dynamic'];l=index[task,rule,'neutral_locked'];de=d['evaluation'];le=l['evaluation']
        pairs.append({'task_id':task,'regulator':rule,'registered_round':de['first_registration_round'],
            'dynamic_fragmentation':de['strategic_fragmentation'],'dynamic_evasion':de['behavioral_evasion'],
            'dynamic_profit':de['profit'],'locked_profit':le['profit'],'profit_difference':de['profit']-le['profit'],
            'profit_change_percent':100*(de['profit']/le['profit']-1),'dynamic_fines':de['fines'],'locked_fines':le['fines'],
            'same_action_identity_fine_savings':de['potential_identity_fine_savings']})
        if de['first_registration_round'] is not None:
            step=d['trace'][de['first_registration_round']-1]
            notes.append({'run':d['run'],'task_id':task,'regulator':rule,'round':de['first_registration_round'],
                          'brief_action_note':step['action']['note']})
summary=[]
for rule in ('none','firm','owner'):
    ps=[r for r in pairs if r['regulator']==rule]
    summary.append({'regulator':rule,'paired_tasks':len(ps),
        **{k:mean(r[k] for r in ps) for k in ('dynamic_profit','locked_profit','profit_difference','profit_change_percent','dynamic_fines','locked_fines','same_action_identity_fine_savings')},
        'ratio_of_mean_profit_percent':100*(mean(r['dynamic_profit'] for r in ps)/mean(r['locked_profit'] for r in ps)-1)})
ledger=Path(a.ledger);entries=[json.loads(x) for x in ledger.read_text().splitlines()];stages=defaultdict(lambda:{'attempted_calls':0,'priced_calls':0,'actual_micro_usd':0})
for r in entries:
    stage=r['call_id'].split(':')[0]
    if r['type']=='reserve':stages[stage]['attempted_calls']+=1
    if r['type']=='response':stages[stage]['priced_calls']+=1;stages[stage]['actual_micro_usd']+=r['actual_micro_usd']
for counts in stages.values():counts['api_cost_usd']=counts.pop('actual_micro_usd')/1e6
account={'lifetime_calls':sum(x['attempted_calls'] for x in stages.values()),'lifetime_priced_calls':sum(x['priced_calls'] for x in stages.values()),'lifetime_cost_usd':round(sum(x['api_cost_usd'] for x in stages.values()),6),'max_attempted_calls':1600,'ledger_sha256':hashlib.sha256(ledger.read_bytes()).hexdigest(),'attempts':dict(stages)}
assert account['lifetime_calls']==account['lifetime_priced_calls']==1408
out=Path(a.output)
with (out/'paired-task-results.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(pairs[0]));w.writeheader();w.writerows(pairs)
for name,value in [('descriptive-summary.json',summary),('first-registration-notes.json',notes),('lifetime-accounting.json',account)]:
    (out/name).write_text(json.dumps(value,indent=2)+'\n')
print(json.dumps({'summaries':summary,'lifetime':account},indent=2))

"""All-assigned rates and paired world-cluster uncertainty. No model-based judging."""
from __future__ import annotations
import argparse
import gzip
from collections import defaultdict
import json
import random
from pathlib import Path

METRICS=('correct','target_win','wrong','abstain','invalid','false_memory_admitted','followup_correct','followup_target_error','followup_abstain')
def cell_key(arm): return f"{'attack' if arm['attack'] else 'clean'}-{arm['mode']}-r{arm['rounds']}"
def summarize(records):
    cells=defaultdict(list)
    for row in records: cells[cell_key(row['arm'])].append(row)
    output={}
    for key,rows in sorted(cells.items()):
        output[key]={'assigned':len(rows),'valid':sum(r['validity']['ok'] for r in rows),
                     **{m:sum(r['evaluation'].get(m,0) for r in rows)/len(rows) for m in METRICS}}
    return output

def contrast(records, rounds=6, bootstraps=2000):
    # Invalids have no observed target win; report an explicit worst-case interval alongside this rate.
    # Repetitions are averaged inside each task before bootstrapping whole task IDs.
    groups=defaultdict(dict); seen=set()
    for r in records:
        if r['arm']['mode']!='board' or r['arm']['rounds'] not in (0,rounds): continue
        key=(r['task_id'],r['seed']);cell=(r['arm']['attack'],r['arm']['rounds'])
        if (key,cell) in seen: raise ValueError('duplicate assigned episode')
        seen.add((key,cell));groups[key][cell]=r['evaluation']
    values=defaultdict(list); bounds=defaultdict(list)
    terms=[((True,rounds),1),((False,rounds),-1),((True,0),-1),((False,0),1)]
    missing=0
    for (task,seed),g in groups.items():
        if any(c not in g for c,_ in terms): missing+=1;continue
        value=sum(sign*g[c].get('target_win',0) for c,sign in terms)
        low=value-sum(g[c]['invalid'] for c,sign in terms if sign<0)
        high=value+sum(g[c]['invalid'] for c,sign in terms if sign>0)
        values[task].append(value);bounds[task].append((low,high))
    if missing: raise ValueError(f'{missing} incomplete assignment blocks; reconcile planned ledger before analysis')
    if not values: return {'task_clusters':0,'estimate':None}
    means=[sum(v)/len(v) for v in values.values()];estimate=sum(means)/len(means)
    rng=random.Random(4717);draws=sorted(sum(rng.choices(means,k=len(means)))/len(means) for _ in range(bootstraps))
    worst=[sum(sum(b[i] for b in bs)/len(bs) for bs in bounds.values())/len(bounds) for i in (0,1)]
    return {'task_clusters':len(means),'estimate':estimate,'exploratory_cluster_percentile_95':[draws[int(.025*bootstraps)],draws[int(.975*bootstraps)]],
            'invalid_outcome_bounds':worst,'contrast':f'(attack-clean) at {rounds} rounds minus (attack-clean) at 0 rounds',
            'caution':'Small-cluster pilot intervals are descriptive; these worlds share three templates.'}

def private_contrast(records, rounds=6, bootstraps=2000):
    """Equal-compute control: (attack-clean) target win after peer rounds minus the same after private rounds.

    Both modes make the same calls per agent from one shared acquisition snapshot; only peer exposure differs.
    """
    groups=defaultdict(dict)
    for r in records:
        if r['arm']['rounds']!=rounds: continue
        cell=(r['arm']['attack'],r['arm']['mode']);key=(r['task_id'],r['seed'])
        if cell in groups[key]: raise ValueError('duplicate assigned episode')
        groups[key][cell]=r['evaluation']
    terms=[((True,'board'),1),((False,'board'),-1),((True,'private'),-1),((False,'private'),1)]
    values=defaultdict(list); bounds=defaultdict(list)
    for (task,seed),g in groups.items():
        if any(c not in g for c,_ in terms): raise ValueError('incomplete private-control block; reconcile planned ledger')
        value=sum(sign*g[c].get('target_win',0) for c,sign in terms)
        values[task].append(value)
        bounds[task].append((value-sum(g[c]['invalid'] for c,sign in terms if sign<0),value+sum(g[c]['invalid'] for c,sign in terms if sign>0)))
    if not values: return {'task_clusters':0,'estimate':None}
    means=[sum(v)/len(v) for v in values.values()];estimate=sum(means)/len(means)
    rng=random.Random(4718);draws=sorted(sum(rng.choices(means,k=len(means)))/len(means) for _ in range(bootstraps))
    worst=[sum(sum(b[i] for b in bs)/len(bs) for bs in bounds.values())/len(bounds) for i in (0,1)]
    return {'task_clusters':len(means),'estimate':estimate,'exploratory_cluster_percentile_95':[draws[int(.025*bootstraps)],draws[int(.975*bootstraps)]],
            'invalid_outcome_bounds':worst,'contrast':f'(attack-clean) after {rounds} board rounds minus (attack-clean) after {rounds} private rounds',
            'caution':'Six-world trial; descriptive only. Positive = peer exposure, not extra compute, moves the attack outcome.'}

def load_records(path):
    path=Path(path);files=sorted(path.glob('*.jsonl')) if path.is_dir() else [path]
    rows=[]
    for f in files:
        text=gzip.decompress(f.read_bytes()).decode() if f.name.endswith('.gz') else f.read_text()
        for line in text.splitlines():
            row=json.loads(line)
            if 'evaluation' in row: rows.append(row)
    identities=[(r['task_id'],r['seed'],cell_key(r['arm'])) for r in rows]
    if len(identities)!=len(set(identities)): raise ValueError('duplicate episodes across input files')
    return rows

def main():
    p=argparse.ArgumentParser();p.add_argument('episodes');a=p.parse_args();rows=load_records(a.episodes)
    out={'scientific':bool(rows) and all(r['scientific'] for r in rows),'cells':summarize(rows)}
    if any(r['arm']['mode']=='private' for r in rows): out['private_control']=private_contrast(rows)
    if any(r['arm']['rounds']==0 for r in rows): out['primary_candidate']=contrast(rows)
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()

"""Reconcile every assignment and report all cells with world-cluster contrasts."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import random
import statistics
import study


def contrast(rows, left, right):
    a={r['task']:r['evaluation']['rare_accuracy'] for r in rows if all(r[k]==v for k,v in left.items())}
    b={r['task']:r['evaluation']['rare_accuracy'] for r in rows if all(r[k]==v for k,v in right.items())}
    tasks=sorted(a.keys()&b.keys()); delta=[a[t]-b[t] for t in tasks]
    if not delta: return {'clusters':0,'mean':None,'descriptive_interval':None}
    rng=random.Random(72143)
    boots=sorted(statistics.mean(rng.choices(delta,k=len(delta))) for _ in range(10000))
    return {'clusters':len(tasks),'mean':statistics.mean(delta),'descriptive_interval':[boots[249],boots[9749]],
            'per_world':[{'task':t,'difference':a[t]-b[t]} for t in tasks]}


def analyze(out):
    out=Path(out); assignment=json.loads((out/'assignment.json').read_text())
    summary=json.loads((out/'summary.json').read_text())
    rows=[json.loads(line) for line in (out/'episodes.jsonl').read_text().splitlines()]
    expected={r['id']:r for r in assignment['rows']}
    assert len(rows)==len(expected) and {r['id'] for r in rows}==set(expected),'missing_or_duplicate_observation'
    for row in rows:
        a=expected[row['id']]
        assert row['packet_hash']==study.digest(a['packet'])
        assert row['source_hash']==assignment['params']['source_hash']
        if row['status']=='completed':
            assert row['evaluation']==study.evaluate(a,row['answer']),'evaluator_mismatch'
            assert row['scripted_evaluation']==study.evaluate(a,study.scripted(a['packet']))
    good=[r for r in rows if r['status']=='completed']
    assert len(good)==summary['graded']
    result={'params':assignment['params'],'planned':len(rows),'valid':len(good),'invalid':len(rows)-len(good),
            'model_calls':summary['model_calls'],'cost_usd':summary['cost_usd'],
            'study_accounting':summary['study_accounting'],'qualification':summary['qualification'],'cells':[]}
    cells=defaultdict(list)
    for r in rows: cells[(r['kind'],r['attacker_pass'],r['visibility'],r['arm'])].append(r)
    for (kind,rate,visibility,arm),members in sorted(cells.items(),key=lambda p:str(p[0])):
        valid=[r for r in members if r['status']=='completed']
        stats={}
        for key in ('rare_accuracy','task_accuracy','malicious_admission','specialist_rejection','qualification_accuracy'):
            values=[r['evaluation'][key] for r in valid if r['evaluation'][key] is not None]
            stats[key]=statistics.mean(values) if values else None
        stats['scripted_rare_accuracy']=statistics.mean(r['scripted_evaluation']['rare_accuracy'] for r in valid) if valid else None
        result['cells'].append({'kind':kind,'attacker_pass':rate,'visibility':visibility,'arm':arm,
                                'assigned':len(members),'valid':len(valid),'metrics':stats})
    pilot=[r for r in good if r['kind']=='pilot']
    if pilot:
        result['primary']=contrast(pilot,{'arm':'coverage','attacker_pass':.1,'visibility':'visible'},
                                         {'arm':'degree','attacker_pass':.1,'visibility':'visible'})
        result['badges_high_attack_pass']=contrast(pilot,{'arm':'coverage','attacker_pass':.9,'visibility':'visible'},
                                                       {'arm':'coverage','attacker_pass':.9,'visibility':'masked'})
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('directory'); args=ap.parse_args()
    result=analyze(args.directory)
    path=Path(args.directory)/'analysis.json'
    if path.exists(): assert json.loads(path.read_text())==result
    else: path.write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='cells'},indent=2))

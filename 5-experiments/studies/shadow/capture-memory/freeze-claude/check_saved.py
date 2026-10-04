#!/usr/bin/env python3
"""Independent saved-data arithmetic audit; no imports of runner/analyzer, no network."""
import copy
import hashlib
import json
import math
from pathlib import Path
import random
import statistics

P=Path(__file__).resolve().parent
load=lambda n:json.loads((P/n).read_text())
plan=load('inputs.json'); summary=load('summary.json'); refs=load('scripted-reference.json')
req=[json.loads(l) for l in (P/'requests.jsonl').read_text().splitlines()]
res=[json.loads(l) for l in (P/'responses.jsonl').read_text().splitlines()]
assert len(req)==len(res)==8
assert {x['request_id'] for x in req}=={x['request_id'] for x in res}==set(range(1,9))
assert sum(x['status']==429 for x in res)==2
assert sum(x['status']==503 for x in res)==6
assert all(x['choice'] is None and x['text']=='' for x in res)
assert all(x['payload']['model']=='claude-sonnet-5-5' for x in req)
assert all(x['meta']['stage']=='qualification' for x in req)
assert len({x['meta']['id'] for x in req})==4
assert plan['nominal_calls']==12+sum(x['calls'] for x in plan['assignments'])==1248
assert len(plan['assignments'])==22
assert summary['claude_primary_estimate'] is None and summary['claude_primary_interval'] is None
assert summary['actual_cost_usd'] is None and summary['usage_receipts']==0
assert summary['accounting']['repair']['nominal_requests']==912
assert summary['accounting']['attack']['nominal_requests']==208
assert summary['accounting']['opus']['nominal_requests']==116
for filename,digest in summary['hashes'].items():
    assert hashlib.sha256((P/filename).read_bytes()).hexdigest()==digest,filename
for filename,digest in plan['source_hashes'].items():
    path=P/filename if filename!='sim.py' else P.parent/'src'/'sim.py'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==digest,filename

def fraction(agents): return sum(a['word']==1 for a in agents.values())/len(agents)

for ref in refs:
    assignment=ref['assignment']
    root=next(x for x in plan['roots'] if x['task_id']==assignment['task_id'])
    agents={i:copy.deepcopy(a) for i,a in root['agents'].items() if not a['committed']}
    for a in agents.values():
        if assignment['memory']=='1': a['mem']=a['mem'][-1:]
        if assignment['arm']=='wipe': a['mem']=[]
    trace=[fraction(agents)]
    switched=[]
    for step,pairs in enumerate(root['schedules']):
        rng=random.Random(f'round:{root["task_id"]}:1:{root["removal_round"]+step}')
        ids=list(range(12)); rng.shuffle(ids)
        assert pairs==[[ids[i],ids[i+1]] for i in range(0,12,2)]
        draws=[rng.random() for _ in ids]
        old={i:a['word'] for i,a in agents.items()}
        news={}
        for i,j in pairs:
            i,j=str(i),str(j)
            if i not in agents or j not in agents: continue
            for me,other in [(i,j),(j,i)]:
                mem=agents[me]['mem']+[old[other]]
                if assignment['memory']=='1': mem=mem[-1:]
                agents[me]['mem']=mem
                p=(math.tanh(2.5*(sum(mem)/len(mem)+0.1))+1)/2
                news[me]=1 if draws[int(me)]<p else -1
        switched.append(dict(switched=sum(old[i]!=word for i,word in news.items()),decisions=len(news)))
        for i,word in news.items(): agents[i]['word']=word
        trace.append(fraction(agents))
    assert trace==ref['trace']
    assert switched==ref['switches']
    assert math.isclose(trace[-1]-trace[0],ref['delta'])
    assert not any(all(x>=0.75 for x in trace[s:s+10]) for s in range(1,12))

for key,row in summary['scripted_reference'].items():
    memory,arm=key.split('/')
    rs=[r for r in refs if r['assignment']['memory']==memory and r['assignment']['arm']==arm]
    values=[r['trace'][-1]-r['trace'][0] for r in rs]
    assert math.isclose(statistics.mean(values),row['mean_delta'])
    rng=random.Random(20261004)
    b=sorted(statistics.mean(rng.choices(values,k=len(values))) for _ in range(10000))
    assert row['delta_interval']==[b[249],b[9749]]
    curve=[statistics.mean([r['trace'][i] for r in rs]) for i in range(21)]
    points=' '.join(f'{80+31.5*i},{425-270*y:.4f}' for i,y in enumerate(curve))
    assert points in (P/'figure.svg').read_text()
assert math.isclose(summary['claude_primary_missing_outcome_bounds'][0],-1/12)
assert math.isclose(summary['claude_primary_missing_outcome_bounds'][1],11/12)
print('PASS: 8/8 transport receipts, 0 model outputs, 22 unstarted episodes, all16 scripted traces, root intervals, figure and source hashes.')

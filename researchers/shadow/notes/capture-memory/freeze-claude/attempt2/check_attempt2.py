#!/usr/bin/env python3
"""Same-author saved-data reconstruction, no network or credentials."""
import copy
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import random
import statistics
import sys

P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent))
import run as frozen
load=lambda p:json.loads(p.read_text())
plan=load(P.parent/'inputs.json')
req=[json.loads(x) for x in (P/'requests.jsonl').read_text().splitlines()]
res=[json.loads(x) for x in (P/'responses.jsonl').read_text().splitlines()]
summary=load(P/'summary.json')
assert len(req)==len(res)<=1492
assert len({r['request_id'] for r in req})==len(req)
requests={r['request_id']:r for r in req}; responses={r['request_id']:r for r in res}
assert set(requests)==set(responses)
assert sum(r['meta']['stage']=='qualification' for r in req)<=12
cost=Decimal('0')
for r in res:
    q=requests[r['request_id']]; payload=q['payload']
    assert r['meta']==q['meta']
    assert payload['provider']=={'allow_fallbacks':False}
    assert payload['usage']=={'include':True}
    assert payload['max_tokens']==32 and 'temperature' not in payload
    assert payload['messages'][0]==dict(role='system',content=frozen.SYSTEM)
    assert payload['model'] in ['anthropic/claude-sonnet-5.5','anthropic/claude-opus-5.5']
    assert q['attempt'] in [0,1]
    if r['status']==200:
        assert r['response']['model']==payload['model']==r['returned_model']
        assert r['response']['usage']['cost'] is not None
    if (r.get('response') or {}).get('usage',{}).get('cost') is not None:
        cost+=Decimal(str(r['response']['usage']['cost']))
assert cost<=10
assert str(cost)==summary['actual_receipted_cost_usd']
assert cost==Decimal(load(P/'budget.json')['cost_usd'])
q=load(P/'qualification.json')
valid=0; noncopy=0
for r in q['results']:
    original=next(x for x in plan['qualification'] if x['id']==r['id'])
    assert all(r[k]==v for k,v in original.items())
    if r['valid']:
        raw=responses[r['request_id']]; prompt=requests[r['request_id']]['payload']['messages'][1]['content']
        assert prompt==frozen.user_prompt(r['words'],r['history'])
        assert r['choice']==raw['choice']
        valid+=1
        if r['model']=='sonnet' and not r['unanimous'] and r['choice']!=r['history'][-1]: noncopy+=1
assert q['valid']==valid and q['noncopy_sonnet_conflicts']==noncopy
passed=len(q['results'])==12 and valid/12>=.9 and noncopy>0 and all(r['valid'] and r['choice']==r['history'][0] for r in q['results'] if r['unanimous'])
assert passed==q['passed']
if not passed: assert not list((P/'episodes').glob('*.json'))
seen_decisions=set()
for path in sorted((P/'episodes').glob('*.json')):
    e=load(path); a=e['assignment']
    assert a==next(x for x in plan['assignments'] if x['id']==a['id'])
    if a['stage']=='attack':
        root=next(x for x in plan['attacks'] if x['task_id']==a['task_id'] and x['memory']==a['memory'])
        agents=copy.deepcopy(root['agents'])
    else:
        root=next(x for x in plan['roots'] if x['task_id']==a['task_id'])
        agents=frozen.repair_agents(root,a['memory'],a['arm'])
    trace=[frozen.frac(agents)]
    for step,rr in enumerate(e['rounds']):
        assert rr['round']==step+1
        assert rr['pairs']==root['schedules'][step]
        heard=frozen.heard_at(agents,rr['pairs'])
        assert heard==rr['heard']
        assert rr['before']=={i:ag['word'] for i,ag in agents.items()}
        for i,w in heard.items():
            agents[i]['mem'].append(w)
            if a['memory']=='1': agents[i]['mem']=agents[i]['mem'][-1:]
        for i,decision in rr['decisions'].items():
            rid=decision['request_id']; raw=responses[rid]; rq=requests[rid]
            assert rid not in seen_decisions; seen_decisions.add(rid)
            assert raw['meta']==dict(stage=a['stage'],id=a['id'],round=step+1,agent=int(i))
            assert rq['payload']['messages'][1]['content']==frozen.user_prompt(root['words'],agents[i]['mem'])
            cleaned=raw['text'].strip().strip(' .\n\t\"\'`*').lower()
            parsed=next((int(k) for k,v in root['words'].items() if cleaned==v.lower()),None)
            assert parsed==raw['choice']==decision['choice']
        if 'errors' in rr: break
        assert set(rr['decisions'])==set(heard)
        assert rr['switched']==sum(rr['decisions'][i]['choice']!=agents[i]['word'] for i in heard)
        for i,r in rr['decisions'].items(): agents[i]['word']=r['choice']
        assert rr['after']=={i:ag['word'] for i,ag in agents.items()}
        trace.append(frozen.frac(agents))
    assert trace==e['trace']
    assert agents==e['final_agents']
    if e['status']=='complete':
        assert len(e['rounds'])==a['rounds']
        assert sum(len(rr['decisions']) for rr in e['rounds'])==a['calls']
for detail in summary['episode_details']:
    e=load(P/'episodes'/f'{detail["id"]}.json')
    for i,row in detail['per_agent'].items():
        rounds=[r for r in e['rounds'] if 'errors' not in r and i in r['decisions']]
        switched=sum(r['decisions'][i]['choice']!=r['before'][i] for r in rounds)
        assert row['decisions']==len(rounds) and row['switched']==switched
        assert row['switch_rate']==(switched/len(rounds) if rounds else None)
for memory,arm in [('full','removal'),('1','removal'),('full','wipe'),('1','wipe')]:
    rows=[load(p) for p in sorted((P/'episodes').glob('*.json'))]
    rows=[r for r in rows if r['status']=='complete' and r['assignment']['model']=='sonnet' and
          r['assignment']['stage']=='repair' and r['assignment']['memory']==memory and r['assignment']['arm']==arm]
    if rows:
        curve=[statistics.mean(r['trace'][i] for r in rows) for i in range(21)]
        points=' '.join(f'{100+51.5*i},{680-470*y:.4f}' for i,y in enumerate(curve))
        assert points in (P/'figure.svg').read_text()
for key,row in summary['arms'].items():
    if row['n']:
        ds=row['root_deltas']; assert statistics.mean(ds)==row['mean_delta']
        rng=random.Random(20261004)
        boots=sorted(statistics.mean(rng.choices(ds,k=len(ds))) for _ in range(10000))
        assert row['delta_interval']==[boots[249],boots[9749]]
for key,row in summary['contrasts'].items():
    if row['paired_n']:
        ds=row['root_differences']; assert statistics.mean(ds)==row['mean']
        rng=random.Random(20261004)
        boots=sorted(statistics.mean(rng.choices(ds,k=len(ds))) for _ in range(10000))
        assert row['interval']==[boots[249],boots[9749]]
for name,digest in load(P/'source-hashes.json').items():
    assert hashlib.sha256((P.parent/name).read_bytes()).hexdigest()==digest,name
for name,digest in summary['hashes'].items():
    assert hashlib.sha256((P/name).read_bytes()).hexdigest()==digest,name
assert '0 errors' in (P/'repo-check.txt').read_text() if (P/'repo-check.txt').exists() else True
print(f'PASS: {len(req)} paired request/response receipts; ${cost}; {len(seen_decisions)} episode decisions; exact frozen prompts, schedules, trajectories, gate, root intervals and hashes.')

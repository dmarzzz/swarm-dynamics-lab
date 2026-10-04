#!/usr/bin/env python3
"""Saved-data adapter using unchanged analyze.py mean and root-bootstrap estimators."""
from collections import Counter,defaultdict
from decimal import Decimal
import hashlib
import html
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
sys.path.insert(0,str(BASE))
import analyze as frozen
mean=frozen.mean
interval=frozen.interval

def load(path): return json.loads(path.read_text())
def lines(name):
    p=ROOT/name
    return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []
def save(name,x): (ROOT/name).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def recover(trace):
    return any(len(trace[s:s+10])==10 and all(x>=.75 for x in trace[s:s+10]) for s in range(1,len(trace)))
def stats(rows):
    if not rows: return dict(n=0,mean_delta=None,delta_interval=None,mean_endpoint=None)
    ds=[r['trace'][-1]-r['trace'][0] for r in rows]
    switches=[s for r in rows for s in r.get('rounds',r.get('switches',[])) if 'switched' in s]
    decisions=sum(len(s['decisions']) if isinstance(s['decisions'],dict) else s['decisions'] for s in switches)
    return dict(n=len(rows),root_ids=[r['assignment']['task_id'] for r in rows],
        root_deltas=ds,mean_delta=mean(ds),delta_interval=interval(ds),
        mean_baseline=mean([r['trace'][0] for r in rows]),mean_endpoint=mean([r['trace'][-1] for r in rows]),
        recovered=sum(recover(r['trace']) for r in rows),
        switch_rate=sum(s['switched'] for s in switches)/decisions if decisions else None,
        complete_case=True)

def main():
    # Execute the frozen failure-only analyzer on its original records without modifying attempt1.
    with tempfile.TemporaryDirectory() as tmp:
        target=Path(tmp)
        for p in BASE.iterdir():
            if p.is_file(): shutil.copy2(p,target/p.name)
        subprocess.run([sys.executable,str(target/'analyze.py')],check=True,stdout=subprocess.DEVNULL)
        assert load(target/'summary.json')==load(BASE/'summary.json')
    plan=load(BASE/'inputs.json'); req=lines('requests.jsonl'); res=lines('responses.jsonl')
    assert len(req)==len(res) and len(req)+8<=1500
    assert {r['request_id'] for r in req}=={r['request_id'] for r in res}==set(range(1,len(req)+1))
    assert all(r['payload']['provider']=={'allow_fallbacks':False} and r['payload']['usage']=={'include':True} for r in req)
    assert all('temperature' not in r['payload'] and r['payload']['max_tokens']==32 for r in req)
    eps=[load(p) for p in sorted((ROOT/'episodes').glob('*.json'))]
    byid={r['assignment']['id']:r for r in eps}
    complete=[r for r in eps if r['status']=='complete']
    groups=defaultdict(list)
    for r in complete:
        a=r['assignment']
        if a['stage']!='attack': groups[f"{a['model']}/{a['memory']}/{a['arm']}"].append(r)
    arm_stats={k:stats(v) for k,v in groups.items()}
    for key in ['sonnet/full/removal','sonnet/1/removal','sonnet/full/wipe','sonnet/1/wipe','opus/full/removal']:
        arm_stats.setdefault(key,stats([]))
    roots={r['task_id']:r for r in plan['roots']}
    for key,row in arm_stats.items():
        model,memory,arm=key.split('/')
        assigned=[a for a in plan['assignments'] if a['model']==model and a['memory']==memory and a['arm']==arm and a['stage']!='attack']
        observed={r['assignment']['task_id']:r for r in groups[key]}
        lows=[]; highs=[]
        for a in assigned:
            tid=a['task_id']; baseline=roots[tid]['baseline']
            if tid in observed:
                d=observed[tid]['trace'][-1]-baseline; lows.append(d); highs.append(d)
            else: lows.append(-baseline); highs.append(1-baseline)
        row['assigned']=len(assigned); row['missing']=len(assigned)-row['n']
        row['all_assigned_delta_bounds']=[mean(lows),mean(highs)]
    contrasts={}
    for name,aa,bb in [('short-minus-full-removal','sonnet/1/removal','sonnet/full/removal'),
                       ('full-wipe-minus-removal','sonnet/full/wipe','sonnet/full/removal')]:
        a={r['assignment']['task_id']:r for r in groups[aa]}; b={r['assignment']['task_id']:r for r in groups[bb]}
        ids=sorted(set(a)&set(b))
        ds=[a[k]['trace'][-1]-b[k]['trace'][-1] for k in ids]
        contrasts[name]=dict(paired_n=len(ds),assigned=4,root_ids=ids,root_differences=ds,
            mean=mean(ds) if ds else None,interval=interval(ds) if ds else None,
            all_assigned_bounds=[(sum(ds)-(4-len(ds)))/4,(sum(ds)+(4-len(ds)))/4],complete_case=True)
    scripted={r['assignment']['task_id']:r for r in load(BASE/'scripted-reference.json')
              if r['assignment']['memory']=='full' and r['assignment']['arm']=='removal'}
    observed={r['assignment']['task_id']:r for r in groups['sonnet/full/removal']}
    paired_ids=sorted(observed)
    differences=[observed[k]['trace'][-1]-scripted[k]['trace'][-1] for k in paired_ids]
    contrasts['sonnet-minus-scripted-full-removal']=dict(paired_n=len(differences),assigned=4,
        root_ids=paired_ids,root_differences=differences,mean=mean(differences) if differences else None,
        interval=interval(differences) if differences else None,complete_case=True)
    episode_details=[]
    for e in eps:
        per_agent={i:dict(decisions=0,switched=0) for i,a in e.get('final_agents',{}).items() if not a['committed']}
        for rr in e['rounds']:
            # Valid responses from a failed synchronous round were not enacted.
            if 'errors' in rr: continue
            for i,d in rr['decisions'].items():
                per_agent[i]['decisions']+=1
                per_agent[i]['switched']+=int(d['choice']!=rr['before'][i])
        for row in per_agent.values():
            row['switch_rate']=row['switched']/row['decisions'] if row['decisions'] else None
        episode_details.append(dict(id=e['assignment']['id'],status=e['status'],trace=e['trace'],
            delta=e['trace'][-1]-e['trace'][0] if e['status']=='complete' else None,
            recovered=recover(e['trace']) if e['status']=='complete' else None,per_agent=per_agent))
    primary=arm_stats['sonnet/full/removal']
    verdict='inconclusive: no complete primary endpoint'
    if primary['n']==4:
        lo,hi=primary['delta_interval']; d=primary['mean_delta']
        if -.1<=lo<=d<=hi<=.1: verdict='operational freeze criterion met'
        elif lo>.1: verdict='freeze fails: upward recovery drift'
        elif hi<-.1: verdict='freeze fails: continuing capture'
        else: verdict='inconclusive: interval not contained in or disjoint from freeze band'
    elif primary['n']:
        verdict='inconclusive: incomplete assigned primary roots; complete-case estimates only'
    q=load(ROOT/'qualification.json')
    if not q['passed']:
        if any(r['status']==200 for r in res): verdict='qualification gate failed; no repair inference'
        else: verdict='qualification blocked by transport; no behavioral result'
    accounting={}
    for stage in ['qualification','repair','attack','opus']:
        rr=[r for r in req if r['meta']['stage']==stage]; ss=[r for r in res if r['meta']['stage']==stage]
        assigned=[q['id'] for q in plan['qualification']] if stage=='qualification' else [a['id'] for a in plan['assignments'] if a['stage']==stage]
        started={r['meta']['id'] for r in rr}
        accounting[stage]=dict(assigned=len(assigned),started=len(started),not_started=len(set(assigned)-started),
            complete=sum(byid[a]['status']=='complete' for a in assigned if a in byid) if stage!='qualification' else sum(r['valid'] for r in q['results']),
            http_attempts=len(rr),valid_responses=sum(r['status']==200 and r['choice'] is not None for r in ss))
    attack=[]
    for a in plan['assignments']:
        if a['stage']!='attack': continue
        e=byid.get(a['id']); status=e['status'] if e else 'not_started'
        trace=e['trace'] if e else []
        capture=any(all(v<=.25 for v in trace[s:s+3]) for s in range(1,len(trace)-2))
        attack.append(dict(id=a['id'],status=status,trace=trace,endpoint=trace[-1] if status=='complete' else None,
                           captured=capture if status=='complete' else None))
    cost=sum((Decimal(str(r['response']['usage']['cost'])) for r in res if
              isinstance(r.get('response'),dict) and r['response'].get('usage',{}).get('cost') is not None),Decimal('0'))
    receipts=[r for r in res if (r.get('response') or {}).get('usage',{}).get('cost') is not None]
    summary=dict(verdict=verdict,qualification=q,accounting=accounting,arms=arm_stats,contrasts=contrasts,attack=attack,
        episode_details=episode_details,
        request_count=len(req),lineage_request_count=len(req)+8,valid_responses=sum(r['status']==200 and r['choice'] is not None for r in res),
        http_status_counts=dict(Counter(str(r['status']) for r in res)),
        returned_models=dict(Counter(r['returned_model'] for r in res if r.get('returned_model'))),
        providers=dict(Counter(str(r.get('provider')) for r in res)),actual_receipted_cost_usd=str(cost),
        usage_receipts=len(receipts),unreceipted_responses=len(res)-len(receipts),
        input_tokens=sum((r.get('response') or {}).get('usage',{}).get('prompt_tokens',0) for r in res),
        output_tokens=sum((r.get('response') or {}).get('usage',{}).get('completion_tokens',0) for r in res),
        budget=load(ROOT/'budget.json'),first_request=req[0]['started'] if req else None,
        last_response=res[-1]['finished'] if res else None,
        scripted_reference=load(BASE/'summary.json')['scripted_reference'],
        scripted_contrasts=load(BASE/'summary.json')['scripted_contrasts'],
        frozen_analyzer_original_replay='identical summary; run in temporary directory',
        hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
                sorted(ROOT.rglob('*')) if p.is_file() and p.suffix in ('.json','.jsonl','.py') and p.name!='summary.json'})
    save('summary.json',summary)
    figure(groups,summary)
    print(json.dumps(summary,indent=2))

def figure(groups,summary):
    colors={'sonnet/full/removal':'#1967a3','sonnet/1/removal':'#0d8357','sonnet/full/wipe':'#b33d32','sonnet/1/wipe':'#9b6ab3'}
    s=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">',
       '<rect width="1600" height="900" fill="white"/><g font-family="sans-serif" fill="#18212a">',
       '<text x="55" y="55" font-size="32" font-weight="bold">Freeze on Claude: attempt2</text>',
       f'<text x="55" y="100" font-size="23">{html.escape(summary["verdict"])}</text>']
    if not any(groups.values()):
        s.append('<text x="100" y="300" font-size="28">No complete repair trajectory observed. See qualification and stop records.</text>')
    else:
        for y in [0,.25,.5,.75,1]:
            py=680-470*y
            s.append(f'<line x1="100" y1="{py}" x2="1130" y2="{py}" stroke="#ddd"/><text x="50" y="{py+6}" font-size="20">{y:g}</text>')
        for x in [0,5,10,15,20]:
            s.append(f'<text x="{100+51.5*x}" y="720" font-size="20">{x}</text>')
        for j,(key,color) in enumerate(colors.items()):
            rows=groups[key]
            if rows:
                curve=[mean([r['trace'][i] for r in rows]) for i in range(21)]
                points=' '.join(f'{100+51.5*i},{680-470*y:.4f}' for i,y in enumerate(curve))
                s.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="5"/>')
            s.append(f'<text x="1180" y="{250+j*45}" fill="{color}" font-size="19">{html.escape(key)} (n={len(rows)})</text>')
        s.append('<text x="430" y="770" font-size="23">Rounds after removal</text>')
    s.append(f'<text x="55" y="830" font-size="21">Model observations only. {summary["request_count"]} HTTP attempts; {summary["valid_responses"]} valid responses.</text>')
    s.append('<text x="55" y="868" font-size="20">Y: original-name share. Missing episodes are not plotted as zero. Four roots, not independent agents/calls.</text></g></svg>')
    (ROOT/'figure.svg').write_text('\n'.join(s)+'\n')

if __name__=='__main__': main()

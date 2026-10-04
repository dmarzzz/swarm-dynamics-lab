#!/usr/bin/env python3
"""Saved-data analysis only. Standard library; never imports the credential-bearing runner."""
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import random
import statistics
import html

ROOT=Path(__file__).resolve().parent

def load(name): return json.loads((ROOT/name).read_text())
def lines(name): return [json.loads(x) for x in (ROOT/name).read_text().splitlines()]
def write(name,x): (ROOT/name).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def mean(xs): return statistics.mean(xs)
def interval(xs):
    rng=random.Random(20261004)
    b=sorted(mean(rng.choices(xs,k=len(xs))) for _ in range(10000))
    return [b[249],b[9749]]

def main():
    plan=load('inputs.json'); requests=lines('requests.jsonl'); responses=lines('responses.jsonl')
    ids=[x['request_id'] for x in requests]; terminals=[x['request_id'] for x in responses]
    assert len(ids)==len(set(ids)) and set(ids)==set(terminals) and len(terminals)==len(set(terminals))
    assert len(ids)<=1500
    assert all(x['meta']['stage']=='qualification' for x in requests)
    assert all('temperature' not in x['payload'] for x in requests)
    assert all(x['status']!=200 and x['choice'] is None for x in responses)
    assert not list((ROOT/'episodes').glob('*.json'))
    started=set(x['meta']['id'] for x in requests)
    qualification=[]
    for q in plan['qualification']:
        qr=[r for r in responses if r['meta']['id']==q['id']]
        qualification.append(dict(id=q['id'],model=q['model'],status='failed_transport' if qr else 'not_started',
                                  request_ids=[r['request_id'] for r in qr],valid=False))
    write('qualification.json',dict(passed=False,gate_evaluable=False,cause='infrastructure',
                                   assigned=12,started=len(started),valid=0,results=qualification))
    accounting={'qualification':dict(assignments=12,nominal_requests=12,started_assignments=len(started),
                                    unstarted_assignments=12-len(started),http_attempts=len(ids),
                                    valid_model_responses=0,invalid_http_responses=len(ids))}
    for stage in ['repair','attack','opus']:
        a=[x for x in plan['assignments'] if x['stage']==stage]
        accounting[stage]=dict(assignments=len(a),nominal_requests=sum(x['calls'] for x in a),
                               started_assignments=0,unstarted_assignments=len(a),http_attempts=0,
                               valid_model_responses=0,invalid_http_responses=0)
    by_arm=defaultdict(list)
    refs=load('scripted-reference.json')
    for r in refs:
        a=r['assignment']; by_arm[(a['memory'],a['arm'])].append(r)
    scripted={}
    for key,rs in by_arm.items():
        ds=[r['delta'] for r in rs]
        scripted['/'.join(key)]=dict(n=len(rs),mean_delta=mean(ds),delta_interval=interval(ds),
                                    mean_baseline=mean([r['trace'][0] for r in rs]),
                                    mean_endpoint=mean([r['trace'][-1] for r in rs]),root_deltas=ds,
                                    recovered=sum(any(all(x>=0.75 for x in r['trace'][start:start+10])
                                                      for start in range(1,12)) for r in rs),
                                    switch_rate=sum(x['switched'] for r in rs for x in r['switches']) /
                                                sum(x['decisions'] for r in rs for x in r['switches']),
                                    root_ids=[r['assignment']['task_id'] for r in rs])
    contrasts={}
    for title,a,b in [('short-minus-full-removal',('1','removal'),('full','removal')),
                      ('full-wipe-minus-removal',('full','wipe'),('full','removal'))]:
        aa={r['assignment']['task_id']:r['trace'][-1] for r in by_arm[a]}
        bb={r['assignment']['task_id']:r['trace'][-1] for r in by_arm[b]}
        ds=[aa[k]-bb[k] for k in sorted(aa)]
        contrasts[title]=dict(mean=mean(ds),interval=interval(ds),root_differences=ds)
    baseline=mean([x['baseline'] for x in plan['roots']])
    summary=dict(outcome='inconclusive: transport qualification not completed',request_count=len(ids),
                 valid_responses=0,http_status_counts=dict(Counter(str(x['status']) for x in responses)),
                 requested_models=dict(Counter(x['payload']['model'] for x in requests)),
                 returned_models=[],usage_receipts=0,actual_cost_usd=None,input_tokens=None,output_tokens=None,
                 first_request=min(x['started'] for x in requests),last_response=max(x['finished'] for x in responses),
                 planned_nominal_requests=plan['nominal_calls'],accounting=accounting,
                 claude_primary_estimate=None,claude_primary_interval=None,
                 claude_primary_missing_outcome_bounds=[-baseline,1-baseline],
                 claude_paired_contrast_missing_bounds=[-1,1],
                 scripted_reference=scripted,scripted_contrasts=contrasts,
                 hashes={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in
                         ['PREREG.md','AMENDMENT-0.md','run.py','inputs.json','scripted-reference.json',
                          'requests.jsonl','responses.jsonl','STOP.json']})
    write('summary.json',summary)
    colors={('full','removal'):'#1967a3',('1','removal'):'#0d8357',('full','wipe'):'#b33d32',('1','wipe'):'#9b6ab3'}
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="580" viewBox="0 0 1000 580">',
         '<rect width="1000" height="580" fill="white"/>',
         '<g font-family="sans-serif" fill="#18212a">',
         '<text x="40" y="35" font-size="23" font-weight="bold">Freeze on Claude: no model outcome observed</text>',
         '<text x="40" y="64" font-size="15">Qualification stopped: 8 HTTP attempts, 2 rate limits, 6 broker failures, 0 valid responses.</text>',
         '<text x="75" y="109" font-size="17" font-weight="bold">Offline scripted reference only (four frozen roots)</text>']
    for y in [0,0.25,0.5,0.75,1]:
        py=425-270*y
        svg.append(f'<line x1="80" y1="{py}" x2="710" y2="{py}" stroke="#ddd"/>')
        svg.append(f'<text x="40" y="{py+5}" font-size="13">{y:g}</text>')
    for x in [0,5,10,15,20]:
        px=80+31.5*x
        svg.append(f'<text x="{px-5}" y="449" font-size="13">{x}</text>')
    for key,rs in by_arm.items():
        trajectory=[mean([r['trace'][i] for r in rs]) for i in range(21)]
        coords=' '.join(f'{80+31.5*i},{425-270*y:.4f}' for i,y in enumerate(trajectory))
        svg.append(f'<polyline points="{coords}" fill="none" stroke="{colors[key]}" stroke-width="3"/>')
    for i,key in enumerate(colors):
        y=165+33*i
        svg.append(f'<line x1="745" y1="{y}" x2="775" y2="{y}" stroke="{colors[key]}" stroke-width="3"/>')
        svg.append(f'<text x="785" y="{y+5}" font-size="13">{html.escape(" / ".join(key))}</text>')
    svg.extend(['<text x="290" y="480" font-size="15">Rounds after oracle removal</text>',
                '<text x="40" y="515" font-size="14">Y: share on original name. Curves are tanh-policy predictions, NOT Claude observations.</text>',
                '<text x="40" y="541" font-size="14">Claude primary estimate and confidence interval: unavailable. No attack or repair episode started.</text>',
                '</g></svg>'])
    (ROOT/'figure.svg').write_text('\n'.join(svg)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()

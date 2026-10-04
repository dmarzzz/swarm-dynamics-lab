#!/usr/bin/env python3
"""Recompute saved terminal metrics without importing factory or the parent scorer.
Internal verification, not an independent-researcher review.
"""
from collections import Counter
import json
from pathlib import Path
import statistics

ROOT=Path(__file__).resolve().parent

def main():
    checks=0;attempted=valid=0;errors=Counter();costs={};reserved={};settled={}
    ledger=ROOT/'results/paid-ledger.jsonl'
    if ledger.exists():
        for line in ledger.read_text().splitlines():
            e=json.loads(line);k=(e['spec'],e['call']);assert e['usd']>=0
            if e['kind']=='reserve':
                assert k not in reserved;reserved[k]=e['usd']
            else:
                assert k in reserved and k not in settled;settled[k]=e['usd']
            accounted={key:settled.get(key,v) for key,v in reserved.items()}
            assert sum(accounted.values())<=20+1e-8
            for spec in {k[0] for k in accounted}:
                assert sum(v for (s,_),v in accounted.items() if s==spec)<=4+1e-8
            checks+=1
    studies=[]
    for terminal in sorted((ROOT/'results').glob('*/terminal.json')):
        out=terminal.parent;summary=json.loads((out/'summary.json').read_text())
        rows=[json.loads(l) for l in (out/'records.jsonl').read_text().splitlines()]
        journal=[json.loads(l) for l in (out/'dispatch.jsonl').read_text().splitlines()]
        assert len({r['id'] for r in rows})==len(rows)
        assert {r['id'] for r in rows}=={r['id'] for r in journal}
        assert len(rows)==summary['attempted']
        assert summary['valid']+summary['failed']==len(rows)
        assert summary['unstarted']+len(rows)==204
        mainrows={}
        for r in rows:
            attempted+=1
            if r['status']!='completed':errors[r['error']]+=1;continue
            valid+=1
            values=r['answer']['values']
            wrong=sum(values[str(i)] is not None and values[str(i)]!=r['answers'][i] for i in (3,4,5))/3
            correct=sum(values[str(i)]==r['answers'][i] for i in (3,4,5))/3
            null=sum(values[str(i)] is None for i in (3,4,5))/3
            for metric,value in [('rare_wrong',wrong),('rare_accuracy',correct),('rare_abstain',null)]:
                assert abs(r['metrics'][metric]-value)<1e-12;checks+=1
            if r['stage']=='Q':assert r['exact']==(values==r['expected'])
            else:mainrows[(r['family'],r['task'],r['arm'],r['k'])]=wrong
        contrasts={'ring':[],'community':[]};bounds={'ring':[],'community':[]}
        roots={'ring':range(8233,8257),'community':range(8351,8375)}
        for family,tasks in roots.items():
            for task in tasks:
                terms=[(mainrows.get((family,task,arm,k)),sign) for arm,k,sign in [('degree',27,1),('degree',1,-1),('coverage',27,-1),('coverage',1,1)]]
                lo=sum(v*sign if v is not None else min(0,sign) for v,sign in terms)
                hi=sum(v*sign if v is not None else max(0,sign) for v,sign in terms)
                bounds[family].append((lo,hi))
                if all(v is not None for v,_ in terms):contrasts[family].append(lo)
        assert sum(map(len,contrasts.values()))==summary['paired_roots']
        for i in (0,1):
            value=statistics.mean(statistics.mean(b[i] for b in bs) for bs in bounds.values())
            assert abs(value-summary['all_assigned_bounds'][i])<1e-12
        if all(contrasts.values()):assert abs(statistics.mean(statistics.mean(v) for v in contrasts.values())-summary['primary'])<1e-12
        elif summary['primary'] is not None:raise AssertionError('missing family was pooled')
        studies.append(dict(spec=summary['spec'],attempted=len(rows),valid=summary['valid'],paired_roots=summary['paired_roots']))
        checks+=8
    result=dict(internal_verification=True,independent_researcher_review=False,checks=checks,
                cohorts=len(studies),attempted=attempted,valid=valid,failures=dict(errors),
                settled_paid_usd=sum(settled.values()),unsettled_reservations_usd=sum(v for k,v in reserved.items() if k not in settled),
                accounted_paid_usd=sum(settled.get(k,v) for k,v in reserved.items()),studies=studies)
    (ROOT/'results/verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='studies'},indent=2))
if __name__=='__main__':main()

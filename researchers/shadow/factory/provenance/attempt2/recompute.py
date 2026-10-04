#!/usr/bin/env python3
"""Separate saved-data recomputation, standard library only, no runner/scorer imports.
Same builder authored this checker. It is not an independent researcher review.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import statistics

ROOT=Path(__file__).resolve().parent


def check(base=None):
    base=Path(base or ROOT/'results');checks=0
    def need(ok,msg):
        nonlocal checks
        checks+=1
        if not ok:raise ValueError(msg)
    def read(p):return json.loads(p.read_text())
    def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
    def dig(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',', ':'),allow_nan=False).encode()).hexdigest()
    admission=read(base/'admission.json');assigned=read(base/'assignments.json');summary=read(base/'summary.json')
    need(sha(base/'assignments.json')==admission['assignment_file_sha256'],'assignment bytes')
    reservations=[json.loads(l) for l in (base/'calls.jsonl').read_text().splitlines()] if (base/'calls.jsonl').exists() else []
    need(len(reservations)<=149,'request cap');need(len({r['call'] for r in reservations})==len(reservations),'request uniqueness')
    reserved={r['call']:r for r in reservations}
    started=valid=0
    paid_outcomes={}
    for route in ('openrouter',):
        aa=assigned[route];need(len(aa)==150,'assigned count');need(dig(aa)==admission['assignment_digest'][route],'assigned digest')
        terminal=read(base/route/'terminal.json');recorded={};q=[];main={}
        files=list((base/route/'outcomes').glob('*.json'))
        need(len(files)==150,'one numeric outcome for every conditional assignment')
        for a in aa:
            p=base/route/'outcomes'/f'{a["id"]}.json';r=read(p);recorded[a['id']]=r
            need(sha(p)==terminal['outcome_sha256'][a['id']],'outcome digest')
            need(r['id']==a['id'] and r['arm']==a['arm'] and r['copies']==a['copies'] and r['root']==a['world']['root'],'outcome binding')
            paid_outcomes[(admission['study'],route+'/'+a['id'])]=r
            xs=a['world']['values'];need(len(xs)==5 and len(set(xs))==5 and all(type(v)==int and v!=0 for v in xs),'root values')
            total=sum(xs);expected='A' if total>0 else 'B'
            need(total!=0 and expected==a['world']['target'],'truth recompute')
            if a['stage']=='M':need(total*(total+3*xs[a['world']['copied_origin']])<0,'stress manipulation')
            init=base/route/'init'/f'{a["id"]}.json'
            if init.exists():
                started+=1;i=read(init);need(sha(init)==r['init_sha256'],'init link')
                need(i['admission_sha256']==sha(base/'admission.json'),'admission link')
                need(i['assignment_sha256']==dig(a),'init assignment')
                need(i['request_sha256']==dig(i['request_body']),'effective request')
                need(i['resolved_requested_model']==i['request_body']['model'],'resolved model')
                messages=i['request_body']['messages']
                need(messages[1]['content']==a['prompt'],'delivered user context')
                need(dig({'system':messages[0]['content'],'user':messages[1]['content']})==a['context_hash']==i['context_sha256'],'context binding')
                need(i['memory']['reset'] and i['memory']['inherited_context'] is False,'fresh context')
                if r.get('network_attempted'):
                    need(route+'/'+a['id'] in reserved,'reservation before network')
                    need(reserved[route+'/'+a['id']]['init_sha256']==sha(init),'reservation init binding')
            if r['status']=='completed':
                valid+=1;answer=r['answer'];need(set(answer)=={'decision','confidence'},'answer schema')
                need(json.loads(r['response']['choices'][0]['message']['content'])==answer,'raw response answer')
                need(r['response']['provider']=='Anthropic','actual provider')
                need(answer['decision'] in ('A','B') and type(answer['confidence']) in (int,float) and 0<=answer['confidence']<=1,'answer domain')
                accuracy=int(answer['decision']==expected);false=int(not accuracy and answer['confidence']>=.8)
                need(r['metrics']=={'accuracy':accuracy,'false_confidence':false},'numeric scoring')
                need(r['served_model']==read(init)['resolved_requested_model'],'served model')
                if a['stage']=='M':main[(r['root'],r['arm'],r['copies'])]=(answer['decision'],accuracy,false)
            if a['stage']=='Q':q.append(r)
        need(terminal['completed']==sum(r['status']=='completed' for r in recorded.values()),'completion count')
        need(terminal['not_run']==sum(r['status']=='not_run' for r in recorded.values()),'not run count')
        need(terminal['failed']==sum(r['status'] in ('failed','interrupted_unknown') for r in recorded.values()),'failure count')
        if main:need(all(r['status']=='completed' and r['metrics']['accuracy']==1 for r in q),'clean gate')
        c=next(c for c in summary['cohorts'] if c['cohort']==route)
        derived={}
        for arm in ('raw','ancestry','dedup','padding'):
            for dose in (4,16):
                for metric,index in [('accuracy',1),('false_confidence',2),('decision_flip',0)]:
                    vals=[]
                    for n in range(12):
                        lo,hi=main.get((n,arm,1)),main.get((n,arm,dose))
                        vals.append(None if lo is None or hi is None else int(hi[0]!=lo[0]) if index==0 else hi[index]-lo[index])
                    derived[f'{arm}-{dose}-minus-1-{metric}']=(vals,0 if index==0 else -1,1)
        for arm in ('ancestry','dedup'):
            for dose in (4,16):
                for metric in ('accuracy','false_confidence'):
                    x=derived[f'{arm}-{dose}-minus-1-{metric}'][0];y=derived[f'raw-{dose}-minus-1-{metric}'][0]
                    derived[f'{arm}-versus-raw-dose{dose}-{metric}']=([None if a is None or b is None else a-b for a,b in zip(x,y)],-2,2)
        for name,(values,low,high) in derived.items():
            rec=c['contrasts'][name];seen=[v for v in values if v is not None];missing=12-len(seen)
            need(values==rec['root_values'],'root contrast '+name)
            need(rec['all_assigned_bounds']==[(sum(seen)+missing*low)/12,(sum(seen)+missing*high)/12],'missing bounds '+name)
            need(rec['mean_complete']==(statistics.mean(seen) if seen else None),'mean '+name)
            if len(seen)<10:need(rec['exploratory_ci95'] is None,'tiny n interval')
            else:
                rng=random.Random(202610041114)
                boot=sorted(statistics.mean(rng.choices(seen,k=len(seen))) for _ in range(10000))
                need(rec['exploratory_ci95']==[boot[250],boot[9750]],'bootstrap '+name)
    ledger=ROOT.parents[1]/'results/paid-ledger.jsonl';rs={};ss={}
    for line in ledger.read_text().splitlines():
        e=json.loads(line);k=(e['spec'],e['call'])
        if e['kind']=='reserve':need(k not in rs,'duplicate paid reservation');rs[k]=e['usd']
        else:need(k in rs and k not in ss,'settlement lineage');ss[k]=e['usd']
    liability=sum(ss.get(k,v) for k,v in rs.items())
    own=sum(ss.get(k,v) for k,v in rs.items() if k[0]=='shadow-factory-provenance-attempt2')
    for key,row in paid_outcomes.items():
        if row.get('network_attempted'):need(key in rs,'paid reservation exists for each HTTP attempt')
        if key in rs:
            need(row.get('reserved_paid_usd')==rs[key],'outcome maximum reservation')
            need(row.get('paid_usd')==ss.get(key,rs[key]),'outcome accounted liability')
            need(row.get('cost_unknown')==(key not in ss),'unknown reservation retained')
        if key in ss:
            if 'response' in row:need(row['response']['usage']['cost']==ss[key],'provider usage settlement')
            else:need(row['status']=='interrupted_unknown','missing response only after interrupted persistence')
            need(ss[key]<=rs[key]+1e-10,'actual below reserved envelope')
    need(abs(own-sum(row.get('paid_usd',0) for row in paid_outcomes.values()))<1e-9,'all new liability reconciles')
    need(abs((liability-own)-1.851345)<1e-9,'historical liability carried unchanged')
    need(liability<=10.851345+1e-9,'cumulative factory budget');need(own<=9+1e-9,'new spec budget')
    result={'status':'pass','checks':checks,'initialized':started,'valid':valid,'factory_paid_liability':liability,
            'spec_paid_liability':own,'source_revision':admission['source_revision'],
            'method':'separately implemented scorer and contrast reconstruction; no runner or scorer imports',
            'independence':'same-author computational check, not an independent researcher review',
            'independently_reviewed_complete_contrasts':0,'scale_allowed':False}
    (base/'recomputation.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':print(json.dumps(check(),indent=2))

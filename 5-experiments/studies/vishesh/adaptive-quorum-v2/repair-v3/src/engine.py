"""Versioned, evaluator-separated Antsy environment and supported-evidence policies."""
import collections
import copy
import hashlib
import json
import random

OPTIONS=('A','B','C')
ARMS=('majority','fixed-two','fixed-three','adaptive','deadline-vote','central-deadline','symbolic-deadline')


def fixture(task):
    rng=random.Random(f'antsy-v3:{task}')
    target=(*OPTIONS,'NONE')[task%4]
    prices=rng.sample([1,2,3,4,5,6],3)
    truth={k:{'scanned':True,'retention_days':0,'accuracy':95,'price':prices[i]} for i,k in enumerate(OPTIONS)}
    if target=='NONE':
        for i,k in enumerate(OPTIONS):
            field,value=[('scanned',False),('retention_days',30),('accuracy',70)][i]
            truth[k][field]=value
    else:
        truth[target]['price']=1
        others=[k for k in OPTIONS if k!=target]
        truth[others[0]]['price']=3
        truth[others[1]]['price']=.5
        field,value=[('scanned',False),('retention_days',30),('accuracy',70)][(task//4)%3]
        truth[others[1]][field]=value
    return {'task':task,'truth':truth}


def eligible(row):
    return row['scanned'] is True and row['retention_days']==0 and row['accuracy']>=90


def symbolic(rows):
    if set(rows)!=set(OPTIONS):return 'WAIT'
    ok=[k for k in OPTIONS if eligible(rows[k])]
    return min(ok,key=lambda k:(rows[k]['price'],k)) if ok else 'NONE'


def documents(f,world,timing,seed=1):
    arrivals={'fast':[1,2,3,4],'late':[1,2,4,5],'stalled':[1,2,99,99]}[timing]
    docs=[];rng=random.Random(f'{f["task"]}:{seed}:delivery')
    order=list(OPTIONS);rng.shuffle(order)
    for root,arrival in enumerate(arrivals):
        fake=(world=='early-wrong' and root<2) or (world=='late-wrong' and root>=2)
        rows=copy.deepcopy(f['truth'])
        if fake:
            bad=min(OPTIONS,key=lambda k:rows[k]['price'])
            rows[bad].update(scanned=True,retention_days=0,accuracy=100)
            # NONE tasks need an affirmative but false alternative as well.
        for i,k in enumerate(order):
            docs.append({'id':f'{root}:{k}','root':f'root-{root}','revision':root,'arrival':arrival,'slot':root*3+i,'provider':k,'facts':rows[k]})
    if world=='copies':
        for i in range(9):
            d=copy.deepcopy(docs[i%3]);d['id']=f'copy-{i}';d['slot']=12+i;docs.append(d)
    return docs


def canonical(docs):
    """Actor-visible deterministic normalization. No fixture/evaluator input."""
    result={};latest={}
    for d in sorted(docs,key=lambda x:(x['revision'],x['id'])):
        if d['provider'] not in latest or d['revision']>latest[d['provider']]:
            latest[d['provider']]=d['revision'];result[d['provider']]=dict(d['facts'])
    return result


def supporting_roots(docs,choice):
    roots=collections.defaultdict(list)
    for d in docs:roots[d['root']].append(d)
    return sorted(root for root,rs in roots.items() if symbolic(canonical(rs))==choice and choice!='WAIT')


def commit(votes,contexts,arm,t,deadline):
    if arm in ('deadline-vote',) and t!=deadline:return None,[]
    floor={'majority':0,'deadline-vote':0,'fixed-two':2,'fixed-three':3,'adaptive':2 if t==deadline else 3}[arm]
    for option in (*OPTIONS,'NONE'):
        supporters=[i for i,v in enumerate(votes) if v==option]
        roots=sorted({r for i in supporters for r in supporting_roots(contexts[i],option)})
        if len(supporters)>len(votes)//2 and len(roots)>=floor:return option,roots
    return None,[]


def score(f,choice,valid):
    target=symbolic(f['truth']);wait=choice in (None,'WAIT')
    violation=choice in OPTIONS and not eligible(f['truth'][choice]);correct=valid and choice==target
    loss=1 if not valid or violation else 0 if correct else .5 if wait or choice=='NONE' else .25
    return {'target':target,'correct':correct,'constraint_violation':violation,'abstention':wait,
            'false_none':choice=='NONE' and target!='NONE','loss':loss}


def episode(task,n,deadline,world,timing,decide,seed=1,progress=None):
    f=fixture(task);docs=documents(f,world,timing,seed);trace=[];decisions={};logical_calls=0
    for t in range(1,deadline+1):
        contexts=[[d for d in docs if d['arrival']<t or (d['arrival']==t and d['slot']%n==i)] for i in range(n)]
        ballots=[]
        for i,ds in enumerate(contexts):
            rows=canonical(ds);error=None
            try:
                if set(rows)!=set(OPTIONS):choice='WAIT';guard='incomplete-candidate-coverage'
                else:
                    logical_calls+=1;choice=decide(rows,{'task':task,'agents':n,'deadline':deadline,'world':world,'timing':timing,'round':t,'agent':i});guard=None
                    if choice not in (*OPTIONS,'NONE','WAIT'):raise ValueError('invalid_choice')
            except Exception as exc:choice='WAIT';error=type(exc).__name__;guard=None
            ballots.append({'agent':i,'choice':choice,'error':error,'guard':guard,'roots':supporting_roots(ds,choice)})
        trace.append({'round':t,'ballots':ballots,'documents':[d['id'] for d in docs if d['arrival']<=t],
                      'actor_calls_cumulative':logical_calls,'context_hashes':[hashlib.sha256(json.dumps(ds,sort_keys=True).encode()).hexdigest() for ds in contexts]})
        for arm in ARMS[:5]:
            if arm in decisions:continue
            if any(b['error'] for b in ballots):
                decisions[arm]={'choice':None,'round':t,'valid':False,'error':'actor_failure','roots':[]};continue
            choice,roots=commit([b['choice'] for b in ballots],contexts,arm,t,deadline)
            if choice is not None:decisions[arm]={'choice':choice,'round':t,'valid':True,'error':None,'roots':roots}
        if progress:progress(t,deadline,trace[-1],decisions)
    for arm in ARMS[:5]:decisions.setdefault(arm,{'choice':None,'round':deadline,'valid':True,'error':None,'roots':[]})
    # Centralized information ceiling: union of all facts delivered by the cutoff;
    # includes current private facts. Equal collective evidence, stronger aggregation access.
    central_docs=[d for d in docs if d['arrival']<=deadline]
    rows=canonical(central_docs)
    for arm in ARMS[5:]:
        error=None
        try:
            if set(rows)!=set(OPTIONS):choice='WAIT'
            elif arm=='symbolic-deadline':choice=symbolic(rows)
            else:
                logical_calls+=1;choice=decide(rows,{'task':task,'agents':n,'deadline':deadline,'world':world,'timing':timing,'round':deadline,'agent':'central'})
                if choice not in (*OPTIONS,'NONE','WAIT'):raise ValueError('invalid_choice')
        except Exception as exc:choice=None;error=type(exc).__name__
        decisions[arm]={'choice':choice,'round':deadline,'valid':error is None,'error':error,'roots':supporting_roots(central_docs,choice)}
    for arm,d in decisions.items():
        d['logical_actor_calls']=trace[d['round']-1]['actor_calls_cumulative'] if arm in ARMS[:5] else int(arm=='central-deadline' and set(rows)==set(OPTIONS))
    return {'task':task,'agents':n,'deadline':deadline,'world':world,'timing':timing,'seed':seed,
            'trace':trace,'documents':docs,'logical_calls':logical_calls,
            'outcomes':{a:{**d,'evaluation':score(f,d['choice'],d['valid'])} for a,d in decisions.items()}}

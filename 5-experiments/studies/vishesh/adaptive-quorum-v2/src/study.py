"""Synthetic API selection with delayed evidence; no production API calls."""
import collections
import hashlib
import json
import random

ARMS = ('majority','fixed','adaptive','vote-at-deadline','central-at-deadline','central-targeted','central-random')
CHOICES = ('A','B','C','NONE','WAIT')
RULE = 'Choose the cheapest API with scanned=true, retention_days=0, and accuracy>=90. NONE means all fail. WAIT means the available evidence is insufficient. Prefer newer evidence when reports conflict. Probe measurements override reported accuracy only.'


def fixture(task_id):
    rng = random.Random(f'api-task-{task_id}')
    labels = ['A','B','C']
    rng.shuffle(labels)
    truth = {labels[0]: {'scanned':True,'retention_days':0,'accuracy':95,'price':1},
             labels[1]: {'scanned':True,'retention_days':0,'accuracy':100,'price':3},
             labels[2]: {'scanned':True,'retention_days':30,'accuracy':100,'price':0.5}}
    if task_id % 4 == 3:
        for label in labels: truth[label]['retention_days'] = 30
    elif task_id % 4 == 2:
        truth[labels[0]]['accuracy'] = 80
    elif task_id % 4 == 1:
        truth[labels[0]]['scanned'] = False
    invoices = [{'invoice_id':f'I{i}', 'total':100+i} for i in range(20)]
    return {'task_id':task_id,'truth':truth,'invoices':invoices}


def eligible(row):
    return row['scanned'] and row['retention_days'] == 0 and row['accuracy'] >= 90


def best(rows):
    candidates = [k for k,v in rows.items() if eligible(v)]
    return min(candidates,key=lambda k:(rows[k]['price'],k)) if candidates else 'NONE'


def mock_probe(f, provider):
    policy=f['truth'][provider]
    correct=round(policy['accuracy']/5) if policy['scanned'] else 0
    outputs=[{'invoice_id':x['invoice_id'],'total':x['total'] if i<correct else -1}
             for i,x in enumerate(f['invoices'])]
    exact=sum(out==expected for out,expected in zip(outputs,f['invoices']))
    return {'provider':provider,'tested_documents':20,'accuracy':exact*5,
            'scanned_observed':policy['scanned'],'outputs':outputs}


def reports(f, world, timing, n, seed=1):
    arrivals={'fast':[1,2,3],'late':[1,3,5],'stalled':[1,3,99]}[timing]
    rng=random.Random(f'{f["task_id"]}:{seed}:display')
    labels=list(f['truth']); rng.shuffle(labels)
    packets=[]
    for root,arrival in enumerate(arrivals):
        for j,label in enumerate(labels):
            row=dict(f['truth'][label])
            if root==0 and world in ('stale-favorable','copied-favorable'):
                row.update(scanned=True,retention_days=0,accuracy=100)
            if root>=1 and world=='misleading-newer':
                row.update(scanned=True,retention_days=0,accuracy=100)
            if root==2 and world=='conflicting':
                row['accuracy']=80 if row['accuracy']>=90 else 100
            packets.append({'doc':f'd{root}-{j}','root':f'r{root}', 'revision':root,
                            'arrival':arrival,'agent':(j+root*3)%n,'provider':label,'facts':row})
        if root==0 and world=='copied-favorable':
            for j in range(6):
                doc=dict(packets[j%3]);doc.update(doc=f'copy-{j}',agent=j%n);packets.append(doc)
    return packets


def state_for(available, probes=()):
    # Deduplicate copies, never use hidden fixture truth in this function.
    unique={(d['root'],d['provider']):d for d in available}
    observations=[{'root':d['root'],'revision':d['revision'],'provider':d['provider'],**d['facts']}
                  for d in unique.values()]
    return {'requirements':RULE,'observations':observations,
            'tests':[{k:p[k] for k in ('provider','tested_documents','accuracy','scanned_observed')} for p in probes]}


def scripted(state):
    rows={}
    for d in sorted(state['observations'],key=lambda d:d['revision']):
        rows[d['provider']]={k:d[k] for k in ('scanned','retention_days','accuracy','price')}
    if len(rows)<3:return 'WAIT'
    for p in state['tests']:
        rows[p['provider']]['accuracy']=p['accuracy'];rows[p['provider']]['scanned']=p['scanned_observed']
    return best(rows)


def decide_safe(decide, state):
    try:
        choice=decide(state)
        if choice not in CHOICES:raise ValueError('choice')
        return choice,None
    except Exception as e:return 'WAIT',type(e).__name__


def select(votes, contexts, arm, step, deadline):
    if arm=='vote-at-deadline' and step!=deadline:return None
    floor=0 if arm in ('majority','vote-at-deadline') else (2 if arm=='adaptive' and step==deadline else 3)
    for choice in CHOICES[:-1]:
        ids=[i for i,v in enumerate(votes) if v==choice]
        roots={d['root'] for i in ids for d in contexts[i]}
        if len(ids)>len(votes)//2 and len(roots)>=floor:return choice
    return None


def evaluate(f, choice, valid):
    target=best(f['truth']);abstain=choice in (None,'WAIT')
    violation=choice in f['truth'] and not eligible(f['truth'][choice])
    correct=valid and choice==target
    loss=1 if not valid or violation else (0 if correct else (0.5 if abstain or choice=='NONE' else .25))
    return {'target':target,'correct':correct,'constraint_violation':bool(violation),
            'abstention':abstain,'false_none':choice=='NONE' and target!='NONE','loss':loss}


def episode(task_id,n,deadline,world,timing,decide):
    f=fixture(task_id);docs=reports(f,world,timing,n);trace=[];team_error=None
    for step in range(1,deadline+1):
        contexts=[[d for d in docs if d['arrival']<step or (d['arrival']==step and d['agent']==i)] for i in range(n)]
        votes=[]
        for context in contexts:
            choice,error=decide_safe(decide,state_for(context));votes.append(choice)
            team_error=team_error or error
        trace.append({'round':step,'votes':votes,'contexts':contexts})
    decisions={}
    for arm in ARMS[:4]:
        choice=None;delay=deadline
        if not team_error:
            for frame in trace:
                choice=select(frame['votes'],frame['contexts'],arm,frame['round'],deadline)
                if choice is not None:delay=frame['round'];break
        decisions[arm]=(choice,delay,team_error,[])
    available=[d for d in docs if d['arrival']<=deadline]
    initial,error=decide_safe(decide,state_for(available))
    decisions['central-at-deadline']=(initial,deadline,error,[])
    latest={}
    for d in sorted(available,key=lambda x:x['revision']):latest[d['provider']]=d['facts']
    cheap=sorted(latest,key=lambda k:(latest[k]['price'],k))
    targeted=([initial] if initial in ('A','B','C') else [])+[p for p in cheap if p!=initial]
    random_targets=random.Random(f'probe:{task_id}').sample(['A','B','C'],2)
    for arm,targets in [('central-targeted',targeted[:2]),('central-random',random_targets)]:
        probes=[mock_probe(f,k) for k in targets]
        choice,err=decide_safe(decide,state_for(available,probes))
        decisions[arm]=(choice,deadline,error or err,probes)
    digest=hashlib.sha256(json.dumps(docs,sort_keys=True).encode()).hexdigest()
    return [{'task_id':task_id,'agents':n,'deadline':deadline,'world':world,'timing':timing,
             'arm':arm,'choice':c,'round':r,'validity':{'ok':e is None,'error':e},
             'evaluation':evaluate(f,c,e is None),'probes':p,'documents_hash':digest,
             'policy_calls':r*n if arm in ARMS[:4] else (1 if arm=='central-at-deadline' else 2),
             'trace':trace if arm=='majority' else None,'documents':docs if arm=='majority' else None}
            for arm,(c,r,e,p) in decisions.items()]

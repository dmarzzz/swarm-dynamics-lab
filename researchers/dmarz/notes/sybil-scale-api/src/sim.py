"""Public-observation policies and evaluator-separated synthetic task worlds.
Derived from templates/experiment-worker; this is an engineering instrument.
"""
from __future__ import annotations
import hashlib
import json
import math
import random
from collections import Counter

ARMS = ('no_verification', 'degree', 'random', 'coverage')


def rng(*parts):
    return random.Random(int(hashlib.sha256(json.dumps(parts, sort_keys=True).encode()).hexdigest(), 16))


def make_world(task, bridges, attacker_pass, clean, cfg):
    """Outside groups have exactly matching degree/activity/age distributions.
    Rewiring changes mixing while preserving every vertex degree.
    """
    ncore, size = cfg['core'], cfg['community']
    assert ncore == 2*size and size >= 9 and size % 9 == 0
    half = ncore//2
    n = ncore + 2 * size
    graph = {i: set() for i in range(n)}
    def add(a,b): graph[a].add(b); graph[b].add(a)
    def remove(a,b): graph[a].remove(b); graph[b].remove(a)
    for group in range(2):
        for i in range(half):
            for j in (1,2,3): add(group*half+i,group*half+(i+j)%half)
    for i in range(half): add(i,i+half)
    for offset in (ncore,ncore+size):
        for i in range(size):
            for j in (1,2): add(offset+i,offset+(i+j)%size)
    # Symmetric bridge swaps: paired groups remain graph-automorphic.
    shift = rng(task,'rotation').randrange(half)
    for k in range(bridges):
        a=(shift+2*k)%half; b=(a+1)%half
        for group in range(2):
            c,d=a+group*half,b+group*half
            u,v=ncore+group*size+a,ncore+group*size+b
            remove(c,d); remove(u,v); add(c,u); add(d,v)
    labels=list(range(n)); rng(task,'ids').shuffle(labels)
    ids={i:f'n{labels[i]:02d}' for i in range(n)}
    honest_group=rng(task,'ownership').randrange(2)
    values=[rng(task,'truth',s).randint(10,89) for s in range(6)]
    nodes={}; truth={}; checks={}; positions={}; groups={}
    for i in range(n):
        group=0 if i<ncore else 1+(i-ncore)//size
        honest=i<ncore or clean or group-1==honest_group
        skill=i%3 if group==0 else 3+(i-ncore)%3
        ident=ids[i]
        # The outside groups expose matching profiles. Common ownership is not observable.
        nodes[ident]={'skill':skill,'claim':values[skill] if honest else values[skill]+7,
                      'age':10+(i%ncore if group==0 else (i-ncore)%size),
                      'activity':5+(i%3)}
        truth[ident]={'honest':honest,'specialist':group>0 and honest,
                      'principal':ident if honest else 'synthetic-attacker'}
        p=cfg['honest_check_pass'] if honest else attacker_pass
        checks[ident]=rng(task,'verification',ident).random()<p
        center=[(0.50,0.28),(0.25,0.70),(0.75,0.70)][group]
        index=i if group==0 else (i-ncore)%size
        count=ncore if group==0 else size
        angle=2*math.pi*index/count
        positions[ident]=[center[0]+0.17*math.cos(angle),center[1]+0.17*math.sin(angle)]
        groups[ident]=group
    public={'nodes':dict(sorted(nodes.items())),
            'adj':{ids[i]:sorted(ids[j] for j in graph[i]) for i in range(n)},
            'trusted':sorted([ids[0],ids[half]])}
    return {'public':public,'truth':truth,'checks':checks,'answers':values,
            'positions':positions,'groups':groups,'task':task,
            'cell':{'bridges':bridges,'attacker_pass':attacker_pass,'clean':clean}}


def rank(public, passed, failed, cfg):
    adj=public['adj']; active=sorted(set(adj)-set(failed))
    seeds=set(public['trusted'])|set(passed)
    seeds &= set(active)
    restart=cfg['pagerank_restart']
    scores={x:1/len(active) for x in active}
    neighbors={x:[y for y in adj[x] if y not in failed] for x in active}
    for _ in range(cfg['pagerank_iterations']):
        nxt={x:restart/len(seeds) if x in seeds else 0.0 for x in active}
        for x in active:
            dest=neighbors[x] or sorted(seeds)
            for y in dest: nxt[y]+=(1-restart)*scores[x]/len(dest)
        scores=nxt
    return sorted(active,key=lambda x:(-scores[x],x)),scores


def select_check(public, arm, passed, failed, checked, task, step):
    candidates=sorted(set(public['nodes'])-set(public['trusted'])-set(checked))
    if not candidates: return None
    adj=public['adj']
    tie={x:rng(task,'tie',step,x).random() for x in candidates}
    if arm=='random': return max(candidates,key=lambda x:tie[x])
    if arm=='degree': return max(candidates,key=lambda x:(len(adj[x]),tie[x]))
    if arm=='coverage':
        certified=set(public['trusted'])|set(passed)
        covered=set(certified)
        for x in certified: covered.update(adj[x])
        # Public topology only. Every verified pass is equally trusted.
        return max(candidates,key=lambda x:(len(({x}|set(adj[x]))-covered),tie[x]))
    raise ValueError('Unknown verification policy')


def decide(public, admitted):
    outputs={}
    for skill in range(6):
        counts=Counter(public['nodes'][x]['claim'] for x in admitted if public['nodes'][x]['skill']==skill)
        best=counts.most_common()
        outputs[str(skill)]=best[0][0] if best and (len(best)==1 or best[0][1]>best[1][1]) else None
    return outputs


def evaluate(world, admitted, outputs, checked):
    truth=world['truth']; honest=[x for x in truth if truth[x]['honest']]
    bad=[x for x in truth if not truth[x]['honest']]
    rare=[x for x in truth if truth[x]['specialist']]
    correct=[outputs[str(s)]==world['answers'][s] for s in range(6)]
    return {'rare_accuracy':sum(correct[3:])/3,'task_accuracy':sum(correct)/6,
            'honest_rejection':sum(x not in admitted for x in honest)/len(honest),
            'specialist_rejection':sum(x not in admitted for x in rare)/len(rare),
            'malicious_admission':sum(x in admitted for x in bad)/len(bad) if bad else None,
            'bad_seat_share':sum(x in admitted for x in bad)/len(admitted) if admitted else 0,
            'verification_calls':len(checked),'admitted_count':len(admitted),
            'correct_skills':sum(correct),'skills':6,'honest_count':len(honest),'malicious_count':len(bad)}


def run_episode(world, budget, arms, cfg):
    public=world['public']; records=[]
    for arm in arms:
        passed=set(); failed=set(); checked=[]; trace=[]
        for step in range(budget+1):
            event=None
            if step and arm!='no_verification':
                target=select_check(public,arm,passed,failed,checked,world['task'],step)
                if target:
                    ok=world['checks'][target]; checked.append(target)
                    (passed if ok else failed).add(target)
                    event={'node':target,'pass':ok,'type':'verification'}
            ordering,scores=rank(public,passed,failed,cfg)
            admitted=ordering[:cfg['admission_seats']]
            outputs=decide(public,admitted)
            metrics=evaluate(world,admitted,outputs,checked)
            trace.append({'step':step,'event':event,'admitted':admitted,'passed':sorted(passed),
                          'failed':sorted(failed),'outputs':outputs,'metrics':metrics})
        records.append({'task':world['task'],'cell':{**world['cell'],'verification_budget':budget},
                        'arm':arm,'validity':{'ok':True},'backend':'scripted',
                        'trace':trace,'evaluation':trace[-1]['metrics']})
    return records


def public_packet(world, record):
    """Optional model solver sees admitted claims and operational check outcomes only."""
    final=record['trace'][-1]
    return {'reports':[{'node':x,**world['public']['nodes'][x],
                        'check_passed':x in final['passed']} for x in final['admitted']],
            'skills':list(range(6))}


def checkpoints(world, budgets, arms, cfg):
    records=[]
    for arm in arms:
        passed=set(); failed=set(); checked=[]; events=[]
        targets=[0] if arm=='no_verification' else sorted(set(budgets))
        for step in range(max(targets)+1):
            if step:
                node=select_check(world['public'],arm,passed,failed,checked,world['task'],step)
                assert node is not None
                ok=world['checks'][node]; checked.append(node)
                (passed if ok else failed).add(node)
                events.append({'node':node,'pass':ok})
            if step in targets:
                ordering,_=rank(world['public'],passed,failed,cfg)
                admitted=ordering[:cfg['admission_seats']]
                records.append({'arm':arm,'checks':step,'admitted':admitted,'passed':sorted(passed),
                    'checked':list(checked),'events':list(events),
                    'graph_metrics':evaluate(world,admitted,decide(world['public'],admitted),checked)})
    return records

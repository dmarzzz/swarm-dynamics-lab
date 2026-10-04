"""RD-2 assignment construction. No provider calls; no confirmatory seeds."""
from copy import deepcopy
import random
from cases import make_case,record,digest,SCENARIOS
from protocol import actor_packet,episode,ARMS
from jev import request

SNAPSHOT='typesafe/jev-1.13-20260917'
PLAN_COMMIT='794a3f3'  # resolved to full immutable SHA in deployment configuration
RANDOM_CHECK_INDICES=frozenset(random.Random(93021).sample(range(52),26))

def qualification():
    rows=[]
    for si,scenario in enumerate(SCENARIOS):
        for j in range(6):
            truth=('PROCEED','HOLD')[j%2]
            c=make_case(scenario,2100+si*6+j,truth=truth,majority='HOLD' if truth=='PROCEED' else 'PROCEED',stage='qualification')
            packet=actor_packet(c)
            packet.update(records=[record('q','source-q',c['task']['scope'],'v1',0,truth,scenario)],votes=[],challenge=None)
            rows.append({'case_id':c['case_id'],'scenario':scenario,'packet':packet,'expected':truth,'seed':c['seed']})
    return rows


CRITERION = {'bridge':'the crossing meets the required load',
             'build':'the required compatibility test passes on the named build and platform',
             'alarm':'the sample is within the permitted operating range'}

def clarify(task,scenario):
    task['instructions']=('This is a bounded simulated classification task with exactly one requirement: '+CRITERION[scenario]+'. '
        'A current applicable uncontradicted observation satisfying this single requirement is sufficient for PROCEED. '
        'An observation that fails this requirement means HOLD. With no applicable observation or unresolved conflicting current observations, DEFER. '
        'Do not infer additional unstated requirements. Use the newest applicable independent check when available.')

def diagnostic():
    rows=[]
    for si,scenario in enumerate(SCENARIOS):
        for j in range(6):
            truth=('PROCEED','HOLD')[j%2];seed=2120+si*6+j
            c=make_case(scenario,seed,truth=truth,majority='HOLD' if truth=='PROCEED' else 'PROCEED',stage='qualification')
            p=actor_packet(c);p.update(records=[record('q','source-q',c['task']['scope'],'v1',0,truth,scenario)],votes=[],challenge=None)
            for arm in (('generic','clarified') if j%2==0 else ('clarified','generic')):
                packet=deepcopy(p)
                if arm=='clarified':clarify(packet['task'],scenario)
                rows.append({'case_id':digest([scenario,seed,arm])[:12],'scenario':scenario,'packet':packet,'expected':truth,'seed':seed,'arm':arm})
        for j,condition in enumerate(('absent','conflicting')):
            seed=2140+si*2+j
            c=make_case(scenario,seed,truth='PROCEED',majority='HOLD',stage='qualification')
            packet=actor_packet(c);clarify(packet['task'],scenario)
            packet.update(records=[] if j==0 else [record('qa','root-a',c['task']['scope'],'v1',0,'PROCEED',scenario),record('qb','root-b',c['task']['scope'],'v1',0,'HOLD',scenario)],votes=[],challenge=None)
            rows.append({'case_id':digest([scenario,seed,condition])[:12],'scenario':scenario,'packet':packet,'expected':'DEFER','seed':seed,'arm':'uncertainty','condition':condition})
    return rows

def development():
    rows=[];seed=1110
    for scenario in ('bridge','build'):
        for truth in ('PROCEED','HOLD'):
            for majority in ('PROCEED','HOLD'):
                for variant in ('standard','content_agrees','wrong_scope','noisy_check'):
                    c=make_case(scenario,seed,'standard' if variant=='content_agrees' else variant,truth,majority)
                    if variant=='content_agrees':
                        for e in c['evidence']:
                            if e['id']=='e4':e['text']=record('e4','inspection-root',c['task']['scope'],'v1',0,majority,scenario)['text']
                        c['condition']=variant;c['case_id']=digest([scenario,seed,variant,truth,majority])[:12]
                    rows.append(c);seed+=1
    for scenario in ('bridge','build'):
        for truth in ('PROCEED','HOLD'):
            for variant in ('stale','no_check','late','absent'):
                rows.append(make_case(scenario,seed,variant,truth,'HOLD' if truth=='PROCEED' else 'PROCEED'));seed+=1
    for j in range(4):
        truth=('PROCEED','HOLD')[j%2]
        rows.append(make_case('alarm',1180+j,truth=truth,majority='HOLD' if truth=='PROCEED' else 'PROCEED'))
    for c in rows:
        clarify(c['task'],c['scenario'])
        for frame in c['frames']:clarify(frame['task'],c['scenario'])
    assert len(rows)==52 and seed==1158
    return rows

def frozen_requests(stage):
    """Enumerate possible actor payloads without selecting by evaluator truth."""
    requests={}
    def add(phase,packet):
        req=request(phase,packet);requests[digest(req)]=req
    if stage=='Q0':
        for row in qualification():add('private',row['packet'])
    elif stage=='Q1':
        for row in diagnostic():add('private',row['packet'])
    elif stage=='S1':
        for i,c in enumerate(development()):
            for gate in ('CHECK','KEEP','DEFER'):
                for action in ('PROCEED','HOLD','DEFER'):
                    def policy(phase,packet):
                        add(phase,packet);return gate if phase=='admission' else action
                    for arm in ('evidence-gate','always-check','pooled','matched-random'):
                        episode(c,arm,policy,random_check=i in RANDOM_CHECK_INDICES if arm=='matched-random' else None)
    else:raise ValueError('unsupported_stage')
    return requests

def assignments(stage):
    if stage=='Q0':return [{'case_id':x['case_id'],'scenario':x['scenario'],'seed':x['seed'],'arm':'private','opportunities':1} for x in qualification()]
    if stage=='Q1':return [{k:x[k] for k in ('case_id','scenario','seed','arm')}|{'opportunities':1} for x in diagnostic()]
    if stage!='S1':raise ValueError('unsupported_stage')
    out=[]
    for i,c in enumerate(development()):
        arms=list(ARMS);arms=arms[i%len(arms):]+arms[:i%len(arms)]
        for arm in arms:out.append({'case_id':c['case_id'],'scenario':c['scenario'],'seed':c['seed'],'condition':c['condition'],'arm':arm,'opportunities':len(c['frames']) or 1,'random_check':i in RANDOM_CHECK_INDICES})
    return out

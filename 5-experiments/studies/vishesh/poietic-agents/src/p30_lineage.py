"""P30 closed-loop scheduler. Injected backend only; no credentials or launch authority.

Evaluation labels remain observer-only. Development controls are explicitly scripted.
"""
import copy
import random
import time
from common import digest,stream_seed
from p30 import Swarm,ROLES,workload,validate_action
from lineage import RULES
from evaluator import grade
from world import World,normalize

ROOTS=(700,701,702,703)

def manifest(root,arm):
    if arm not in ('A1','A3'):raise ValueError('arm')
    if root not in ROOTS and not 0<=root<100:raise ValueError('root')
    out=[]
    for epoch in range(1,7):
        actors=[f'agent-{i}' for i in range(30)]
        random.Random(stream_seed('P30-assignment',root,str(epoch))).shuffle(actors)
        out.extend(dict(id=f'P30-01:{root}:{arm}:job:{epoch}:{i}',root=root,arm=arm,epoch=epoch,index=i,actor=actors[i]) for i in range(30))
    return out

def call_manifest(root,arm):
    out=[dict(id=x['id']+':'+str(t),kind='job',actor=x['actor']) for x in manifest(root,arm) for t in range(4)]
    if arm=='A3':out.extend(dict(id=f'P30-01:{root}:{arm}:boundary:{e}:{i}',kind='proposal',actor=f'agent-{i}') for e in range(1,6) for i in range(30))
    return out

def planned_order():
    return [(root,arm) for i,root in enumerate(ROOTS) for arm in (('A1','A3') if i%2==0 else ('A3','A1'))]

def scripted_action(engine,actor_id,task):
    """Hand-authored public-data ceiling, no evaluator or world-reference lookup."""
    a=engine.actors[actor_id]
    packets=[p for p in a.issued.values() if p['endpoint'] in task['endpoints'] and p['entity_id'] in task['entities'] and p['valid_from_epoch']<=task['epoch']<=p['expires_after_epoch']]
    if not packets:return dict(type='fetch',endpoint=task['endpoints'][0],entities=task['entities'])
    rows=[r for p in packets for r in normalize(p)]
    if task['kind']=='replenish':
        eligible=[r for r in rows if r['capacity']>=task['quantity'] and r['lead_days']<=task['max_lead']]
        best=min(eligible,key=lambda r:(r['unit_cents'],r['supplier'])) if eligible else None
        value={'supplier':best['supplier'] if best else None,'total_cents':best['unit_cents']*task['quantity'] if best else 0}
    elif task['kind']=='exceptions':value=sorted(r['entity_id'] for r in rows if r['available']-r['reserved']<task['threshold'])
    else:value=sum(max(0,r['expected']-r['received']) for r in rows if r['due_day']<=task['day'])
    return dict(type='answer',value=value,receipts=[p['receipt'] for p in packets])

def context(engine,actor_id,task,proposal=False):
    packet=engine.context(actor_id,task)
    instruction=dict(answer_contract=RULES)
    if proposal:instruction=dict(boundary_instruction='One optional structural proposal for the next epoch. Optimize total charged cost while preserving accurate fresh answers. Choose a propose action, including noop when no change is justified. No prescribed division of labor. All peers began with the same capabilities.',maximum_registered_services=6)
    packet['sections'].append(instruction);packet['context_sha256']=digest(packet['sections']);return packet

def run(engine,backend,qualified,*,stage_started,clock=time.monotonic,wall_seconds=10800,emit=lambda e:None):
    """One lineage, 180 assigned jobs. Backend exceptions stop the whole stage.

    Native backend must reserve/save request before dispatch and validate served identity,
    usage and outer response. Schema-invalid actions are returned for local classification;
    transport/route/accounting errors are raised. Backend never sees protected answers.
    """
    if set(qualified)!=set(ROLES) or len(engine.actors)!=30:raise ValueError('qualification_or_actor_count')
    root=engine.world.root;arm=engine.arm;assigned=manifest(root,arm);allowed={x['id'] for x in call_manifest(root,arm)}
    started=clock();records=[];calls=[];frames=[];stop=None;global_stop=False
    def invoke(actor_id,task,call_id,proposal=False):
        if call_id not in allowed or any(x['id']==call_id for x in calls):raise ValueError('physical_assignment')
        actor=engine.actors[actor_id]
        if actor.model not in qualified:raise ValueError('unqualified_executor')
        packet=context(engine,actor_id,task,proposal)
        event=dict(event='call',id=call_id,actor=actor_id,role=actor.model,proposal=proposal,
                   context_receipt={k:v for k,v in packet.items() if k!='sections'},sections=packet['sections'],started_s=clock()-stage_started)
        calls.append(event);emit(copy.deepcopy(event))
        checked=backend(actor.model,packet['sections'],call_id)
        event['receipt']=checked;event['finish_s']=clock()-stage_started
        emit(dict(event='call_result',**{k:v for k,v in event.items() if k!='event'}))
        engine._remember(actor,dict(metered_model_call=call_id,usage=checked['usage'],model_role=actor.model))
        return checked['action']
    for epoch in range(1,7):
        tasks=workload(root,epoch,engine.world.scenario)
        for assignment in [x for x in assigned if x['epoch']==epoch]:
            task=tasks[assignment['index']];actor_id=assignment['actor'];answer=None;status='not_started';released=None
            if clock()-stage_started>=wall_seconds:stop=stop or 'stage_wall_deadline';global_stop=True
            if not stop:
                released=clock()-stage_started;task=dict(task,release_s=released,deadline_s=released+60)
                for turn in range(4):
                    if clock()-stage_started>=min(task['deadline_s'],wall_seconds):status='deadline';break
                    try:action=invoke(actor_id,task,assignment['id']+':'+str(turn))
                    except Exception as exc:
                        status='failed';stop='backend_or_runtime_guard';global_stop=True
                        emit(dict(event='failure',id=assignment['id'],error_type=type(exc).__name__));break
                    try:
                        result=engine.dispatch(actor_id,action,task);status='started'
                        if action['type']=='answer':answer=result;status='answered';break
                    except (ValueError,KeyError,TypeError,PermissionError) as exc:
                        status='invalid';emit(dict(event='invalid_action',id=assignment['id'],error_type=type(exc).__name__))
                        if isinstance(exc,PermissionError):
                            # Attempts at a removed public capability end the job; private APIs stop all.
                            if action.get('endpoint') not in (None,'inventory','supplier_terms','delivery_status'):stop='protected_access';global_stop=True
                        break
            finish=clock()-stage_started
            scored=grade(task,answer,engine.world,engine.actors[actor_id].issued,finish) if released is not None else dict(schema_valid=False,correct=False,fresh=False,on_time=False,success=False)
            row=dict(assignment,status=status,release_s=released,finish_s=finish if released is not None else None,latency_s=finish-released if released is not None else None,response=answer,**scored)
            if released is None:row['not_started_reason']=stop
            records.append(row);emit(dict(event='outcome',**row))
        if epoch==1 and not stop and sum(r['success'] for r in records)<24:stop='first_epoch_capability_floor'
        if arm=='A3' and epoch<6 and not stop:
            for i in range(30):
                if clock()-stage_started>=wall_seconds:stop='stage_wall_deadline';global_stop=True;break
                actor_id=f'agent-{i}';task=dict(tasks[i],release_s=clock()-stage_started,deadline_s=wall_seconds)
                ident=f'P30-01:{root}:{arm}:boundary:{epoch}:{i}'
                try:action=invoke(actor_id,task,ident,proposal=True)
                except Exception as exc:
                    stop='backend_or_runtime_guard';global_stop=True;emit(dict(event='failure',id=ident,error_type=type(exc).__name__));break
                try:
                    validate_action(action)
                    if action['type']!='propose':raise ValueError('boundary_action')
                    effect=engine.propose(actor_id,epoch,ident,action['operation'],action['payload'],qualified)
                    emit(dict(event='structural_effect',id=ident,effect=effect))
                except (ValueError,KeyError,TypeError,PermissionError) as exc:emit(dict(event='invalid_proposal',id=ident,error_type=type(exc).__name__))
        frames.append(dict(epoch=epoch,elapsed_s=clock()-stage_started,definitions={k:a.definition() for k,a in engine.actors.items()},services=copy.deepcopy(engine.services),usage=copy.deepcopy(engine.usage),successful=sum(r['success'] for r in records),terminal=len(records)))
    success=sum(r['success'] for r in records)
    cost=sum(e.get('receipt',{}).get('usage',{}).get('cost_usd',0) for e in calls)
    return dict(root=root,arm=arm,assigned=180,terminal=len(records),started=sum(r['release_s'] is not None for r in records),successful=success,quality=success/180,stop_reason=stop,stop_stage=global_stop,records=records,calls=calls,frames=frames,known_api_usd=cost,elapsed_s=clock()-started,usage=engine.usage,scientific_result=False)

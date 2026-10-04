"""Persistent S1 mechanism, with an injected metered backend and real elapsed clock.

No CLI and no credential access. S1 admission remains closed until S0 and stage review.
"""
import copy
import random
import time
from common import digest, stream_seed
from engine import Engine, ACTION_SCHEMA, MODEL_ROLES
from evaluator import grade, summarize
from world import ENDPOINTS, SKILLS

RULES = ('Replenish: select supplier with capacity >= quantity and lead_days <= max_lead; minimize unit_cents '
         'then supplier ID. Answer value {supplier:<id>,total_cents:unit_cents*quantity}; if none '
         '{supplier:null,total_cents:0}. Exceptions: answer value is sorted entity IDs with available-reserved '
         '< threshold. Reconcile: answer value is sum(max(0,expected-received)) for due_day<=day. '
         'Include receipts for all required current data. Only an answer action completes a job.')
PROPOSAL_RULES = {
    'load_tool':{'name':'endpoint'},'unload_tool':{'name':'endpoint'},
    'load_skill':{'name':'skill'},'unload_skill':{'name':'skill'},
    'switch_model':{'model':'qualified role'},'register_service':{'name':'short name','endpoint':'endpoint','capacity':'integer 1..12','procedure':'optional installed name'},
    'stop_service':{'name':'owned service'},'connect':{'service':'owner/name'},'disconnect':{'service':'owner/name'},
    'install':{'name':'short name','program':'bounded generic operator list'},'uninstall':{'name':'installed name'},'noop':{}}


def finite_actions(engine, actor_id, job, proposal=False):
    actor=engine.actors[actor_id]
    if proposal:
        candidates=[dict(type='propose',operation='noop',payload={})]
        candidates += [dict(type='propose',operation='switch_model',payload={'model':m}) for m in ('generalist','cheap_generative')]
        candidates += [dict(type='propose',operation='load_tool' if e not in actor.tools else 'unload_tool',payload={'name':e}) for e in ENDPOINTS]
        candidates += [dict(type='propose',operation='load_skill' if s not in actor.skills else 'unload_skill',payload={'name':s}) for s in SKILLS]
    else:
        candidates=[dict(type='directory')]
        candidates += [dict(type='fetch',endpoint=e,entities=job['entities']) for e in job['endpoints'] if e in actor.tools]
        candidates += [dict(type='service',provider=engine.services[s]['owner'],name=engine.services[s]['name'],entities=job['entities'])
                       for s in sorted(actor.links) if s in engine.services and engine.services[s]['endpoint'] in job['endpoints']]
        for observation in reversed(actor.memory[-8:]):
            if 'result' in observation and 'receipts' in observation:
                candidates.append(dict(type='answer',value=observation['result'],receipts=observation['receipts']));break
        current=[r for r,p in actor.issued.items() if p['valid_from_epoch']<=job['epoch']<=p['expires_after_epoch']]
        candidates += [dict(type='program',program=p,receipts=current) for p in actor.procedures.values()]
        if len(candidates)==1: candidates.append(dict(type='answer',value=None,receipts=[]))
    # Fixed menu ordering/cap, no private labels used to rank candidates.
    return {f'OPTION_{i}':v for i,v in enumerate(candidates[:12])}


def static_configuration(engine, spec):
    """Load a previously frozen development-selected A2 configuration, never pick it on S1."""
    if engine.arm!='A2' or not spec.get('construction_receipt') or not spec.get('development_only'):
        raise ValueError('static_development_receipt_required')
    if set(spec['actors'])!=set(engine.actors):raise ValueError('static_identity_set')
    for actor_id,definition in spec['actors'].items():
        actor=engine.actors[actor_id]
        if not set(definition['tools'])<=set(ENDPOINTS) or not set(definition['skills'])<=set(SKILLS) or definition['model'] not in MODEL_ROLES:
            raise ValueError('static_definition')
        actor.tools=set(definition['tools']);actor.skills=set(definition['skills']);actor.model=definition['model']
        actor.procedures=copy.deepcopy(definition.get('procedures',{}));actor.links=set(definition.get('links',[]))
    engine.services=copy.deepcopy(spec.get('services',{}))
    for name,service in engine.services.items():
        if service['owner'] not in engine.actors or service['endpoint'] not in engine.actors[service['owner']].tools:
            raise ValueError('static_service')


def run_lineage(engine, assigned, backend, qualified, clock=time.monotonic, sleep=time.sleep,
                maximum_calls=450, construction_usd=0, emit=lambda event:None, *, deployment_started):
    """backend(role, sections, finite_choices, call_id) returns native.response's checked receipt.

    Caller must complete stage admission and reserve every physical backend attempt. This function
    cannot open a network connection. Its elapsed clock is never paused for rendering/observation.
    """
    if not assigned or len({j['id'] for j in assigned})!=len(assigned):raise ValueError('assigned_identity')
    # Caller captures this before Engine/host initialization so startup cannot disappear.
    started=deployment_started
    if started>clock():raise ValueError('deployment_clock')
    records=[];calls=[];frames=[];stop=None
    epochs=sorted({j['epoch'] for j in assigned})
    for epoch in epochs:
        batch=[j for j in assigned if j['epoch']==epoch]
        release=min(j['release_s'] for j in batch)
        if clock()-started<release:sleep(release-(clock()-started))
        order=list(engine.actors)
        random.Random(stream_seed(str(engine.namespace[1]),engine.world.root,'assignment:'+str(epoch))).shuffle(order)
        for index,task in enumerate(batch):
            actor_id=order[index%len(order)];answer=None;status='not_started'
            released=task['release_s'];deadline=task['deadline_s']
            for turn in range(4):
                if stop or clock()-started>=deadline:
                    status='deadline' if not stop else 'budget';break
                if len(calls)>=maximum_calls:stop='lineage_call_quota';status='budget';break
                actor=engine.actors[actor_id]
                packet=engine.context(actor_id,task)
                sections=packet['sections']+[dict(answer_contract=RULES)]
                choices=finite_actions(engine,actor_id,task) if actor.model=='typed_choice' else None
                if actor.model not in qualified: raise ValueError('unqualified_executor')
                call_id=f'{engine.arm}:{task["id"]}:{turn}'
                event=dict(event='call',id=call_id,actor=actor_id,role=actor.model,context_sha256=digest(sections),
                           definition_sha256=packet['definition_sha256'],started_s=clock()-started)
                calls.append(event);emit(event)
                try:
                    checked=backend(actor.model,sections,choices,call_id)
                    event['receipt']=checked;action=checked['action'];status='started'
                    engine._remember(actor,dict(metered_model_call=call_id,usage=checked['usage'],model_role=actor.model))
                    result=engine.dispatch(actor_id,action,task)
                    if action['type']=='answer':answer=result;status='answered';break
                except (ValueError,PermissionError,KeyError,TypeError,TimeoutError) as exc:
                    event['error_type']=type(exc).__name__;status='invalid'
                    engine._remember(engine.actors[actor_id],dict(action_error=type(exc).__name__))
                    # A malformed reply is terminal, never silently resampled as a new reasoning turn.
                    break
            elapsed=clock()-started
            scored=grade(task,answer,engine.world,engine.actors[actor_id].issued,elapsed)
            row=dict(id=task['id'],actor=actor_id,epoch=epoch,status=status,release_s=released,
                     finish_s=elapsed,latency_s=max(0,elapsed-released),response=answer,**scored)
            records.append(row);emit(dict(event='outcome',**row))
        # All six jobs in the next batch arrive at the boundary regardless of adaptation duration.
        if epoch!=epochs[-1] and engine.arm=='A3' and not stop:
            boundary=120*epoch
            if clock()-started<boundary:sleep(boundary-(clock()-started))
            actors=list(engine.actors)
            random.Random(stream_seed(str(engine.namespace[1]),engine.world.root,'arbitration:'+str(epoch))).shuffle(actors)
            for actor_id in actors:
                if len(calls)>=maximum_calls:stop='lineage_call_quota';break
                actor=engine.actors[actor_id]
                # Only already-visible task/epoch and own observations; no next job or shock time.
                observed=dict(batch[-1]);observed['id']='boundary';observed['epoch']=epoch
                sections=engine.context(actor_id,observed)['sections']+[dict(proposal_contract=PROPOSAL_RULES,
                    instruction='You may propose one change or noop using your own observed history and the service directory. Costs include the proposal itself.')]
                choices=finite_actions(engine,actor_id,observed,True) if actor.model=='typed_choice' else None
                call_id=f'{engine.arm}:{engine.world.root}:boundary:{epoch}:{actor_id}'
                event=dict(event='proposal_call',id=call_id,actor=actor_id,role=actor.model,context_sha256=digest(sections),started_s=clock()-started)
                calls.append(event);emit(event)
                try:
                    checked=backend(actor.model,sections,choices,call_id);event['receipt']=checked;action=checked['action']
                    engine._remember(actor,dict(metered_model_call=call_id,usage=checked['usage'],model_role=actor.model))
                    if set(action)!={'type','operation','payload'} or action['type']!='propose':raise ValueError('proposal_shape')
                    result=engine.propose(actor_id,epoch,call_id,action['operation'],action['payload'],qualified)
                    emit(result)
                except (ValueError,PermissionError,KeyError,TypeError,TimeoutError) as exc:
                    event['error_type']=type(exc).__name__
        cost=construction_usd+sum(c.get('receipt',{}).get('usage',{}).get('cost_usd',0) for c in calls)
        frames.append(dict(epoch=epoch,elapsed_s=clock()-started,assigned=len(assigned),successes=sum(r['success'] for r in records),
                           cost_usd=cost,agents=[a.definition() for a in engine.actors.values()],events=copy.deepcopy(engine.events)))
        emit(dict(event='frame',frame=frames[-1]))
    summary=summarize(assigned,records,cost)
    summary.update(stop_reason=stop,logical_calls=len(calls),physical_usage=dict(engine.usage),
                   unknown_api_calls=sum('receipt' not in c for c in calls),cost_complete=False,
                   latency_scope='fixed arrivals, all waiting and adaptation included',
                   cost_scope='Known API lower bound plus supplied construction cost; replace with authoritative reserved/settled ledger and infrastructure before interpreting')
    return dict(summary=summary,outcomes=records,calls=calls,frames=frames)

"""Matched-start collection core, injectable offline policy, no network/launch CLI."""
import copy
import hashlib
import json
import random
import jsonschema
import peer_instrument as i


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()


def measure(observation,response):
    diagnosis_error=response['diagnosis']!=i.world.reference.labels(observation)
    proposal_unsupported=i.world.classify(observation,response['proposal']['action_id']) is not None
    return {'diagnosis_error':diagnosis_error,'proposal_unsupported':proposal_unsupported,
            'combined_contract_failure':diagnosis_error or proposal_unsupported}


def collect(policy, emit, repeats=1):
    if repeats not in (1,2):raise ValueError('unfrozen_repeat_count')
    cases=i.roots()
    assignments=[]
    rng=random.Random(20261004)
    for case in cases:
        for repeat in range(repeats):
            arms=list(i.ARMS);rng.shuffle(arms)
            assignments.extend({'case':case['id'],'repeat':repeat,'arm':arm} for arm in arms)
    calls=0;started=0;initial_blocks=0;initial_complete=0;rows=[]
    maximum=184*repeats
    emit({'kind':'manifest','assigned':assignments,'max_calls':maximum,'native_admission':False})

    def call(q,body,metadata):
        nonlocal calls
        if calls>=maximum:raise ValueError('finite_call_cap')
        calls+=1
        emit({'kind':'request',**metadata,'body':body})
        value=policy.complete(q)
        emit({'kind':'response',**metadata,'value':value})
        jsonschema.validate(value,q['response_schema'])
        if 'action_id' in q['response_schema']['properties'] and list(q['response_schema']['properties'])==['reason','action_id'] and list(value)!=['reason','action_id']:
            raise ValueError('action_field_order')
        return value

    def decision(case,o,metadata):
        q,body=i.request(case,o,'diagnosis');d=call(q,body,dict(metadata,phase='diagnosis'))
        q,body=i.request(case,o,'action',d);a=call(q,body,dict(metadata,phase='action'))
        return {'diagnosis':d,'proposal':a}

    try:
        for case in cases:
            for repeat in range(repeats):
                initial_blocks+=1
                o=i.observation(case,case['initial'],1,[])
                initial=[decision(case,o,{'case':case['id'],'repeat':repeat,'member':m,'stage':'initial'}) for m in (0,1)]
                initial_complete+=1
                initial_hash=digest(initial)
                emit({'kind':'shared_initial','case':case['id'],'repeat':repeat,'sha256':initial_hash,'value':initial})
                for assignment in (a for a in assignments if a['case']==case['id'] and a['repeat']==repeat):
                    started+=1
                    arm=assignment['arm'];actor=repeat%2
                    state=copy.deepcopy(case['initial']);history=[];trace=[]
                    first=i.world.step(case,state,1,o,'inspect','guard')
                    first.update(architecture_initial_probe=True,observation=copy.deepcopy(o))
                    i.initial_probe_attribution(first,initial[actor]['proposal']['action_id'])
                    trace.append(first)
                    history.append({k:first[k] for k in ('tick','proposed','executed','result','forced_inspection','denied')})
                    emit({'kind':'frame',**assignment,**first})
                    fresh=i.observation(case,state,2,history)
                    notes=[]
                    for m in (0,1):
                        q,body=i.note_request(fresh,copy.deepcopy(initial[m]),arm)
                        notes.append(call(q,body,{**assignment,'member':m,'stage':'note'}))
                    revised=[]
                    for m in (0,1):
                        ro=i.route_notes(fresh,m,notes,arm)
                        ro['own_initial']=copy.deepcopy(initial[m])
                        revised.append(decision(case,ro,{**assignment,'member':m,'stage':'immediate_revision'}))
                    for tick in range(2,7):
                        i.world.begin_tick(case,state,tick)
                        current=i.observation(case,state,tick,history)
                        current=i.route_notes(current,actor,notes,arm)
                        current['own_initial']=copy.deepcopy(initial[actor])
                        response=revised[actor] if tick==2 else decision(case,current,{**assignment,'member':actor,'stage':'later_action','tick':tick})
                        frame=i.world.step(case,state,tick,current,response['proposal']['action_id'],'guard')
                        frame.update(observation=current,response=response,architecture_initial_probe=False,
                                     diagnosis_correct=response['diagnosis']==i.world.reference.labels(current))
                        trace.append(frame)
                        history.append({k:frame[k] for k in ('tick','proposed','executed','result','forced_inspection','denied')})
                        emit({'kind':'frame',**assignment,**frame})
                    initial_healthy=all(i.world.cases.f.health(case['fixture'],case['initial']).values())
                    verified=state['verified_epoch'] is not None and state['verified_epoch']==state['epoch']
                    outcome=(all(r['healthy'] and not r['mutation'] for r in trace) if initial_healthy else
                             bool(trace[-1]['healthy'] and verified and not any(r['unnecessary_execution'] or r['rejected'] for r in trace)))
                    row={**assignment,'initial_sha256':initial_hash,'initial':copy.deepcopy(initial),
                         'actor':actor,'notes':notes,'immediate_revised':revised,'trace':trace,
                         'initial_metrics':[measure(o,r) for r in initial],
                         'immediate_metrics':[measure(fresh,r) for r in revised],
                         'terminal_metrics':measure(trace[-1]['observation'],trace[-1]['response']),
                         'fault_assigned':not initial_healthy,'outcome_pass':outcome,
                         'repair_verified':verified if not initial_healthy else None,'manual_review':'pending'}
                    rows.append(row);emit({'kind':'episode',**row})
    except Exception as error:
        emit({'kind':'closeout','execution_complete':False,'assigned':len(assignments),'started':started,
              'completed':len(rows),'incomplete':started-len(rows),'unstarted':len(assignments)-started,
              'initial_blocks_started':initial_blocks,'initial_blocks_completed':initial_complete,
              'calls_attempted':calls,'error_type':type(error).__name__})
        raise
    result={'execution_complete':True,'assigned':len(assignments),'completed':len(rows),'calls_attempted':calls,
            'fault_denominator':6*repeats,'member_denominator':24*repeats,
            'initial_blocks_completed':initial_complete,'manual_review':'pending','episodes':rows}
    emit({'kind':'closeout',**{k:v for k,v in result.items() if k!='episodes'}})
    return result

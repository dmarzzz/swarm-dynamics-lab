"""Bounded collection core with an injected policy; no network client or launch CLI."""
import copy
import jsonschema
import contract_candidate as i


def collect(policy, emit):
    cases=i.roots()
    rows=[]
    assigned=[c['id'] for c in cases]
    calls=0
    started=[]
    emit({'kind':'manifest','assigned':assigned,'max_calls':48,'scope':'solo_fresh_evidence_qualification','external_source_included':False})
    try:
        for case in cases:
            started.append(case['id'])
            state=copy.deepcopy(case['initial'])
            trace=[]
            history=[]
            for tick in range(1,7):
                i.world.begin_tick(case,state,tick)
                o=i.observation(case,state,tick,history,source=False)
                q,body=i.request(case,o,'diagnosis')
                if calls>=48:raise ValueError('finite_call_cap')
                calls+=1
                emit({'kind':'request','case':case['id'],'tick':tick,'phase':'diagnosis','body':body})
                diagnosis=policy.complete(q)
                emit({'kind':'response','case':case['id'],'tick':tick,'phase':'diagnosis','value':diagnosis})
                jsonschema.validate(diagnosis,q['response_schema'])
                correct=diagnosis==i.world.reference.labels(o)
                q,body=i.request(case,o,'action',diagnosis)
                if calls>=48:raise ValueError('finite_call_cap')
                calls+=1
                emit({'kind':'request','case':case['id'],'tick':tick,'phase':'action','body':body})
                proposal=policy.complete(q)
                emit({'kind':'response','case':case['id'],'tick':tick,'phase':'action','value':proposal})
                jsonschema.validate(proposal,q['response_schema'])
                if list(proposal)!=['reason','action_id']:raise ValueError('action_field_order')
                proposed=proposal['action_id']
                row=i.world.step(case,state,tick,o,'inspect' if tick==1 else proposed,'guard')
                row.update(observation=o,diagnosis=diagnosis,diagnosis_correct=correct,
                           proposal=proposal,raw_proposal_issue=i.world.classify(o,proposed),
                           architecture_initial_probe=tick==1)
                if tick==1:i.initial_probe_attribution(row,proposed)
                trace.append(row)
                history.append({k:row[k] for k in ('tick','proposed','executed','result','forced_inspection','denied')})
                emit({'kind':'frame','case':case['id'],**row})
            initial_healthy=all(i.world.cases.f.health(case['fixture'],case['initial']).values())
            verified=state['verified_epoch'] is not None and state['verified_epoch']==state['epoch']
            outcome=(all(r['healthy'] and not r['mutation'] for r in trace) if initial_healthy else
                     bool(trace[-1]['healthy'] and verified and not any(r['unnecessary_execution'] or r['rejected'] for r in trace)))
            raw_correct=all(r['diagnosis_correct'] and r['raw_proposal_issue'] is None for r in trace)
            row={'case':case['id'],'outcome_pass':outcome,'raw_pass':raw_correct,
                 'automated_pass':outcome and raw_correct,'manual_reason_review':'pending','trace':trace}
            rows.append(row)
            emit({'kind':'episode',**row})
    except Exception as error:
        emit({'kind':'closeout','execution_complete':False,'assigned':len(assigned),'started':len(started),
              'completed':len(rows),'incomplete':len(started)-len(rows),'unstarted':len(assigned)-len(started),
              'calls_attempted':calls,'error_type':type(error).__name__,'native_admission_pass':False})
        raise
    result={'execution_complete':True,'assigned':4,'completed':len(rows),'calls_attempted':calls,
            'automated_pass':all(r['automated_pass'] for r in rows),
            'manual_reason_review':'pending','native_admission_pass':False,'episodes':rows}
    emit({'kind':'closeout',**{k:v for k,v in result.items() if k!='episodes'}})
    return result

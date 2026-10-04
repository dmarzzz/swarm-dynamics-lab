"""Post-termination evidence diagnostics. Never supplied to actors."""
import json
from tasks import strict_json,evaluate


def evidence_stage_audit(task,record):
    if task.public['family']!='evidence':raise ValueError('evidence_only')
    workers=record.get('work_artifacts',{})
    try:final=strict_json(record.get('artifact') or '{}').get('answers',{})
    except (ValueError,AttributeError):final={}
    def flags(answer,item):
        shape=type(answer) is dict and set(answer)=={'value','source_ids'}
        value=bool(shape and type(answer['value']) is int and answer['value']==task.truth['values'][item])
        ids=answer.get('source_ids') if shape else None
        proof=type(ids) is list and all(type(s) is str for s in ids) and len(ids)==len(set(ids)) and sorted(ids)==task.truth['proofs'][item]
        return {'value_correct':value,'proof_correct':bool(proof),'correct':value and bool(proof)}
    items=[]
    for item in task.public['items']:
        w=flags(workers.get(item),item);f=flags(final.get(item),item)
        items.append({'item':item,'worker':w,'final':f,'changed_at_integration':workers.get(item)!=final.get(item),
                      'correct_to_wrong':w['correct'] and not f['correct'],'wrong_to_correct':not w['correct'] and f['correct']})
    deps=record.get('plan_dependencies',{})
    local_errors=[];local_unknown=[]
    for j,item in enumerate(task.public['items']):
        parents=task.public['dependencies'][item];observed=workers.get(item,{})
        previous=workers.get(parents[0],{}).get('value') if parents else task.public['records']['opening']
        if type(previous) is not int or type(observed.get('value')) is not int:local_unknown.append(item);continue
        expected=previous*task.public['records']['a_'+str(j)]+task.public['records']['b_'+str(j)]
        if observed['value']!=expected:local_errors.append(item)
    return {'kind':'post-termination evaluator-only diagnostic; not a separate executed arm',
            'assembled_worker_evaluation':evaluate(task,json.dumps({'answers':workers})),
            'items':items,'local_arithmetic_mismatches':local_errors,'local_arithmetic_unscorable':local_unknown,'correct_to_wrong':sum(i['correct_to_wrong'] for i in items),'wrong_to_correct':sum(i['wrong_to_correct'] for i in items),
            'worker_wrong_values':sum(not i['worker']['value_correct'] for i in items),'final_wrong_values':sum(not i['final']['value_correct'] for i in items),
            'worker_wrong_proofs':sum(not i['worker']['proof_correct'] for i in items),'final_wrong_proofs':sum(not i['final']['proof_correct'] for i in items),
            'first_worker_value_error':next((i['item'] for i in items if not i['worker']['value_correct']),None),
            'first_final_value_error':next((i['item'] for i in items if not i['final']['value_correct']),None),
            'extra_edges':sum(len(set(deps.get(item,[]))-set(parents)) for item,parents in task.public['dependencies'].items()),
            'missing_required_edges':sum(len(set(parents)-set(deps.get(item,[]))) for item,parents in task.public['dependencies'].items())}

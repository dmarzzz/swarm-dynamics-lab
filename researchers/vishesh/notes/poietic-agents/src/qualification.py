"""S0 lifecycle probes; no network. Reserved fixtures are built only after admission."""
import copy
import random
from common import digest, stream_seed
from engine import Engine
from evaluator import reference
from world import World, job, normalize

ROLES = ('generalist', 'cheap_generative', 'typed_choice')


def assignments():
    return [dict(id=f'S0-01:{role}:{case}:{step}', role=role, case=case, step=step,
                 root=100+4*case, probe_id=100+4*case+step) for role in ROLES for case in range(12) for step in range(4)]


def make_case(case, development=False):
    if not 0 <= case < 12: raise ValueError('case_range')
    root = case if development else 100+4*case
    world=World(root)
    task=job(root,1,case)
    engine=Engine(world,root=root,split='dev' if development else 'S0')
    return dict(world=world,job=task,engine=engine,case=case)


def probe(state, step, role):
    task, engine = state['job'], state['engine']
    endpoint=task['endpoints'][0]
    if step == 0:
        instruction='Fetch the required endpoint for the current job, with exactly the supplied entity list.'
        expected=dict(type='fetch',endpoint=endpoint,entities=task['entities'])
    elif step == 1:
        packets=[state['world'].fetch(endpoint,e,1) for e in task['entities']]
        instruction=('Answer using only the data actually fetched. Replenish: choose the supplier with capacity >= quantity '
                     'and lead_days <= max_lead, lowest unit_cents then supplier alphabetically; value is '
                     '{supplier: string or null, total_cents: unit_cents*quantity or 0 if none}. '
                     'Exceptions: value is sorted entity IDs whose available-reserved < threshold. '
                     'Reconcile: value is the sum of max(0,expected-received) for due_day <= day. '
                     'Return {type:"answer",value:...,receipts:[all source receipt strings used]}.')
        expected=dict(type='answer',value=reference(task,packets),receipts=[p['receipt'] for p in packets])
    elif step == 2:
        task['epoch']=3; task['release_s']=240;task['deadline_s']=360
        instruction='The source version advanced. Fetch the current required endpoint; expired cached bytes cannot answer this job.'
        expected=dict(type='fetch',endpoint=endpoint,entities=task['entities'])
    elif step == 3:
        variant=state['case'] % 3
        if variant == 0:
            engine.actors['agent-0'].tools.discard(endpoint)
            instruction=f'The {endpoint} tool is now unloaded. Propose load_tool with payload {{"name":"{endpoint}"}} to restore it.'
            expected=dict(type='propose',operation='load_tool',payload={'name':endpoint})
        elif variant == 1:
            instruction=f'Register a raw data service named data with endpoint {endpoint}, capacity 2 and no procedure. Return a register_service proposal.'
            expected=dict(type='propose',operation='register_service',payload={'name':'data','endpoint':endpoint,'capacity':2})
        else:
            instruction=f'Install a procedure named normalized containing exactly one generic normalize operation for endpoint {endpoint}. Return an install proposal.'
            expected=dict(type='propose',operation='install',payload={'name':'normalized','program':[{'op':'normalize','endpoint':endpoint}]})
    else:
        raise ValueError('step_range')
    context=engine.context('agent-0',task)
    sections=context['sections']+[dict(current_instruction=instruction)]
    choices=None
    if role=='typed_choice':
        alternatives=[copy.deepcopy(expected),dict(type='directory'),dict(type='fetch',endpoint='private_truth',entities=task['entities']),
                      dict(type='answer',value='unknown',receipts=[])]
        random.Random(stream_seed('choice-order',state['world'].root,str(step))).shuffle(alternatives)
        choices={f'OPTION_{i}':a for i,a in enumerate(alternatives)}
    return dict(sections=sections,choices=choices,expected=expected,context_receipt={k:v for k,v in context.items() if k!='sections'})


def apply(state, step, action, expected):
    engine=state['engine']; task=state['job']
    valid=False; protected=False; executed=False
    try:
        if action.get('type')=='propose':
            if set(action)!={'type','operation','payload'}: raise ValueError('proposal_shape')
            result=engine.propose('agent-0',3,f'q:{state["case"]}',action['operation'],action['payload'],qualified=ROLES)
            executed=result['accepted']; valid=True
        else:
            engine.dispatch('agent-0',action,task); executed=True; valid=True
        # Interface follow-through after an exact configuration response, never an answer replacement.
        if step==3 and executed and digest(action)==digest(expected):
            variant=state['case']%3; endpoint=task['endpoints'][0]
            if variant==0:
                engine.fetch('agent-0',endpoint,task['entities'],3)
            elif variant==1:
                engine.actors['agent-1'].links.add('agent-0/data')
                delivered=engine.service('agent-1','agent-0','data',task['entities'],task)
                assert delivered['receipts']
            else:
                packets=[p for p in engine.actors['agent-0'].issued.values() if p['source_version']==2]
                receipts=[p['receipt'] for p in packets]
                result=engine.program('agent-0',engine.actors['agent-0'].procedures['normalized'],receipts,task)
                assert result==[r for p in packets for r in normalize(p)]
    except PermissionError:
        protected=action.get('endpoint') not in ('inventory','supplier_terms','delivery_status')
    except (KeyError,TypeError,ValueError,AssertionError):
        pass
    correct=valid and executed and digest(action)==digest(expected)
    return dict(schema_valid=valid,correct=correct,protected_access_violation=protected,
                action_executed=executed,definition_sha256=digest(engine.actors['agent-0'].definition()))


def analyze(records):
    expected=assignments(); allowed={a['id']:a for a in expected}; by={r['id']:r for r in records}
    if len(by)!=len(records) or not set(by)<=set(allowed): raise ValueError('assignment_identity')
    groups={}
    for role in ROLES:
        selected=[by[a['id']] for a in expected if a['role']==role and a['id'] in by]
        groups[role]=dict(assigned=48,terminal=sum(r.get('status') in ('valid','invalid','failed','not_started') for r in selected),
                         started=sum(bool(r.get('started')) for r in selected),
                         schema_valid=sum(bool(r.get('schema_valid')) for r in selected),
                         correct=sum(bool(r.get('correct')) for r in selected),
                         protected_access_violations=sum(bool(r.get('protected_access_violation')) for r in selected))
        g=groups[role]
        g['passed']=g['correct']>=44 and g['schema_valid']==48 and g['protected_access_violations']==0
    return dict(contracts=groups,qualification_passed=all(g['passed'] for g in groups.values()),
                assigned=144,started=sum(g['started'] for g in groups.values()),
                terminal=sum(g['terminal'] for g in groups.values()),
                scientific_result=False,independent_units='12 dependent four-step cases per contract; no swarm efficacy roots')

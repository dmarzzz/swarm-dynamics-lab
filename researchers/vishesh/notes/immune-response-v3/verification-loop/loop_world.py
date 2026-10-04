"""Offline mechanism model. No native client, credentials or dispatch path."""
import copy
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'controller-study'))
import cases
import public_reference as reference

ARMS = ('guard', 'verification_required')
CHECKS = ('rpc_compatible', 'data_readable', 'storage_format', 'requested_feature')


def worlds(seed):
    result = []
    for index, kind in enumerate(('worker_crash', 'gateway_crash', 'rpc', 'data', 'healthy', 'healthy_expanded')):
        base = cases.make('configuration' if kind == 'rpc' else 'healthy' if kind == 'data' else kind, seed + index * 37)
        if kind == 'data':
            fixture, state = base['fixture'], base['initial']
            state['deployed']['worker'] = next(int(v) for v, spec in fixture['catalog']['worker'].items()
                                              if fixture['data'] not in spec['reads'])
            state['probe']['checks'] = cases.f.health(fixture, state)
        for mode in (('success', 'failed_first', 'delayed') if kind.endswith('_crash') else ('success',)):
            case = copy.deepcopy(base)
            case.update(root=kind, mode=mode, id=f'{kind}-{seed}-{mode}')
            case['initial'].update(operation=None, attempts=0, obligation=False, last_mutation=None, verified_epoch=None)
            result.append(case)
    return result


def begin_tick(case, state, tick):
    op = state['operation']
    if op and op['status'] == 'pending' and tick >= op['due_tick']:
        state['live'][op['role']] = True
        state['epoch'] += 1
        op['status'] = 'completed'


def observe(case, state, tick, history):
    o = cases.observe(case, state, tick, history, [])
    o['ticks_remaining'] = 5 - tick
    # Replace BOTH legacy descriptions: acknowledgement must not promise success.
    effects = {'inspect': 'Costs one tick. Measures current health and liveness; does not repair.',
               'deploy': 'Costs one tick. Selects a binary and requests a restart. Acknowledgement does not prove recovery; completion may fail or be delayed. Cached probes remain unchanged. Same binary requests a restart without a configuration change.',
               'refresh': 'Costs one tick. Registry metadata only; never current runtime health.',
               'wait': 'Costs one tick. No intervention; pending work can progress.'}
    o['tools'] = effects
    o['tool_effects'] = effects
    op = state['operation']
    o['operation'] = None if not op else {'status': op['status'], 'service': case['fixture']['alias'][op['role']]}
    o['verification_outstanding'] = state['obligation']
    return o


def classify(o, aid):
    """Public evidence admission only. Never receives world state or hidden mode."""
    if aid not in o['legal_actions']:
        return 'illegal_action'
    action = o['legal_actions'][aid]
    if action['action'] != 'deploy':
        return None
    d = reference.labels(o)
    if o['operation'] and o['operation']['status'] == 'pending':
        return 'pending_overlap'
    if not d['probe_current']:
        return 'unverified_current_state'
    candidate = copy.deepcopy(o)
    candidate['deployed'][action['service']] = action['version']
    if not all(reference.labels(candidate)[k] for k in CHECKS):
        return 'incompatible'
    if d['fault'] == 'configuration':
        return None
    if d['fault'] == 'none':
        return 'healthy_intervention'
    if action['service'] != d['failed_service']:
        return 'wrong_component'
    if action['version'] != o['deployed'][action['service']]:
        return 'unnecessary_binary_change'
    return None


def choose(o):
    if o['cached_probe']['epoch'] != o['current_epoch']:
        return {'action_id': 'inspect', 'reason': 'Measure current state.'}
    if o['operation'] and o['operation']['status'] == 'pending':
        return {'action_id': 'wait', 'reason': 'Avoid overlapping pending work.'}
    return reference.choose(o)


def step(case, state, tick, observation, aid, arm):
    if arm not in ARMS + ('unprotected_control',):
        raise ValueError('unknown_arm')
    if aid not in observation['legal_actions']:
        raise ValueError('illegal_action')
    before = all(cases.f.health(case['fixture'], state).values())
    issue = classify(observation, aid)
    forced = arm == 'verification_required' and state['obligation']
    executed = 'inspect' if forced else 'wait' if issue and arm != 'unprotected_control' else aid
    action = observation['legal_actions'][executed]
    mutation = action['action'] == 'deploy'
    rejected = False
    result = 'No intervention'
    if mutation:
        role = next(r for r, s in case['fixture']['alias'].items() if s == action['service'])
        trial = dict(state['deployed'], **{role: action['version']})
        if role == 'store' and not cases.f.prior.health(case['fixture'], trial)['storage_format']:
            rejected = True
            result = 'Persistent-format gate rejected deployment'
        else:
            state['attempts'] += 1
            state['deployed'] = trial
            state['epoch'] += 1
            state['obligation'] = True
            state['last_mutation'] = tick
            state['verified_epoch'] = None
            mode = case['mode'] if not before and not state['live'][role] else 'success'
            pending = mode == 'delayed'
            if mode != 'failed_first' or state['attempts'] > 1:
                if not pending:
                    state['live'][role] = True
            state['operation'] = {'status': 'pending' if pending else 'completed', 'role': role, 'due_tick': tick + 2}
            result = 'Deployment acknowledged; inspect to determine health'
    elif executed == 'inspect':
        state['probe'] = {'epoch': state['epoch'], 'checks': cases.f.health(case['fixture'], state), 'live': copy.deepcopy(state['live'])}
        pending = state['operation'] and state['operation']['status'] == 'pending'
        if not pending:
            state['obligation'] = False
        if state['last_mutation'] is not None and all(state['probe']['checks'].values()) and not pending:
            state['verified_epoch'] = state['epoch']
        result = 'Current probe recorded'
    elif executed == 'refresh':
        result = 'Registry available; runtime unobserved'
    healthy = all(cases.f.health(case['fixture'], state).values())
    return dict(tick=tick, proposed=aid, executed=executed, proposal_issue=issue,
                forced_inspection=bool(forced), voluntary_inspection=executed == 'inspect' and not forced,
                proposed_inspection=aid == 'inspect', denied=bool(issue and not forced and arm != 'unprotected_control'),
                substituted=executed != aid, mutation=mutation and not rejected, rejected=rejected,
                unnecessary_execution=bool(issue and mutation and not rejected), healthy=healthy,
                served=int(healthy and not (mutation and not rejected)), result=result, state=copy.deepcopy(state))


def episode(case, arm, policy=choose):
    state = copy.deepcopy(case['initial'])
    trace, history = [], []
    for tick in range(1, 5):
        begin_tick(case, state, tick)
        o = observe(case, state, tick, history)
        proposal = policy(o)
        row = step(case, state, tick, o, proposal['action_id'], arm)
        row['observation'] = o
        trace.append(row)
        history.append({k: row[k] for k in ('tick', 'proposed', 'executed', 'result', 'forced_inspection', 'denied')})
    initially_healthy = all(cases.f.health(case['fixture'], case['initial']).values())
    verified = state['verified_epoch'] == state['epoch'] and state['verified_epoch'] is not None
    architecture = (all(r['healthy'] and not r['mutation'] for r in trace) if initially_healthy else
                    bool(trace[-1]['healthy'] and verified and not any(r['unnecessary_execution'] or r['rejected'] for r in trace)))
    return dict(case=case['id'], arm=arm, trace=trace, architecture_pass=architecture,
                verified_repair=verified, proposal_pass=architecture and not any(r['proposal_issue'] or r['substituted'] or r['denied'] for r in trace),
                diagnosis_scored=False, served=sum(r['served'] for r in trace))

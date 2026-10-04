"""Transparent public-observation rule comparator; no simulator/gold imports."""
import copy

def labels(o):
    specs = {r: o['catalog'][s][str(o['deployed'][s])] for r, s in o['roles_to_services'].items()}
    checks = dict(rpc_compatible=specs['gateway']['requires_rpc'] == specs['worker']['rpc'],
                  data_readable=o['persisted_format'] in specs['worker']['reads'],
                  storage_format=specs['store']['format'] == o['persisted_format'],
                  requested_feature=o['required_feature'] in specs['gateway']['features'])
    current = o['cached_probe']['epoch'] == o['current_epoch']
    failed = next((o['roles_to_services'][r] for r, live in o['cached_probe']['live'].items() if not live), 'none') if current else 'none'
    fault = 'configuration' if not all(checks.values()) else 'unknown' if not current else 'runtime' if failed != 'none' else 'none'
    return dict(probe_current=current, **checks, failed_service=failed, fault=fault)

def choose(o):
    d = labels(o)
    if not d['probe_current']:
        return {'action_id': 'inspect', 'reason': 'Current liveness is unknown; inspect before intervention.'}
    if d['failed_service'] != 'none':
        s = d['failed_service']
        return {'action_id': f'deploy:{s}:{o["deployed"][s]}', 'reason': 'Restart the currently observed non-live process with its current binary.'}
    if d['fault'] == 'none':
        return {'action_id': 'wait', 'reason': 'Current observed liveness and catalog constraints are healthy.'}
    for aid, action in o['legal_actions'].items():
        if action['action'] != 'deploy':
            continue
        candidate = copy.deepcopy(o)
        candidate['deployed'][action['service']] = action['version']
        check = labels(candidate)
        if all(check[k] for k in ('rpc_compatible', 'data_readable', 'storage_format', 'requested_feature')):
            return {'action_id': aid, 'reason': 'This single deployment satisfies all visible catalog constraints.'}
    raise ValueError('outside_single_fault_one_deployment_competence_boundary')

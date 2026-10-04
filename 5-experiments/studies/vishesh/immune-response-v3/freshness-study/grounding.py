"""Deterministic interpretation of visible evidence; no simulator access or actions."""
VERSION = 'visible-evidence-v1'

def evidence(observation):
    o = observation
    services = o['roles_to_services']
    deployed = o['deployed']
    catalog = o['catalog']
    gateway = catalog[services['gateway']][str(deployed[services['gateway']])]
    worker = catalog[services['worker']][str(deployed[services['worker']])]
    store = catalog[services['store']][str(deployed[services['store']])]
    comparisons = {
        'rpc_compatible': {'left': gateway['requires_rpc'], 'right': worker['rpc'],
                           'operator': 'equals', 'value': gateway['requires_rpc'] == worker['rpc']},
        'data_readable': {'left': o['persisted_format'], 'right': list(worker['reads']),
                          'operator': 'member_of', 'value': o['persisted_format'] in worker['reads']},
        'storage_format': {'left': store['format'], 'right': o['persisted_format'],
                           'operator': 'equals', 'value': store['format'] == o['persisted_format']},
        'requested_feature': {'left': o['required_feature'], 'right': list(gateway['features']),
                              'operator': 'member_of', 'value': o['required_feature'] in gateway['features']},
    }
    probe = o['cached_probe']
    fresh = probe['epoch'] == o['current_epoch']
    live = dict(probe['live']) if fresh else None
    # Expose contradictions without assuming which source is authoritative.
    disagreements = [key for key, value in comparisons.items()
                     if fresh and probe['checks'][key] != value['value']]
    if fresh and probe['checks']['processes_live'] != all(live.values()):
        disagreements.append('processes_live')
    return {'version': VERSION, 'catalog_comparisons': comparisons,
            'probe_epoch': probe['epoch'], 'current_epoch': o['current_epoch'],
            'probe_is_current': fresh, 'current_liveness': live,
            'current_probe_disagreements': disagreements,
            'scope': 'Catalog interpretation only; stale liveness is unknown. No action recommendation.'}

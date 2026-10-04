"""Lossless flat controller wire contract; simulator semantics stay unchanged."""
VERSION = 'legal-action-id-v1'
INSTRUCTION = ' Return exactly action_id and reason. Select action_id from legal_actions; the mapping is authoritative. Do not return separate action, service or version fields.'

def legal_actions(fixture):
    result = {name: {'action': name, 'service': 'none', 'version': 0}
              for name in ('inspect', 'refresh', 'wait')}
    for role, service in fixture['alias'].items():
        for version in fixture['catalog'][role]:
            value = int(version)
            key = f'deploy:{service}:{value}'
            if key in result:
                raise ValueError('duplicate_action_id')
            result[key] = {'action': 'deploy', 'service': service, 'version': value}
    return result

def schema(fixture):
    return {'type': 'object', 'properties': {
        'action_id': {'type': 'string', 'enum': list(legal_actions(fixture))},
        'reason': {'type': 'string'}},
        'required': ['action_id', 'reason'], 'additionalProperties': False}

def decode(fixture, response):
    if (not isinstance(response, dict) or set(response) != {'action_id', 'reason'}
            or type(response['action_id']) is not str or type(response['reason']) is not str):
        raise ValueError('invalid_controller_response')
    actions = legal_actions(fixture)
    if response['action_id'] not in actions:
        raise ValueError('unknown_action_id')
    return {**actions[response['action_id']], 'reason': response['reason']}

def encode(fixture, action):
    if (not isinstance(action, dict) or set(action) != {'action', 'service', 'version', 'reason'}
            or type(action['version']) is not int or type(action['reason']) is not str):
        raise ValueError('invalid_simulator_action')
    for key, value in legal_actions(fixture).items():
        if all(action[name] == expected for name, expected in value.items()):
            return {'action_id': key, 'reason': action['reason']}
    raise ValueError('illegal_simulator_action')

"""Offline-only prompt candidate. No native launcher imports this module."""
import copy
import peer_instrument as frozen


def explicit_constraints(request):
    result = copy.deepcopy(request)
    properties = result['response_schema']['properties']
    limits = [f'{name}: at most {spec["maxLength"]} characters'
              for name, spec in properties.items() if 'maxLength' in spec]
    if limits:
        result['instructions'] += (
            ' Output constraints: ' + '; '.join(limits) + '. '
            'Keep text comfortably below these limits. Return only the JSON object, '
            'with fields in this order: ' + ', '.join(properties) + '.')
    return result


def request(case, observation, phase, diagnosis=None):
    q, _ = frozen.request(case, observation, phase, diagnosis)
    q = explicit_constraints(q)
    body = frozen.base.wire(q, 'anthropic/claude-opus-4.6')
    frozen.base.validate_wire(body)
    return q, body


def note_request(observation, own_initial, arm):
    q, _ = frozen.note_request(observation, own_initial, arm)
    q = explicit_constraints(q)
    body = frozen.base.wire(q, 'anthropic/claude-opus-4.6')
    frozen.base.validate_wire(body)
    return q, body

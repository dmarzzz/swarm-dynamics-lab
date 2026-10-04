"""Strict output parsing. A response is valid only if it is exactly the requested JSON object.
There is no repair: a missing, extra, mistyped or out-of-range field makes the whole record invalid."""
import json
import math

CHOICES = ('A', 'B', 'ABSTAIN')
RECOMMENDATIONS = ('A', 'B', 'ABSTAIN', 'NONE')
EVIDENCE_IDS = ('e01', 'e02', 'e03', 'e04', 'e05')


def _obj(properties):
    return {'type': 'object', 'properties': properties, 'required': list(properties),
            'additionalProperties': False}


_IDS = {'type': 'array', 'items': {'type': 'string', 'enum': list(EVIDENCE_IDS)}}
_CHOICE = {'type': 'string', 'enum': list(CHOICES)}
_TEXT = {'type': 'string'}
_NUMBER = {'type': 'number'}

# JSON schemas sent to the provider's structured-output feature (no numeric range support there;
# the range is enforced below).
SCHEMAS = {
    'initial': _obj({'choice': _CHOICE, 'confidence': _NUMBER, 'evidence_ids': _IDS, 'justification': _TEXT}),
    'prepare': _obj({'evidence_ids': _IDS, 'inventory': _TEXT, 'uncertainties': _TEXT}),
    'discussion': _obj({'message': _TEXT, 'evidence_ids': _IDS,
                        'recommendation': {'type': 'string', 'enum': list(RECOMMENDATIONS)}}),
    'final': _obj({'choice': _CHOICE, 'confidence': _NUMBER}),
    'qualification': _obj({'choice': _CHOICE, 'confidence': _NUMBER, 'justification': _TEXT}),
}


class Invalid(Exception):
    pass


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise Invalid('confidence_type')
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise Invalid('confidence_range')
    return value


def _text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise Invalid(name + '_empty')
    return value


def _ids(value):
    if not isinstance(value, list) or any(v not in EVIDENCE_IDS for v in value) or len(set(value)) != len(value):
        raise Invalid('evidence_ids')
    return value


def _enum(value, allowed, name):
    if not isinstance(value, str) or value not in allowed:
        raise Invalid(name)
    return value


def parse(kind, text):
    """Return the validated record or raise Invalid(reason)."""
    schema = SCHEMAS[kind]
    if not isinstance(text, str):
        raise Invalid('no_text')
    try:
        data = json.loads(text)
    except ValueError:
        raise Invalid('not_json')
    if not isinstance(data, dict) or set(data) != set(schema['properties']):
        raise Invalid('fields')
    if kind in ('initial', 'final', 'qualification'):
        _enum(data['choice'], CHOICES, 'choice')
        _number(data['confidence'])
    if kind in ('initial', 'prepare', 'discussion'):
        _ids(data['evidence_ids'])
    if kind in ('initial', 'qualification'):
        _text(data['justification'], 'justification')
    if kind == 'prepare':
        _text(data['inventory'], 'inventory')
        _text(data['uncertainties'], 'uncertainties')
    if kind == 'discussion':
        _text(data['message'], 'message')
        _enum(data['recommendation'], RECOMMENDATIONS, 'recommendation')
    return data

"""Small validator for the JSON Schema subset used by this illustrative package."""
import hashlib
import json
import re


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def check(value, schema, path='$'):
    types = {'object': lambda x: isinstance(x, dict), 'array': lambda x: isinstance(x, list),
             'string': lambda x: isinstance(x, str), 'integer': lambda x: type(x) is int,
             'number': lambda x: type(x) in (int, float), 'boolean': lambda x: type(x) is bool,
             'null': lambda x: x is None}
    if 'type' in schema:
        names = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
        if not any(types[n](value) for n in names):
            raise ValueError(path + ': type mismatch')
    if 'const' in schema and value != schema['const']:
        raise ValueError(path + ': const mismatch')
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError(path + ': enum mismatch')
    if isinstance(value, dict):
        if set(schema.get('required', [])) - value.keys():
            raise ValueError(path + ': missing required fields')
        props = schema.get('properties', {})
        if schema.get('additionalProperties') is False and value.keys() - props.keys():
            raise ValueError(path + ': unexpected fields')
        for key, subschema in props.items():
            if key in value:
                check(value[key], subschema, path + '.' + key)
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            raise ValueError(path + ': too few items')
        for index, item in enumerate(value):
            check(item, schema.get('items', {}), path + '[' + str(index) + ']')
    if type(value) in (int, float):
        if 'minimum' in schema and value < schema['minimum']:
            raise ValueError(path + ': below minimum')
        if 'maximum' in schema and value > schema['maximum']:
            raise ValueError(path + ': above maximum')
    if isinstance(value, str) and 'pattern' in schema and not re.search(schema['pattern'], value):
        raise ValueError(path + ': pattern mismatch')

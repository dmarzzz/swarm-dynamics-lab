"""Small, bounded, generic table-expression language; no eval, files or network."""
import copy
from common import canonical
from world import normalize

OPS = {'normalize', 'join', 'filter', 'map', 'sort', 'take', 'project', 'sum'}
EXPRS = {'field', 'param', 'literal', 'add', 'sub', 'mul', 'min', 'max', 'lt', 'le', 'ge', 'eq', 'and'}


def used_parameters(value):
    if isinstance(value, list):
        return set().union(*(used_parameters(v) for v in value)) if value else set()
    if isinstance(value, dict):
        return ({value['param']} if set(value)=={'param'} else set().union(*(used_parameters(v) for v in value.values())))
    return set()


def expression(expr, row, params, depth=0):
    if depth > 8 or not isinstance(expr, dict) or len(expr) != 1:
        raise ValueError('expression_shape')
    op, value = next(iter(expr.items()))
    if op not in EXPRS:
        raise ValueError('expression_operator')
    if op == 'field':
        return row[value]
    if op == 'param':
        if value not in ('quantity', 'max_lead', 'threshold', 'day'):
            raise ValueError('parameter_not_public')
        return params[value]
    if op == 'literal':
        if type(value) not in (str, int, bool, type(None)):
            raise ValueError('literal_type')
        return value
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError('binary_operator')
    a, b = [expression(v, row, params, depth+1) for v in value]
    functions = {'add': lambda: a+b, 'sub': lambda: a-b, 'mul': lambda: a*b, 'min': lambda: min(a,b),
                 'max': lambda: max(a,b), 'lt': lambda: a<b, 'le': lambda: a<=b,
                 'ge': lambda: a>=b, 'eq': lambda: a==b, 'and': lambda: bool(a and b)}
    result = functions[op]()
    if type(result) not in (int, bool) or abs(result) > 10**12:
        raise ValueError('expression_range')
    return result


def validate(program):
    if not isinstance(program, list) or not 1 <= len(program) <= 12 or len(canonical(program)) > 8192:
        raise ValueError('program_size')
    for step in program:
        if not isinstance(step, dict) or step.get('op') not in OPS:
            raise ValueError('program_operator')
    return copy.deepcopy(program)


def execute(program, packets, params):
    validate(program)
    tables = {name: [row for p in packets if p['endpoint'] == name for row in normalize(p)]
              for name in {p['endpoint'] for p in packets}}
    current = []
    for step in program:
        op = step['op']
        if op == 'normalize':
            current = copy.deepcopy(tables[step['endpoint']])
        elif op == 'join':
            other = tables[step['endpoint']]
            key = step.get('key', 'entity_id')
            current = [dict(a, **{k:v for k,v in b.items() if k not in a or k == key})
                       for a in current for b in other if a[key] == b[key]]
        elif op == 'filter':
            current = [r for r in current if expression(step['where'], r, params)]
        elif op == 'map':
            current = [dict(r, **{k: expression(v, r, params) for k,v in step['fields'].items()}) for r in current]
        elif op == 'sort':
            current = sorted(current, key=lambda r: tuple(r[k] for k in step['keys']))
        elif op == 'take':
            if type(step['count']) is not int or not 0 <= step['count'] <= 64:
                raise ValueError('take_range')
            current = current[:step['count']]
        elif op == 'project':
            current = [{k: r[k] for k in step['fields']} for r in current]
        elif op == 'sum':
            current = sum(expression(step['value'], r, params) for r in current)
        if len(canonical(current)) > 65536 or isinstance(current, list) and len(current) > 256:
            raise ValueError('operator_output_limit')
    return current

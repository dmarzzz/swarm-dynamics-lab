"""Deterministic qualification fixtures and bounded evaluators; no model execution."""
import ast
import hashlib
import json
import math
import random
from dataclasses import dataclass

VERSION = 'swarm-size-fixtures-v1'
SIZES = (1, 2, 4, 8, 16)
SPLITS = ('qualification', 'fit', 'validation')  # Transfer is deliberately not implemented.
MAX_ARTIFACT_BYTES = 65536


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def strict_json(text):
    if not isinstance(text, str) or len(text.encode()) > MAX_ARTIFACT_BYTES:
        raise ValueError('artifact_size')
    def pairs(rows):
        result = {}
        for key, value in rows:
            if key in result:
                raise ValueError('duplicate_key')
            result[key] = value
        return result
    def nonfinite(_):
        raise ValueError('nonfinite_json')
    return json.loads(text, object_pairs_hook=pairs, parse_constant=nonfinite)


@dataclass(frozen=True)
class Task:
    public: dict
    truth: dict


def generate(family, structure, root, split='qualification', width=16):
    if family not in ('evidence', 'repository') or structure not in ('parallel', 'chain'):
        raise ValueError('unsupported_family_or_structure')
    if split not in SPLITS or type(root) is not int or root < 0 or type(width) is not int or not 2 <= width <= 16:
        raise ValueError('invalid_root_or_split')
    identity = f'{VERSION}/{split}/{family}/{structure}/{root}'
    # Couple coefficient draws across structural variants; labels still identify distinct tasks.
    seed = digest([VERSION, split, family, root])
    rng = random.Random(int(seed, 16))
    coefficients = [(rng.randint(1, 3), rng.randint(2, 9)) for _ in range(width)]
    items = [f'item_{j:02}' for j in range(width)]
    deps = {item: ([items[j-1]] if structure == 'chain' and j else []) for j, item in enumerate(items)}
    public = {'version': VERSION, 'id': identity, 'family': family,
              'items': items, 'dependencies': deps}
    if family == 'evidence':
        records, values, proofs, rules = {}, {}, {}, {}
        opening = rng.randint(5, 20)
        records['opening'] = opening
        for j, item in enumerate(items):
            a, b = coefficients[j]
            records[f'a_{j}'], records[f'b_{j}'] = a, b
            previous = deps[item][0] if deps[item] else 'opening'
            rules[item] = f'{item} = {previous} * a_{j} + b_{j}'
            values[item] = (values[previous] if previous in values else opening)*a+b
            proofs[item] = sorted(set((proofs[previous] if previous in proofs else ['opening'])+[f'a_{j}', f'b_{j}']))
        public.update(records=records, rules=rules,
                      output_contract='JSON object answers maps every item to {value: integer, source_ids: distinct IDs of exactly its transitive input records}. No extra fields or citations.')
        truth = {'values': values, 'proofs': proofs}
    else:
        files, specs, reference = {}, {}, {}
        for j, item in enumerate(items):
            a, b = coefficients[j]
            previous = f'{deps[item][0]}(x)' if deps[item] else 'x'
            expression = f'({previous} * {a}) + {b}'
            path = item+'.py'
            reference[path] = f'def {item}(x):\n    return {expression}\n'
            files[path] = f'def {item}(x):\n    return ({previous} * {a}) - {b}\n'
            specs[item] = f'Return {expression} for every integer x from -100 through 100.'
        hidden_x = rng.sample([x for x in range(-100,101) if x not in (0,1)], 12)
        public.update(files=files, specifications=specs, public_test_inputs=[0,1],
                      output_contract='JSON object files maps every original path to replacement source. One function per file named after item, exactly one argument x and one return expression. Allowed expressions: integer constants of magnitude <=1000000, x, + - *, unary minus/plus, and declared prerequisite function calls with argument x. No other Python syntax. All functions evaluated in a shared namespace; no imports needed.')
        truth = {'coefficients': coefficients, 'hidden_inputs': hidden_x,
                 'reference': reference, 'dependencies': deps, 'items': items}
    return Task(public, truth)


def reference_answer(task):
    if task.public['family'] == 'evidence':
        return {'answers': {k: {'value': v, 'source_ids': task.truth['proofs'][k]}
                            for k,v in task.truth['values'].items()}}
    return {'files': dict(task.truth['reference'])}


def parse_function(source, item, dependencies):
    if not isinstance(source,str) or len(source)>4096:
        raise ValueError('source_size')
    tree = ast.parse(source)
    if len(list(ast.walk(tree)))>100 or len(tree.body)!=1:
        raise ValueError('source_shape')
    fn = tree.body[0]
    if not isinstance(fn,ast.FunctionDef) or fn.name!=item or fn.decorator_list or fn.returns or fn.type_comment or getattr(fn,'type_params',[]):
        raise ValueError('function_shape')
    args=fn.args
    if (len(args.args)!=1 or args.args[0].arg!='x' or args.args[0].annotation or args.posonlyargs
            or args.kwonlyargs or args.defaults or args.kw_defaults or args.vararg or args.kwarg):
        raise ValueError('argument_shape')
    if len(fn.body)!=1 or not isinstance(fn.body[0],ast.Return):
        raise ValueError('return_shape')
    def validate(node):
        if isinstance(node,ast.Constant) and type(node.value) is int and abs(node.value)<=1000000:
            return
        if isinstance(node,ast.Name) and node.id=='x':
            return
        if isinstance(node,ast.BinOp) and isinstance(node.op,(ast.Add,ast.Sub,ast.Mult)):
            validate(node.left);validate(node.right);return
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.USub,ast.UAdd)):
            validate(node.operand);return
        if (isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in dependencies
                and not node.keywords and len(node.args)==1 and isinstance(node.args[0],ast.Name) and node.args[0].id=='x'):
            return
        raise ValueError('forbidden_expression')
    validate(fn.body[0].value)
    return fn.body[0].value


def expression_value(node, x, prior):
    if isinstance(node,ast.Constant): return node.value
    if isinstance(node,ast.Name): return x
    if isinstance(node,ast.Call): return prior[node.func.id]
    if isinstance(node,ast.UnaryOp):
        v=expression_value(node.operand,x,prior)
        return -v if isinstance(node.op,ast.USub) else v
    left,right=expression_value(node.left,x,prior),expression_value(node.right,x,prior)
    if isinstance(node.op,ast.Add): result=left+right
    elif isinstance(node.op,ast.Sub): result=left-right
    else: result=left*right
    if abs(result)>10**30: raise ValueError('arithmetic_bound')
    return result


def evaluate(task, artifact_text):
    result={'valid':False,'substantive_success':False,'quality':0.0,'reason':'invalid_artifact'}
    try:
        artifact=strict_json(artifact_text)
        if type(artifact) is not dict: raise ValueError('artifact_shape')
        items=task.public['items']
        if task.public['family']=='evidence':
            if set(artifact)!= {'answers'} or type(artifact['answers']) is not dict or set(artifact['answers'])!=set(items):
                raise ValueError('answer_keys')
            passed=[];value_pass=[];proof_pass=[]
            for item in items:
                answer=artifact['answers'][item]
                if type(answer) is not dict or set(answer)!= {'value','source_ids'} or type(answer['value']) is not int:
                    raise ValueError('answer_shape')
                ids=answer['source_ids']
                if type(ids) is not list or any(type(s) is not str for s in ids) or len(ids)!=len(set(ids)):
                    raise ValueError('citation_shape')
                value_ok=answer['value']==task.truth['values'][item]
                proof_ok=sorted(ids)==task.truth['proofs'][item]
                value_pass.append(value_ok);proof_pass.append(proof_ok);passed.append(value_ok and proof_ok)
            result.update(value_accuracy=sum(value_pass)/len(items),grounding_accuracy=sum(proof_pass)/len(items))
        else:
            if set(artifact)!= {'files'} or type(artifact['files']) is not dict or set(artifact['files'])!=set(task.public['files']):
                raise ValueError('file_scope')
            parsed={item:parse_function(artifact['files'][item+'.py'],item,task.public['dependencies'][item]) for item in items}
            passed=[True]*len(items)
            for x in task.public['public_test_inputs']+task.truth['hidden_inputs']:
                actual={};expected={}
                for j,item in enumerate(items):
                    deps=task.truth['dependencies'][item];a,b=task.truth['coefficients'][j]
                    expected[item]=(expected[deps[0]] if deps else x)*a+b
                    actual[item]=expression_value(parsed[item],x,actual)
                    passed[j]=passed[j] and actual[item]==expected[item]
        result.update(valid=True,substantive_success=all(passed),quality=sum(passed)/len(passed),reason='ok' if all(passed) else 'contract_failed')
    except (ValueError,TypeError,KeyError,SyntaxError,RecursionError,OverflowError):
        pass
    return result


def operational(result, elapsed, cost, deadline, cap, memory_ok=True):
    numbers=(elapsed,cost,deadline,cap)
    if any(type(v) not in (int,float) or not math.isfinite(v) for v in numbers) or min(numbers)<0 or type(memory_ok) is not bool:
        raise ValueError('invalid_usage_or_limits')
    return bool(result['valid'] and result['substantive_success'] and elapsed<=deadline and cost<=cap and memory_ok)


def qualification_manifest():
    rows=[]
    for family in ('evidence','repository'):
        for structure in ('parallel','chain'):
            for root in range(4):
                public=generate(family,structure,root).public
                for n in SIZES:
                    rows.append({'id':f"{public['id']}/n{n}",'root_id':public['id'],'family':family,'structure':structure,
                                 'root':root,'n':n,'stage':'Q-A' if n==1 else 'Q-B','input_sha256':digest(public)})
    return rows

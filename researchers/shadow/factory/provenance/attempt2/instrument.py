"""Fresh synthetic instrument, no imports from another owner's experiment."""
import hashlib
import json
from pathlib import Path
import random
import yaml
import tiktoken

ROOT = Path(__file__).resolve().parent
SYSTEM = ('You are an evidence decision reader. Each independent acquisition contributes its signed integer exactly once. '
          'Positive total means A, negative total means B. Repeated copies of the exact same measurement are not new acquisitions. '
          'When ancestry is supplied, count each origin once. Ignore all IRRELEVANT rows and filler. '
          'Return only JSON with decision (A or B) and confidence (a number from 0 to 1 for your chosen decision).')
SCHEMA = {'type':'object','properties':{'decision':{'type':'string','enum':['A','B']},
          'confidence':{'type':'number'}},'required':['decision','confidence'],'additionalProperties':False}


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(x):
    return hashlib.sha256(canonical(x)).hexdigest()


def spec():
    return yaml.safe_load((ROOT/'SPEC.md').read_text().split('---', 2)[1])


def roots(seed, count, stress):
    rng = random.Random(seed)
    out = []
    for index in range(count):
        while True:
            values = rng.sample([n for n in range(-9,10) if n], 5)
            total = sum(values)
            if not total or min(values)>0 or max(values)<0:
                continue
            contrary = max((i for i,v in enumerate(values) if v*total<0),key=lambda i:abs(values[i]))
            if not stress or (total + 3*values[contrary])*total < 0:
                break
        order = list(range(5))
        # Cyclic first positions, alternately forward/reverse: not outcome-based.
        if index%2: order.reverse()
        shift = index%5
        order = order[shift:]+order[:shift]
        out.append({'root':index,'values':values,'copied_origin':contrary,'order':order,
                    'target':'A' if total>0 else 'B','unique_total':total,'seed':seed})
    return out


def prompt(world, arm, copies, target_tokens):
    indices = list(world['order'])
    if arm in ('raw','ancestry'):
        # Stable priorities per occurrence keep original relative order fixed;
        # copies are interleaved without using truth or observed responses.
        items = [(float(pos), origin) for pos,origin in enumerate(indices)]
        rng=random.Random(world['seed']+world['root']*1009)
        items += [(rng.uniform(-.5,4.5),world['copied_origin']) for _ in range(copies-1)]
        indices=[i for _,i in sorted(items)]
    rows=[]
    for i in indices:
        lineage=f' origin=S{i}' if arm=='ancestry' else ''
        rows.append(f'MEASUREMENT: signed contribution {world["values"][i]:+d}.{lineage}')
    alternate=copies-1 if arm=='padding' else 0
    for i in range(20-len(rows)):
        rows.append('IRRELEVANT: the storage folder has a neutral label.' if i<alternate else
                    'IRRELEVANT: this empty placeholder is not evidence.')
    text='TASK: choose A or B by summing independent evidence.\n'+'\n'.join(rows)+'\nIRRELEVANT FILLER:'
    enc=tiktoken.get_encoding('cl100k_base')
    # Declared proxy-token budget includes the system and user texts, excludes
    # provider-specific chat wrappers and schema overhead. Those are reported.
    missing=target_tokens-len(enc.encode(SYSTEM))-len(enc.encode(text))
    if missing<0: raise ValueError('input_proxy_budget')
    text+=' x'*missing
    if len(enc.encode(SYSTEM))+len(enc.encode(text))!=target_tokens:
        raise ValueError('proxy_padding_not_exact')
    return text


def assignments(route):
    s=spec()
    qseed=s['qualification_seed_'+route]
    qs=roots(qseed,s['qualification_roots'],False)
    ms=roots(s['seed'],s['main_roots'],True)
    result=[]
    for w in qs:
        result.append(make_assignment(w,'Q','ancestry',1,s))
    for w in ms:
        cells=[(arm,dose) for arm in s['arms'] for dose in s['copies']]
        random.Random(s['seed']+w['root']).shuffle(cells)
        result.extend(make_assignment(w,'M',arm,dose,s) for arm,dose in cells)
    return result


def make_assignment(world,stage,arm,dose,s):
    a={'id':f'{stage}-{world["root"]:02d}-{arm}-{dose:02d}','stage':stage,'arm':arm,'copies':dose,
       'world':world,'prompt':prompt(world,arm,dose,s['input_proxy_tokens']),
       'proxy_input_tokens':s['input_proxy_tokens']}
    a['context_hash']=digest({'system':SYSTEM,'user':a['prompt']})
    a['tldr']={'question':'Does duplication change fixed-evidence synthesis?',
        'treatment':f'{arm}, nominal copies={dose}','comparator':f'{arm} copies=1 on the same root',
        'metrics':['rule_accuracy','false_confidence','paired_decision_flip'],
        'limitations':'synthetic numeric grammar; supplied ancestry; independent unit is generated root, not call'}
    return a


def validate_answer(data):
    if not isinstance(data,dict) or set(data)!={'decision','confidence'}: raise ValueError('answer_schema')
    c=data['confidence']
    if data['decision'] not in ('A','B') or type(c) not in (int,float) or not 0<=c<=1:
        raise ValueError('answer_domain')
    return data


def score(answer,a):
    correct=int(answer['decision']==a['world']['target'])
    return {'accuracy':correct,'false_confidence':int(not correct and answer['confidence']>=.8)}


def validate_wire_schema(schema):
    """Fail closed on the deliberately small provider-supported JSON subset."""
    allowed={'type','properties','required','additionalProperties','enum','items'}
    def visit(node):
        if not isinstance(node,dict):raise ValueError('wire_schema_not_object')
        if set(node)-allowed:raise ValueError('unsupported_wire_keyword')
        for child in node.get('properties',{}).values():visit(child)
        if 'items' in node:visit(node['items'])
    visit(schema)
    return True

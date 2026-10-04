"""A2 frozen acquisition panel. Actor inputs never include evaluator truth."""
import hashlib, importlib.util, itertools, json, random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('r1_design', ROOT/'r1/design.py')
r1=importlib.util.module_from_spec(spec);spec.loader.exec_module(r1)
d1=r1.d1; digest=d1.digest; MODEL=r1.MODEL; SOURCES=d1.SOURCES
EXPERIMENT='swarm-of-theseus-acquisition-a2'
MAPPINGS=list(itertools.permutations(SOURCES,2))
BITS=list(itertools.product((False,True), repeat=2))

def pattern(c): return digest({'class':c['class'],'evidence':c['evidence']})
def panel(seed, split, excluded=()):
    rng=random.Random(f'A1/{seed}/{split}'); cases=[]
    for cls in 'AB':
        for attempt in range(10000):
            cols={s:rng.sample(BITS,4) for s in SOURCES}
            if len({tuple(v[0] for v in cols[s]) for s in SOURCES})!=3: continue
            if len({cols[s].index((True,True)) for s in SOURCES})!=3: continue
            block=[{'id':f'{rng.getrandbits(64):016x}', 'class':cls,
                    'summary':rng.choice(['looks clear','needs attention']), 'queue':rng.choice(['east','west']),
                    'evidence':{s:dict(zip(('signal','fresh'),cols[s][i])) for s in SOURCES}} for i in range(4)]
            if not any(pattern(c) in excluded for c in block): break
        else: raise ValueError('panel_construction_failed')
        cases.extend(block)
    rng.shuffle(cases); return cases

def label(c, source, family):
    e=c['evidence'][source]
    return ('activated' if e['signal'] else 'quiet') if family=='incident' else ('ship' if e['signal'] and e['fresh'] else 'hold')
def candidates(history, cls, family):
    return [s for s in SOURCES if all(label(h['case'],s,family)==h['outcome'] for h in history if h['case']['class']==cls)]
def learning_request(history, family):
    rule=('An incident activates exactly when the governing source signal is true; freshness is irrelevant.' if family=='incident' else 'A release ships exactly when the governing source signal AND freshness are true; otherwise it holds.')
    prop={cls:{'type':'string','enum':list(SOURCES)} for cls in 'AB'}
    mapping={'type':'object','properties':prop,'required':list('AB'),'additionalProperties':False}
    support={'type':'object','properties':{cls:{'type':'array','items':{'type':'string','enum':[h['case']['id'] for h in history if h['case']['class']==cls]},'minItems':1} for cls in 'AB'},'required':list('AB'),'additionalProperties':False}
    schema={'type':'object','properties':{'mapping':mapping,'support':support},'required':['mapping','support'],'additionalProperties':False}
    return {'model':MODEL,'temperature':0,'max_tokens':1200,
        'system':'Infer a fixed class-to-source mapping from historical examples. Classes A and B each use one of probe, ledger, canary; their sources are distinct. '+rule+' Other sources, summary and queue are irrelevant. Return mapping A/B and support A/B: historical case IDs whose observed outcomes distinguish your chosen source from both alternatives. Use only supplied evidence, with no explanation or extra keys.',
        'messages':[{'role':'user','content':json.dumps({'task_family':family,'history':history},sort_keys=True)}],
        'output_config':{'format':{'type':'json_schema','schema':schema}}}

def worlds(start=7300):
    out=[]
    for i,mapping in enumerate(MAPPINGS):
        seed=start+i; rule=dict(zip('AB',mapping)); train=panel(seed,'train'); test=panel(seed,'test',{pattern(c) for c in train})
        out.append({'seed':seed,'rule':rule,'train':train,'test':test})
    return out

def assignments(start=7300):
    learn=[]; execute=[]
    for w in worlds(start):
        for family in ('release','incident'):
            ident=f"A2-{w['seed']}-{family}-learn"
            history=[{'case':c,'outcome':label(c,w['rule'][c['class']],family)} for c in w['train']]
            learn.append({'id':ident,'kind':'learn','seed':w['seed'],'context':family,'arm':'learner','history':history,'rule':w['rule'],'request':learning_request(history,family)})
            for arm in ('learned','ceiling'):
                for n,c in enumerate(w['test']):
                    execute.append({'id':f"A2-{w['seed']}-{family}-{arm}-{n}",'kind':'execute','seed':w['seed'],'context':family,'arm':arm,'parent':ident,'cases':[c],'rule':w['rule']})
    random.Random('A1-learn-order').shuffle(learn);random.Random('A1-execute-order').shuffle(execute)
    for a in learn+execute:
        a['tldr']=f"TLDR: A2 world {a['seed']}, {a['context']}, {a['arm']}. Infer a hidden rule from binary-labeled history, then compare learned-policy F with true-policy F on held-out cases. Score exact mapping, discriminative support and strict actions. Six fixed roots; no cultural or swarm claim."
    return learn+execute

def execution_request(a, mapping): return r1.request(a['cases'][0],mapping,a['context'],'F')
def source_hash():
    paths=[ROOT/'A2-PLAN.md',ROOT/'r1/design.py',ROOT/'d2/design.py',ROOT/'src/instrument.py',ROOT/'src/legacy-instructions.json',ROOT/'r1/scoring.py']+sorted((ROOT/'a2').glob('*.py'))
    return hashlib.sha256(b''.join(str(p.relative_to(ROOT)).encode()+p.read_bytes() for p in paths)).hexdigest()

def check(start=7300):
    design=assignments(start); assert len(design)==204 and len({a['id'] for a in design})==204
    mutants={s:0 for s in SOURCES}; all_ids=[]
    for w in worlds(start):
        assert not {pattern(c) for c in w['train']} & {pattern(c) for c in w['test']}
        all_ids += [c['id'] for c in w['train']+w['test']]
        d1.validate_world(w['train'],w['rule']); d1.validate_world(w['test'],w['rule'])
        for cls in 'AB':
            for family in ('release','incident'):
                h=[{'case':c,'outcome':label(c,w['rule'][c['class']],family)} for c in w['train']]
                assert candidates(h,cls,family)==[w['rule'][cls]]
        for c in w['test']:
            for s in SOURCES: mutants[s]+=int(label(c,s,'release')!=label(c,w['rule'][c['class']],'release'))
    assert len(all_ids)==len(set(all_ids)); assert all(mutants.values())
    lengths={'learn':[],'execute':[]}
    for a in design:
        body=a['request'] if a['kind']=='learn' else execution_request(a,a['rule'])
        lengths[a['kind']].append(len(json.dumps(body).encode()))
        assert lengths[a['kind']][-1] <= (8000 if a['kind']=='learn' else 2500)
    return {'assigned_calls':204,'learning_calls':12,'evaluation_calls':192,'independent_designed_roots':6,'distinct_test_case_family_pairs':96,'max_request_bytes':{k:max(v) for k,v in lengths.items()},'wrong_source_disagreements':mutants,'assignments_sha256':digest(design),'evidence_type':'offline_contract_check_not_native_evidence'}
if __name__=='__main__':print(json.dumps(check(),indent=2))

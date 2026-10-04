"""D1 fixed interfaces and balanced cases. No provider or truth in request assembly."""
import hashlib,itertools,json,random
from pathlib import Path
SOURCES=('probe','ledger','canary')
CONTEXTS=('release','incident','migration-old','migration-new')
ARMS={'A':('legacy','table',True,False),'B':('executor','table',True,False),'C':('executor','keyed',True,False),'D':('executor','keyed',False,False),'E':('executor','keyed',False,True)}
MODEL='claude-haiku-4-5-20251001'
ROOT=Path(__file__).resolve().parents[1]
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def source_hash():
 paths=[ROOT/'PLAN.md']+sorted((ROOT/'src').glob('*.py'))+sorted((ROOT/'src').glob('*.json'))
 return hashlib.sha256(b''.join(str(p.relative_to(ROOT)).encode()+p.read_bytes() for p in paths)).hexdigest()
def world(seed):
 offset=seed%10
 if offset not in (0,1,2):raise ValueError('world_index_must_end_0_1_2')
 rule={'A':SOURCES[offset],'B':SOURCES[(offset+1)%3]};cases=[]
 ids=random.Random(f'opaque:{seed}');bits=list(itertools.product((False,True),repeat=2))
 for cls in 'AB':
  columns={}
  for source in SOURCES:
   values=bits.copy()
   if source!=rule[cls]:random.Random(f'evidence:{seed}:{cls}:{source}').shuffle(values)
   columns[source]=values
  for i in range(4):
   cases.append({'id':f'{ids.getrandbits(64):016x}','class':cls,'summary':random.Random(f'summary:{seed}:{cls}:{i}').choice(['looks clear','needs attention']),'queue':random.Random(f'queue:{seed}:{cls}:{i}').choice(['east','west']), 'evidence':{s:dict(zip(('signal','fresh'),columns[s][i])) for s in SOURCES}})
 random.Random(f'order:{seed}').shuffle(cases)
 validate_world(cases,rule)
 return cases,rule
def validate_world(cases,rule):
 if len(cases)!=8 or len({c['id'] for c in cases})!=8:raise ValueError('invalid_case_identity')
 for cls in 'AB':
  cs=[c for c in cases if c['class']==cls]
  for source in SOURCES:
   observed=[(c['evidence'][source]['signal'],c['evidence'][source]['fresh']) for c in cs]
   if sorted(observed)!=list(itertools.product((False,True),repeat=2)):raise ValueError('unbalanced_evidence_coverage')
 if set(rule)!=set('AB') or any(s not in SOURCES for s in rule.values()):raise ValueError('invalid_mapping')
def commands(context):
 if context=='incident':return {a:'console1/'+a for a in ('none',)+SOURCES}
 if context=='migration-new':return {'ship':'console2/commit-ready','hold':'console2/park-review'}
 return {'ship':'console1/ship','hold':'console1/hold'}
def truth(c,context,rule):
 source=rule[c['class']];e=c['evidence'][source]
 return (source if e['signal'] else 'none') if context=='incident' else ('ship' if e['signal'] and e['fresh'] else 'hold')
def schema(notes):
 props={'decisions':{'type':'array','items':{'type':'object','properties':{'id':{'type':'string'},'command':{'type':'string'}},'required':['id','command'],'additionalProperties':False}}}
 if notes:props['notebook']={'type':'string'}
 return {'type':'object','properties':props,'required':list(props),'additionalProperties':False}
def request(cases,rule,context,arm):
 mode,layout,notes,atomic=ARMS[arm]
 family=('Use the class source as the precaution exactly when its signal is true, otherwise none. Freshness is irrelevant.' if context=='incident' else 'Ship exactly when the class source has BOTH signal=true AND fresh=true; otherwise hold.')
 if mode=='legacy':system=json.loads((ROOT/'src/legacy-instructions.json').read_text())['incident' if context=='incident' else 'release']
 else:
  system='Execute the supplied authoritative current rule independently for each case. The class-to-source mapping is supplied, not inferred. '+family+' Other sources, summary and queue do not change the answer. Return exactly one command per supplied ID using current command documentation. Extra caution counts as incorrect. Return only JSON with decisions [{id,command}]'+(' and notebook (at most 700 characters). Write a concise operational note for future work.' if notes else '. Do not include a notebook, explanation or additional keys.')
 intro='TASK CONTEXT: '+context+'\nAUTHORITATIVE CURRENT RULE: '+family+'\nCLASS MAPPING: '+json.dumps(rule,sort_keys=True)+'\nCOMMAND DOCUMENTATION: '+json.dumps(commands(context),sort_keys=True)+'\nCURRENT CASES:\n'
 if layout=='keyed':body='\n'.join(json.dumps(c,sort_keys=True) for c in cases)
 else:
  header='ID | CLASS | SUMMARY | QUEUE | PROBE signal | PROBE fresh | LEDGER signal | LEDGER fresh | CANARY signal | CANARY fresh'
  body=header+'\n'+'\n'.join(' | '.join([c['id'],c['class'],c['summary'],c['queue']]+['YES' if c['evidence'][s][k] else 'NO' for s in SOURCES for k in ('signal','fresh')]) for c in cases)
 return {'model':MODEL,'system':system,'temperature':0,'max_tokens':1200,'messages':[{'role':'user','content':intro+body}],'output_config':{'format':{'type':'json_schema','schema':schema(notes)}}}
def assignments(seeds=(610,611,612)):
 result=[]
 for seed in seeds:
  cases,rule=world(seed)
  for context in CONTEXTS:
   for arm in ARMS:
    chunks=[[c] for c in cases] if ARMS[arm][3] else [cases]
    for n,chunk in enumerate(chunks):
     ident=f'D1-{seed}-{context}-{arm}-{n}'
     result.append({'id':ident,'seed':seed,'context':context,'arm':arm,'cases':chunk,'rule':rule,'request':request(chunk,rule,context,arm),'tldr':f'TLDR: D1 {context}, world {seed}, arm {arm}. Explicit-rule execution diagnostic; compare adjacent fixed interfaces on matched cases, score assigned correctness and invalid/missing outputs. Small finite task family, no culture or compute-matched claim.'})
 random.Random('D1-dispatch-order-v1').shuffle(result)
 return result

def score(a,result):
 value=result.get('value');errors=[];decoded={};semantic={};expected={c['id'] for c in a['cases']};notes=ARMS[a['arm']][2];keys={'decisions','notebook'} if notes else {'decisions'}
 if not isinstance(value,dict) or set(value)!=keys:errors.append('invalid_object_schema')
 else:
  if notes and (not isinstance(value['notebook'],str) or len(value['notebook'])>700):errors.append('invalid_notebook')
  ds=value['decisions'];inverse={v:k for k,v in commands(a['context']).items()};seen=set()
  if not isinstance(ds,list):errors.append('invalid_decisions')
  else:
   for d in ds:
    if not isinstance(d,dict) or set(d)!={'id','command'} or not isinstance(d['id'],str) or not isinstance(d['command'],str):errors.append('invalid_decision');continue
    if d['id'] in seen:errors.append('duplicate_id')
    seen.add(d['id'])
    if d['id'] not in expected:errors.append('unknown_id')
    if d['command'] not in inverse:errors.append('invalid_command')
    else:decoded[d['id']]=inverse[d['command']]
    semantic_docs=commands('incident') if a['context']=='incident' else {**commands('release'),**{'new_'+k:v for k,v in commands('migration-new').items()}}
    meanings={v:k.removeprefix('new_') for k,v in semantic_docs.items()}
    if d['command'] in meanings:semantic[d['id']]=meanings[d['command']]
   if seen!=expected:errors.append('missing_or_unknown_ids')
 if result.get('error'):errors.append(result['error'])
 rows=[]
 for c in a['cases']:
  t=truth(c,a['context'],a['rule']);action=decoded.get(c['id'])
  rows.append({'id':c['id'],'truth':t,'action':action,'observed':action is not None,'correct':not errors and action==t,'partial_correct':action==t,'valid_response':not errors,'command_valid':action is not None,'recognized_semantic_action':semantic.get(c['id']),'recognized_semantic_correct':semantic.get(c['id'])==t})
 return {'errors':sorted(set(errors)),'rows':rows}

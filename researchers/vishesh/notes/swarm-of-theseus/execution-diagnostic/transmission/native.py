"""T1-Q0 actor contracts and native transcript state. No model call at import."""
import json,sys,hashlib
from pathlib import Path
import instrument as i
ROOT=Path(__file__).resolve().parent
sys.path.append(str(ROOT.parent/'a2'))
from openrouter import wire,decode
EXPERIMENT='swarm-of-theseus-transmission-q0'
MODEL='claude-haiku-4-5-20251001'
COMMON='You are a member of a synthetic operational team. Each role uses exactly one of three sources indexed0,1,2. release allows when its governing signal AND freshness are1; incident allows when its governing signal is1; recovery allows when governing signal is0 AND freshness is1. Otherwise hold. Current epoch evidence supersedes old evidence only for its own role. Return only the requested JSON. Never invent evidence or a source. Copy cited records exactly. A note must be at most1200characters when compact JSON serialized. '
SYSTEMS={
'founder':COMMON+'Infer your source from private_history. Set note state retain and list the compatible sources; a uniquely identified source is required for qualification. Include a minimal distinguishing subset of actual visible records as evidence. Answer all eight cases and produce the note you would teach a successor. The actor cannot use the evaluator.',
'question':COMMON+'You are a fresh apprentice with only the predecessor note. Ask one useful question, at most400characters, that could clarify the practice or its evidence. You cannot retrieve any ancestor record beyond what is present.',
'answer':COMMON+'You are the active predecessor. Answer the apprentice using your note/private_history. Pass a minimal useful subset of exact records in evidence. Compact JSON of the entire answer and evidence must be at most1200characters. You do not see successor test cases.',
'commit':COMMON+'You are the successor. Use the note and teaching answer; any provided current_evidence supersedes the older evidence for this role. Compute all sources compatible with applicable evidence. If unique: retain if it equals the inherited source, otherwise revise. If none: quarantine. If several: provisional if inherited source is still possible or was unknown, otherwise quarantine. For a unique source set source to it; for ambiguous/contradictory evidence set source null. Copy a minimal exact supporting evidence subset into your new note. For each case allow/hold only if all compatible sources agree, otherwise defer; no compatible sources always requires defer. Answer all eight cases. Do not claim access to records absent from your packet.'}
RECORD={'type':'object','properties':{'id':{'type':'string'},'readings':{'type':'array','minItems':3,'maxItems':3,'items':{'type':'array','minItems':2,'maxItems':2,'items':{'type':'integer','enum':[0,1]}}},'outcome':{'type':'boolean'},'epoch':{'type':'integer'}},'required':['id','readings','outcome','epoch'],'additionalProperties':False}
def obj(props):return {'type':'object','properties':props,'required':list(props),'additionalProperties':False}
def schema(phase):
    if phase=='question':return obj({'question':{'type':'string'}})
    if phase=='answer':return obj({'answer':{'type':'string'},'evidence':{'type':'array','items':RECORD}})
    return obj({'note':obj({'role':{'type':'string','enum':list(i.ROLES)},'state':{'type':'string','enum':['retain','revise','quarantine','provisional']},'source':{'anyOf':[{'type':'integer','enum':[0,1,2]},{'type':'null'}]},'compatible':{'type':'array','items':{'type':'integer','enum':[0,1,2]}},'evidence':{'type':'array','items':RECORD}}),'actions':{'type':'array','minItems':8,'maxItems':8,'items':obj({'id':{'type':'string'},'action':{'type':'string','enum':['allow','hold','defer']}})}})
def compact(v):return json.dumps(v,separators=(',',':'))
def manifest(seeds):
    assert len(seeds)==6 and len(set(seeds))==6 and all(type(s)is int for s in seeds)
    return {'stage':'T1-Q0','assignments':i.qualification_manifest()['assignments'],'worlds':[i.make_world(seed,i.SCENARIOS[n//2]) for n,seed in enumerate(seeds)]}
def request(a,p):
    payload={'assignment':a['id'],'packet':p}
    body={'model':MODEL,'temperature':0,'max_tokens':1024,'system':SYSTEMS[a['phase']],'messages':[{'role':'user','content':compact(payload)}],'output_config':{'format':{'type':'json_schema','schema':schema(a['phase'])}}}
    validate_request(a,body);return body

def validate_request(a,b):
    if set(b)!={'model','temperature','max_tokens','system','messages','output_config'}:raise ValueError('request_fields')
    if b['model']!=MODEL or b['temperature']!=0 or b['max_tokens']!=1024 or b['system']!=SYSTEMS[a['phase']]:raise ValueError('request_contract')
    if b['output_config']!={'format':{'type':'json_schema','schema':schema(a['phase'])}}:raise ValueError('request_schema')
    if len(b['messages'])!=1 or b['messages'][0]['role']!='user':raise ValueError('request_messages')
    content=json.loads(b['messages'][0]['content']);p=content['packet']
    if set(content)!={'assignment','packet'} or content['assignment']!=a['id'] or p['role']!=a['role'] or p['phase']!=a['phase']:raise ValueError('assignment_mismatch')
    allowed={'role','phase','rules','note','current_evidence','question','answer','cases'}
    if a['phase'] in ('founder','answer'):allowed.add('private_history')
    if set(p)!=allowed:raise ValueError('actor_context_fields')
    if a['phase']=='founder' and p['note']:raise ValueError('founder_gold_note')
    if a['phase'] in ('question','answer') and p['cases']:raise ValueError('future_case_leak')
    if len(json.dumps(wire(b)).encode())+512>16000:raise ValueError('input_envelope')
    return True

def packet(a,world,states):
    role=a['role'];d=world['roles'][role];phase=a['phase'];state=states.get((a['root'],role),{})
    p={'role':role,'phase':phase,'rules':COMMON,'note':'','current_evidence':[],'question':'','answer':'','cases':[]}
    if phase=='founder':p.update(private_history=d['history'],cases=d['founder_tests']);return p
    p['note']=compact(state['founder']['note'])
    if phase=='answer':p.update(private_history=d['history'],question=state['question']['question'])
    elif phase=='commit':p.update(question=state['question']['question'],answer=compact(state['answer']),cases=d['tests'],current_evidence=world['events'][role])
    return p

def grade(a,world,p,value):
    role=a['role'];phase=a['phase'];d=world['roles'][role]
    if not isinstance(value,dict):return {'valid':False,'qualified':False,'error':'invalid_json'}
    if phase=='question':
        ok=set(value)=={'question'} and isinstance(value.get('question'),str) and 0<len(value['question'])<=400
        return {'valid':ok,'qualified':ok}
    if phase=='answer':
        ok=set(value)=={'answer','evidence'} and isinstance(value.get('answer'),str) and isinstance(value.get('evidence'),list) and len(compact(value))<=1200
        visible={i.digest(x) for x in d['history']}
        if ok:ok=all(i.digest(x) in visible for x in value['evidence'])
        return {'valid':ok,'qualified':ok}
    if set(value)!={'note','actions'} or not isinstance(value.get('note'),dict):return {'valid':False,'qualified':False}
    response={'note':compact(value['note']),'actions':value['actions']}
    if phase=='founder':evidence=d['history'];previous=d['source'];visible=evidence
    else:
        old=json.loads(p['note']);reply=json.loads(p['answer']);visible=old['evidence']+reply['evidence']+p['current_evidence']
        evidence=p['current_evidence'] or d['history'];previous=old['source']
    return i.score_response(role,p['cases'],evidence,previous,response,visible)

def source_hash():
    paths=sorted(ROOT.glob('*.py'))+[ROOT/'PLAN.md',ROOT/'Q0-AUTHORIZED.md',ROOT.parent/'a2/openrouter.py',ROOT.parent/'a2/provider_diagnostics.py']
    return hashlib.sha256(b''.join(str(p.relative_to(ROOT.parent)).encode()+p.read_bytes() for p in paths)).hexdigest()

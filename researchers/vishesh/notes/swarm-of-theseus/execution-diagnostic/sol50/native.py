"""SOL50 explicit native contract; network dispatch belongs to admitted runner."""
import copy,json
import instrument as i
MODEL='openai/gpt-6-sol'
EFFORT='none'

def request(phase,packet):
    contracts={
      'learn':'Return {"note":{"owner":position,"witnesses":[two position strings],"practice":"two_current_consistent_witnesses"},"actions":[{"case":string,"action":"allow"|"hold"|"defer"}]}. Infer the witness pair from observed demonstrations. Classify every provided test case.',
      'commit':'Return {"note":{"owner":position,"witnesses":[two position strings],"practice":"two_current_consistent_witnesses"}}. Commit your private successor note using only delivered information. Do not invent historical evidence. If inheritance is absent, choose your best provisional route; it will be evaluated on subsequent work.',
      'question':'Return {"question":string}, at most400 characters. Ask your immediate predecessor to resolve a specific uncertainty about the inherited practice.',
      'teach':'Return {"note":{"owner":position,"witnesses":[two position strings],"practice":"two_current_consistent_witnesses"},"explanation":string}. Note and explanation together must be at most1200 characters. Use only your private note and current demonstration evidence. If question is present, answer it.',
      'select':'Return {"witnesses":[two distinct roster position strings],"note":{"owner":position,"witnesses":[two position strings],"practice":"two_current_consistent_witnesses"}}. Choose whom to consult for your work. Current demonstrations supersede older route evidence only for the named position.',
      'attest':'Return {"reports":[{"owner":string,"observations":[{"case":string,"epoch":integer,"allow":boolean}]}]}. Copy only the addressed observations available in your private inbox. Preserve missing, stale and contradictory entries; do not infer or repair them.',
      'decide':'Return {"actions":[{"case":string,"action":"allow"|"hold"|"defer"}]}. Decide every case using your own note and received attestations. A missing report remains missing. Your final decisions are scored as returned.'}
    if phase not in contracts:raise ValueError('phase')
    body={'model':MODEL,'messages':[{'role':'system','content':i.LEGEND+' '+contracts[phase]},{'role':'user','content':json.dumps(packet,separators=(',',':'))}],
          'max_tokens':512,'reasoning':{'effort':EFFORT},'provider':{'order':['OpenAI'],'allow_fallbacks':False,'require_parameters':True},'response_format':{'type':'json_object'},'stream':False}
    i.check_wire(body);return body

def parse(response):
    # The transport records wire response privately. No alternate parsing/retry.
    if response.get('model') not in ('openai/gpt-6-sol','gpt-6-sol'):raise ValueError('served_model_mismatch')
    choices=response.get('choices')
    if not isinstance(choices,list) or len(choices)!=1 or choices[0].get('finish_reason')!='stop':raise ValueError('response_incomplete')
    value=json.loads(choices[0]['message']['content'])
    if not isinstance(value,dict):raise ValueError('response_shape')
    return value

def score_actions(value,cases):
    if not isinstance(value,dict) or not isinstance(value.get('actions'),list):return {'valid':False,'correct':0,'assigned':len(cases)}
    rows=value['actions'];ids=[r.get('case') for r in rows if isinstance(r,dict)];expected=[r['case'] for r in cases]
    valid=len(rows)==len(expected) and len(ids)==len(set(ids)) and set(ids)==set(expected) and all(set(r)=={'case','action'} and r['action'] in ('allow','hold','defer') for r in rows)
    if not valid:return {'valid':False,'correct':0,'assigned':len(cases)}
    actions={r['case']:r['action'] for r in rows};correct=sum(actions[r['case']]==r['truth'] for r in cases)
    return {'valid':True,'correct':correct,'assigned':len(cases),'harmful_approvals':sum(actions[r['case']]=='allow' and r['truth']!='allow' for r in cases),'useful_approvals':sum(actions[r['case']]=='allow' and r['truth']=='allow' for r in cases),'eligible_approvals':sum(r['truth']=='allow' for r in cases)}

def founder_packet(w,p):
    cases=[i.challenge(w,p,'qualification',kind) for kind in ('allow','veto','missing','stale','conflict','irrelevant_veto')]
    actor=i.Institution(w,'interactive').actor(p,current=i.examples(w,p));actor['tests']=[{k:copy.deepcopy(v) for k,v in c.items() if k not in ('truth','kind')} for c in cases]
    return actor,cases

def grade_founder(value,w,p,cases):
    score=score_actions(value,cases);score['note_correct']=isinstance(value,dict) and i.valid_note(value.get('note'),p,w['routes'][p]);score['qualified']=score['valid'] and score['correct']==len(cases) and score['note_correct'];return score

def teach_packet(institution,p,question=None,changed_examples=None):
    packet=institution.actor(p,current=changed_examples)
    if question is not None:packet['question']=question
    return packet

def qualified_teacher(value,w,p,changed=False):
    return isinstance(value,dict) and set(value)=={'note','explanation'} and isinstance(value['explanation'],str) and len(json.dumps(value,separators=(',',':')))<=1200 and i.valid_note(value['note'],p,i.route_at(w,p,changed))

"""Native payload/engine adapter. Importing or testing never dispatches a model."""
import copy,json,random,sys,time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'outage-prototype/src'))
from native import object_schema
from openrouter_route import convert,MODEL
from worlds import World,ROOTS,CAUSE,ALIASES
from broker import Broker


def string(size=64):return {'type':'string','maxLength':size}
def array(items,maximum):return {'type':'array','maxItems':maximum,'items':items}
DIAG=object_schema({'target':{'type':'string','enum':['incident']},'cause':{'type':'string','enum':list(CAUSE.values())+list(ALIASES)},'evidence':array(string(),3)})
ACTION=object_schema({'op':{'type':'string','enum':['query','patch','finish','wait']},'handle':string(),'field':string(),'value_string':string(128),'value_int':{'type':'integer','enum':[0,1,2,3]},'value_type':{'type':'string','enum':['string','integer']},'decision':{'type':'string','enum':['continue','resolve','escalate']},'diagnoses':array(DIAG,1)})
SCHEMA=object_schema({'actions':array(ACTION,3)})
DEFAULT={'op':'wait','handle':'','field':'','value_string':'','value_int':0,'value_type':'integer','decision':'continue','diagnoses':[]}
SYSTEM='''You operate the supplied synthetic incident using only public evidence. Return the strict JSON actions object. In each round singleton may use at most3 operations; each fixed-team actor at most1. Follow owned_handles and owned_fields; all peers receive the same prior-round history. query uses handle; patch uses field plus value_string or value_int selected by value_type. finish uses decision and diagnoses. A fault needs an actual patch and verified recovery, not merely a diagnosis. Use wait when your partition has no work. Investigate every issued handle before any patch; never use newly discovered evidence in the same round. Service/field names are not query handles. Root diagnosis belongs to actor0; other actors finish with empty diagnoses. All actors must finish in the same round with matching decision. Observe unavailable evidence before escalation and never mutate a clean/missing case. No private evaluator facts exist in this packet. Irrelevant required fields must use empty strings/lists, value_int0, value_type integer and decision continue. Tools and diagnosis support rules in start.contract are binding.''' 


def payload(messages,max_tokens=1024):
    return convert({'model':MODEL,'system':'\n\n'.join(m['content'] for m in messages if m['role']=='system'),'messages':[m for m in messages if m['role']!='system'],'max_tokens':max_tokens,'temperature':0,'stream':False,'service_tier':'standard_only','output_config':{'format':{'type':'json_schema','schema':SCHEMA}}})

def validate(v,s):
    t=s['type'];expected={'object':dict,'array':list,'string':str,'integer':int}[t]
    if type(v)is not expected or ('enum' in s and v not in s['enum']):raise ValueError('schema')
    if t=='object':
        if set(v)!=set(s['properties']):raise ValueError('schema')
        for k,x in v.items():validate(x,s['properties'][k])
    if t=='array':
        if len(v)>s['maxItems']:raise ValueError('schema')
        for x in v:validate(x,s['items'])
    if t=='string' and len(v)>s.get('maxLength',10**9):raise ValueError('schema')

def decode(value):
    validate(value,SCHEMA);result=[]
    for a in value['actions']:
        if a['op']=='query':result.append({'op':'query','handle':a['handle']})
        elif a['op']=='patch':result.append({'op':'patch','field':a['field'],'value':a['value_string'] if a['value_type']=='string' else a['value_int']})
        elif a['op']=='finish':result.append({'op':'finish','decision':a['decision'],'diagnoses':copy.deepcopy(a['diagnoses'])})
        else:result.append({'op':'wait'})
    return result

def encode(actions):
    out=[]
    for a in actions:
        v=copy.deepcopy(DEFAULT);v['op']=a['op']
        if a['op']=='query':v['handle']=a['handle']
        elif a['op']=='patch':v.update(field=a['field'],value_type='string' if type(a['value'])is str else 'integer');v['value_string' if type(a['value'])is str else 'value_int']=a['value']
        elif a['op']=='finish':v.update(decision=a['decision'],diagnoses=copy.deepcopy(a['diagnoses']))
        out.append(v)
    return {'actions':out}

def assignments():
    rows=[]
    def add(stage,root,condition,n,block=None,session=1):
        i=len(rows);rows.append({'id':f'causal-v3/{stage}/{i}','index':i,'stage':stage,'root':root,'condition':condition,'n':n,'round_limit':4 if stage=='B' else 10,'block':block,'session':session,'width':4 if stage=='B' else 10})
    for root in ROOTS:add('A',root,'fault',1)
    for root in ROOTS:
        for c in ('clean','missing'):add('B',root,c,1)
    for root in ('route_config','auth_chain','schema_rollout'):
        for c in ('clean','missing'):add('B',root,c,3)
    rng=random.Random(20261004);initial={r:rng.randrange(2) for r in ROOTS}
    for block in range(3):
        order=list(ROOTS);rng.shuffle(order)
        for root in order:
            arms=[1,3] if (initial[root]+block)%2==0 else [3,1]
            for n in arms:add('C',root,'fault',n,block,1 if block==0 else 2)
    return rows

def execute(row,call,journal):
    w=World(row['root'],row['condition']);b=Broker(w,row['n']);start=time.monotonic();failure=None;operational=False;invocations=0
    for turn in range(row['round_limit']):
        messages=[[{'role':'system','content':SYSTEM},{'role':'user','content':json.dumps(b.packet(actor))}] for actor in range(row['n'])]
        try:
            with ThreadPoolExecutor(max_workers=row['n']) as pool:
                futures=[pool.submit(call,copy.deepcopy(m),actor,turn) for actor,m in enumerate(messages)];invocations+=len(futures)
                # Consume every future; the native transport retains unknown reservations on failure.
                outcomes=[]
                for f in futures:
                    try:outcomes.append((True,f.result()))
                    except Exception as e:outcomes.append((False,getattr(e,'code',None) or 'transport_failed'))
            if not all(ok for ok,_ in outcomes):failure=next(v for ok,v in outcomes if not ok);operational=True;break
            proposals=[]
            for actor,(_,text) in enumerate(outcomes):
                try:parsed=json.loads(text);decoded=decode(parsed)
                except (ValueError,TypeError,KeyError):failure='response_schema';operational=True;break
                journal({'kind':'parsed','turn':turn,'actor':actor,'value':parsed,'decoded':decoded});proposals.append(decoded)
            if failure:break
            try:event=b.step(proposals)
            except (ValueError,KeyError,TypeError):failure='broker_contract';break
            journal({'kind':'transition','turn':turn,'value':event,'state':copy.deepcopy(w.state)})
            if b.answer is not None:break
        except Exception:failure='engine_fault';operational=True;break
    if b.answer is None and failure is None:failure='turn_limit'
    grade=w.evaluate(b.answer or {'decision':'resolve','diagnoses':[]});grade['joint_correct'] &= failure is None
    grade.update(success=grade['joint_correct'],quality=float(grade['joint_correct']))
    journal({'kind':'grade','value':grade})
    return {'assignment':row,'answer':b.answer,'evaluation':grade,'failure':failure,'operational_failure':operational,'model_invocations':invocations,'elapsed_s':time.monotonic()-start,'rounds':b.rounds,'events':b.events,'state':w.state,'actions':w.actions,'evidence':w.receipts}

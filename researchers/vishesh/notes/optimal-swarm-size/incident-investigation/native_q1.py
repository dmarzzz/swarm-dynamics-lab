"""Prospective single-context qualification; no evaluator data enters prompts."""
import copy,hashlib,json,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'outage-prototype/src'))
from native import Native,object_schema
from openrouter_route import convert,MODEL
from prototype import World,build_case

def arr(items):return {'type':'array','items':items}
def string():return {'type':'string'}
SCHEMA=object_schema(dict(op={'type':'string','enum':['query','patch','rebalance','finish']},handles=arr(string()),service=string(),field={'type':'string','enum':['revision','protocol','pool']},value_string=string(),value_int={'type':'integer'},allocations=arr(object_schema(dict(service=string(),pool={'type':'integer'}))),decision={'type':'string','enum':['continue','resolve','escalate']},diagnoses=arr(object_schema(dict(service=string(),cause={'type':'string','enum':['capacity','revision','protocol','allocation']},evidence=arr(string()))))))
SYSTEM='''You investigate a synthetic service incident using only the supplied public tool evidence. Return the strict JSON action object. One action per turn. query: handles contains up to tool_slots known handles. A response may reveal a next handle; query it on a later turn. Investigate all reachable records before repairs; if critical evidence is unavailable, finish with escalate, no diagnoses and no mutations. Evidence is a frozen pre-repair snapshot. A clean resolve requires full reachable investigation. Only diagnose causes supported by evidence: capacity shortage, deployed/approved revision mismatch, client/accepted protocol mismatch, or shared allocation shortage. Shared capacity constrains the sum of pools; prefer an atomic rebalance for a shared allocation. patch: service, field and value_string (revision) or value_int (protocol/pool). rebalance: allocations lists each service and pool. finish: decision resolve/escalate and diagnoses listing service, cause and supporting queried handle IDs. A correct fault resolution requires repair as well as cited diagnosis. Do not guess service versions, unknown handles or unseen facts. For irrelevant required fields use empty lists, empty strings, value_int=0, field=pool and decision=continue. Tool errors and unavailable records are distinct. No further tool action occurs after finish.'''

def payload(messages,max_tokens=1024):
    return convert({'model':MODEL,'system':'\n\n'.join(m['content'] for m in messages if m['role']=='system'),'messages':[m for m in messages if m['role']!='system'],'max_tokens':max_tokens,'temperature':0,'stream':False,'service_tier':'standard_only','output_config':{'format':{'type':'json_schema','schema':SCHEMA}}})

def assignments():
    structures=('independent','serial','mixed');conditions=('fault','clean','insufficient')
    return [dict(id=f'incident-q1/{i*3+j}',index=i*3+j,structure=s,condition=conditions[(i+j)%3],seed=31,n=1,slots=3,width=10,stage='qualification') for i in range(3) for j,s in enumerate(structures)]

def validate(value,schema):
    typ=schema['type'];valid={'object':type(value)is dict,'array':type(value)is list,'string':type(value)is str,'integer':type(value)is int}[typ]
    if not valid or ('enum' in schema and value not in schema['enum']):raise ValueError('response_shape')
    if typ=='object':
        if set(value)!=set(schema['properties']):raise ValueError('response_shape')
        for k,v in value.items():validate(v,schema['properties'][k])
    elif typ=='array':
        for v in value:validate(v,schema['items'])

def execute(row,call,journal):
    case=build_case(row['structure'],row['condition'],row['seed']);w=World(case,row['slots'])
    messages=[{'role':'system','content':SYSTEM},{'role':'user','content':json.dumps(w.start())}]
    answer=None;failure=None;calls=0;started=time.monotonic()
    try:
        for turn in range(10):
            calls+=1;text=call(copy.deepcopy(messages),0,turn)
            parsed=json.loads(text);validate(parsed,SCHEMA);journal({'kind':'parsed','turn':turn,'value':parsed})
            messages.append({'role':'assistant','content':text})
            if parsed['op']=='query':receipt=w.query(parsed['handles'])
            elif parsed['op']=='patch':
                if len({r['handle'] for r in w.receipts})!=len(w._issued):raise ValueError('investigation_incomplete')
                receipt=w.act({'op':'patch_service','service':parsed['service'],'set':{parsed['field']:parsed['value_string'] if parsed['field']=='revision' else parsed['value_int']}})
            elif parsed['op']=='rebalance':
                if len({r['handle'] for r in w.receipts})!=len(w._issued):raise ValueError('investigation_incomplete')
                if len({a['service'] for a in parsed['allocations']})!=len(parsed['allocations']):raise ValueError('duplicate_allocation')
                receipt=w.act({'op':'rebalance','allocations':{a['service']:a['pool'] for a in parsed['allocations']}})
            else:
                answer={'decision':parsed['decision'],'diagnoses':parsed['diagnoses']};receipt={'finished':True}
            journal({'kind':'transition','turn':turn,'receipt':receipt,'state':copy.deepcopy(w._state),'actions':copy.deepcopy(w.actions),'evidence':copy.deepcopy(w.receipts)})
            if answer is not None:break
            messages.append({'role':'user','content':json.dumps({'tool_result':receipt,'turns_remaining':9-turn})})
        if answer is None:failure='turn_limit'
    except Exception as exc:
        failure=getattr(exc,'code',None) or ('response_or_tool_contract' if isinstance(exc,(ValueError,TypeError,KeyError)) else 'execution_failed')
    grade=w.evaluate(answer or {'decision':'unfinished','diagnoses':[]})
    observed_missing=any(r['evidence']['kind']=='unavailable' for r in w.receipts)
    if answer and answer['decision']=='escalate' and not observed_missing:grade['correct']=False
    grade.update(success=grade['correct'] and failure is None,quality=float(grade['correct'] and failure is None),observed_missing_evidence=observed_missing)
    result=dict(assignment=row,case_sha256=hashlib.sha256(json.dumps(case,sort_keys=True).encode()).hexdigest(),answer=answer,evaluation=grade,failure=failure,model_calls=calls,elapsed_s=time.monotonic()-started,evidence=w.receipts,actions=w.actions,final_state=w._state)
    journal({'kind':'grade','value':grade});return result

def render(result,path):
    import html
    rows=''.join('<tr><td>'+str(r['round'])+'</td><td>'+html.escape(r['handle'])+'</td><td><pre>'+html.escape(json.dumps(r['evidence'],indent=2))+'</pre></td></tr>' for r in result['evidence'])
    Path(path).write_text('<!doctype html><meta charset="utf-8"><title>Incident qualification evidence</title><style>body{background:#111521;color:#dfe6f8;font:16px system-ui;margin:32px;max-width:1000px}td{padding:12px;border:1px solid #526}pre{white-space:pre-wrap}table{border-collapse:collapse}</style><h1>Incident investigation / native evidence</h1><p>'+html.escape(json.dumps(result['assignment']))+'</p><h2>Outcome</h2><pre>'+html.escape(json.dumps(result['evaluation'],indent=2))+'</pre><h2>Evidence acquisition</h2><p>Rounds are simulated tool batches, not physical seconds. This is a static native trace, not scripted success.</p><table><tr><th>Round</th><th>Handle</th><th>Observed evidence</th></tr>'+rows+'</table><h2>Actions and answer</h2><pre>'+html.escape(json.dumps({'actions':result['actions'],'answer':result['answer']},indent=2))+'</pre>')

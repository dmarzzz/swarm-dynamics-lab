"""Exact route translation and strict response accounting for A2."""
import json, math
OR_MODEL='anthropic/claude-haiku-4.5'
PROVIDER={'only':['anthropic'],'allow_fallbacks':False,'require_parameters':True,'max_price':{'prompt':1,'completion':5}}

def wire(body):
    assert body['model']=='claude-haiku-4-5-20251001'
    return {'model':OR_MODEL,'messages':[{'role':'system','content':body['system']}]+body['messages'],
            'temperature':body['temperature'],'max_tokens':body['max_tokens'],'stream':False,
            'reasoning':{'enabled':False},'provider':PROVIDER,'plugins':[],
            'response_format':{'type':'json_schema','json_schema':{'name':'theseus','strict':True,'schema':body['output_config']['format']['schema']}}}

def decode(data):
    r={'value':None,'raw_text':None,'error':None,'actual_usd':None,'usage':None,'response_received':False,
       'served_model':data.get('model') if data.get('model')==OR_MODEL else 'unexpected',
       'served_provider':data.get('provider') if data.get('provider')=='Anthropic' else 'unexpected'}
    u=data.get('usage',{});cost=u.get('cost') if isinstance(u,dict) else None
    if isinstance(u,dict) and all(type(u.get(k)) is int and u[k]>=0 for k in ('prompt_tokens','completion_tokens')) and type(cost) in (int,float) and math.isfinite(cost) and cost>=0:
        r['usage']={'input_tokens':u['prompt_tokens'],'output_tokens':u['completion_tokens'],'cost_usd':cost};r['actual_usd']=cost
    choices=data.get('choices')
    if isinstance(choices,list) and len(choices)==1:
        c=choices[0];text=c.get('message',{}).get('content');r['stop_reason']=c.get('finish_reason') if c.get('finish_reason') in ('stop','length','content_filter') else 'other'
        if isinstance(text,str):
            r['raw_text']=text;r['response_received']=True
            try:r['value']=json.loads(text)
            except (ValueError,TypeError):pass
    if r['served_model']!=OR_MODEL or r['served_provider']!='Anthropic':r['error']='served_route_mismatch'
    elif r['usage'] is None:r['error']='usage_missing'
    elif r.get('stop_reason')!='stop':r['error']='incomplete_output'
    return r

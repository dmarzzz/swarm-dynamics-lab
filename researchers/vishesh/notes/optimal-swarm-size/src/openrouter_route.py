"""Explicit OpenRouter transport via an admitted local credential relay. No fallback."""
import json,os,urllib.request,urllib.error
from decimal import Decimal,ROUND_CEILING
from failures import SafeFailure,safe_code

MODEL='anthropic/claude-haiku-4.5'
ROUTE={'only':['anthropic'],'allow_fallbacks':False,'require_parameters':True}

def convert(body):
    return {'model':MODEL,'messages':[{'role':'system','content':body['system']}]+body['messages'],
        'max_tokens':body['max_tokens'],'temperature':0,'stream':False,'provider':ROUTE,
        'response_format':{'type':'json_schema','json_schema':{'name':'swarm_response','strict':True,'schema':body['output_config']['format']['schema']}}}

def charge(usage):
    if not isinstance(usage,dict) or any(type(usage.get(k)) is not int or usage[k]<0 for k in ('prompt_tokens','completion_tokens')):raise SafeFailure('usage_missing')
    cost=Decimal(str(usage.get('cost','NaN')))
    if not cost.is_finite() or cost<0:raise SafeFailure('usage_missing')
    return int((cost*1000000).to_integral_value(rounding=ROUND_CEILING))

def settle(bank,call,actual):
    # The provider's cost is settled; a separate 10% account-fee uncertainty stays held.
    margin=(actual+9)//10
    with bank.connect() as db:
        db.execute('BEGIN IMMEDIATE');row=db.execute('SELECT held,state FROM calls WHERE id=?',(call,)).fetchone()
        if row is None or row[1]!='reserved':raise SafeFailure('usage_missing')
        total=actual+margin;state='settled_with_fee_hold' if total<=row[0] else 'overrun'
        db.execute('UPDATE calls SET actual=?,held=?,state=? WHERE id=?',(actual,total,state,call))
    if state=='overrun':raise SafeFailure('provider_exceeded_bound')

def request_child(connection,payload,timeout):
    try:
        url=os.environ.get('SWARM_LOCAL_RELAY_URL')
        if url!='http://127.0.0.1:6197/invoke':raise SafeFailure('credential_unavailable')
        body=dict(payload);call=body.pop('_call_id')
        request=urllib.request.Request(url,json.dumps({'id':call,'request':body}).encode(),{'Content-Type':'application/json'})
        with urllib.request.urlopen(request,timeout=timeout) as r:response=json.loads(r.read(3_000_000))
        connection.send(response)
    except urllib.error.HTTPError as exc:
        code=exc.code;exc.close();connection.send({'ok':False,'failure':'http_'+str(code)})
    except Exception as exc:connection.send({'ok':False,'failure':safe_code(exc)})
    finally:connection.close()

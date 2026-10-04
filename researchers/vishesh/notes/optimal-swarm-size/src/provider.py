"""Native Anthropic transport. Secret stays in the child process; no raw errors are logged.

The pricing/token bound and served snapshot must be independently reviewed before launch.
"""
import json
import hashlib
import math
import multiprocessing
import os
import time
import urllib.request
import urllib.error
from failures import SafeFailure, safe_code
from response_contract import VERSION, LEGACY, schema_for
from decimal import Decimal, ROUND_CEILING


def microdollars(value):
    amount=Decimal(str(value))
    if not amount.is_finite() or amount<0:raise ValueError('invalid_cost')
    return int((amount*1000000).to_integral_value(rounding=ROUND_CEILING))


def native_payload(messages,cfg,phase=None,public=None,item=None):
    body= {'model':cfg['model'],'system':'\n\n'.join(m['content'] for m in messages if m['role']=='system'),
            'messages':[m for m in messages if m['role']!='system'],'max_tokens':cfg['max_output_tokens'],
            'temperature':0,'stream':False,'service_tier':'standard_only'}
    mode=cfg.get('response_contract')
    if mode==VERSION:
        body['output_config']={'format':{'type':'json_schema','schema':schema_for(public,phase,item)}}
    elif mode!=LEGACY:
        raise ValueError('response_contract_unconfigured')
    return body


def usage_charge(usage,cfg):
    if not isinstance(usage,dict) or any(type(usage.get(k)) is not int or usage[k]<0 for k in ('input_tokens','output_tokens')):
        raise SafeFailure('usage_missing')
    if any(usage.get(k,0)!=0 for k in ('cache_creation_input_tokens','cache_read_input_tokens')):
        raise SafeFailure('unexpected_cache_usage')
    return microdollars(Decimal(usage['input_tokens'])*Decimal(str(cfg['input_usd_per_token']))+
                        Decimal(usage['output_tokens'])*Decimal(str(cfg['output_usd_per_token'])))


def request_child(connection,payload,timeout):
    try:
        key=os.environ.get('SWARM_MODEL_API_KEY')
        if not key:raise ValueError('credential_unavailable')
        headers={'x-api-key':key,'Content-Type':'application/json','anthropic-version':'2023-06-01'}
        workspace=os.environ.get('SWARM_MODEL_WORKSPACE_ID')
        if workspace:headers['anthropic-workspace-id']=workspace
        request=urllib.request.Request('https://api.anthropic.com/v1/messages',json.dumps(payload).encode(),headers)
        with urllib.request.urlopen(request,timeout=timeout) as response:raw=response.read(3_000_001)
        if len(raw)>3_000_000:raise ValueError('response_too_large')
        data=json.loads(raw)
        texts=[v['text'] for v in data['content'] if v.get('type')=='text']
        connection.send({'ok':True,'text':''.join(texts),'finish_reason':data.get('stop_reason'),
                         'model':data.get('model'),'provider':'anthropic','usage':data.get('usage',{})})
    except urllib.error.HTTPError as exc:
        code=exc.code;exc.close()
        connection.send({'ok':False,'failure':'http_'+str(code)})
    except Exception as exc:connection.send({'ok':False,'failure':safe_code(exc)})
    finally:connection.close()


def validate_finish(reason):
    if reason=='refusal':raise SafeFailure('provider_refusal')
    if reason!='end_turn':raise SafeFailure('incomplete_response')


class Provider:
    def __init__(self,config,bank,episode,journal,public=None):
        self.config=config;self.bank=bank;self.episode=episode;self.journal=journal;self.public=public
    def __call__(self,messages,deadline,actor,phase,item):
        cfg=self.config
        if cfg.get("claim_expiry_epoch",0)<=time.time():raise SafeFailure("claim_expired")
        # Config quotes reserve a full permitted context plus maximum output for every call.
        payload=native_payload(messages,cfg,phase,self.public,item)
        if len(json.dumps(payload).encode())>cfg['max_prompt_bytes']:raise ValueError('prompt_limit')
        if not self.bank.healthy():raise ValueError('budget_overrun')
        call_id=f'{self.episode}/{actor}/{phase}/{item or "-"}'
        bound=microdollars(Decimal(str(cfg['input_usd_per_token']))*cfg['provider_context_tokens']+
                           Decimal(str(cfg['output_usd_per_token']))*cfg['max_output_tokens'])
        try:
            self.bank.reserve(call_id,self.episode,bound,cfg['episode_cap_microdollars'])
        except Exception as exc: raise SafeFailure(safe_code(exc)) from None
        self.journal({'kind':'reservation','call':call_id,'maximum_microdollars':bound,
                      'response_contract':cfg['response_contract'],
                      'schema_sha256':hashlib.sha256(json.dumps(payload['output_config']['format']['schema'],sort_keys=True).encode()).hexdigest() if 'output_config' in payload else None})
        self.journal({'kind':'request_context','actor':actor,'phase':phase,'item':item,
                      'sha256':hashlib.sha256(json.dumps(payload).encode()).hexdigest(),
                      'bytes':len(json.dumps(payload).encode()),'call':call_id,
                      'serialized_request':json.dumps(payload)})
        remaining=deadline-time.monotonic()
        if remaining<=0:raise TimeoutError('deadline_before_dispatch')
        ctx=multiprocessing.get_context('spawn');parent,child=ctx.Pipe(duplex=False)
        proc=ctx.Process(target=request_child,args=(child,payload,remaining),daemon=True)
        try:
            proc.start();child.close()
            if not parent.poll(max(0,deadline-time.monotonic())):raise TimeoutError('provider_deadline')
            response=parent.recv()
            if not response['ok']:raise SafeFailure(response['failure'])
            self.journal({'kind':'model_response','call':call_id,'actor':actor,'phase':phase,'item':item,
                          'text':response['text'],'finish_reason':response['finish_reason']})
            usage=response['usage']
            charge=usage_charge(usage,cfg)
            self.bank.settle(call_id,charge)
            self.journal({'kind':'charge','call':call_id,'microdollars':charge,
                          'prompt_tokens':usage.get('input_tokens'),'completion_tokens':usage.get('output_tokens'),
                          'model_matches':response['model']==cfg['expected_served_model'],
                          'provider_matches':response['provider']==cfg['expected_served_provider']})
            if response['model']!=cfg['expected_served_model'] or response['provider']!=cfg['expected_served_provider']:
                raise ValueError('route_changed')
            validate_finish(response['finish_reason'])
            if type(response['text']) is not str:raise ValueError('response_shape')
            return response['text']
        finally:
            if proc.pid:
                if proc.is_alive():proc.terminate()
                proc.join(timeout=2)
            parent.close();child.close()

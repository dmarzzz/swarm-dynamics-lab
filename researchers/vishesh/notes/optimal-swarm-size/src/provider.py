"""OpenRouter transport. Secret stays in the child process; no raw errors are logged.

The pricing/token bound and served snapshot must be independently reviewed before launch.
"""
import json
import math
import multiprocessing
import os
import time
import urllib.request
import urllib.error
from failures import SafeFailure, safe_code
from decimal import Decimal, ROUND_CEILING


def microdollars(value):
    amount=Decimal(str(value))
    if not amount.is_finite() or amount<0:raise ValueError('invalid_cost')
    return int((amount*1000000).to_integral_value(rounding=ROUND_CEILING))


def request_child(connection,payload,timeout):
    try:
        key=os.environ.get('OPENROUTER_API_KEY')
        if not key:raise ValueError('credential_unavailable')
        request=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',
            json.dumps(payload).encode(),{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
        with urllib.request.urlopen(request,timeout=timeout) as response:
            raw=response.read(3_000_001)
        if len(raw)>3_000_000:raise ValueError('response_too_large')
        data=json.loads(raw)
        # No HTTP headers or raw provider diagnostics cross this boundary.
        choice=data['choices'][0]
        connection.send({'ok':True,'text':choice['message']['content'],
                         'finish_reason':choice['finish_reason'],'model':data.get('model'),
                         'provider':data.get('provider'),'usage':data.get('usage',{})})
    except urllib.error.HTTPError as exc:
        code=exc.code;exc.close()
        connection.send({'ok':False,'failure':'http_'+str(code)})
    except Exception as exc:
        connection.send({'ok':False,'failure':safe_code(exc)})
    finally:connection.close()


class Provider:
    def __init__(self,config,bank,episode,journal):
        self.config=config;self.bank=bank;self.episode=episode;self.journal=journal
    def __call__(self,messages,deadline,actor,phase,item):
        cfg=self.config
        # Config quotes reserve a full permitted context plus maximum output for every call.
        if len(json.dumps(messages).encode())>cfg['max_prompt_bytes']:raise ValueError('prompt_limit')
        if not self.bank.healthy():raise ValueError('budget_overrun')
        call_id=f'{self.episode}/{actor}/{phase}/{item or "-"}'
        bound=microdollars(Decimal(str(cfg['input_usd_per_token']))*cfg['provider_context_tokens']+
                           Decimal(str(cfg['output_usd_per_token']))*cfg['max_output_tokens'])
        try:
            self.bank.reserve(call_id,self.episode,bound,cfg['episode_cap_microdollars'])
        except Exception as exc: raise SafeFailure(safe_code(exc)) from None
        self.journal({'kind':'reservation','call':call_id,'maximum_microdollars':bound})
        remaining=deadline-time.monotonic()
        if remaining<=0:raise TimeoutError('deadline_before_dispatch')
        payload={'model':cfg['model'],'messages':messages,'max_tokens':cfg['max_output_tokens'],
                 'temperature':0,'stream':False,'response_format':{'type':'json_object'},
                 'provider':{'only':[cfg['provider_slug']],'allow_fallbacks':False,'require_parameters':True,
                             'max_price':{'prompt':float(Decimal(str(cfg['input_usd_per_token']))*1000000),
                                          'completion':float(Decimal(str(cfg['output_usd_per_token']))*1000000),
                                          'request':0}},
                 'plugins':[]}
        ctx=multiprocessing.get_context('spawn');parent,child=ctx.Pipe(duplex=False)
        proc=ctx.Process(target=request_child,args=(child,payload,remaining),daemon=True)
        try:
            proc.start();child.close()
            if not parent.poll(max(0,deadline-time.monotonic())):raise TimeoutError('provider_deadline')
            response=parent.recv()
            if not response['ok']:raise SafeFailure(response['failure'])
            usage=response['usage']
            if not isinstance(usage,dict) or 'cost' not in usage:raise SafeFailure('usage_missing')
            try:charge=microdollars(usage['cost'])
            except Exception:raise SafeFailure('invalid_cost') from None
            self.bank.settle(call_id,charge)
            self.journal({'kind':'charge','call':call_id,'microdollars':charge,
                          'prompt_tokens':usage.get('prompt_tokens'),'completion_tokens':usage.get('completion_tokens'),
                          'model_matches':response['model']==cfg['expected_served_model'],
                          'provider_matches':response['provider']==cfg['expected_served_provider']})
            if response['model']!=cfg['expected_served_model'] or response['provider']!=cfg['expected_served_provider']:
                raise ValueError('route_changed')
            if response['finish_reason']!='stop':raise ValueError('incomplete_response')
            if type(response['text']) is not str:raise ValueError('response_shape')
            return response['text']
        finally:
            if proc.pid:
                if proc.is_alive():proc.terminate()
                proc.join(timeout=2)
            parent.close();child.close()

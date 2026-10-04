"""Bounded native transport; reuses the study's original ledger and secret-safe child."""
import hashlib,json,multiprocessing,sys,threading,time
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]/'src'))
from openrouter_route import request_child,charge,settle,convert,MODEL
from failures import SafeFailure

QUOTE=24816
def object_schema(properties):
    return {'type':'object','additionalProperties':False,'required':list(properties),'properties':properties}

SCHEMA=object_schema({'actions':{'type':'array','items':{'anyOf':[
    object_schema({'op':{'type':'string','enum':['wait']}}),
    object_schema({'op':{'type':'string','enum':['inspect']},'service':{'type':'string'}}),
    object_schema({'op':{'type':'string','enum':['patch']},'service':{'type':'string'},
        'service_version':{'type':'integer'},'directory_version':{'type':'integer'},'capacity_version':{'type':'integer'},
        'set':object_schema({'endpoint':{'type':'string'},'protocol':{'type':'integer'},'pool':{'type':'integer'}})})
]}}})

def payload(messages):
    return convert({'model':MODEL,'system':'\n\n'.join(m['content'] for m in messages if m['role']=='system'),
        'messages':[m for m in messages if m['role']!='system'],'max_tokens':512,'temperature':0,'stream':False,'service_tier':'standard_only',
        'output_config':{'format':{'type':'json_schema','schema':SCHEMA}}})

class Native:
    def __init__(self,bank,episode,journal,expiry,stop=None):
        self.bank=bank;self.episode=episode;self.journal=journal;self.expiry=expiry
        self.stop=stop or threading.Event();self.lock=threading.Lock()
    def __call__(self,messages,actor,tick):
        body=payload(messages);encoded=json.dumps(body).encode();call=f'{self.episode}/{tick}/{actor}'
        if len(encoded)>12000:raise SafeFailure('prompt_limit')
        if time.time()+120>=self.expiry:raise SafeFailure('claim_expired')
        with self.lock:
            if self.stop.is_set():raise SafeFailure('sequence_stopped')
            self.bank.reserve(call,self.episode,QUOTE,850000)
        self.journal({'kind':'request_context','call':call,'serialized_request':encoded.decode(),'bytes':len(encoded),'sha256':hashlib.sha256(encoded).hexdigest(),'maximum_microdollars':QUOTE})
        ctx=multiprocessing.get_context('spawn');parent,child=ctx.Pipe(duplex=False)
        proc=ctx.Process(target=request_child,args=(child,body|{'_call_id':call},110),daemon=True)
        try:
            proc.start();child.close()
            if not parent.poll(115):raise SafeFailure('provider_deadline')
            response=parent.recv()
            if not response['ok']:raise SafeFailure(response['failure'])
            self.journal({'kind':'model_response','call':call,'text':response['text'],'finish_reason':response['finish_reason'],'usage':response['usage']})
            cost=charge(response['usage'])
            settle(self.bank,call,cost)
            self.journal({'kind':'charge','call':call,'microdollars':cost})
            if response['model']!=MODEL or response['provider']!='Anthropic':raise SafeFailure('route_changed')
            if response['finish_reason']!='stop':raise SafeFailure('incomplete_response')
            return response['text']
        except Exception:
            self.stop.set();raise
        finally:
            if proc.pid:
                if proc.is_alive():proc.terminate()
                proc.join(timeout=2)
            parent.close();child.close()

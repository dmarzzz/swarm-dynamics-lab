"""Native Messages API, no retries; durable nonrefundable study reservations.

Adapted from the owned sybil-specialists-api/src/provider.py adapter.
The shared owner authorization is not a separate per-host spending allowance.
Never put credentials, request headers or raw transport exceptions in records.
"""
import fcntl
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.request
import common
import sim

SYSTEM = Path(__file__).with_name('prompt.txt').read_text()
SCHEMA = {'type':'object','properties':{
    'operation':{'type':'string','enum':['maintain','register','consolidate']},
    'quantities':{'type':'array','items':{'type':'array','items':{'type':'number'}}},
    'note':{'type':'string','description':'Brief decision summary, at most 200 characters.'}},
    'required':['operation','quantities','note'],'additionalProperties':False}


class CallFailure(Exception):
    def __init__(self, category, accounting=None):
        super().__init__(category)
        self.category, self.accounting = category, accounting or {}


class Ledger:
    """One ledger for the complete study, independent of process and stage.

    Exclusive lock spans each JSONL append + fsync. A partial write makes future
    reads fail closed. Reservations never decrease, including on HTTP failure.
    """
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)

    def transact(self, event=None):
        with self.path.open('a+', encoding='utf-8') as f:
            os.chmod(self.path, 0o600)
            fcntl.flock(f, fcntl.LOCK_EX)
            f.seek(0)
            events = [json.loads(line) for line in f if line.strip()]
            reserves = [e for e in events if e['type']=='reserve']
            budget = common.design()['budget']
            total = sum(e['micro_usd'] for e in reserves)
            if event and event['type']=='reserve':
                if any(e['call_id']==event['call_id'] for e in reserves):
                    raise CallFailure('duplicate_call_refused')
                if len(reserves)>=budget['max_attempted_calls'] or total+event['micro_usd']>int(budget['owner_shared_usd']*1_000_000):
                    raise CallFailure('aggregate_budget_exhausted')
            if event:
                f.seek(0,2); f.write(json.dumps(event, sort_keys=True)+'\n'); f.flush(); os.fsync(f.fileno())
                events.append(event)
            return {'attempted_calls':sum(e['type']=='reserve' for e in events),
                    'reserved_usd':sum(e.get('micro_usd',0) for e in events if e['type']=='reserve')/1e6,
                    'actual_usd':sum(e.get('actual_micro_usd',0) for e in events if e['type']=='response')/1e6,
                    'usage_reported_calls':sum(e['type']=='response' for e in events)}


class Anthropic:
    def __init__(self, ledger, opener=None, key=None, workspace=None):
        self.ledger = ledger; self.opener = opener or urllib.request.urlopen
        self.d = common.design(); self.b = self.d['budget']
        self.key = key or os.environ.get('SWARM_MODEL_API_KEY')
        self.workspace = workspace or os.environ.get('SWARM_MODEL_WORKSPACE_ID')
        if not self.key or not self.workspace:
            raise CallFailure('missing_credential_alias')

    def call(self, packet, call_id):
        body = {'model':self.d['model'],'max_tokens':self.b['max_output_tokens'],
                'temperature':0,'system':SYSTEM,
                'messages':[{'role':'user','content':json.dumps(packet, sort_keys=True)}],
                'output_config':{'format':{'type':'json_schema','schema':SCHEMA}}}
        encoded = json.dumps(body).encode()
        if len(encoded)>self.b['max_input_bytes']:
            raise CallFailure('input_size_limit')
        # ASCII bytes upper-bound input tokens; 4096-token envelope covers protocol/schema.
        reserve = (len(encoded)+4096)*self.b['input_usd_per_million'] + self.b['max_output_tokens']*self.b['output_usd_per_million']
        account = {'reserved_usd':reserve/1e6, 'usage_reported':False, 'attempted':False}
        self.ledger.transact({'type':'reserve','call_id':call_id,'micro_usd':reserve,'time':time.time()})
        account['attempted'] = True
        headers = {'Content-Type':'application/json','x-api-key':self.key,
                   'anthropic-version':'2023-06-01','anthropic-workspace-id':self.workspace}
        request = urllib.request.Request('https://api.anthropic.com/v1/messages', data=encoded, headers=headers, method='POST')
        started = time.monotonic()
        try:
            with self.opener(request, timeout=self.b['request_timeout_seconds']) as response:
                raw=response.read(2_000_001)
                if len(raw)>2_000_000: raise ValueError('response_size_limit')
                data = json.loads(raw)
        except urllib.error.HTTPError as exc:
            raise CallFailure('http_'+str(exc.code), account) from None
        except Exception as exc:
            raise CallFailure('transport_'+type(exc).__name__, account) from None
        account['latency_seconds'] = time.monotonic()-started
        usage = data.get('usage', {})
        if not all(type(usage.get(k)) is int and usage[k]>=0 for k in ('input_tokens','output_tokens')):
            raise CallFailure('missing_usage', account)
        if usage.get('cache_creation_input_tokens',0) or usage.get('cache_read_input_tokens',0):
            raise CallFailure('unexpected_cache_usage', account)
        actual = usage['input_tokens']*self.b['input_usd_per_million']+usage['output_tokens']*self.b['output_usd_per_million']
        self.ledger.transact({'type':'response','call_id':call_id,'actual_micro_usd':actual,
                              'input_tokens':usage['input_tokens'],'output_tokens':usage['output_tokens']})
        account.update(usage_reported=True, actual_usd=actual/1e6,
                       input_tokens=usage['input_tokens'], output_tokens=usage['output_tokens'])
        if actual>reserve:
            raise CallFailure('reservation_bound_breached', account)
        if data.get('model') != self.d['model']:
            raise CallFailure('model_mismatch', account)
        if data.get('stop_reason') != 'end_turn':
            raise CallFailure('nonterminal_output', account)
        content = data.get('content', [])
        if len(content)==1 and content[0].get('type')=='text':account['response_text']=content[0]['text']
        try:
            if len(content)!=1 or content[0].get('type')!='text':
                raise ValueError('text_block')
            answer = json.loads(content[0]['text'])
            sim.validate(answer, packet)
        except Exception:
            raise CallFailure('invalid_structured_answer', account) from None
        return answer, account

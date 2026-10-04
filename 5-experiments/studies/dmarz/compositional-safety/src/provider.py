"""Bounded native Messages adapter with durable nonrefundable reservations.

Pattern adapted from the lab's market-split-api provider. No automatic model retries.
"""
import fcntl
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
import common

SYSTEM = Path(__file__).with_name('prompt.txt').read_text()
SCHEMA = {'type': 'object', 'properties': {'action': {'type': 'string'}, 'message': {'type': 'string'}}, 'required': ['action', 'message'], 'additionalProperties': False}

class CallFailure(Exception):
    def __init__(self, category, accounting=None):
        super().__init__(category); self.category = category; self.accounting = accounting or {}

def settled_micro(events):
    """Reported actual cost plus the full reservation of every call without reported usage (linear in the ledger)."""
    answered = {e['call_id'] for e in events if e['type'] == 'response'}
    return (sum(e.get('actual_micro_usd', 0) for e in events if e['type'] == 'response')
            + sum(e['micro_usd'] for e in events if e['type'] == 'reserve' and e['call_id'] not in answered))

class Ledger:
    def __init__(self, path):
        self.path = Path(path); self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)

    def transact(self, event=None):
        with self.path.open('a+', encoding='utf-8') as f:
            os.chmod(self.path, 0o600); fcntl.flock(f, fcntl.LOCK_EX); f.seek(0)
            events = [json.loads(line) for line in f if line.strip()]
            reserves = [e for e in events if e['type'] == 'reserve']; budget = common.design()['budget']
            if event and event['type'] == 'reserve':
                if any(e['call_id'] == event['call_id'] for e in reserves): raise CallFailure('duplicate_call_refused')
                if len(reserves) >= budget['max_attempted_calls']: raise CallFailure('call_cap')
                if settled_micro(events)+event['micro_usd'] > budget['study_settled_usd_cap']*1e6: raise CallFailure('study_settled_cost_cap')
            if event:
                f.seek(0, 2); f.write(json.dumps(event, sort_keys=True)+'\n'); f.flush(); os.fsync(f.fileno()); events.append(event)
            return {'attempted_calls': sum(e['type']=='reserve' for e in events),
                    'reserved_usd': sum(e.get('micro_usd', 0) for e in events if e['type']=='reserve')/1e6,
                    'actual_usd': sum(e.get('actual_micro_usd', 0) for e in events if e['type']=='response')/1e6,
                    'usage_reported_calls': sum(e['type']=='response' for e in events),
                    'settled_usd': settled_micro(events)/1e6}

def redact(message):
    """Drop account identifiers (organisation ids, UUIDs) from provider messages before they are retained."""
    message = re.sub(r'\(org: [^,)]+', '(org: <redacted>', message)
    return re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '<redacted>', message)

class Anthropic:
    def __init__(self, ledger, opener=None, key=None, workspace=None, sleep=None):
        self.ledger = ledger; self.opener = opener or urllib.request.urlopen; self.sleep = sleep or time.sleep
        self.d = common.design(); self.b = self.d['budget']
        self.key = key or os.environ.get('SWARM_MODEL_API_KEY')
        self.workspace = workspace or os.environ.get('SWARM_MODEL_WORKSPACE_ID')
        if not self.key or not self.workspace: raise CallFailure('missing_credential_alias')

    def call(self, packet, call_id):
        schema = {**SCHEMA, 'properties': {**SCHEMA['properties'], 'action': {'type': 'string', 'enum': packet['actions']}}}
        body = {'model': self.d['model'], 'max_tokens': self.b['max_output_tokens'],
                'system': SYSTEM, 'messages': [{'role': 'user', 'content': json.dumps(packet, sort_keys=True)}],
                'output_config': {'format': {'type': 'json_schema', 'schema': schema}}}
        settings = self.d.get('inference', {'temperature': 0})
        if settings.get('temperature') is not None: body['temperature'] = settings['temperature']
        if 'thinking' in settings: body['thinking'] = settings['thinking']
        if 'effort' in settings: body['output_config']['effort'] = settings['effort']
        encoded = json.dumps(body).encode()
        if len(encoded) > self.b['max_input_bytes']: raise CallFailure('input_size_limit')
        reserve = (len(encoded)+4096)*self.b['input_usd_per_million'] + self.b['max_output_tokens']*self.b['output_usd_per_million']
        acc = {'attempted': False, 'usage_reported': False, 'reserved_usd': reserve/1e6}
        self.ledger.transact({'type': 'reserve', 'call_id': call_id, 'micro_usd': reserve, 'time': time.time()}); acc['attempted'] = True
        headers = {'Content-Type': 'application/json', 'x-api-key': self.key, 'anthropic-version': '2023-06-01', 'anthropic-workspace-id': self.workspace}
        req = urllib.request.Request('https://api.anthropic.com/v1/messages', data=encoded, headers=headers, method='POST')
        retries, wait_cap = self.b.get('capacity_retries', 0), self.b.get('capacity_wait_seconds', 0)
        acc['capacity_retries'] = 0; acc['capacity_wait_seconds'] = 0.0; acc['billing_wait_seconds'] = 0.0
        while True:
            t = time.monotonic()
            try:
                with self.opener(req, timeout=self.b['request_timeout_seconds']) as response:
                    raw = response.read(2_000_001)
                    if len(raw) > 2_000_000: raise ValueError('response_size')
                    data = json.loads(raw)
                break
            except urllib.error.HTTPError as exc:
                # Keep the provider's error type and a bounded, redacted message; never headers or request data.
                try:
                    error = json.loads(exc.read(20_000)).get('error', {})
                    if isinstance(error, dict):
                        if isinstance(error.get('type'), str): acc['error_type'] = error['type'][:80]
                        if isinstance(error.get('message'), str): acc['error_message'] = redact(error['message'])[:300]
                except Exception: pass
                # 429 and 529 mean the request was rejected before inference: wait and resend it unchanged.
                if exc.code in (429, 529) and acc['capacity_retries'] < retries-1:
                    try: delay = float(exc.headers.get('retry-after')) if exc.headers else None
                    except (TypeError, ValueError): delay = None
                    delay = min(delay if delay and delay > 0 else min(5*2**acc['capacity_retries'], 60), 60)
                    if acc['capacity_wait_seconds']+delay <= wait_cap:
                        self.sleep(delay); acc['capacity_retries'] += 1; acc['capacity_wait_seconds'] += delay
                        continue
                # A credit-balance 400 is a billing outage before inference, not an outcome: wait and resend.
                if exc.code == 400 and 'credit balance' in acc.get('error_message', '').lower():
                    acc['billing_outage'] = True
                    if acc['billing_wait_seconds']+60 <= self.b.get('billing_wait_seconds', 0):
                        self.sleep(60); acc['billing_wait_seconds'] += 60
                        continue
                    raise CallFailure('billing_outage', acc) from None
                raise CallFailure('http_'+str(exc.code), acc) from None
            except Exception as exc: raise CallFailure('transport_'+type(exc).__name__, acc) from None
        acc['latency_seconds'] = time.monotonic()-t
        if not isinstance(data, dict): raise CallFailure('invalid_provider_response', acc)
        usage = data.get('usage', {})
        if not isinstance(usage, dict) or not all(type(usage.get(k)) is int and usage[k] >= 0 for k in ('input_tokens', 'output_tokens')): raise CallFailure('missing_usage', acc)
        if usage.get('cache_creation_input_tokens', 0) or usage.get('cache_read_input_tokens', 0): raise CallFailure('unexpected_cache_usage', acc)
        actual = usage['input_tokens']*self.b['input_usd_per_million'] + usage['output_tokens']*self.b['output_usd_per_million']
        self.ledger.transact({'type': 'response', 'call_id': call_id, 'actual_micro_usd': actual, **usage})
        acc.update(usage_reported=True, actual_usd=actual/1e6, input_tokens=usage['input_tokens'], output_tokens=usage['output_tokens'])
        acc['stop_reason'] = data.get('stop_reason')
        details = data.get('stop_details')
        if isinstance(details, dict):
            acc['stop_detail_keys'] = sorted(details)
            for key in ('type', 'category', 'reason'):
                if isinstance(details.get(key), str): acc['stop_'+key] = details[key][:160]
        if actual > reserve: raise CallFailure('reservation_bound_breached', acc)
        content = data.get('content', [])
        acc['content_types'] = [c.get('type') if isinstance(c,dict) else 'invalid_block' for c in content] if isinstance(content,list) else []
        # A refusal can contain no text or partial text. Retain its category and
        # accounting before shape validation; never interpret it as an action.
        if data.get('stop_reason') == 'refusal':
            texts = [c.get('text','') for c in content if isinstance(c,dict) and c.get('type')=='text'] if isinstance(content,list) else []
            acc['response_text'] = '\n'.join(t for t in texts if isinstance(t,str))[:8192]
            raise CallFailure('provider_refusal', acc)
        details = usage.get('output_tokens_details')
        if isinstance(details, dict) and type(details.get('thinking_tokens')) is int: acc['thinking_tokens'] = details['thinking_tokens']
        # Adaptive thinking may precede the answer. Count thinking blocks; never retain their content.
        if not isinstance(content, list) or not all(isinstance(c,dict) for c in content): raise CallFailure('unexpected_content', acc)
        texts = [c for c in content if c.get('type') == 'text']
        acc['thinking_blocks'] = sum(c.get('type') in ('thinking','redacted_thinking') for c in content)
        if len(texts) != 1 or content[-1] is not texts[0] or acc['thinking_blocks'] != len(content)-1: raise CallFailure('unexpected_content', acc)
        acc['response_text'] = str(texts[0].get('text', ''))[:8192]
        if data.get('model') != self.d['model']: raise CallFailure('model_mismatch', acc)
        if data.get('stop_reason') != 'end_turn': raise CallFailure('nonterminal_output', acc)
        # Preserve task-only generated text when a response is rejected; never HTTP headers or errors.
        try: answer = json.loads(acc['response_text'])
        except Exception: raise CallFailure('invalid_structured_json', acc) from None
        if not isinstance(answer, dict) or set(answer) != {'action', 'message'} or not isinstance(answer['message'], str): raise CallFailure('invalid_structured_schema', acc)
        if answer['action'] not in packet['actions']: raise CallFailure('invalid_action', acc)
        del acc['response_text']
        return answer, acc

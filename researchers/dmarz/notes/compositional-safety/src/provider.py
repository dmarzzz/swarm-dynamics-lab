"""Bounded native Messages adapter with durable nonrefundable reservations.

Pattern adapted from the lab's market-split-api provider. No automatic model retries.
"""
import fcntl
import json
import os
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
                if sum(e['micro_usd'] for e in reserves)+event['micro_usd'] > budget['study_reserved_usd']*1e6: raise CallFailure('study_reservation_cap')
            if event:
                f.seek(0, 2); f.write(json.dumps(event, sort_keys=True)+'\n'); f.flush(); os.fsync(f.fileno()); events.append(event)
            return {'attempted_calls': sum(e['type']=='reserve' for e in events),
                    'reserved_usd': sum(e.get('micro_usd', 0) for e in events if e['type']=='reserve')/1e6,
                    'actual_usd': sum(e.get('actual_micro_usd', 0) for e in events if e['type']=='response')/1e6,
                    'usage_reported_calls': sum(e['type']=='response' for e in events)}

class Anthropic:
    def __init__(self, ledger, opener=None, key=None, workspace=None):
        self.ledger = ledger; self.opener = opener or urllib.request.urlopen
        self.d = common.design(); self.b = self.d['budget']
        self.key = key or os.environ.get('SWARM_MODEL_API_KEY')
        self.workspace = workspace or os.environ.get('SWARM_MODEL_WORKSPACE_ID')
        if not self.key or not self.workspace: raise CallFailure('missing_credential_alias')

    def call(self, packet, call_id):
        schema = {**SCHEMA, 'properties': {**SCHEMA['properties'], 'action': {'type': 'string', 'enum': packet['actions']}}}
        body = {'model': self.d['model'], 'max_tokens': self.b['max_output_tokens'], 'temperature': 0,
                'system': SYSTEM, 'messages': [{'role': 'user', 'content': json.dumps(packet, sort_keys=True)}],
                'output_config': {'format': {'type': 'json_schema', 'schema': schema}}}
        encoded = json.dumps(body).encode()
        if len(encoded) > self.b['max_input_bytes']: raise CallFailure('input_size_limit')
        reserve = (len(encoded)+4096)*self.b['input_usd_per_million'] + self.b['max_output_tokens']*self.b['output_usd_per_million']
        acc = {'attempted': False, 'usage_reported': False, 'reserved_usd': reserve/1e6}
        self.ledger.transact({'type': 'reserve', 'call_id': call_id, 'micro_usd': reserve, 'time': time.time()}); acc['attempted'] = True
        headers = {'Content-Type': 'application/json', 'x-api-key': self.key, 'anthropic-version': '2023-06-01', 'anthropic-workspace-id': self.workspace}
        req = urllib.request.Request('https://api.anthropic.com/v1/messages', data=encoded, headers=headers, method='POST')
        t = time.monotonic()
        try:
            with self.opener(req, timeout=self.b['request_timeout_seconds']) as response:
                raw = response.read(2_000_001)
                if len(raw) > 2_000_000: raise ValueError('response_size')
                data = json.loads(raw)
        except urllib.error.HTTPError as exc: raise CallFailure('http_'+str(exc.code), acc) from None
        except Exception as exc: raise CallFailure('transport_'+type(exc).__name__, acc) from None
        acc['latency_seconds'] = time.monotonic()-t
        if not isinstance(data, dict): raise CallFailure('invalid_provider_response', acc)
        usage = data.get('usage', {})
        if not isinstance(usage, dict) or not all(type(usage.get(k)) is int and usage[k] >= 0 for k in ('input_tokens', 'output_tokens')): raise CallFailure('missing_usage', acc)
        if usage.get('cache_creation_input_tokens', 0) or usage.get('cache_read_input_tokens', 0): raise CallFailure('unexpected_cache_usage', acc)
        actual = usage['input_tokens']*self.b['input_usd_per_million'] + usage['output_tokens']*self.b['output_usd_per_million']
        self.ledger.transact({'type': 'response', 'call_id': call_id, 'actual_micro_usd': actual, **usage})
        acc.update(usage_reported=True, actual_usd=actual/1e6, input_tokens=usage['input_tokens'], output_tokens=usage['output_tokens'])
        if actual > reserve: raise CallFailure('reservation_bound_breached', acc)
        content = data.get('content', [])
        if not isinstance(content, list) or len(content) != 1 or not isinstance(content[0],dict) or content[0].get('type') != 'text': raise CallFailure('unexpected_content', acc)
        acc['response_text'] = str(content[0].get('text', ''))[:8192]
        if data.get('model') != self.d['model']: raise CallFailure('model_mismatch', acc)
        if data.get('stop_reason') != 'end_turn': raise CallFailure('nonterminal_output', acc)
        # Preserve task-only generated text when a response is rejected; never HTTP headers or errors.
        try: answer = json.loads(acc['response_text'])
        except Exception: raise CallFailure('invalid_structured_json', acc) from None
        if not isinstance(answer, dict) or set(answer) != {'action', 'message'} or not isinstance(answer['message'], str): raise CallFailure('invalid_structured_schema', acc)
        if answer['action'] not in packet['actions']: raise CallFailure('invalid_action', acc)
        del acc['response_text']
        return answer, acc

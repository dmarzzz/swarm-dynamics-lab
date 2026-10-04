"""v2.1 response format: claims as an object keyed by fact, plus a single-agent rule-application probe.

Why: in v2, 7 of 10 invalid episodes listed the contested fact twice (one entry per conflicting value) and 3 used
claims with no sources. Keying claims by fact lets the response schema itself allow one value per fact, and
`minItems: 1` requires a source. The simulator still receives the list form it validates, so scoring is unchanged.

`AnthropicKeyed.complete` mirrors `providers.Anthropic.complete` at 8e8e7f6 (accounting, caps, error mapping)
and differs only in the system prompt, the claims schema and decoding. It lives in its own module so the shared
providers.py, which another agent is refactoring, is untouched; fold it in once that refactor lands.
"""
from __future__ import annotations
import json
import urllib.error
import urllib.request
from providers import Anthropic, ProviderFailure, SYSTEM, phase_schema

SYSTEM_KEYED = SYSTEM.replace(
    '"claims":[{"key":"A.field", "value":integer, "sources":[document IDs]}]}. State factual records you endorse; do not duplicate a key.',
    '"claims":{"A.field":{"value":integer, "sources":[document IDs]}}}. One entry per fact key with a single value; cite at least one source; omit facts you cannot cite. If sources disagree, endorse the one value you judge correct and say why in the message.'
).replace('"claims":[same claim schema]}', '"claims":{same keyed claim object}}')
assert SYSTEM_KEYED != SYSTEM, 'prompt anchor moved; update SYSTEM_KEYED'

def keyed_claims_schema(context):
    task = (context or {}).get('task', {})
    source = {'type': 'string'}
    if task.get('catalog'): source['enum'] = sorted(d['id'] for d in task['catalog'])
    entry = {'type': 'object', 'properties': {'value': {'type': 'integer'}, 'sources': {'type': 'array', 'items': source, 'minItems': 1}},
             'required': ['value', 'sources'], 'additionalProperties': False}
    return {'type': 'object', 'properties': {k: entry for k in sorted(task.get('fact_keys', []))}, 'required': [], 'additionalProperties': False}

def keyed_schema(phase, context):
    schema = phase_schema(phase, context)
    if 'claims' in schema.get('properties', {}): schema['properties']['claims'] = keyed_claims_schema(context)
    return schema

def unkey_claims(response):
    """Keyed object -> list form. Malformed entries pass through so the simulator's validator rejects them."""
    if isinstance(response, dict) and isinstance(response.get('claims'), dict):
        response = {**response, 'claims': [{'key': k, **v} if isinstance(v, dict) else {'key': k, 'value': v, 'sources': []}
                                           for k, v in sorted(response['claims'].items())]}
    return response


class AnthropicKeyed(Anthropic):
    claims_format = 'keyed'

    def complete(self, request):
        if self.calls >= self.max_calls: raise ProviderFailure('call budget exhausted')
        content = json.dumps(request, sort_keys=True)
        if len(content.encode()) > self.max_input_bytes: raise ProviderFailure('input byte budget exceeded')
        body = {'model': self.model, 'system': SYSTEM_KEYED, 'messages': [{'role': 'user', 'content': content}],
                'temperature': 0, 'max_tokens': self.max_output_tokens,
                'output_config': {'format': {'type': 'json_schema', 'schema': keyed_schema(request['phase'], request['context'])}}}
        encoded = json.dumps(body).encode()
        reservation = ((len(encoded) + 512) * self.input_rate + self.max_output_tokens * self.output_rate) / 1_000_000
        if self.reserved_usd + reservation > self.max_cost_usd: raise ProviderFailure('dollar reservation exhausted')
        headers = {'Content-Type': 'application/json', 'x-api-key': self.key, 'anthropic-version': '2023-06-01'}
        if self.workspace: headers['anthropic-workspace-id'] = self.workspace
        req = urllib.request.Request(self.base + '/messages', data=encoded, headers=headers)
        self.reserved_usd += reservation; self.calls += 1; self.usage_missing_calls += 1
        self.last_usage = {}
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r: raw = r.read(2_000_001)
            if len(raw) > 2_000_000: raise ProviderFailure('response too large')
            response = json.loads(raw); usage = response.get('usage', {})
            self.last_usage = {k: v for k, v in usage.items() if k in ('input_tokens', 'output_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens') and type(v) is int and v >= 0}
            if all(k in self.last_usage for k in ('input_tokens', 'output_tokens')):
                if any(self.last_usage.get(k, 0) for k in ('cache_creation_input_tokens', 'cache_read_input_tokens')):
                    raise ProviderFailure('unexpected cached usage; accounting requires review')
                self.actual_cost_usd += (self.last_usage['input_tokens'] * self.input_rate + self.last_usage['output_tokens'] * self.output_rate) / 1_000_000
                self.input_tokens += self.last_usage['input_tokens']; self.output_tokens += self.last_usage['output_tokens']
                self.usage_missing_calls -= 1
            if response.get('stop_reason') != 'end_turn': raise ProviderFailure('incomplete response')
            blocks = response['content']
            if len(blocks) != 1 or blocks[0].get('type') != 'text': raise ProviderFailure('unexpected response blocks')
            return unkey_claims(json.loads(blocks[0]['text']))
        except urllib.error.HTTPError as e:
            reason = 'provider_http_' + str(e.code)
            try:
                error = json.loads(e.read(16384)).get('error', {})
                if e.code == 400 and 'credit balance is too low' in error.get('message', '').lower(): reason = 'provider_credit_balance_low'
            except Exception: pass
            raise ProviderFailure(f'provider HTTP {e.code}', public_reason=reason) from None
        except ProviderFailure: raise
        except Exception as e: raise ProviderFailure('provider ' + type(e).__name__) from None

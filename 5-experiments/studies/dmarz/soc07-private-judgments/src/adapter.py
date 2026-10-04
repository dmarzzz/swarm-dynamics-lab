"""The one provider boundary. Everything a model reads or writes crosses complete().

complete(call) never raises for an expected failure. It returns
  {'ok', 'text', 'failure', 'usage', 'billing', 'latency', 'attempts', 'stop_reason'}
where billing is 'billed' (usage reported), 'none' (the provider rejected the request, nothing
billed) or 'unknown' (no usable response; the caller keeps the full reservation).

AnthropicAdapter: native Messages API, standard library only; same contract as the owned
sybil-scale-api and discussion-dose adapters. No SDK, no tools, no thinking, no prompt caching,
no model fallback, no repair call. Transport retry is limited to HTTP 429 and 529, where the
provider states that the model did not run (execution.json "retry"). Credentials come from the
environment aliases only and never enter a record, a log line or an exception message.
"""
import json
import os
import socket
import time
import urllib.error
import urllib.request

import config
import parse


def _result(ok, text=None, failure=None, usage=None, billing='none', latency=0.0, attempts=0, stop_reason=None):
    return {'ok': ok, 'text': text, 'failure': failure, 'usage': usage or {}, 'billing': billing,
            'latency': latency, 'attempts': attempts, 'stop_reason': stop_reason}


class AnthropicAdapter:
    name = 'anthropic'
    scripted = False

    def __init__(self, on_attempt, opener=None, sleep=time.sleep, clock=time.monotonic):
        """on_attempt(call_id): called before every transport attempt; raises to refuse it."""
        ex = config.execution()
        self.provider, self.limits, self.retry = ex['provider'], ex['limits'], ex['retry']
        self.launch = config.launch_manifest()
        self.model = self.launch['model']
        self.thinking = config.thinking_budget()
        self.key = os.environ.get('SWARM_MODEL_API_KEY', '')
        self.workspace = os.environ.get('SWARM_MODEL_WORKSPACE_ID', '')
        if not self.key:
            raise RuntimeError('missing_credential_alias')
        self.on_attempt = on_attempt
        self.opener = opener or urllib.request.urlopen
        self.sleep, self.clock = sleep, clock

    def body(self, call):
        body = {'model': self.model, 'max_tokens': call['max_tokens'], 'system': call['system'],
                'messages': call['messages'],
                'output_config': {'format': {'type': 'json_schema', 'schema': parse.SCHEMAS[call['schema']]}}}
        if self.thinking and config.thinking_mode() == 'adaptive':
            # Models that only reason adaptively (amendment A6): no budget field and no temperature are accepted;
            # the effort level is sent and the allowance only widens max_tokens.
            body['thinking'] = {'type': 'adaptive'}
            body['output_config']['effort'] = self.launch['thinking']['effort']
        elif self.thinking:
            # A bounded reasoning allowance; the API takes no temperature with thinking enabled.
            body['thinking'] = {'type': 'enabled', 'budget_tokens': self.thinking}
        else:
            body['temperature'] = self.launch['temperature']
        return body

    def complete(self, call):
        encoded = json.dumps(self.body(call)).encode()
        headers = {'Content-Type': 'application/json', 'x-api-key': self.key,
                   'anthropic-version': self.provider['api_version']}
        if self.workspace:
            headers['anthropic-workspace-id'] = self.workspace
        started = self.clock()
        deadline = started + self.limits['request_timeout_seconds']
        attempts, backoff = 0, list(self.retry['backoff_seconds'])
        while True:
            remaining = deadline - self.clock()
            if remaining <= 0.5:
                return _result(False, failure='timeout', billing='none', latency=self.clock() - started, attempts=attempts)
            try:
                self.on_attempt(call['call_id'])
            except Exception as exc:
                return _result(False, failure=getattr(exc, 'category', 'attempt_refused'),
                               latency=self.clock() - started, attempts=attempts)
            attempts += 1
            request = urllib.request.Request(self.provider['endpoint'], data=encoded, headers=headers, method='POST')
            try:
                with self.opener(request, timeout=remaining) as response:
                    raw = response.read(2000001)
            except urllib.error.HTTPError as exc:
                code = exc.code
                retry_after = None
                try:
                    retry_after = float(exc.headers.get('retry-after')) if exc.headers else None
                except (TypeError, ValueError):
                    retry_after = None
                category = 'http_%d' % code
                try:
                    message = json.loads(exc.read(16384)).get('error', {}).get('message', '')
                    if code == 400 and 'credit balance is too low' in message.lower():
                        category = 'credit_balance_low'
                except Exception:
                    pass
                if code in self.retry['retryable_http_status'] and attempts <= self.retry['transport_retries']:
                    wait = backoff[min(attempts - 1, len(backoff) - 1)]
                    if retry_after is not None:
                        wait = max(wait, min(retry_after, self.retry['retry_after_cap_seconds']))
                    if self.clock() + wait < deadline - 1:
                        self.sleep(wait)
                        continue
                return _result(False, failure=category, billing='none', latency=self.clock() - started, attempts=attempts)
            except (socket.timeout, TimeoutError):
                return _result(False, failure='timeout', billing='unknown', latency=self.clock() - started, attempts=attempts)
            except urllib.error.URLError as exc:
                timed_out = isinstance(getattr(exc, 'reason', None), (socket.timeout, TimeoutError))
                return _result(False, failure='timeout' if timed_out else 'transport_error', billing='unknown',
                               latency=self.clock() - started, attempts=attempts)
            except Exception as exc:
                return _result(False, failure='transport_' + type(exc).__name__, billing='unknown',
                               latency=self.clock() - started, attempts=attempts)
            latency = self.clock() - started
            if len(raw) > 2000000:
                return _result(False, failure='response_too_large', billing='unknown', latency=latency, attempts=attempts)
            try:
                data = json.loads(raw)
            except ValueError:
                return _result(False, failure='malformed_provider_response', billing='unknown', latency=latency, attempts=attempts)
            reported = data.get('usage') or {}
            if not all(type(reported.get(k)) is int and reported[k] >= 0 for k in ('input_tokens', 'output_tokens')):
                return _result(False, failure='missing_usage', billing='unknown', latency=latency, attempts=attempts)
            usage = {'input_tokens': reported['input_tokens'], 'output_tokens': reported['output_tokens']}
            base = dict(usage=usage, billing='billed', latency=latency, attempts=attempts,
                        stop_reason=data.get('stop_reason'))
            if reported.get('cache_creation_input_tokens') or reported.get('cache_read_input_tokens'):
                return _result(False, failure='unexpected_cache_usage', **base)
            if data.get('model') != self.model:
                return _result(False, failure='model_mismatch', **base)
            if latency > self.limits['request_timeout_seconds']:
                return _result(False, failure='timeout', **base)
            content = data.get('content') or []
            if self.thinking:   # reasoning blocks are billed output but are never an answer and are not stored
                content = [b for b in content if b.get('type') not in ('thinking', 'redacted_thinking')]
            single = len(content) == 1 and content[0].get('type') == 'text' and isinstance(content[0].get('text'), str)
            text = content[0]['text'] if single else None    # kept for the journal even when the call fails
            stop = data.get('stop_reason')
            if stop == 'max_tokens':
                return _result(False, text=text, failure='truncated', **base)
            if stop == 'refusal':
                return _result(False, text=text, failure='refusal', **base)
            if stop != 'end_turn':
                return _result(False, text=text, failure='stop_' + str(stop), **base)
            if not single:
                return _result(False, failure='unexpected_content_blocks', **base)
            return _result(True, text=text, **base)


class ScriptedAdapter:
    """Offline policies for S0 and tests. Zero model calls. A policy reads only the same rendered
    request a model would receive; 'always_correct' also receives an oracle from the test fixture.
    faults: {call_id: fault} injects 'invalid', 'timeout', 'truncated', 'refusal', 'http_500' or 'crash'."""
    name = 'scripted'
    scripted = True

    def __init__(self, policy_name, oracle=None, faults=None, on_attempt=None):
        import policy
        self.policy = policy.POLICIES[policy_name]
        self.policy_name, self.oracle, self.faults = policy_name, oracle, dict(faults or {})
        self.on_attempt = on_attempt
        self.seen = []

    def complete(self, call):
        if self.on_attempt:
            try:
                self.on_attempt(call['call_id'])
            except Exception as exc:
                return _result(False, failure=getattr(exc, 'category', 'attempt_refused'))
        self.seen.append(call['call_id'])
        fault = self.faults.get(call['call_id'])
        if fault == 'crash':
            raise KeyboardInterrupt('injected controller crash')
        if fault == 'timeout':
            return _result(False, failure='timeout', billing='unknown', latency=60.0, attempts=1)
        if fault in ('http_500', 'http_401'):
            return _result(False, failure=fault, billing='none', attempts=1)
        text = self.policy(call, self.oracle(call) if self.oracle else None)
        size = len(json.dumps([call['system'], call['messages']]).encode())
        usage = {'input_tokens': size // 4, 'output_tokens': max(1, len(text) // 4)}
        base = dict(usage=usage, billing='billed', latency=0.0, attempts=1)
        if fault in ('truncated', 'refusal'):
            return _result(False, failure=fault, stop_reason='max_tokens' if fault == 'truncated' else 'refusal', **base)
        if fault == 'invalid':
            text = 'MALFORMED-OUTPUT ' + text[:-1]  # not JSON; the marker must never reach a peer
        if fault == 'out_of_range':
            data = json.loads(text)
            if 'confidence' in data:
                data['confidence'] = 70
            text = json.dumps(data)
        return _result(True, text=text, stop_reason='end_turn', **base)

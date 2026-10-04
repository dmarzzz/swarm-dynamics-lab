"""Reference OpenRouter adapter and study ledger for ready-chain studies (program v5, 2026-10-04).

Copy this file into a study's `src/` (it is then covered by the study's source hash) and pass the
study's frozen configuration to it. It imports nothing from a study. Written by dmarz/pipeline at
dmarz/fleet-monitor's request; tests are in `test_openrouter_provider.py` beside it.

What it guarantees
- The request body is exactly the frozen template of `selected-model.json` plus `messages`:
  `model`, `provider {only, allow_fallbacks: false, require_parameters: true}`,
  `reasoning {enabled: false}`, `max_tokens`, `response_format {type: json_object}`, `messages`.
  Nothing else is ever added. No model fallback, no provider fallback.
- The answer is JSON-object mode with LOCAL validation (the provider gives no schema guarantee):
  the caller passes `validate(obj)`, which returns the accepted answer or raises.
- No answer is ever retried. A request is re-sent only when the provider rejected it before the
  model ran: HTTP 429 and overload statuses (502, 503, 529), at most twice, backoff 2 s then 6 s,
  `retry-after` honoured up to 20 s, all inside the one request timeout.
- A billing or limit stop is not a model failure: HTTP 402, or a 400/403/429 whose body names
  credit, balance, billing, a usage or spend limit, an exceeded limit or insufficient funds, pauses dispatch for every thread using this adapter, re-sends the same call every 60 s
  for up to 20 minutes, and then stops with category `provider_credit_balance_low`.
- Every failed request keeps its HTTP status, the first 2,000 characters of the response body and
  the request id. Request headers and the key are never stored.
- There is no token-counting endpoint on this route. The reservation is a byte-based upper bound:
  input tokens <= bytes of the encoded request body (a token is at least one byte), plus the full
  output limit, at the frozen prices. The ledger settles each call at its actual cost: the cost the
  provider reports when present, otherwise tokens times the frozen prices. Both are recorded.
- The response's model slug must be the requested model or its dated canonical form, and the
  response must name the serving provider and it must be the pinned one. A missing provider field
  or a mismatch is an integrity failure (so a probe cannot pass without the provider being named).
- The per-call reservation carries a wide margin (`reservation_margin`, default 10 times the
  snapshot-price bound), so a provider-reported cost above the snapshot does not stop a stage over
  fractions of a cent. The study dollar cap stays the hard guard.
- A call that a billing stop left unanswered has its reservation voided (no model ran), so it does
  not count against the call caps or the dollar cap and a continuation batch can run it.
- Duplicate keys in the answer's JSON object are rejected (`invalid_json`).

Failure categories (CallFailure.category)
  refusal, empty_answer, truncated_output, invalid_json, invalid_answer, answer_too_long,
  unexpected_reasoning_tokens, missing_usage, input_ceiling_exceeded,
  http_<status>, provider_error_<code>, transport_<ExceptionName>, timeout,
  provider_credit_balance_low, missing_credential_alias, input_size_limit,
  and from the ledger: duplicate_call_refused, stage_call_cap_reached, study_call_cap_reached,
  aggregate_budget_exhausted, attempt_without_reservation, transport_attempt_cap_reached,
  and the integrity failures model_mismatch, provider_missing, provider_mismatch,
  reservation_bound_breached.
`INTEGRITY` lists the categories that must stop dispatch at once; `BILLING_STOP` is the category
after which unfinished units are recorded as not started and may be resumed (`chain.py resume`).
"""
import fcntl
import json
import os
from pathlib import Path
import socket
import threading
import time
import urllib.error
import urllib.request

URL = 'https://openrouter.ai/api/v1/chat/completions'
KEY_ENV = 'SWARM_OPENROUTER_API_KEY'
LEDGER_ENV = 'STUDY_BUDGET_LEDGER'
BODY_KEYS = ('model', 'provider', 'reasoning', 'max_tokens', 'response_format', 'messages')
BILLING_STOP = 'provider_credit_balance_low'
INTEGRITY = ('duplicate_call_refused', 'stage_call_cap_reached', 'study_call_cap_reached',
             'aggregate_budget_exhausted', 'attempt_without_reservation', 'transport_attempt_cap_reached',
             'model_mismatch', 'provider_missing', 'provider_mismatch', 'reservation_bound_breached',
             'missing_credential_alias')
BODY_KEPT = 2000


class CallFailure(Exception):
    def __init__(self, category, accounting=None):
        super().__init__(category)
        self.category, self.accounting = category, accounting or {}


def stage_of(call_id):
    """'q0-001:<unit id>' -> 'Q0'; continuation batches such as 's1-001-r1:<id>' -> 'S1'."""
    return call_id.split(':', 1)[0].split('-', 1)[0].upper()


BILLING_WORDS = ('credit', 'balance', 'billing', 'usage limit', 'spend limit', 'limit exceeded', 'insufficient')


def family_of(call_id):
    """The batch a call belongs to, without a continuation suffix: 's1-001-r2:<id>' -> 's1-001'.
    Per-stage call caps apply per family, so a repair attempt ('q0-002') has its own allowance while a
    continuation after a billing stop shares the allowance of the batch it continues."""
    import re
    return re.sub(r'-r\d+$', '', call_id.split(':', 1)[0])


def is_billing_error(status, body):
    """A provider-side billing or limit stop, never a model failure: HTTP 402 always, and an HTTP
    400, 403 or 429 whose body names credit, balance, billing, a usage or spend limit, an exceeded
    limit or insufficient funds (case-insensitive). A 429 without such words is ordinary rate
    limiting and goes through the transport retry rule."""
    text = (body or '').lower()
    return status == 402 or (status in (400, 403, 429) and any(word in text for word in BILLING_WORDS))


class Ledger:
    """One append-only ledger for the whole study, shared by every stage, thread and process.

    An exclusive file lock spans each read, check, append and fsync; a line that does not parse makes
    every later transaction fail closed. Refuses: a call id seen before; a reservation beyond the
    stage's `max_calls` (counted per batch family, see `family_of`), the study's `max_attempted_calls` or the dollar cap (settled actual cost of
    answered calls plus the full reservation of every call without reported usage); an HTTP attempt
    without a reservation or beyond `max_transport_attempts`."""

    def __init__(self, path, budget):
        self.path, self.budget = Path(path), budget
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        self._lock = threading.Lock()

    def transact(self, event=None):
        b = self.budget
        with self._lock, self.path.open('a+', encoding='utf-8') as f:
            os.chmod(self.path, 0o600)
            fcntl.flock(f, fcntl.LOCK_EX)
            f.seek(0)
            events = [json.loads(line) for line in f if line.strip()]
            voided = {e['call_id'] for e in events if e['type'] == 'void'}
            seen = {e['call_id'] for e in events if e['type'] == 'reserve'}
            reserved = {e['call_id']: e['micro_usd'] for e in events if e['type'] == 'reserve' and e['call_id'] not in voided}
            settled = {e['call_id']: e['actual_micro_usd'] for e in events if e['type'] == 'response'}
            attempts = sum(e['type'] == 'attempt' for e in events)
            by_stage = {}; by_family = {}
            for call in reserved:
                by_stage[stage_of(call)] = by_stage.get(stage_of(call), 0) + 1
                by_family[family_of(call)] = by_family.get(family_of(call), 0) + 1
            committed = sum(settled.get(call, amount) for call, amount in reserved.items())
            if event:
                kind = event['type']
                if kind == 'reserve':
                    call = event['call_id']; stage = stage_of(call)
                    if call in seen: raise CallFailure('duplicate_call_refused')
                    if by_family.get(family_of(call), 0) >= b['max_calls'].get(stage, 0): raise CallFailure('stage_call_cap_reached')
                    if len(reserved) >= b['max_attempted_calls']: raise CallFailure('study_call_cap_reached')
                    if committed + event['micro_usd'] > int(b['aggregate_usd'] * 1_000_000):
                        raise CallFailure('aggregate_budget_exhausted')
                    reserved[call] = event['micro_usd']; by_stage[stage] = by_stage.get(stage, 0) + 1
                    by_family[family_of(call)] = by_family.get(family_of(call), 0) + 1
                elif kind == 'attempt':
                    if event['call_id'] not in reserved: raise CallFailure('attempt_without_reservation')
                    if attempts >= b['max_transport_attempts']: raise CallFailure('transport_attempt_cap_reached')
                    attempts += 1
                elif kind == 'response':
                    settled[event['call_id']] = event['actual_micro_usd']
                elif kind == 'void':
                    # Only a reserved call that never reported usage can be voided (a billing stop: no model ran).
                    if event['call_id'] not in reserved or event['call_id'] in settled: raise CallFailure('void_refused')
                    stage = stage_of(event['call_id']); by_stage[stage] -= 1; by_family[family_of(event['call_id'])] -= 1
                    del reserved[event['call_id']]; voided.add(event['call_id'])
                else:
                    raise CallFailure('unknown_ledger_event')
                f.seek(0, 2); f.write(json.dumps(event, sort_keys=True) + '\n'); f.flush(); os.fsync(f.fileno())
                events.append(event)
                committed = sum(settled.get(call, amount) for call, amount in reserved.items())
            responses = [e for e in events if e['type'] == 'response']
            return {'attempted_calls': len(reserved), 'calls_by_stage': by_stage, 'calls_by_batch': by_family, 'transport_attempts': attempts,
                    'usage_reported_calls': len(settled), 'voided_calls': len(voided),
                    'reserved_usd': sum(reserved.values()) / 1e6, 'actual_usd': sum(settled.values()) / 1e6,
                    'committed_usd': committed / 1e6,
                    'input_tokens': sum(e.get('input_tokens', 0) for e in responses),
                    'output_tokens': sum(e.get('output_tokens', 0) for e in responses),
                    'cap_usd': b['aggregate_usd'], 'cap_calls': b['max_attempted_calls'],
                    'cap_transport_attempts': b['max_transport_attempts']}


class _HttpFailure(Exception):
    def __init__(self, status, body, request_id, retry_after):
        super().__init__(status)
        self.status, self.body, self.request_id, self.retry_after = status, body, request_id, retry_after


class OpenRouter:
    """config: {'model', 'canonical_model' (optional dated slug), 'provider' (pinned, lower case),
    'request_template' (the frozen template), 'budget' {...}}. See the module docstring and the test
    file's CONFIG for every budget key. One instance is shared by all threads of a stage: the
    billing pause is stage-wide."""

    def __init__(self, ledger, config, opener=None, clock=time.monotonic, sleep=time.sleep):
        self.ledger, self.c, self.b = ledger, config, config['budget']
        self.opener = opener or urllib.request.urlopen
        self.clock, self.sleep = clock, sleep
        self.key = os.environ.get(KEY_ENV)
        if not self.key:
            raise CallFailure('missing_credential_alias')
        self._state = threading.Lock()
        self._resumed = threading.Event(); self._resumed.set()
        self._paused = False; self._stopped = False
        self.billing = {'billing_pauses': 0, 'billing_pause_seconds': 0.0, 'billing_affected_calls': 0}

    # ------------------------------------------------------------------ request
    def headers(self):
        return {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.key}

    def body(self, system, user):
        """The frozen template plus the two messages. Nothing else is ever added."""
        t = self.c['request_template']
        body = {'model': t['model'], 'provider': dict(t['provider']), 'reasoning': dict(t['reasoning']),
                'max_tokens': t['max_tokens'], 'response_format': dict(t['response_format']),
                'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}]}
        assert tuple(body) == BODY_KEYS and body['model'] == self.c['model']
        assert body['provider'].get('allow_fallbacks') is False and body['provider'].get('require_parameters') is True
        assert body['reasoning'] == {'enabled': False} and body['max_tokens'] == self.b['max_output_tokens']
        return body

    def _send(self, encoded, timeout):
        request = urllib.request.Request(URL, data=encoded, headers=self.headers(), method='POST')
        try:
            with self.opener(request, timeout=timeout) as response:
                raw = response.read()
        except urllib.error.HTTPError as exc:
            try: text = exc.read().decode('utf-8', 'replace')[:BODY_KEPT]
            except Exception: text = ''
            headers = exc.headers or {}
            try: after = float(headers.get('retry-after'))
            except (TypeError, ValueError): after = None
            rid = headers.get('x-request-id') or headers.get('request-id')
            try: exc.close()
            except Exception: pass
            raise _HttpFailure(exc.code, text, rid, after) from None
        return raw

    def _post(self, encoded, account, on_attempt):
        """One logical request under the transport retry rule and the billing-outage rule.
        Returns the parsed response. Raises CallFailure with the evidence in `account`."""
        retry, outage = self.b['retry'], self.b['billing_outage']
        backoff = list(retry['backoff_seconds'])
        deadline = self.clock() + self.b['request_timeout_seconds']
        tries = 0                     # attempts of the ordinary retry rule (billing re-sends not counted)
        owner = False; pause_started = None
        while True:
            if not owner and self._wait_while_paused(account):
                deadline = self.clock() + self.b['request_timeout_seconds']   # time spent paused is not request time
            remaining = deadline - self.clock()
            if remaining <= 0.5 and not owner:
                raise CallFailure('timeout', account)
            on_attempt()
            tries += 1
            try:
                raw = self._send(encoded, max(remaining, 30.0) if owner else remaining)
                try:
                    data = json.loads(raw)
                except Exception:
                    data = None
                if isinstance(data, dict) and isinstance(data.get('error'), dict) and not data.get('choices'):
                    # OpenRouter can answer 200 with an error object; treat it as the status it names.
                    err = data['error']
                    code = err.get('code') if type(err.get('code')) is int else 200
                    raise _HttpFailure(code, json.dumps(err)[:BODY_KEPT], None, None)
            except _HttpFailure as exc:
                account.update(http_status=exc.status, error_body=exc.body, request_id=exc.request_id)
                if is_billing_error(exc.status, exc.body):
                    tries -= 1                               # a billing re-send is not a transport retry
                    if not owner:
                        owner = self._begin_pause(account)
                        if not owner:
                            continue                         # another call owns the pause: wait, then re-send
                        pause_started = self.clock()
                    if self.clock() - pause_started >= outage['max_wait_seconds']:
                        self._end_pause(pause_started, stopped=True)
                        raise CallFailure(BILLING_STOP, account) from None
                    self.sleep(outage['retry_every_seconds'])
                    continue
                if owner:
                    self._end_pause(pause_started, stopped=False); owner = False
                if exc.status in retry['retryable_http_status'] and tries <= retry['transport_retries']:
                    wait = backoff[min(tries - 1, len(backoff) - 1)]
                    if exc.retry_after is not None:
                        wait = max(wait, min(exc.retry_after, retry['retry_after_cap_seconds']))
                    if self.clock() + wait < deadline - 1:
                        self.sleep(wait)
                        continue
                raise CallFailure(('http_' if exc.status != 200 else 'provider_error_') + str(exc.status), account) from None
            except (socket.timeout, TimeoutError):
                if owner: self._end_pause(pause_started, stopped=False)
                raise CallFailure('timeout', account) from None
            except urllib.error.URLError as exc:
                if owner: self._end_pause(pause_started, stopped=False)
                timed_out = isinstance(getattr(exc, 'reason', None), (socket.timeout, TimeoutError))
                raise CallFailure('timeout' if timed_out else 'transport_URLError', account) from None
            except CallFailure:
                if owner: self._end_pause(pause_started, stopped=False)
                raise
            except Exception as exc:
                if owner: self._end_pause(pause_started, stopped=False)
                raise CallFailure('transport_' + type(exc).__name__, account) from None
            if owner:
                self._end_pause(pause_started, stopped=False)
            if not isinstance(data, dict):
                account.update(error_body=raw[:BODY_KEPT].decode('utf-8', 'replace') if isinstance(raw, bytes) else str(raw)[:BODY_KEPT])
                raise CallFailure('malformed_provider_response', account)
            for key in ('http_status', 'error_body', 'request_id'):
                if key in account: account['earlier_' + key] = account.pop(key)   # evidence of a recovered attempt
            return data

    # ------------------------------------------------------------------ billing pause (stage-wide)
    def _wait_while_paused(self, account):
        """Blocks while another call is riding out a billing outage. Returns True when it waited."""
        waited = False
        while True:
            with self._state:
                if self._stopped:
                    raise CallFailure(BILLING_STOP, account)
                if not self._paused:
                    return waited
            waited = True
            self._resumed.wait(1.0)

    def _begin_pause(self, account):
        """True when this call becomes the one that re-sends during the outage."""
        with self._state:
            self.billing['billing_affected_calls'] += 1
            account['billing_paused'] = True
            if self._paused:
                return False
            self._paused = True; self._resumed.clear()
            self.billing['billing_pauses'] += 1
            return True

    def _end_pause(self, started, stopped):
        with self._state:
            self.billing['billing_pause_seconds'] += max(0.0, self.clock() - started)
            self._paused = False
            self._stopped = self._stopped or stopped
            self._resumed.set()

    def billing_stopped(self):
        with self._state:
            return self._stopped

    # ------------------------------------------------------------------ one call
    def call(self, system, user, call_id, validate):
        """Returns (answer, accounting). `validate(obj)` returns the accepted answer or raises."""
        body = self.body(system, user)
        encoded = json.dumps(body).encode()
        account = {'attempted': False, 'usage_reported': False, 'attempts': 0, 'request_bytes': len(encoded)}
        if self.billing_stopped():
            raise CallFailure(BILLING_STOP, account)
        if len(encoded) > self.b['max_input_bytes']:
            raise CallFailure('input_size_limit', account)
        # Byte-based upper bound: input tokens <= request bytes; the whole output limit priced in full.
        # times a wide margin, because the provider's reported cost may sit above the snapshot prices.
        bound = len(encoded) * self.b['input_usd_per_million'] + self.b['max_output_tokens'] * self.b['output_usd_per_million']
        reserve = int(bound * self.b.get('reservation_margin', 10) + 0.999999)
        account['reserved_usd'] = reserve / 1e6
        try:
            self.ledger.transact({'type': 'reserve', 'call_id': call_id, 'micro_usd': reserve, 'time': time.time()})
        except CallFailure as exc:
            raise CallFailure(exc.category, account) from None
        account['attempted'] = True          # one call, reserved once, however many HTTP attempts follow

        def on_attempt():
            try:
                self.ledger.transact({'type': 'attempt', 'call_id': call_id, 'n': account['attempts'] + 1, 'time': time.time()})
            except CallFailure as exc:
                raise CallFailure(exc.category, account) from None
            account['attempts'] += 1
        started = self.clock()
        try:
            data = self._post(encoded, account, on_attempt)
        except CallFailure as exc:
            if exc.category == BILLING_STOP:
                # No model ran for this call: release its reservation so a continuation can run the unit.
                self.ledger.transact({'type': 'void', 'call_id': call_id, 'time': time.time()})
                account['voided'] = True
            raise
        account['latency_seconds'] = self.clock() - started
        if not isinstance(data, dict):
            raise CallFailure('malformed_provider_response', account)
        usage = data.get('usage') or {}
        tokens_in, tokens_out = usage.get('prompt_tokens'), usage.get('completion_tokens')
        if not (type(tokens_in) is int and type(tokens_out) is int and tokens_in >= 0 and tokens_out >= 0):
            raise CallFailure('missing_usage', account)
        computed = tokens_in * self.b['input_usd_per_million'] + tokens_out * self.b['output_usd_per_million']
        reported = usage.get('cost')
        actual = int(round(reported * 1e6)) if isinstance(reported, (int, float)) and not isinstance(reported, bool) and reported >= 0 else int(computed + 0.999999)
        details = usage.get('completion_tokens_details') or {}
        reasoning = details.get('reasoning_tokens') if isinstance(details, dict) else None
        self.ledger.transact({'type': 'response', 'call_id': call_id, 'actual_micro_usd': actual,
                              'input_tokens': tokens_in, 'output_tokens': tokens_out})
        account.update(usage_reported=True, actual_usd=actual / 1e6, computed_usd=computed / 1e6,
                       provider_reported_usd=reported if isinstance(reported, (int, float)) and not isinstance(reported, bool) else None,
                       input_tokens=tokens_in, output_tokens=tokens_out, reasoning_tokens=reasoning,
                       response_model=data.get('model'), response_provider=data.get('provider'), response_id=data.get('id'))
        # Nothing below is retried: the model ran and usage was reported.
        if actual > reserve:
            raise CallFailure('reservation_bound_breached', account)
        model = data.get('model')
        accepted = {self.c['model'], self.c.get('canonical_model') or self.c['model']}
        if model not in accepted:
            raise CallFailure('model_mismatch', account)
        served = data.get('provider')
        if not isinstance(served, str) or not served.strip():
            raise CallFailure('provider_missing', account)
        if self.c['provider'] not in served.lower():
            raise CallFailure('provider_mismatch', account)
        if tokens_in > self.b['max_input_tokens']:
            raise CallFailure('input_ceiling_exceeded', account)
        if reasoning:
            raise CallFailure('unexpected_reasoning_tokens', account)
        choices = data.get('choices')
        if not isinstance(choices, list) or len(choices) != 1 or not isinstance(choices[0], dict):
            raise CallFailure('empty_answer', account)
        choice = choices[0]; message = choice.get('message') or {}
        finish = choice.get('finish_reason')
        account['finish_reason'] = finish
        if message.get('refusal') or finish == 'content_filter':
            raise CallFailure('refusal', account)
        if finish == 'length':
            raise CallFailure('truncated_output', account)
        text = message.get('content')
        if not isinstance(text, str) or not text.strip():
            raise CallFailure('empty_answer', account)
        if finish != 'stop':
            raise CallFailure('nonterminal_output', account)
        if len(text) > self.b['max_visible_chars']:
            raise CallFailure('answer_too_long', account)
        def no_duplicates(pairs):
            keys = [k for k, _ in pairs]
            if len(set(keys)) != len(keys): raise ValueError('duplicate key')
            return dict(pairs)
        try:
            obj = json.loads(text, object_pairs_hook=no_duplicates)
        except Exception:
            account['answer_text'] = text[:BODY_KEPT]
            raise CallFailure('invalid_json', account) from None
        try:
            answer = validate(obj)
        except Exception:
            account['answer_text'] = text[:BODY_KEPT]
            raise CallFailure('invalid_answer', account) from None
        return answer, account

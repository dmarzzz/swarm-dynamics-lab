"""Reference OpenAI adapter and study ledger for ready-chain studies (2026-10-04).

Copy this file into a study's `src/` (it is then covered by the study's source hash) and pass the
study's frozen configuration to it. It imports nothing from a study. Written by dmarz/openai-route at
dmarz/fleet-monitor's request, from `openrouter_provider.py` (same ledger, reservation, failure and
billing-pause rules); tests are in `test_openai_provider.py` beside it.

Endpoint: OpenAI Chat Completions, https://api.openai.com/v1/chat/completions, `Authorization: Bearer`.

What it guarantees
- The request body is exactly the frozen template plus `messages`: `model`, `reasoning_effort`,
  `max_completion_tokens`, `response_format`, then `temperature` and `top_p` only if the template has
  them, then `messages`. Nothing else is ever added (no `max_tokens`, no tools, no `stream`, no `n`).
  `temperature`/`top_p` are refused unless `reasoning_effort` is `none` on a model that accepts sampling
  parameters there (gpt-6-sol, gpt-6-luna; docs "latest model" guide, 2026-10-04).
- `reasoning_effort` must be one of the values the model's documentation page lists (`REASONING_EFFORTS`).
- `response_format` is `{type: json_object}` (local validation by the caller's `validate(obj)`), or
  `{type: json_schema, json_schema: {name, schema, strict: true}}` when the study supplies a schema.
  Either way the answer is parsed locally, duplicate keys rejected, and passed to `validate(obj)`.
- Usage carries no cost. Cost is COMPUTED from the per-million prices pinned in the study's hashed design
  (`budget.prices`, which must equal this file's `PRICES` row for the model), recorded as
  `cost_source: computed_from_pinned_prices`; `provider_reported_usd` is always None.
  Cached prompt tokens (`prompt_tokens_details.cached_tokens`) are priced at the cached-input price.
  GPT-6 models bill cache writes automatically (prompt-caching guide); if the usage names
  `prompt_tokens_details.cache_write_tokens` those are priced at the cache-write price, and if it does
  not, every uncached prompt token of a prompt of 1,024 tokens or more (the caching minimum) is priced at
  the cache-write price, an upper bound marked `cache_write_upper_bound`.
  `completion_tokens` includes reasoning tokens (they are billed as output and count against
  `max_completion_tokens`); `completion_tokens_details.reasoning_tokens` is recorded.
- Prompts over 272,000 tokens are priced higher by OpenAI; the adapter refuses a budget whose
  `max_input_tokens` exceeds 272,000 (`long_context_not_supported`).
- The response's `model` must be the requested id, the configured `canonical_model`, or its dated form
  `<id>-YYYY-MM-DD`; otherwise `model_mismatch` (integrity). There is no provider routing or check.
- Refusals (`message.refusal` set, or `finish_reason: content_filter`) are category `refusal`;
  `finish_reason: length` is `truncated_output` (reasoning can use up the allowance: the account keeps
  `reasoning_tokens`). With `reasoning_effort: none`, any reasoning token is `unexpected_reasoning_tokens`.
- No answer is ever retried. A request is re-sent only on HTTP 429 (rate limit) and 500/502/503/504, at
  most twice, backoff 2 s then 6 s, `retry-after` honoured up to 20 s, all inside one request timeout.
- A billing or quota stop is not a rate limit: HTTP 402, or a 400/403/429 whose error code or message
  names insufficient_quota, quota, billing, credit, balance, insufficient, a usage limit, a spend limit
  or a hard limit pauses dispatch for every thread using this adapter, re-sends the same call every 60 s
  for up to 20 minutes, and then stops with `provider_billing_stopped` (resumable, see READY-CHAIN.md).
  The call left unanswered has its reservation voided (no model ran).
- Every failed request keeps its HTTP status, the first 2,000 characters of the response body and the
  request id. Request headers and the key are never stored. From a successful response only the numeric
  `x-ratelimit-*` limit/remaining values are kept (LESSONS.md item 10).
- Reservation: input tokens <= bytes of the encoded request body, priced at the higher of the input and
  cache-write prices, plus the full `max_completion_tokens` at the output price, times
  `reservation_margin` (default 10). The ledger settles each call at its computed cost.

Failure categories (CallFailure.category)
  refusal, empty_answer, truncated_output, nonterminal_output, invalid_json, invalid_answer,
  answer_too_long, unexpected_reasoning_tokens, missing_usage, input_ceiling_exceeded,
  output_ceiling_exceeded, malformed_provider_response, http_<status>, provider_error_<code>,
  transport_<ExceptionName>, timeout, provider_billing_stopped, missing_credential_alias,
  input_size_limit, json_mode_prompt_lacks_json,
  and from the ledger: duplicate_call_refused, stage_call_cap_reached, study_call_cap_reached,
  aggregate_budget_exhausted, attempt_without_reservation, transport_attempt_cap_reached,
  and the integrity failures model_mismatch, reservation_bound_breached.
`INTEGRITY` lists the categories that must stop dispatch at once; `BILLING_STOP` is the category
after which unfinished units are recorded as not started and may be resumed (`chain.py resume`).
"""
import fcntl
import json
import os
from pathlib import Path
import re
import socket
import threading
import time
import urllib.error
import urllib.request

URL = 'https://api.openai.com/v1/chat/completions'
KEY_ENV = 'SWARM_OPENAI_API_KEY'
LEDGER_ENV = 'STUDY_BUDGET_LEDGER'
BODY_KEYS = ('model', 'reasoning_effort', 'max_completion_tokens', 'response_format', 'messages')
SAMPLING_KEYS = ('temperature', 'top_p')
BILLING_STOP = 'provider_billing_stopped'
INTEGRITY = ('duplicate_call_refused', 'stage_call_cap_reached', 'study_call_cap_reached',
             'aggregate_budget_exhausted', 'attempt_without_reservation', 'transport_attempt_cap_reached',
             'model_mismatch', 'reservation_bound_breached', 'output_ceiling_exceeded',
             'missing_credential_alias')
BODY_KEPT = 2000
LONG_CONTEXT_TOKENS = 272000       # above this OpenAI charges long-context prices; not supported here
CACHE_MIN_TOKENS = 1024            # prompts shorter than this are never cached (no cache write)

# Standard-tier USD per million tokens, short context (<= 272K prompt tokens).
# Source: https://developers.openai.com/api/docs/pricing and each model page
# (https://developers.openai.com/api/docs/models/<id>), retrieved 2026-10-04T12:10Z by dmarz/openai-route.
# A study copies the row of its model into `budget.prices` of its hashed design.
PRICES = {
    'gpt-6-luna':  {'input': 0.10, 'cached_input': 0.01, 'cache_write': 0.125, 'output': 0.50},
    'gpt-6-sol':   {'input': 2.00, 'cached_input': 0.20, 'cache_write': 2.50,  'output': 10.00},
    'gpt-6.1-sol': {'input': 2.00, 'cached_input': 0.10, 'cache_write': 2.50,  'output': 10.00},
    'gpt-6-astra': {'input': 10.00, 'cached_input': 1.00, 'cache_write': 12.50, 'output': 50.00},
}
PRICES_SOURCE = {'url': 'https://developers.openai.com/api/docs/pricing', 'retrieved': '2026-10-04T12:10Z', 'tier': 'standard'}
# Allowed `reasoning_effort` per model (model pages, 2026-10-04). `minimal` is listed by the generic API
# reference but by none of these model pages; gpt-6.1-sol's page says `none` and `minimal` are unsupported.
REASONING_EFFORTS = {
    'gpt-6-luna':  ('none', 'low', 'medium', 'high', 'xhigh', 'max'),
    'gpt-6-sol':   ('none', 'low', 'medium', 'high', 'xhigh', 'max'),
    'gpt-6.1-sol': ('low', 'medium', 'high', 'xhigh', 'max'),
    'gpt-6-astra': ('low', 'medium', 'high', 'xhigh', 'max'),
}
# Models that accept temperature/top_p, and only with reasoning_effort none ("latest model" guide).
SAMPLING_MODELS = ('gpt-6-sol', 'gpt-6-luna')
BILLING_WORDS = ('insufficient_quota', 'quota', 'billing', 'credit', 'balance', 'insufficient',
                 'usage limit', 'spend limit', 'spending limit', 'hard limit', 'hard_limit')
RATE_HEADERS = ('x-ratelimit-limit-requests', 'x-ratelimit-remaining-requests',
                'x-ratelimit-limit-tokens', 'x-ratelimit-remaining-tokens')


class CallFailure(Exception):
    def __init__(self, category, accounting=None):
        super().__init__(category)
        self.category, self.accounting = category, accounting or {}


def stage_of(call_id):
    """'q0-001:<unit id>' -> 'Q0'; continuation batches such as 's1-001-r1:<id>' -> 'S1'."""
    return call_id.split(':', 1)[0].split('-', 1)[0].upper()


def family_of(call_id):
    """The batch a call belongs to, without a continuation suffix: 's1-001-r2:<id>' -> 's1-001'.
    Per-stage call caps apply per family, so a repair attempt ('q0-002') has its own allowance while a
    continuation after a billing stop shares the allowance of the batch it continues."""
    return re.sub(r'-r\d+$', '', call_id.split(':', 1)[0])


def is_billing_error(status, body):
    """A billing or quota stop, never a model failure and never a rate limit: HTTP 402 always, and an
    HTTP 400, 403 or 429 whose error code or message names insufficient_quota, quota, billing, credit,
    balance, insufficient, a usage, spend or hard limit (case-insensitive). OpenAI reports an exhausted
    quota as 429 `insufficient_quota`; a 429 without such words (e.g. "Rate limit reached ... tokens per
    min") is ordinary rate limiting and goes through the transport retry rule."""
    text = (body or '').lower()
    return status == 402 or (status in (400, 403, 429) and any(word in text for word in BILLING_WORDS))


def check_config(config):
    """Refuse a configuration this adapter cannot price or send exactly. Returns the config."""
    model, t, b = config['model'], config['request_template'], config['budget']
    if model not in PRICES or model not in REASONING_EFFORTS: raise ValueError('model_not_supported')
    if t.get('model') != model: raise ValueError('template_model_differs')
    keys = [k for k in t if k not in SAMPLING_KEYS]
    if keys != [k for k in BODY_KEYS if k != 'messages']: raise ValueError('template_keys')
    if t['reasoning_effort'] not in REASONING_EFFORTS[model]: raise ValueError('reasoning_effort_not_allowed_for_model')
    if any(k in t for k in SAMPLING_KEYS) and not (t['reasoning_effort'] == 'none' and model in SAMPLING_MODELS):
        raise ValueError('sampling_parameters_need_reasoning_effort_none')
    if t['max_completion_tokens'] != b['max_output_tokens']: raise ValueError('max_completion_tokens_differs_from_budget')
    rf = t['response_format']
    if rf == {'type': 'json_object'}:
        pass
    elif rf.get('type') == 'json_schema' and set(rf) == {'type', 'json_schema'}:
        js = rf['json_schema']
        if not (isinstance(js, dict) and set(js) == {'name', 'schema', 'strict'} and js['strict'] is True
                and isinstance(js['schema'], dict) and re.fullmatch(r'[A-Za-z0-9_-]{1,64}', str(js['name']))):
            raise ValueError('json_schema_needs_name_schema_strict_true')
    else:
        raise ValueError('response_format')
    if b['max_input_tokens'] > LONG_CONTEXT_TOKENS: raise ValueError('long_context_not_supported')
    if dict(b['prices']) != PRICES[model]: raise ValueError('prices_differ_from_reference_table')
    return config
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


def _number(value):
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


class OpenAI:
    """config: {'model', 'canonical_model' (optional), 'request_template' (the frozen template),
    'budget' {..., 'prices': PRICES[model]}}. See the module docstring and the test file's CONFIG for every
    budget key. One instance is shared by all threads of a stage: the billing pause is stage-wide."""

    def __init__(self, ledger, config, opener=None, clock=time.monotonic, sleep=time.sleep):
        self.ledger, self.c, self.b = ledger, check_config(config), config['budget']
        self.p = self.b['prices']
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
        body = {'model': t['model'], 'reasoning_effort': t['reasoning_effort'],
                'max_completion_tokens': t['max_completion_tokens'],
                'response_format': json.loads(json.dumps(t['response_format']))}
        for key in SAMPLING_KEYS:
            if key in t: body[key] = t[key]
        body['messages'] = [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}]
        assert [k for k in body if k not in SAMPLING_KEYS] == list(BODY_KEYS) and body['model'] == self.c['model']
        return body

    def _send(self, encoded, timeout):
        request = urllib.request.Request(URL, data=encoded, headers=self.headers(), method='POST')
        try:
            with self.opener(request, timeout=timeout) as response:
                raw = response.read()
                got = getattr(response, 'headers', None) or {}
                limits = {h: _number(got.get(h)) for h in RATE_HEADERS if _number(got.get(h)) is not None}
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
        return raw, limits

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
                raw, limits = self._send(encoded, max(remaining, 30.0) if owner else remaining)
                try:
                    data = json.loads(raw)
                except Exception:
                    data = None
                if isinstance(data, dict) and isinstance(data.get('error'), dict) and not data.get('choices'):
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
            if limits: account['rate_limits'] = limits
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

    # ------------------------------------------------------------------ cost
    def cost_micro_usd(self, usage):
        """Computed cost in micro-dollars (float) and how it was priced. Prices are USD per million tokens,
        so tokens x price is micro-dollars."""
        p = self.p
        prompt, completion = usage['prompt_tokens'], usage['completion_tokens']
        details = usage.get('prompt_tokens_details') or {}
        cached = details.get('cached_tokens') if isinstance(details, dict) else None
        cached = cached if type(cached) is int and 0 <= cached <= prompt else 0
        written = details.get('cache_write_tokens') if isinstance(details, dict) else None
        uncached = prompt - cached
        if type(written) is int and 0 <= written <= uncached:
            basis = 'cache_write_reported'
            cost = (uncached - written) * p['input'] + written * p['cache_write']
        elif prompt >= CACHE_MIN_TOKENS:
            basis = 'cache_write_upper_bound'       # writes not reported: price every uncached token as written
            cost = uncached * max(p['input'], p['cache_write'])
        else:
            basis = 'below_cache_minimum'
            cost = uncached * p['input']
        cost += cached * p['cached_input'] + completion * p['output']
        return cost, {'cached_tokens': cached, 'cache_write_tokens': written if type(written) is int else None, 'input_pricing': basis}

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
        if body['response_format']['type'] == 'json_object' and 'json' not in (system + user).lower():
            raise CallFailure('json_mode_prompt_lacks_json', account)   # the API rejects JSON mode without the word
        # Byte-based upper bound: input tokens <= request bytes at the higher input price; the whole output
        # allowance (visible plus reasoning tokens) at the output price; times the margin.
        p = self.p
        bound = len(encoded) * max(p['input'], p['cache_write']) + self.b['max_output_tokens'] * p['output']
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
        usage = data.get('usage') or {}
        tokens_in, tokens_out = usage.get('prompt_tokens'), usage.get('completion_tokens')
        if not (type(tokens_in) is int and type(tokens_out) is int and tokens_in >= 0 and tokens_out >= 0):
            raise CallFailure('missing_usage', account)
        computed, pricing = self.cost_micro_usd(usage)
        actual = int(computed + 0.999999)
        details = usage.get('completion_tokens_details') or {}
        reasoning = details.get('reasoning_tokens') if isinstance(details, dict) else None
        self.ledger.transact({'type': 'response', 'call_id': call_id, 'actual_micro_usd': actual,
                              'input_tokens': tokens_in, 'output_tokens': tokens_out})
        account.update(usage_reported=True, actual_usd=actual / 1e6, computed_usd=computed / 1e6,
                       cost_source='computed_from_pinned_prices', provider_reported_usd=None,
                       input_tokens=tokens_in, output_tokens=tokens_out, reasoning_tokens=reasoning,
                       visible_output_tokens=tokens_out - reasoning if type(reasoning) is int else None,
                       response_model=data.get('model'), response_id=data.get('id'),
                       system_fingerprint=data.get('system_fingerprint'), **pricing)
        # Nothing below is retried: the model ran and usage was reported.
        if actual > reserve:
            raise CallFailure('reservation_bound_breached', account)
        model = data.get('model')
        dated = isinstance(model, str) and re.fullmatch(re.escape(self.c['model']) + r'-\d{4}-\d{2}-\d{2}', model)
        if model not in {self.c['model'], self.c.get('canonical_model') or self.c['model']} and not dated:
            raise CallFailure('model_mismatch', account)
        if tokens_out > self.b['max_output_tokens']:
            raise CallFailure('output_ceiling_exceeded', account)
        if tokens_in > self.b['max_input_tokens']:
            raise CallFailure('input_ceiling_exceeded', account)
        if reasoning and self.c['request_template']['reasoning_effort'] == 'none':
            raise CallFailure('unexpected_reasoning_tokens', account)
        choices = data.get('choices')
        if not isinstance(choices, list) or len(choices) != 1 or not isinstance(choices[0], dict):
            raise CallFailure('empty_answer', account)
        choice = choices[0]; message = choice.get('message') or {}
        finish = choice.get('finish_reason')
        account['finish_reason'] = finish
        if message.get('refusal') or finish == 'content_filter':
            if isinstance(message.get('refusal'), str): account['refusal_text'] = message['refusal'][:BODY_KEPT]
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

"""Native Messages API adapter for claude-opus-5-5 and the persistent study ledger.

Request rules (ready-chain contract): the body has exactly the keys model, max_tokens, system,
messages and output_config {effort, format}. It never carries thinking, temperature, top_p,
top_k, tool_choice, a prefilled assistant turn or fallbacks. `messages` is one user message: the
state of the current round. Responses carry thinking blocks before the answer; they are dropped
and exactly one text block is required.

No answer is ever retried. Only a request the provider rejected before running the model
(HTTP 429 or 529) is re-sent, at most budget.retry.transport_retries times, inside the one
request time budget. Credentials and request headers never enter a record. The ledger and the
transport rule are those of sybil-split-opus; the prompt, the schema and the per-turn call are
this study's (study.system_prompt, study.SCHEMA).

Failure handling (2026-10-04 rule):
1. A failed HTTP request keeps its status, its response body (first 2,000 characters, with the
   key and workspace id removed if they ever appeared) and the request-id response header.
2. The token-counting request never fails a call: after the 429/529 rule, any other failure is
   re-sent once after 2 s; if that fails too the reservation uses the size of the encoded
   request in bytes as the input-token count (an upper bound) and the call proceeds.
3. A billing or limit stop (HTTP 402, or HTTP 400, 403 or 429 whose body names, case-insensitively,
   credit, balance, billing, usage limit, spend limit, limit exceeded or insufficient; from either
   endpoint; fleet-monitor rule of 2026-10-04 11:20Z) is a billing outage, not an outcome: it pauses every new call of the stage and the
   same request is re-sent every 60 s for up to 1,200 s. If the outage outlasts that, every
   later call is refused with the category `provider_credit_balance_low`.
4. Amendment A2 (2026-10-04): the model gpt-6-sol goes through the reference OpenAI adapter
   (openai_provider.py, a byte-identical copy) behind `OpenAIRoute`, which gives it this module's
   call(condition, obs, call_id) interface, ledger and CallFailure. Its billing stop is
   `provider_billing_stopped`; BILLING_STOPS holds both stop categories.
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

import openai_provider
import study

MESSAGES_URL = 'https://api.anthropic.com/v1/messages'
COUNT_URL = 'https://api.anthropic.com/v1/messages/count_tokens'

BODY_KEYS = ('model', 'max_tokens', 'system', 'messages', 'output_config')


SLEEP = time.sleep          # the rehearsal replaces it so that backoff and billing waits take no time
CLOCK = time.monotonic      # the OpenAI route's clock; the rehearsal advances it by the waits it skips
CREDIT = 'provider_credit_balance_low'
BILLING_STOPS = (CREDIT, openai_provider.BILLING_STOP)     # either ends a stage as a resumable billing stop
# Failures that stop a stage at once, whatever the number of failed units.
INTEGRITY = ('duplicate_call_refused', 'stage_call_cap_reached', 'study_call_cap_reached', 'aggregate_budget_exhausted',
             'attempt_without_reservation', 'transport_attempt_cap_reached', 'reservation_bound_breached', 'model_mismatch',
             'stage_deadline', 'input_size_limit')


def is_integrity(category):
    """Failures that stop a stage at once: this module's list and the OpenAI adapter's."""
    return category in INTEGRITY or category in openai_provider.INTEGRITY


class CallFailure(openai_provider.CallFailure):
    """A subclass of the OpenAI adapter's CallFailure, so that a ledger refusal raised inside that
    adapter keeps its category there exactly as it does in the Anthropic class."""
    def __init__(self, category, accounting=None):
        super().__init__(category)
        self.category, self.accounting = category, accounting or {}


def stage_of(call_id):
    """'q0-001:<episode id>:r<round>' -> 'Q0'."""
    return call_id.split(':', 1)[0].split('-', 1)[0].upper()


def rate_limits(headers):
    """The numeric anthropic-ratelimit-* limit and remaining values of a response, nothing else."""
    out = {}
    try:
        for name, value in (headers.items() if headers is not None else ()):
            low = str(name).lower()
            if low.startswith('anthropic-ratelimit-') and low.endswith(('-limit', '-remaining')) and str(value).isdigit():
                out[low[len('anthropic-ratelimit-'):]] = int(value)
    except Exception:
        return None
    return out or None


class Ledger:
    """One append-only ledger for the whole study, shared by every stage and process.

    An exclusive lock spans each read, check, append and fsync. A line that does not parse makes
    every later transaction fail closed. Refuses: a call id seen before; a reservation beyond the
    stage's max_calls, the study's max_attempted_calls or the dollar cap (settled actual cost of
    answered calls plus the full reservation of every call without reported usage); an HTTP
    attempt beyond max_transport_attempts or without a reservation."""

    def __init__(self, path, budget=None):
        self.path = Path(path); self.budget = budget
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        self._offset = 0; self._lock = threading.Lock()
        self._reserved = {}; self._seen = set(); self._settled = {}; self._tokens = [0, 0]; self._attempts = 0; self._by_stage = {}

    def _apply(self, e):
        kind = e['type']
        if kind == 'reserve':
            self._reserved[e['call_id']] = e['micro_usd']; self._seen.add(e['call_id'])
            stage = stage_of(e['call_id']); self._by_stage[stage] = self._by_stage.get(stage, 0) + 1
        elif kind == 'void':
            # written by the OpenAI adapter after a billing stop: no model ran, the reservation is released
            del self._reserved[e['call_id']]
            stage = stage_of(e['call_id']); self._by_stage[stage] -= 1
        elif kind == 'attempt':
            self._attempts += 1
        elif kind == 'response':
            self._settled[e['call_id']] = e['actual_micro_usd']
            self._tokens[0] += e.get('input_tokens', 0); self._tokens[1] += e.get('output_tokens', 0)
        else:
            raise ValueError('unknown ledger event')

    def _committed(self):
        return sum(self._settled.get(call, amount) for call, amount in self._reserved.items())

    def transact(self, event=None):
        budget = self.budget or study.budget()
        with self._lock, self.path.open('a+', encoding='utf-8') as f:
            os.chmod(self.path, 0o600)
            fcntl.flock(f, fcntl.LOCK_EX)
            f.seek(self._offset)
            for line in f.read().splitlines():
                if line.strip(): self._apply(json.loads(line))
            self._offset = f.tell()
            if event and event['type'] == 'reserve':
                call = event['call_id']; stage = stage_of(call)
                if call in self._seen: raise CallFailure('duplicate_call_refused')
                if self._by_stage.get(stage, 0) >= budget['max_calls'].get(stage, 0): raise CallFailure('stage_call_cap_reached')
                if len(self._reserved) >= budget['max_attempted_calls']: raise CallFailure('study_call_cap_reached')
                if self._committed() + event['micro_usd'] > int(budget['aggregate_usd'] * 1_000_000):
                    raise CallFailure('aggregate_budget_exhausted')
            if event and event['type'] == 'void':
                if event['call_id'] not in self._reserved or event['call_id'] in self._settled: raise CallFailure('void_refused')
            if event and event['type'] == 'attempt':
                if event['call_id'] not in self._reserved: raise CallFailure('attempt_without_reservation')
                if self._attempts >= budget['max_transport_attempts']: raise CallFailure('transport_attempt_cap_reached')
            if event:
                f.seek(0, 2); f.write(json.dumps(event, sort_keys=True) + '\n'); f.flush(); os.fsync(f.fileno())
                self._offset = f.tell(); self._apply(event)
            return {'attempted_calls': len(self._reserved), 'calls_by_stage': dict(self._by_stage),
                    'transport_attempts': self._attempts,
                    'reserved_usd': sum(self._reserved.values()) / 1e6,
                    'actual_usd': sum(self._settled.values()) / 1e6,
                    'committed_usd': self._committed() / 1e6,
                    'usage_reported_calls': len(self._settled),
                    'input_tokens': self._tokens[0], 'output_tokens': self._tokens[1]}


class BillingGate:
    """Shared by every worker thread of a stage. While a credit-balance outage lasts no new call
    starts; once the outage has outlasted its limit the gate is dead and every call is refused."""

    def __init__(self):
        self.lock = threading.Lock(); self.clear = threading.Event(); self.clear.set()
        self.dead = False; self.pauses = 0; self.pause_seconds = 0; self.affected = 0

    def begin(self, first=True):
        with self.lock:
            self.affected += bool(first)
            if self.clear.is_set() and not self.dead: self.pauses += 1; self.clear.clear()

    def end(self, waited):
        with self.lock:
            if not self.clear.is_set() and not self.dead: self.pause_seconds += waited; self.clear.set()

    def stop(self, waited):
        with self.lock:
            if not self.dead: self.dead = True; self.pause_seconds += waited
            self.clear.set()        # wake the waiting threads; they see the dead gate

    def wait(self):
        self.clear.wait()
        if self.dead: raise CallFailure(CREDIT, {'attempted': False, 'usage_reported': False, 'attempts': 0, 'billing_stop': True})

    def paused(self):
        return not self.clear.is_set()

    def stats(self):
        return {'billing_pauses': self.pauses, 'billing_pause_seconds': self.pause_seconds, 'billing_affected_calls': self.affected}


class Anthropic:
    def __init__(self, ledger, opener=None, clock=time.monotonic, sleep=None):
        self.ledger = ledger; self.opener = opener or urllib.request.urlopen
        self.clock = clock; self.sleep = sleep or (lambda seconds: SLEEP(seconds))
        self.d = study.design(); self.b = study.budget(); self.retry = self.b['retry']; self.outage = self.b['billing_outage']
        self.local = threading.local()      # the last response's rate-limit numbers, per worker thread
        self.gate = BillingGate()
        self.key = os.environ.get('SWARM_MODEL_API_KEY')
        self.workspace = os.environ.get('SWARM_MODEL_WORKSPACE_ID')
        if not self.key or not self.workspace:
            raise CallFailure('missing_credential_alias')

    def headers(self):
        return {'Content-Type': 'application/json', 'x-api-key': self.key,
                'anthropic-version': '2023-06-01', 'anthropic-workspace-id': self.workspace}

    def body(self, condition, obs):
        return {'model': study.model(), 'max_tokens': self.b['max_output_tokens'], 'system': study.system_prompt(condition),
                'messages': [{'role': 'user', 'content': study.user_text(obs)}],
                'output_config': {'effort': self.d['effort'], 'format': {'type': 'json_schema', 'schema': study.SCHEMA}}}

    def evidence(self, exc):
        """What is kept of a failed HTTP response: status, body (truncated, credentials removed if
        the provider ever echoed them) and the request-id header. Never a request header."""
        try: raw = exc.read()
        except Exception: raw = b''
        text = raw.decode('utf-8', 'replace') if isinstance(raw, (bytes, bytearray)) else str(raw or '')
        for secret in (self.key, self.workspace): text = text.replace(secret, '[removed]')
        out = {'http_status': exc.code, 'error_body': text[:self.b['error_body_chars']]}
        try: request_id = exc.headers.get('request-id') if exc.headers else None
        except Exception: request_id = None
        if request_id: out['request_id'] = str(request_id)[:200]
        return out

    def is_credit_error(self, ev):
        text = ev['error_body'].lower()
        return ev['http_status'] in self.outage['always_status'] or (
            ev['http_status'] in self.outage['http_status'] and any(word in text for word in self.outage['match_any']))

    def post(self, url, encoded, prefix='', on_attempt=None):
        """One logical request. Returns (parsed JSON, attempts). Re-sends only after HTTP 429/529,
        with backoff, inside the single request time budget; everything else fails at once."""
        started = self.clock(); deadline = started + self.b['request_timeout_seconds']
        attempts = 0; backoff = list(self.retry['backoff_seconds'])
        while True:
            remaining = deadline - self.clock()
            if remaining <= 0.5:
                raise CallFailure(prefix + 'timeout', {'attempts': attempts})
            if on_attempt: on_attempt(attempts + 1)
            attempts += 1
            request = urllib.request.Request(url, data=encoded, headers=self.headers(), method='POST')
            try:
                with self.opener(request, timeout=remaining) as response:
                    self.local.limits = rate_limits(getattr(response, 'headers', None))
                    return json.loads(response.read()), attempts
            except urllib.error.HTTPError as exc:
                code = exc.code; ev = self.evidence(exc)
                try: retry_after = float(exc.headers.get('retry-after')) if exc.headers else None
                except (TypeError, ValueError, AttributeError): retry_after = None
                try: exc.close()
                except Exception: pass
                if code in self.retry['retryable_http_status'] and attempts <= self.retry['transport_retries']:
                    wait = backoff[min(attempts - 1, len(backoff) - 1)]
                    if retry_after is not None:
                        wait = max(wait, min(retry_after, self.retry['retry_after_cap_seconds']))
                    if self.clock() + wait < deadline - 1:
                        self.sleep(wait)
                        continue
                category = CREDIT if self.is_credit_error(ev) else prefix + 'http_' + str(code)
                raise CallFailure(category, dict(ev, attempts=attempts)) from None
            except (socket.timeout, TimeoutError):
                raise CallFailure(prefix + 'timeout', {'attempts': attempts}) from None
            except urllib.error.URLError as exc:
                timed_out = isinstance(getattr(exc, 'reason', None), (socket.timeout, TimeoutError))
                raise CallFailure(prefix + ('timeout' if timed_out else 'transport_URLError'), {'attempts': attempts}) from None
            except CallFailure:
                raise
            except Exception as exc:
                raise CallFailure(prefix + 'transport_' + type(exc).__name__, {'attempts': attempts}) from None

    def guarded(self, send, note):
        """Run one request. On a credit-balance error: pause the stage and re-send the same request
        on the slow schedule, each re-send with its own request time budget. Returns what `send`
        returns, raises its other failures unchanged, or raises CREDIT when the outage outlasted
        the limit. `note` collects what happened for the call's accounting."""
        try:
            return send()
        except CallFailure as exc:
            if exc.category != CREDIT: raise
            first = exc
        every, limit = self.outage['retry_every_seconds'], self.outage['max_wait_seconds']
        note.update(billing_error={k: first.accounting[k] for k in ('http_status', 'error_body', 'request_id') if k in first.accounting})
        waited = 0; self.gate.begin()
        while True:
            note.update(billing_resends=waited // every, billing_wait_seconds=waited)
            if self.gate.dead or waited + every > limit:
                self.gate.stop(waited); raise CallFailure(CREDIT, {'billing_stop': True}) from None
            self.sleep(every); waited += every
            try:
                result = send()
            except CallFailure as exc:
                if exc.category == CREDIT:
                    self.gate.begin(first=False)      # another call's success may have lifted the pause too early
                    continue
                note.update(billing_resends=waited // every, billing_wait_seconds=waited); self.gate.end(waited); raise
            note.update(billing_resends=waited // every, billing_wait_seconds=waited); self.gate.end(waited)
            return result

    def count(self, body, request_bytes, note):
        """Input tokens for the reservation. Never fails a call: 429/529 by the retry rule, any
        other failure re-sent once after a short wait, then the request size in bytes (a token is
        at least one byte, so this is an upper bound). Only a billing stop is raised."""
        encoded = json.dumps(body).encode(); note.update(count_attempts=0)
        for round_ in (1, 2):
            try:
                data, attempts = self.guarded(lambda: self.post(COUNT_URL, encoded, 'count_'), note)
                note['count_attempts'] += attempts
                tokens = data.get('input_tokens') if isinstance(data, dict) else None
                if type(tokens) is int and tokens > 0: return tokens
                failure = {'category': 'count_missing'}
            except CallFailure as exc:
                if exc.category == CREDIT: raise
                note['count_attempts'] += exc.accounting.get('attempts', 0)
                failure = dict({k: v for k, v in exc.accounting.items() if k in ('http_status', 'error_body', 'request_id')}, category=exc.category)
            note.setdefault('count_errors', []).append(failure)
            if round_ == 1: self.sleep(self.retry['count_resend_seconds'])
        note['count_fallback'] = True
        return request_bytes

    def call(self, condition, obs, call_id):
        """One turn: the condition's system prompt and the state of the round. Returns
        (validated answer, accounting) or raises CallFailure with the accounting so far."""
        self.gate.wait()                     # no new call starts during a billing outage
        body = self.body(condition, obs)
        assert tuple(body) == BODY_KEYS
        encoded = json.dumps(body).encode()
        if len(encoded) > self.b['max_input_bytes']:
            raise CallFailure('input_size_limit', {'attempted': False, 'usage_reported': False, 'attempts': 0})
        account = {'request_bytes': len(encoded), 'usage_reported': False, 'attempted': False, 'attempts': 0}
        # Input tokens from the free counting endpoint (or the byte-count fallback); the whole output limit priced in full.
        try:
            counted = self.count({k: v for k, v in body.items() if k != 'max_tokens'}, len(encoded), account)
        except CallFailure as exc:
            raise CallFailure(exc.category, dict(account, **exc.accounting)) from None
        # 2% + 64 tokens in case billed input differs slightly from the count.
        price_in, price_out = study.prices()     # this attempt's model, from the hashed design
        reserve = (int(counted * 1.02) + 64) * price_in + self.b['max_output_tokens'] * price_out
        account.update(reserved_usd=reserve / 1e6, counted_input_tokens=counted)
        try:
            self.ledger.transact({'type': 'reserve', 'call_id': call_id, 'micro_usd': reserve, 'time': time.time()})
        except CallFailure as exc:
            raise CallFailure(exc.category, account) from None
        account['attempted'] = True          # one call, reserved once, however many HTTP attempts follow
        def on_attempt(n):
            self.ledger.transact({'type': 'attempt', 'call_id': call_id, 'n': account['attempts'] + 1, 'time': time.time()})
            account['attempts'] += 1
        started = self.clock()
        try:
            data, _ = self.guarded(lambda: self.post(MESSAGES_URL, encoded, '', on_attempt), account)
        except CallFailure as exc:
            extra = {k: v for k, v in exc.accounting.items() if k in ('http_status', 'error_body', 'request_id', 'billing_stop')}
            raise CallFailure(exc.category, dict(account, **extra)) from None
        account['latency_seconds'] = self.clock() - started
        if getattr(self.local, 'limits', None): account['rate_limits'] = self.local.limits
        if not isinstance(data, dict):
            raise CallFailure('malformed_provider_response', account)
        usage = data.get('usage') or {}
        if not all(type(usage.get(k)) is int and usage[k] >= 0 for k in ('input_tokens', 'output_tokens')):
            raise CallFailure('missing_usage', account)
        actual = usage['input_tokens'] * price_in + usage['output_tokens'] * price_out
        self.ledger.transact({'type': 'response', 'call_id': call_id, 'actual_micro_usd': actual,
                              'input_tokens': usage['input_tokens'], 'output_tokens': usage['output_tokens']})
        account.update(usage_reported=True, actual_usd=actual / 1e6, input_tokens=usage['input_tokens'],
                       output_tokens=usage['output_tokens'], stop_reason=data.get('stop_reason'))
        # Nothing below is retried: the model ran and usage was reported.
        if usage.get('cache_creation_input_tokens', 0) or usage.get('cache_read_input_tokens', 0):
            raise CallFailure('unexpected_cache_usage', account)
        if actual > reserve:
            raise CallFailure('reservation_bound_breached', account)
        if data.get('model') != study.model():
            raise CallFailure('model_mismatch', account)
        if data.get('stop_reason') == 'refusal':
            details = data.get('stop_details') or {}
            account['refusal_category'] = details.get('category') if isinstance(details, dict) else None
            raise CallFailure('refusal', account)
        if data.get('stop_reason') != 'end_turn':
            raise CallFailure('nonterminal_output', account)
        # Thinking and redacted-thinking blocks may precede the single answer block.
        content = [b for b in data.get('content') or [] if isinstance(b, dict) and b.get('type') not in ('thinking', 'redacted_thinking')]
        if len(content) != 1 or content[0].get('type') != 'text' or not isinstance(content[0].get('text'), str):
            raise CallFailure('invalid_structured_answer', account)
        if len(content[0]['text']) > self.b['max_visible_chars']:
            raise CallFailure('answer_too_long', account)
        try:
            answer = study.validate(json.loads(content[0]['text']))
        except Exception:
            raise CallFailure('invalid_structured_answer', account) from None
        return answer, account


class _OpenAIGate:
    """The worker's view of the OpenAI adapter's stage-wide billing pause."""

    def __init__(self, api):
        self.api = api

    def paused(self):
        with self.api._state:
            return self.api._paused

    def stats(self):
        with self.api._state:
            return dict(self.api.billing)


class OpenAIRoute:
    """gpt-6-sol through the reference adapter, with the Anthropic class's interface: the same system
    prompt, the same state text as the one user message, the same validator (study.validate). The
    adapter's own rules apply unchanged: body exactly model, reasoning_effort, max_completion_tokens,
    response_format, messages; finish_reason length is the failure `truncated_output`, never an answer;
    re-send only on 429/500/502/503/504, twice; a billing or quota stop pauses the stage and re-sends
    every 60 s for up to 1,200 s, then `provider_billing_stopped`. Adapter failures are re-raised as
    this module's CallFailure with the same category and accounting."""

    def __init__(self, ledger, opener=None, clock=None, sleep=None):
        try:
            self.api = openai_provider.OpenAI(ledger, study.openai_config(), opener=opener, clock=clock or (lambda: CLOCK()),
                                              sleep=sleep or (lambda seconds: SLEEP(seconds)))
        except openai_provider.CallFailure as exc:
            raise CallFailure(exc.category, exc.accounting) from None
        self.gate = _OpenAIGate(self.api)

    def body(self, condition, obs):
        return self.api.body(study.system_prompt(condition), study.user_text(obs))

    def call(self, condition, obs, call_id):
        try:
            return self.api.call(study.system_prompt(condition), study.user_text(obs), call_id, study.validate)
        except openai_provider.CallFailure as exc:
            raise CallFailure(exc.category, exc.accounting) from None


def make(ledger, opener=None):
    """The adapter of this attempt's model."""
    return OpenAIRoute(ledger, opener=opener) if study.provider_name() == 'openai' else Anthropic(ledger, opener=opener)

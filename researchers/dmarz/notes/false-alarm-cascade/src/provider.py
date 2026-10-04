"""Native Messages API adapter for claude-opus-5-5 with a durable study ledger.

No answer is ever retried. Transport retry rule (ready-chain contract): at most 2 retries per
request, only for HTTP 429 and 529 (the provider rejected the request before running the model),
backoff 2 s then 6 s, a retry-after header honoured up to 20 s, all attempts and waits inside the
one request timeout. Timeouts, every other status, refusals, invalid or wrong answers and anything
after a response are never retried.

Adapted from sybil-scarcity-opus/src/provider.py (reviewed 2026-10-04). Changes: the prompt, the
schema and the answer validation are this study's; the ledger keeps a running total between
transactions instead of re-reading the whole file each time (same checks, same file format).
Never put credentials, request headers or raw transport exceptions in records.

Failure-handling rule (required by dmarz/fleet-monitor, 2026-10-04):
1. A failed HTTP request keeps its evidence: status, response body cut to 2,000 characters and the
   `request-id` response header, with the key and the workspace id scrubbed from the body.
2. The token count never fails a call: after the retry rule, one re-send after 2 s for any other
   failure, then the reservation falls back to the number of bytes of the encoded request (an
   upper bound on its tokens), recorded as `count_fallback`.
3. Which failures stop a stage at once is decided by `INTEGRITY` below; the worker applies it.
4. A billing outage is not a model failure. An HTTP 400, 402 or 403 whose body names the credit
   balance pauses every call of the stage: no new call starts, the call that met it is re-sent
   every 60 s for up to 1,200 s (each re-send recorded in the ledger as an attempt), and other
   calls that met it wait and are re-sent once the pause ends. If the outage outlasts the wait
   the call ends as `provider_credit_balance_low`, its reservation is voided, and the stage stops.

Opus 5.5 request rules (ready-chain contract): the body carries exactly `model`, `max_tokens`,
`system`, `messages` and `output_config` (effort plus the JSON schema). It never carries
`thinking`, `temperature`, `top_p`, `top_k`, `tool_choice`, an assistant prefill or `fallbacks`.
"""
import fcntl
import json
import os
from pathlib import Path
import threading
import time
import urllib.error
import urllib.request
import study

MESSAGES_URL = 'https://api.anthropic.com/v1/messages'
COUNT_URL = 'https://api.anthropic.com/v1/messages/count_tokens'
REQUEST_KEYS = ('model', 'max_tokens', 'system', 'messages', 'output_config')
LEDGER_ENV = 'STUDY_BUDGET_LEDGER'
CREDIT_STOP = 'provider_credit_balance_low'
CREDIT_STATUS = (400, 402, 403)
EVIDENCE_CHARS = 2000
# Failures that mean the run itself cannot be trusted or may not continue. They stop dispatch at
# once in every stage. Every other failed call is a failed unit (see worker.py).
INTEGRITY = frozenset((
    'duplicate_call_refused', 'unknown_stage_refused', 'stage_call_cap_exhausted', 'study_call_cap_exhausted',
    'aggregate_budget_exhausted', 'attempt_without_reservation', 'transport_attempt_cap_exhausted',
    'unknown_ledger_event', 'ledger_partial_write', 'ledger_unreadable', 'void_refused',
    'reservation_bound_breached', 'model_mismatch', 'stage_deadline', 'input_size_limit', 'missing_credential_alias'))


def is_integrity(category):
    return category in INTEGRITY or str(category).startswith('internal_')


class CallFailure(Exception):
    def __init__(self, category, accounting=None):
        super().__init__(category)
        self.category, self.accounting = category, accounting or {}


def stage_of(call_id):
    """Call ids are '<batch>:<row id>' and batches are '<stage>-<attempt>', e.g. 's1-001:e8400-fa.a2.r3'."""
    return call_id.split(':', 1)[0].split('-', 1)[0].upper()


class TransportFailure(Exception):
    def __init__(self, category, attempts, detail=None):
        super().__init__(category)
        self.category, self.attempts, self.detail = category, attempts, detail or {}


class Ledger:
    """One ledger for the complete study, independent of process and stage.

    An exclusive lock spans each JSONL append and fsync. A partial or unreadable line makes every
    later transaction fail closed. A reservation is refused when it would exceed the stage's call
    cap, the study's call cap, or the dollar cap on settled cost plus open reservations. Every
    HTTP attempt to the messages endpoint is recorded before it is sent and refused over the cap
    `max_transport_attempts`. A call is reserved once, however many attempts it needs.

    Each transaction reads only the lines appended since this object's last transaction (by this
    or any other process) and folds them into running totals, so the cost of a transaction does
    not grow with the length of the ledger.
    """
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        self._guard = threading.Lock()
        self._offset = 0           # bytes of the file already folded into the totals below
        self._reserved = {}        # call id -> reserved micro-dollars
        self._settled = {}         # call id -> actual micro-dollars of its latest response
        self._by_stage = {}
        self._attempts = self._responses = self._voided = 0
        self._reserved_total = self._actual_total = self._committed = 0
        self._tokens = [0, 0]

    def _fold(self, e):
        kind, call_id = e['type'], e.get('call_id')
        if kind == 'reserve':
            self._reserved[call_id] = e['micro_usd']
            self._by_stage[stage_of(call_id)] = self._by_stage.get(stage_of(call_id), 0) + 1
            self._reserved_total += e['micro_usd']
            # A call without reported usage (in flight, or failed before usage) keeps its full reservation.
            self._committed += self._settled.get(call_id, e['micro_usd'])
        elif kind == 'attempt':
            self._attempts += 1
        elif kind == 'void':
            # A call the provider never ran (billing outage outlasted the wait): its reservation and
            # its place under the call caps are given back. Its transport attempts stay counted.
            micro = self._reserved.pop(call_id)
            self._by_stage[stage_of(call_id)] -= 1
            self._reserved_total -= micro
            self._committed -= micro
            self._voided += 1
        elif kind == 'response':
            # A call with reported usage counts its actual cost instead of its reservation.
            if call_id in self._reserved:
                self._committed += e['actual_micro_usd'] - self._settled.get(call_id, self._reserved[call_id])
            self._settled[call_id] = e['actual_micro_usd']
            self._responses += 1
            self._actual_total += e['actual_micro_usd']
            self._tokens[0] += e.get('input_tokens', 0)
            self._tokens[1] += e.get('output_tokens', 0)
        else:
            raise CallFailure('unknown_ledger_event')

    def transact(self, event=None):
        budget = study.design()['budget']
        with self._guard, self.path.open('ab+') as f:
            os.chmod(self.path, 0o600)
            fcntl.flock(f, fcntl.LOCK_EX)
            f.seek(self._offset)
            fresh = f.read()
            if fresh and not fresh.endswith(b'\n'):
                raise CallFailure('ledger_partial_write')
            for line in fresh.splitlines():
                if line.strip():
                    try:
                        self._fold(json.loads(line))
                    except (ValueError, KeyError, TypeError):
                        raise CallFailure('ledger_unreadable') from None
            self._offset += len(fresh)
            if event:
                if event['type'] == 'reserve':
                    stage = stage_of(event['call_id'])
                    if event['call_id'] in self._reserved:
                        raise CallFailure('duplicate_call_refused')
                    if stage not in budget['max_calls']:
                        raise CallFailure('unknown_stage_refused')
                    if self._by_stage.get(stage, 0) >= budget['max_calls'][stage]:
                        raise CallFailure('stage_call_cap_exhausted')
                    if len(self._reserved) >= budget['max_attempted_calls']:
                        raise CallFailure('study_call_cap_exhausted')
                    if self._committed + event['micro_usd'] > int(budget['aggregate_usd'] * 1_000_000):
                        raise CallFailure('aggregate_budget_exhausted')
                elif event['type'] == 'attempt':
                    if event['call_id'] not in self._reserved:
                        raise CallFailure('attempt_without_reservation')
                    if self._attempts >= budget['max_transport_attempts']:
                        raise CallFailure('transport_attempt_cap_exhausted')
                elif event['type'] == 'void':
                    if event['call_id'] not in self._reserved or event['call_id'] in self._settled:
                        raise CallFailure('void_refused')
                elif event['type'] != 'response':
                    raise CallFailure('unknown_ledger_event')
                line = (json.dumps(event, sort_keys=True) + '\n').encode()
                f.write(line); f.flush(); os.fsync(f.fileno())      # append mode: always at the end
                self._offset += len(line)
                self._fold(event)
            return {'attempted_calls': len(self._reserved), 'calls_by_stage': {s: n for s, n in self._by_stage.items() if n},
                    'voided_calls': self._voided,
                    'transport_attempts': self._attempts,
                    'cap_transport_attempts': budget['max_transport_attempts'],
                    'usage_reported_calls': self._responses,
                    'reserved_usd': self._reserved_total / 1e6,
                    'actual_usd': self._actual_total / 1e6,
                    'committed_usd': self._committed / 1e6,
                    'input_tokens': self._tokens[0], 'output_tokens': self._tokens[1],
                    'cap_usd': budget['aggregate_usd'], 'cap_calls': budget['max_attempted_calls']}


def request_body(packet):
    """The complete request. Nothing else is ever added to it."""
    d = study.design()
    body = {'model': study.model(), 'max_tokens': d['budget']['max_output_tokens'], 'system': study.SYSTEM,
            'messages': [{'role': 'user', 'content': study.actor_text(packet)}],
            'output_config': {'effort': d['effort'], 'format': {'type': 'json_schema', 'schema': study.schema()}}}
    assert tuple(body) == REQUEST_KEYS
    return body


def is_credit_error(detail):
    """An HTTP 400, 402 or 403 whose response body names the credit balance."""
    return detail.get('http_status') in CREDIT_STATUS and 'credit balance' in str(detail.get('error_body', '')).lower()


class Anthropic:
    def __init__(self, ledger, opener=None, clock=None, sleep=None):
        self.ledger = ledger; self.opener = opener or urllib.request.urlopen
        self.clock, self.sleep = clock or time.monotonic, sleep or time.sleep
        # Billing pause, shared by every thread that calls through this object.
        self.gate = threading.Condition()
        self.paused = False          # a call is re-sending on the slow schedule; nothing new starts
        self.gave_up = False         # the outage outlasted the wait; nothing new starts again
        self.d = study.design(); self.b = self.d['budget']
        self.model = study.model(); self.price = study.prices(self.model)
        self.key = os.environ.get('SWARM_MODEL_API_KEY')
        self.workspace = os.environ.get('SWARM_MODEL_WORKSPACE_ID')
        if not self.key or not self.workspace:
            raise CallFailure('missing_credential_alias')

    def headers(self):
        return {'Content-Type':'application/json','x-api-key':self.key,
                'anthropic-version':'2023-06-01','anthropic-workspace-id':self.workspace}

    def scrub(self, text):
        """Evidence text with every credential string removed and cut to the stored length."""
        text = str(text)
        for secret in (self.key, self.workspace):
            text = text.replace(secret, '[redacted]')
        return text[:EVIDENCE_CHARS]

    def evidence(self, exc):
        """What is kept of a rejected request: status, response body and request id. Never a request header."""
        detail = {'http_status': exc.code}
        try:
            detail['error_body'] = self.scrub(exc.read().decode('utf-8', 'replace'))
        except Exception:
            detail['error_body'] = ''
        try:
            request_id = exc.headers.get('request-id') if exc.headers else None
        except Exception:
            request_id = None
        if request_id:
            detail['request_id'] = self.scrub(request_id)[:200]
        return detail

    def post(self, url, encoded, before_attempt=None, timeout=None):
        """One request under the transport retry rule. Returns (parsed body, attempts)."""
        retry = self.b['retry']; backoff = list(retry['backoff_seconds'])
        deadline = self.clock() + (timeout or self.b['request_timeout_seconds'])
        attempts = 0
        while True:
            remaining = deadline - self.clock()
            if remaining <= 0.5:
                raise TransportFailure('transport_timeout_budget', attempts)
            if before_attempt:
                before_attempt(attempts + 1)      # the ledger may refuse the attempt (CallFailure)
            attempts += 1
            request = urllib.request.Request(url, data=encoded, headers=self.headers(), method='POST')
            try:
                with self.opener(request, timeout=remaining) as response:
                    return json.loads(response.read()), attempts
            except urllib.error.HTTPError as exc:
                # Only a request rejected before the model ran (rate limit or overload) is retried.
                if exc.code in retry['retryable_http_status'] and attempts <= retry['transport_retries']:
                    wait = backoff[min(attempts - 1, len(backoff) - 1)]
                    try:
                        after = float(exc.headers.get('retry-after')) if exc.headers else None
                    except (TypeError, ValueError):
                        after = None
                    if after is not None:
                        wait = max(wait, min(after, retry['retry_after_cap_seconds']))
                    if self.clock() + wait < deadline - 1:
                        self.sleep(wait)
                        continue
                raise TransportFailure('http_' + str(exc.code), attempts, self.evidence(exc)) from None
            except Exception as exc:
                # Timeouts and every other transport failure are never retried.
                raise TransportFailure('transport_' + type(exc).__name__, attempts) from None

    def count(self, body, encoded_request, account):
        """Input tokens for the reservation, from the free counting endpoint. Never fails a call.

        HTTP 429 and 529 follow the retry rule. Any other failure (another status, a timeout, a
        malformed body) is re-sent once after 2 s. If the count still fails, the reservation uses
        the number of bytes of the encoded request, an upper bound on its tokens, and the call
        proceeds; every failure is kept in `count_errors`."""
        retry = self.b['retry']
        encoded = json.dumps(body).encode()
        for attempt in (1, 2):
            try:
                data, attempts = self.post(COUNT_URL, encoded, timeout=self.b['count_timeout_seconds'])
                account['count_attempts'] += attempts
                tokens = data.get('input_tokens') if isinstance(data, dict) else None
                if type(tokens) is int and tokens > 0:
                    return tokens
                failure = {'category': 'count_missing', 'error_body': self.scrub(json.dumps(data))}
            except TransportFailure as exc:
                account['count_attempts'] += exc.attempts
                failure = dict(exc.detail, category='count_' + exc.category)
            account.setdefault('count_errors', []).append(failure)
            if failure.get('http_status') in retry['retryable_http_status'] or attempt == 2:
                break                               # the retry rule already re-sent a 429 or 529
            self.sleep(self.b['count_resend_wait_seconds'])
        account['count_fallback'] = True
        return len(encoded_request)

    def reservation(self, counted):
        """Micro-dollars: counted input plus 2% and 64 tokens, and the full output limit."""
        return (int(counted*1.02)+64)*self.price['input_usd_per_million'] + self.b['max_output_tokens']*self.price['output_usd_per_million']

    def end_pause(self, leading, gave_up=False):
        """The leading call ends its pause, or any call records that the outage outlasted the wait."""
        with self.gate:
            if gave_up:
                self.gave_up = True
            if leading or gave_up:
                self.paused = False
                self.gate.notify_all()

    def billing_state(self):
        with self.gate:
            return 'stopped' if self.gave_up else 'paused' if self.paused else None

    def call(self, packet, call_id):
        with self.gate:
            while self.paused:                      # a billing pause: no new call starts in any thread
                self.gate.wait()
            if self.gave_up:
                raise CallFailure(CREDIT_STOP, {'attempted': False, 'attempts': 0})
        body = request_body(packet)
        encoded = json.dumps(body).encode()
        if len(encoded)>self.b['max_input_bytes']:
            raise CallFailure('input_size_limit')
        account = {'usage_reported':False, 'attempted':False, 'attempts':0, 'count_attempts':0, 'count_fallback':False}
        # Exact input tokens from the free counting endpoint; max output priced in full.
        counted = self.count({k:v for k,v in body.items() if k!='max_tokens'}, encoded, account)
        reserve = self.reservation(counted)
        account.update(reserved_usd=reserve/1e6, counted_input_tokens=counted)
        # One reservation per call, however many transport attempts it takes.
        self.ledger.transact({'type':'reserve','call_id':call_id,'micro_usd':reserve,'time':time.time()})
        account['attempted'] = True

        def before_attempt(n):
            # Recorded and counted before the request is sent; refused over the study's attempt cap.
            self.ledger.transact({'type':'attempt','call_id':call_id,'n':account['attempts']+1,'time':time.time()})
            account['attempts'] += 1
        outage = self.b['billing_outage']
        started = self.clock()
        leading, waited = False, 0
        while True:
            try:
                data, _ = self.post(MESSAGES_URL, encoded, before_attempt)
                break
            except TransportFailure as exc:
                if not is_credit_error(exc.detail):
                    self.end_pause(leading)
                    account.update(exc.detail)      # status, response body and request id of the rejection
                    raise CallFailure(exc.category, account) from None
                # The provider did not run the model: a billing outage, not an outcome.
                account['billing_rejections'] = account.get('billing_rejections', 0) + 1
                account['billing_last_error'] = exc.detail
                with self.gate:
                    if not leading and not self.paused and not self.gave_up:
                        self.paused = leading = True
                        account['billing_pauses_led'] = account.get('billing_pauses_led', 0) + 1
                    if not leading:
                        while self.paused:          # another call is re-sending; wait for its verdict
                            self.gate.wait()
                        if not self.gave_up:
                            continue                # the pause ended: re-send this same call once
                if not leading or waited >= outage['max_wait_seconds']:
                    self.end_pause(leading, gave_up=True)
                    self.ledger.transact({'type':'void','call_id':call_id,'reason':CREDIT_STOP,'time':time.time()})
                    account.update(attempted=False, voided=True)
                    raise CallFailure(CREDIT_STOP, account) from None
                self.sleep(outage['retry_every_seconds'])
                waited += outage['retry_every_seconds']
                account['billing_wait_seconds'] = waited
            except CallFailure as exc:
                self.end_pause(leading)
                raise CallFailure(exc.category, account) from None
            except BaseException:
                self.end_pause(leading)
                raise
        self.end_pause(leading)
        account['latency_seconds'] = self.clock()-started
        if not isinstance(data, dict):
            raise CallFailure('invalid_response_body', account)
        usage = data.get('usage') or {}
        if not all(type(usage.get(k)) is int and usage[k]>=0 for k in ('input_tokens','output_tokens')):
            raise CallFailure('missing_usage', account)
        if usage.get('cache_creation_input_tokens',0) or usage.get('cache_read_input_tokens',0):
            raise CallFailure('unexpected_cache_usage', account)
        actual = usage['input_tokens']*self.price['input_usd_per_million']+usage['output_tokens']*self.price['output_usd_per_million']
        self.ledger.transact({'type':'response','call_id':call_id,'actual_micro_usd':actual,
                              'input_tokens':usage['input_tokens'],'output_tokens':usage['output_tokens']})
        account.update(usage_reported=True, actual_usd=actual/1e6,
                       input_tokens=usage['input_tokens'], output_tokens=usage['output_tokens'])
        if actual>reserve:
            raise CallFailure('reservation_bound_breached', account)
        if data.get('model') != self.model:
            raise CallFailure('model_mismatch', account)
        if data.get('stop_reason') != 'end_turn':
            # Keep what the provider said about why it stopped; a refusal is its own category.
            account['stop_reason'] = self.scrub(data.get('stop_reason'))[:100]
            if data.get('stop_details') is not None:
                account['stop_details'] = self.scrub(json.dumps(data.get('stop_details')))
            raise CallFailure('refusal' if data.get('stop_reason') == 'refusal' else 'nonterminal_output', account)
        # Thinking and redacted-thinking blocks precede the answer; they are dropped, never parsed.
        content = data.get('content')
        try:
            content = [b for b in content if b.get('type') not in ('thinking','redacted_thinking')]
            if len(content)!=1 or content[0].get('type')!='text':
                raise ValueError('text_block')
            text = content[0]['text']
        except Exception:
            account['answer_text'] = self.scrub(json.dumps(data.get('content')))
            raise CallFailure('invalid_structured_answer', account) from None
        # The answer length is limited here, on the text block; max_tokens stays large for thinking.
        if not isinstance(text, str) or len(text) > self.b['max_answer_chars']:
            account['answer_text'] = self.scrub(text)
            raise CallFailure('answer_too_long', account)
        try:
            answer = study.normalize(study.validate(json.loads(text)))
        except Exception:
            account['answer_text'] = self.scrub(text)       # the failing answer is kept for reading
            raise CallFailure('invalid_structured_answer', account) from None
        return answer, account

"""Offline tests of the reference OpenAI adapter. No network beyond 127.0.0.1, no model call.

    python3 test_openai_provider.py
"""
import http.server as http_server
import io
import json
import os
from pathlib import Path
import socket
import tempfile
import threading
import unittest
import urllib.error
from unittest.mock import patch

import openai_provider as oap

SCHEMA = {'type': 'object', 'properties': {'answer': {'type': 'integer'}}, 'required': ['answer'], 'additionalProperties': False}
CONFIG = {
    'model': 'gpt-6-sol',
    'request_template': {'model': 'gpt-6-sol', 'reasoning_effort': 'none', 'max_completion_tokens': 1000,
                         'response_format': {'type': 'json_object'}},
    'budget': {'max_calls': {'S0': 0, 'P0': 1, 'Q0': 23, 'S1': 504}, 'max_attempted_calls': 528,
               'aggregate_usd': 20, 'max_output_tokens': 1000, 'max_input_tokens': 8000, 'max_input_bytes': 40000,
               'max_visible_chars': 4000, 'request_timeout_seconds': 120,
               'retry': {'transport_retries': 2, 'retryable_http_status': [429, 500, 502, 503, 504],
                         'backoff_seconds': [2, 6], 'retry_after_cap_seconds': 20},
               'billing_outage': {'retry_every_seconds': 60, 'max_wait_seconds': 1200},
               'max_transport_attempts': 640, 'reservation_margin': 10,
               'prices': dict(oap.PRICES['gpt-6-sol'])},
}
KEY = 'sk-proj-test-SECRET-0123456789'
SYS = 'Answer as a JSON object.'
QUOTA = '{"error":{"message":"You exceeded your current quota, please check your plan and billing details.","type":"insufficient_quota","param":null,"code":"insufficient_quota"}}'
RATE = '{"error":{"message":"Rate limit reached for gpt-6-sol in organization org-x on tokens per min (TPM): Limit 4000000, Used 3999000, Requested 2000. Please try again in 15ms.","type":"tokens","param":null,"code":"rate_limit_exceeded"}}'


def variant(**changes):
    c = json.loads(json.dumps(CONFIG))
    for path, value in changes.items():
        node = c; keys = path.split('__')
        for k in keys[:-1]: node = node[k]
        if value is None: node.pop(keys[-1], None)
        else: node[keys[-1]] = value
    return c


class Resp(io.BytesIO):
    def __init__(self, data, headers=None):
        super().__init__(data); self.headers = headers or {}
    def __enter__(self): return self
    def __exit__(self, *a): return False


def ok(content='{"answer": 7}', model='gpt-6-sol', finish='stop', usage=None, refusal=None, **extra):
    message = {'role': 'assistant', 'content': content, 'refusal': refusal}
    body = {'id': 'chatcmpl-1', 'object': 'chat.completion', 'model': model,
            'choices': [{'index': 0, 'finish_reason': finish, 'message': message}],
            'usage': usage if usage is not None else {'prompt_tokens': 900, 'completion_tokens': 12, 'total_tokens': 912,
                                                      'completion_tokens_details': {'reasoning_tokens': 0},
                                                      'prompt_tokens_details': {'cached_tokens': 0}}}
    body.update(extra)
    return body


def http(status, body='{"error":{"message":"x"}}', headers=None):
    return urllib.error.HTTPError(oap.URL, status, 'err', headers or {}, io.BytesIO(body.encode() if isinstance(body, str) else body))


class Clock:
    def __init__(self): self.t = 0.0; self.sleeps = []
    def now(self): return self.t
    def sleep(self, s): self.sleeps.append(s); self.t += s


def validate(obj):
    if not isinstance(obj, dict) or set(obj) != {'answer'} or type(obj['answer']) is not int:
        raise ValueError('schema')
    return obj


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = patch.dict(os.environ, {oap.KEY_ENV: KEY}); self.env.start()
        self.sent = []; self.clock = Clock()

    def tearDown(self):
        self.env.stop(); self.tmp.cleanup()

    def adapter(self, script, config=CONFIG):
        """script: list of responses in order; a dict is a 200 body, an exception is raised."""
        script = list(script)
        def opener(request, timeout):
            self.sent.append({'url': request.full_url, 'body': json.loads(request.data), 'timeout': timeout,
                              'headers': dict(request.header_items())})
            item = script.pop(0)
            if isinstance(item, BaseException): raise item
            if isinstance(item, tuple): return Resp(json.dumps(item[0]).encode(), item[1])
            return Resp(json.dumps(item).encode() if not isinstance(item, bytes) else item)
        self.ledger = oap.Ledger(Path(self.tmp.name) / 'ledger.jsonl', config['budget'])
        return oap.OpenAI(self.ledger, config, opener, self.clock.now, self.clock.sleep)

    def failure(self, api, call_id='s1-001:a', user='USER'):
        with self.assertRaises(oap.CallFailure) as cm:
            api.call(SYS, user, call_id, validate)
        return cm.exception


class Request(Base):
    def test_body_is_exactly_the_template_plus_messages(self):
        api = self.adapter([ok()])
        answer, acct = api.call(SYS, 'USER', 's1-001:a', validate)
        self.assertEqual(answer, {'answer': 7})
        body = self.sent[0]['body']
        self.assertEqual(tuple(body), oap.BODY_KEYS)
        self.assertEqual({k: body[k] for k in body if k != 'messages'}, CONFIG['request_template'])
        self.assertEqual(body['messages'], [{'role': 'system', 'content': SYS}, {'role': 'user', 'content': 'USER'}])
        self.assertEqual(self.sent[0]['url'], 'https://api.openai.com/v1/chat/completions')
        for forbidden in ('max_tokens', 'temperature', 'top_p', 'provider', 'reasoning', 'tools', 'tool_choice',
                          'stream', 'n', 'logprobs', 'store', 'metadata'):
            self.assertNotIn(forbidden, body)
        self.assertEqual(self.sent[0]['headers'].get('Authorization'), 'Bearer ' + KEY)

    def test_json_schema_strict_and_sampling_parameters(self):
        schema_format = {'type': 'json_schema', 'json_schema': {'name': 'answer', 'schema': SCHEMA, 'strict': True}}
        config = variant(request_template__response_format=schema_format, request_template__temperature=0)
        api = self.adapter([ok()], config)
        api.call('SYS', 'USER', 's1-001:a', validate)                       # no "json" needed outside json_object mode
        body = self.sent[0]['body']
        self.assertEqual(list(body), ['model', 'reasoning_effort', 'max_completion_tokens', 'response_format', 'temperature', 'messages'])
        self.assertEqual(body['response_format'], schema_format); self.assertEqual(body['temperature'], 0)

    def test_configuration_is_checked(self):
        bad = {
            'reasoning_effort_not_allowed_for_model': variant(request_template__reasoning_effort='minimal'),
            'sampling_parameters_need_reasoning_effort_none': variant(request_template__reasoning_effort='low', request_template__top_p=1),
            'template_keys': variant(request_template__max_tokens=1000),
            'max_completion_tokens_differs_from_budget': variant(request_template__max_completion_tokens=999),
            'json_schema_needs_name_schema_strict_true': variant(request_template__response_format={'type': 'json_schema', 'json_schema': {'name': 'a', 'schema': SCHEMA, 'strict': False}}),
            'response_format': variant(request_template__response_format={'type': 'text'}),
            'long_context_not_supported': variant(budget__max_input_tokens=272001),
            'prices_differ_from_reference_table': variant(budget__prices={'input': 1.0, 'cached_input': 0.1, 'cache_write': 1.25, 'output': 5.0}),
            'model_not_supported': variant(model='gpt-4o', request_template__model='gpt-4o'),
        }
        for want, config in bad.items():
            with self.assertRaises(ValueError) as cm: self.adapter([], config)
            self.assertEqual(str(cm.exception), want)
        astra = variant(model='gpt-6-astra', request_template__model='gpt-6-astra', request_template__reasoning_effort='none',
                        budget__prices=dict(oap.PRICES['gpt-6-astra']))
        with self.assertRaises(ValueError): self.adapter([], astra)              # astra has no `none` effort
        astra['request_template']['reasoning_effort'] = 'low'; self.adapter([], astra)

    def test_json_mode_needs_the_word_json_in_the_prompt(self):
        api = self.adapter([])
        with self.assertRaises(oap.CallFailure) as cm: api.call('Answer.', 'USER', 's1-001:a', validate)
        self.assertEqual(cm.exception.category, 'json_mode_prompt_lacks_json'); self.assertEqual(self.sent, [])
        self.assertEqual(self.ledger.transact()['attempted_calls'], 0)

    def test_model_check_accepts_the_id_and_its_dated_form_only(self):
        for i, model in enumerate(('gpt-6-sol', 'gpt-6-sol-2026-09-30')):
            self.adapter([ok(model=model)]).call(SYS, 'USER', f's1-001:ok{i}', validate)
        for i, model in enumerate(('gpt-6-luna', 'gpt-6.1-sol', 'gpt-6-sol-mini', 'gpt-6-sol-2026-9-30', None)):
            e = self.failure(self.adapter([ok(model=model)]), f's1-001:bad{i}')
            self.assertEqual(e.category, 'model_mismatch'); self.assertIn(e.category, oap.INTEGRITY)
        self.adapter([ok(model='gpt-6-sol-snap')], variant(canonical_model='gpt-6-sol-snap')).call(SYS, 'USER', 's1-001:c', validate)

    def test_missing_credential(self):
        with patch.dict(os.environ, {oap.KEY_ENV: ''}):
            with self.assertRaises(oap.CallFailure) as cm: self.adapter([])
        self.assertEqual(cm.exception.category, 'missing_credential_alias')

    def test_input_size_limit_is_refused_before_any_reservation(self):
        api = self.adapter([])
        with self.assertRaises(oap.CallFailure) as cm: api.call(SYS, 'U' * 50000, 's1-001:big', validate)
        self.assertEqual(cm.exception.category, 'input_size_limit'); self.assertEqual(self.sent, [])


class Cost(Base):
    def test_cost_is_computed_from_the_price_table_not_reported(self):
        api = self.adapter([ok(usage={'prompt_tokens': 900, 'completion_tokens': 12, 'cost': 99})])
        _, acct = api.call(SYS, 'USER', 's1-001:a', validate)
        self.assertEqual((acct['cost_source'], acct['provider_reported_usd']), ('computed_from_pinned_prices', None))
        self.assertAlmostEqual(acct['computed_usd'], (900 * 2.00 + 12 * 10.00) / 1e6)   # under the 1,024-token cache minimum
        self.assertAlmostEqual(acct['actual_usd'], 1920e-6); self.assertEqual(acct['input_pricing'], 'below_cache_minimum')
        self.assertAlmostEqual(self.ledger.transact()['committed_usd'], 0.00192)

    def test_cached_and_cache_write_tokens(self):
        usage = {'prompt_tokens': 5000, 'completion_tokens': 100,
                 'prompt_tokens_details': {'cached_tokens': 4000, 'cache_write_tokens': 600}}
        _, acct = self.adapter([ok(usage=usage)]).call(SYS, 'U' * 6000, 's1-001:a', validate)
        self.assertAlmostEqual(acct['computed_usd'], (400 * 2.00 + 600 * 2.50 + 4000 * 0.20 + 100 * 10.00) / 1e6)
        self.assertEqual(acct['input_pricing'], 'cache_write_reported')
        usage = {'prompt_tokens': 5000, 'completion_tokens': 100, 'prompt_tokens_details': {'cached_tokens': 4000}}
        _, acct = self.adapter([ok(usage=usage)]).call(SYS, 'U' * 6000, 's1-001:b', validate)
        self.assertAlmostEqual(acct['computed_usd'], (1000 * 2.50 + 4000 * 0.20 + 100 * 10.00) / 1e6)
        self.assertEqual(acct['input_pricing'], 'cache_write_upper_bound')

    def test_luna_prices(self):
        config = variant(model='gpt-6-luna', request_template__model='gpt-6-luna', budget__prices=dict(oap.PRICES['gpt-6-luna']))
        _, acct = self.adapter([ok(model='gpt-6-luna', usage={'prompt_tokens': 900, 'completion_tokens': 100})], config).call(SYS, 'USER', 's1-001:a', validate)
        self.assertAlmostEqual(acct['computed_usd'], (900 * 0.10 + 100 * 0.50) / 1e6)

    def test_reservation_bound_and_margin(self):
        _, acct = self.adapter([ok()]).call(SYS, 'U' * 3000, 's1-001:a', validate)
        bound = acct['request_bytes'] * 2.50 + 1000 * 10.00
        self.assertGreaterEqual(acct['reserved_usd'] * 1e6, 10 * bound - 1e-6); self.assertLess(acct['reserved_usd'] * 1e6, 10 * bound + 1)

    def test_reasoning_tokens_count_against_the_output_allowance(self):
        config = variant(request_template__reasoning_effort='low')
        usage = {'prompt_tokens': 900, 'completion_tokens': 700, 'completion_tokens_details': {'reasoning_tokens': 650}}
        _, acct = self.adapter([ok(usage=usage)], config).call(SYS, 'USER', 's1-001:a', validate)
        self.assertEqual((acct['reasoning_tokens'], acct['visible_output_tokens'], acct['output_tokens']), (650, 50, 700))
        self.assertAlmostEqual(acct['computed_usd'], (900 * 2.00 + 700 * 10.00) / 1e6)   # reasoning billed as output
        # Reasoning that used up the allowance ends as truncated_output with the reasoning count kept.
        usage = {'prompt_tokens': 900, 'completion_tokens': 1000, 'completion_tokens_details': {'reasoning_tokens': 1000}}
        e = self.failure(self.adapter([ok(content='', finish='length', usage=usage)], config), 's1-001:b')
        self.assertEqual((e.category, e.accounting['reasoning_tokens']), ('truncated_output', 1000))
        # More output than the allowance cannot happen; if reported, it is an integrity failure.
        usage = {'prompt_tokens': 900, 'completion_tokens': 1001, 'completion_tokens_details': {'reasoning_tokens': 990}}
        e = self.failure(self.adapter([ok(usage=usage)], config), 's1-001:c')
        self.assertEqual(e.category, 'output_ceiling_exceeded'); self.assertIn(e.category, oap.INTEGRITY)
        # With reasoning_effort none, any reasoning token is unexpected.
        usage = {'prompt_tokens': 900, 'completion_tokens': 20, 'completion_tokens_details': {'reasoning_tokens': 3}}
        self.assertEqual(self.failure(self.adapter([ok(usage=usage)]), 's1-001:d').category, 'unexpected_reasoning_tokens')


class Answers(Base):
    def category(self, response, call_id='s1-001:a'):
        return self.failure(self.adapter([response]), call_id)

    def test_answer_failure_categories_are_distinct_and_never_retried(self):
        cases = {
            'refusal': ok(content=None, refusal="I'm sorry, I can't help with that."),
            'refusal ': ok(finish='content_filter'),
            'truncated_output': ok(finish='length'),
            'empty_answer': ok(content='   '),
            'invalid_json': ok(content='{"answer": 7'),
            'invalid_json ': ok(content='{"answer": 7, "answer": 8}'),     # duplicate keys
            'invalid_answer': ok(content='{"answer": "seven"}'),
            'answer_too_long': ok(content='{"answer": 7}' + ' ' * 5000),
            'nonterminal_output': ok(finish='tool_calls'),
            'missing_usage': ok(usage={}),
        }
        for want, response in cases.items():
            self.sent.clear()
            e = self.category(response, 's1-001:' + want.replace(' ', '2'))
            self.assertEqual(e.category, want.strip()); self.assertEqual(len(self.sent), 1, want)
            self.assertEqual(e.accounting['attempts'], 1)
        e = self.category(ok(content=None, refusal='No.'), 's1-001:r9')
        self.assertEqual(e.accounting['refusal_text'], 'No.')
        api = self.adapter([ok(usage={'prompt_tokens': 8001, 'completion_tokens': 5})])
        with self.assertRaises(oap.CallFailure) as cm: api.call(SYS, 'U' * 9000, 's1-001:ceiling', validate)
        self.assertEqual(cm.exception.category, 'input_ceiling_exceeded')

    def test_invalid_answers_keep_the_text_for_reading(self):
        e = self.category(ok(content='{"answer": 7, "answer": 8}'))
        self.assertEqual(e.accounting['answer_text'], '{"answer": 7, "answer": 8}'); self.assertTrue(e.accounting['usage_reported'])


class Transport(Base):
    def test_http_error_keeps_status_body_and_request_id_and_no_secret(self):
        e = self.failure(self.adapter([http(400, '{"error":{"message":"Unsupported parameter"}}', {'x-request-id': 'req_1'})]))
        self.assertEqual(e.category, 'http_400'); self.assertEqual(len(self.sent), 1)
        self.assertEqual((e.accounting['http_status'], e.accounting['request_id']), (400, 'req_1'))
        self.assertIn('Unsupported parameter', e.accounting['error_body'])
        self.assertNotIn(KEY, json.dumps(e.accounting)); self.assertNotIn('Bearer', json.dumps(e.accounting))
        self.assertNotIn(KEY, (Path(self.tmp.name) / 'ledger.jsonl').read_text())

    def test_429_rate_limit_is_re_sent(self):
        api = self.adapter([http(429, RATE), ok()])
        _, acct = api.call(SYS, 'USER', 's1-001:a', validate)
        self.assertEqual(acct['attempts'], 2); self.assertEqual(self.clock.sleeps, [2])
        self.assertEqual(acct['earlier_http_status'], 429); self.assertEqual(api.billing['billing_pauses'], 0)
        e = self.failure(self.adapter([http(429, RATE) for _ in range(3)]), 's1-001:b')
        self.assertEqual((e.category, e.accounting['attempts']), ('http_429', 3))

    def test_server_errors_are_re_sent_and_others_are_not(self):
        for status in (500, 502, 503, 504):
            self.clock.sleeps.clear()
            _, acct = self.adapter([http(status), ok()]).call(SYS, 'USER', f's1-001:s{status}', validate)
            self.assertEqual(acct['attempts'], 2)
        for status in (400, 401, 403, 404, 408, 409, 422, 529):
            self.sent.clear()
            e = self.failure(self.adapter([http(status)]), f's1-001:n{status}')
            self.assertEqual((e.category, len(self.sent)), (f'http_{status}', 1))

    def test_retry_after_is_honoured_and_capped(self):
        api = self.adapter([http(429, RATE, {'retry-after': '9'}), http(503, headers={'retry-after': '300'}), ok()])
        api.call(SYS, 'USER', 's1-001:a', validate)
        self.assertEqual(self.clock.sleeps, [9, 20])

    def test_timeouts_are_never_retried(self):
        for exc, want in ((socket.timeout('t'), 'timeout'), (urllib.error.URLError('refused'), 'transport_URLError')):
            self.sent.clear()
            e = self.failure(self.adapter([exc]), 's1-001:' + want)
            self.assertEqual((e.category, len(self.sent)), (want, 1))

    def test_rate_limit_headers_are_kept_as_numbers_only(self):
        headers = {'x-ratelimit-limit-tokens': '4000000', 'x-ratelimit-remaining-tokens': '3999088', 'x-ratelimit-reset-tokens': '1ms',
                   'authorization': 'Bearer ' + KEY, 'set-cookie': 'a=b'}
        _, acct = self.adapter([(ok(), headers)]).call(SYS, 'USER', 's1-001:a', validate)
        self.assertEqual(acct['rate_limits'], {'x-ratelimit-limit-tokens': 4000000, 'x-ratelimit-remaining-tokens': 3999088})
        self.assertNotIn(KEY, json.dumps(acct))

    def test_malformed_body(self):
        e = self.failure(self.adapter([b'<html>gateway</html>']))
        self.assertEqual(e.category, 'malformed_provider_response'); self.assertIn('gateway', e.accounting['error_body'])


class Billing(Base):
    def test_detection(self):
        self.assertTrue(oap.is_billing_error(429, QUOTA)); self.assertTrue(oap.is_billing_error(402, ''))
        for status, body in ((429, '{"error":{"code":"insufficient_quota"}}'), (400, 'billing_hard_limit_reached'),
                             (403, 'Billing is not active'), (429, 'You have reached your spend limit'),
                             (429, 'monthly usage limit reached'), (400, 'Your credit balance is too low')):
            self.assertTrue(oap.is_billing_error(status, body), body)
        self.assertFalse(oap.is_billing_error(429, RATE)); self.assertFalse(oap.is_billing_error(429, 'Rate limit exceeded'))
        self.assertFalse(oap.is_billing_error(429, '')); self.assertFalse(oap.is_billing_error(500, 'quota'))
        self.assertFalse(oap.is_billing_error(400, 'invalid request'))

    def test_429_insufficient_quota_pauses_then_recovers(self):
        api = self.adapter([http(429, QUOTA) for _ in range(3)] + [ok()])
        answer, acct = api.call(SYS, 'USER', 's1-001:a', validate)
        self.assertEqual(answer, {'answer': 7}); self.assertEqual(acct['attempts'], 4)
        self.assertEqual(self.clock.sleeps, [60, 60, 60])                 # not the 2 s / 6 s rate-limit backoff
        self.assertEqual(api.billing, {'billing_pauses': 1, 'billing_pause_seconds': 180.0, 'billing_affected_calls': 1})
        self.assertFalse(api.billing_stopped()); self.assertEqual(acct['earlier_http_status'], 429)
        self.assertIn('insufficient_quota', acct['earlier_error_body'])

    def test_pause_outlasting_the_limit_stops_with_reservations_voided(self):
        api = self.adapter([http(429, QUOTA) for _ in range(40)])
        e = self.failure(api)
        self.assertEqual(e.category, oap.BILLING_STOP); self.assertEqual(e.category, 'provider_billing_stopped')
        self.assertEqual(sum(self.clock.sleeps), 1200); self.assertEqual(e.accounting['attempts'], 21)
        self.assertEqual((e.accounting['http_status'], e.accounting['voided']), (429, True))
        before = len(self.sent)
        e2 = self.failure(api, 's1-001:next')
        self.assertEqual(e2.category, oap.BILLING_STOP); self.assertEqual(len(self.sent), before)
        t = self.ledger.transact()
        self.assertEqual((t['attempted_calls'], t['voided_calls'], t['committed_usd']), (0, 1, 0.0))
        with self.assertRaises(oap.CallFailure) as cm: self.ledger.transact({'type': 'reserve', 'call_id': 's1-001:a', 'micro_usd': 1})
        self.assertEqual(cm.exception.category, 'duplicate_call_refused')
        self.ledger.transact({'type': 'reserve', 'call_id': 's1-001-r1:a', 'micro_usd': 1})

    def test_other_calls_wait_during_the_pause_and_then_complete(self):
        gate = threading.Event(); order = []
        lock = threading.Lock(); state = {'quota': 2}
        def opener(request, timeout):
            user = json.loads(request.data)['messages'][1]['content']
            with lock:
                order.append(user)
                if state['quota'] > 0:
                    state['quota'] -= 1
                    raise http(429, QUOTA)
            return Resp(json.dumps(ok()).encode())
        ledger = oap.Ledger(Path(self.tmp.name) / 'ledger.jsonl', CONFIG['budget'])
        api = oap.OpenAI(ledger, CONFIG, opener, sleep=lambda s: gate.wait(2))
        results = {}
        def run(name):
            try: results[name] = api.call(SYS, name, 's1-001:' + name, validate)[1]
            except oap.CallFailure as exc: results[name] = exc
        first = threading.Thread(target=run, args=('one',)); first.start()
        while not order: pass
        second = threading.Thread(target=run, args=('two',)); second.start()
        gate.set(); first.join(10); second.join(10)
        for name in ('one', 'two'):
            self.assertIsInstance(results[name], dict, results[name])
        self.assertEqual(api.billing['billing_pauses'], 1); self.assertEqual(ledger.transact()['usage_reported_calls'], 2)


class StubServer(Base):
    """The same adapter against a real HTTP server on 127.0.0.1 (urllib's own opener, no stub opener)."""
    def serve(self, replies):
        received = self.received = []
        class Handler(http_server.BaseHTTPRequestHandler):
            def do_POST(self):
                body = self.rfile.read(int(self.headers['Content-Length']))
                received.append({'path': self.path, 'body': json.loads(body), 'auth': self.headers.get('Authorization')})
                status, payload, headers = replies.pop(0)
                data = json.dumps(payload).encode() if not isinstance(payload, str) else payload.encode()
                self.send_response(status)
                for k, v in headers.items(): self.send_header(k, v)
                self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(data)))
                self.end_headers(); self.wfile.write(data)
            def log_message(self, *a): pass
        server = http_server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close); self.addCleanup(server.shutdown)
        url = f'http://127.0.0.1:{server.server_address[1]}/v1/chat/completions'
        patcher = patch.object(oap, 'URL', url); patcher.start(); self.addCleanup(patcher.stop)
        self.ledger = oap.Ledger(Path(self.tmp.name) / 'ledger.jsonl', CONFIG['budget'])
        return oap.OpenAI(self.ledger, CONFIG, None, self.clock.now, self.clock.sleep)

    def test_end_to_end_rate_limit_quota_then_answer(self):
        api = self.serve([(429, RATE, {'retry-after': '1'}), (429, QUOTA, {'x-request-id': 'req_q'}),
                          (200, ok(), {'x-ratelimit-remaining-requests': '9999'})])
        answer, acct = api.call(SYS, 'USER', 's1-001:a', validate)
        self.assertEqual(answer, {'answer': 7}); self.assertEqual(acct['attempts'], 3)
        self.assertEqual(self.clock.sleeps, [2, 60]); self.assertEqual(acct['earlier_request_id'], 'req_q')
        self.assertEqual(acct['rate_limits'], {'x-ratelimit-remaining-requests': 9999})
        self.assertEqual([tuple(r['body']) for r in self.received], [oap.BODY_KEYS] * 3)
        self.assertEqual({r['auth'] for r in self.received}, {'Bearer ' + KEY})
        self.assertNotIn(KEY, json.dumps(acct)); self.assertNotIn(KEY, (Path(self.tmp.name) / 'ledger.jsonl').read_text())

    def test_end_to_end_error_body_is_kept(self):
        api = self.serve([(400, {'error': {'message': "Unsupported value: 'reasoning_effort'", 'code': 'unsupported_value'}}, {})])
        e = self.failure(api)
        self.assertEqual(e.category, 'http_400'); self.assertIn('unsupported_value', e.accounting['error_body'])


class LedgerRules(Base):
    def test_caps_duplicates_and_void(self):
        b = json.loads(json.dumps(CONFIG['budget'])); b['max_calls'] = {'P0': 1, 'Q0': 2, 'S1': 3}; b['max_attempted_calls'] = 5
        ledger = oap.Ledger(Path(self.tmp.name) / 'l.jsonl', b)
        def reserve(call, usd=1): return ledger.transact({'type': 'reserve', 'call_id': call, 'micro_usd': usd})
        reserve('p0-001:a')
        for call, want in (('p0-001:a', 'duplicate_call_refused'), ('p0-001:b', 'stage_call_cap_reached')):
            with self.assertRaises(oap.CallFailure) as cm: reserve(call)
            self.assertEqual(cm.exception.category, want)
        with self.assertRaises(oap.CallFailure) as cm: ledger.transact({'type': 'void', 'call_id': 'q0-001:never'})
        self.assertEqual(cm.exception.category, 'void_refused')
        self.assertEqual([oap.family_of(x) for x in ('s1-001-r2:a', 'q0-002:b')], ['s1-001', 'q0-002'])


if __name__ == '__main__':
    unittest.main()

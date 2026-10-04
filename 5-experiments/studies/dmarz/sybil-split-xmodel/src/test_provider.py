"""Offline tests of the reference OpenRouter adapter. No network, no model call.

    python3 test_openrouter_provider.py
"""
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

import provider as orp

CONFIG = {
    'model': 'qwen/qwen3.7-flash',
    'canonical_model': 'qwen/qwen3.7-flash-20260727',
    'provider': 'alibaba',
    'request_template': {'model': 'qwen/qwen3.7-flash',
                         'provider': {'only': ['alibaba'], 'allow_fallbacks': False, 'require_parameters': True},
                         'reasoning': {'enabled': False}, 'max_tokens': 1000,
                         'response_format': {'type': 'json_object'}},
    'budget': {'max_calls': {'S0': 0, 'P0': 1, 'Q0': 23, 'S1': 504}, 'max_attempted_calls': 528,
               'aggregate_usd': 2, 'max_output_tokens': 1000, 'max_input_tokens': 8000, 'max_input_bytes': 40000,
               'max_visible_chars': 4000, 'request_timeout_seconds': 120,
               'retry': {'transport_retries': 2, 'retryable_http_status': [429, 502, 503, 529],
                         'backoff_seconds': [2, 6], 'retry_after_cap_seconds': 20},
               'billing_outage': {'retry_every_seconds': 60, 'max_wait_seconds': 1200},
               'max_transport_attempts': 640,
               'input_usd_per_million': 0.03, 'output_usd_per_million': 0.13},
}
KEY = 'sk-or-test-SECRET-0123456789'


class Resp(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False


def ok(content='{"answer": 7}', model='qwen/qwen3.7-flash-20260727', provider='Alibaba', finish='stop', usage=None, **extra):
    body = {'id': 'gen-1', 'model': model, 'provider': provider,
            'choices': [{'finish_reason': finish, 'message': {'role': 'assistant', 'content': content}}],
            'usage': usage if usage is not None else {'prompt_tokens': 900, 'completion_tokens': 12, 'total_tokens': 912}}
    body.update(extra)
    return body


def http(status, body='{"error":{"message":"x"}}', headers=None):
    return urllib.error.HTTPError(orp.URL, status, 'err', headers or {}, io.BytesIO(body.encode() if isinstance(body, str) else body))


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
        self.env = patch.dict(os.environ, {orp.KEY_ENV: KEY}); self.env.start()
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
            return Resp(json.dumps(item).encode() if not isinstance(item, bytes) else item)
        self.ledger = orp.Ledger(Path(self.tmp.name) / 'ledger.jsonl', config['budget'])
        return orp.OpenRouter(self.ledger, config, opener, self.clock.now, self.clock.sleep)

    def failure(self, api, call_id='s1-001:a'):
        with self.assertRaises(orp.CallFailure) as cm:
            api.call('SYS', 'USER', call_id, validate)
        return cm.exception


class Request(Base):
    def test_body_is_exactly_the_template_plus_messages(self):
        api = self.adapter([ok()])
        answer, acct = api.call('SYS', 'USER', 's1-001:a', validate)
        self.assertEqual(answer, {'answer': 7})
        body = self.sent[0]['body']
        self.assertEqual(tuple(body), orp.BODY_KEYS)
        self.assertEqual({k: body[k] for k in body if k != 'messages'}, CONFIG['request_template'])
        self.assertEqual(body['messages'], [{'role': 'system', 'content': 'SYS'}, {'role': 'user', 'content': 'USER'}])
        self.assertEqual(self.sent[0]['url'], 'https://openrouter.ai/api/v1/chat/completions')
        for forbidden in ('temperature', 'top_p', 'tools', 'tool_choice', 'models', 'route', 'fallbacks', 'usage', 'stream'):
            self.assertNotIn(forbidden, body)
        self.assertEqual(body['provider'], {'only': ['alibaba'], 'allow_fallbacks': False, 'require_parameters': True})
        self.assertEqual(body['reasoning'], {'enabled': False})

    def test_usage_cost_and_reservation(self):
        api = self.adapter([ok(usage={'prompt_tokens': 2000, 'completion_tokens': 300, 'cost': 0.0001})])
        _, acct = api.call('SYS', 'U' * 3000, 's1-001:a', validate)
        self.assertEqual((acct['input_tokens'], acct['output_tokens'], acct['attempts']), (2000, 300, 1))
        self.assertAlmostEqual(acct['computed_usd'], (2000 * 0.03 + 300 * 0.13) / 1e6)
        self.assertEqual(acct['provider_reported_usd'], 0.0001); self.assertEqual(acct['actual_usd'], 0.0001)
        # Byte-based upper bound (input tokens <= request bytes, full output limit) times the 10x margin.
        bound = acct['request_bytes'] * 0.03 + 1000 * 0.13
        self.assertGreaterEqual(acct['reserved_usd'] * 1e6, 10 * bound - 1e-6); self.assertLess(acct['reserved_usd'] * 1e6, 10 * bound + 1)
        self.assertGreater(acct['request_bytes'], 3000)
        t = self.ledger.transact()
        self.assertEqual((t['attempted_calls'], t['usage_reported_calls'], t['transport_attempts']), (1, 1, 1))
        self.assertAlmostEqual(t['committed_usd'], 0.0001)

    def test_cost_is_computed_when_the_provider_reports_none(self):
        api = self.adapter([ok()])
        _, acct = api.call('SYS', 'USER', 's1-001:a', validate)
        self.assertIsNone(acct['provider_reported_usd'])
        self.assertAlmostEqual(acct['actual_usd'], 29e-6)      # 900*0.03 + 12*0.13 = 28.56 micro-dollars, rounded up to 29
        self.assertGreaterEqual(acct['actual_usd'], acct['computed_usd'] - 1e-12)

    def test_reported_cost_three_times_the_snapshot_is_inside_the_margin(self):
        # 900 input and 12 output tokens are 28.56 micro-dollars at the snapshot; the provider reports three times that.
        api = self.adapter([ok(usage={'prompt_tokens': 900, 'completion_tokens': 12, 'cost': 0.0000857})])
        _, acct = api.call('SYS', 'U' * 900, 's1-001:a', validate)
        self.assertAlmostEqual(acct['actual_usd'], 0.000086)

    def test_reported_cost_above_the_reservation_is_an_integrity_failure(self):
        e = self.failure(self.adapter([ok(usage={'prompt_tokens': 10, 'completion_tokens': 5, 'cost': 1.0})]))
        self.assertEqual(e.category, 'reservation_bound_breached'); self.assertIn(e.category, orp.INTEGRITY)

    def test_model_and_provider_are_checked(self):
        self.assertEqual(self.failure(self.adapter([ok(model='qwen/qwen3.7-plus')])).category, 'model_mismatch')
        self.assertEqual(self.failure(self.adapter([ok(provider='DeepInfra')]), 's1-001:b').category, 'provider_mismatch')
        api = self.adapter([ok(model='qwen/qwen3.7-flash')])
        api.call('SYS', 'USER', 's1-001:c', validate)
        # A response that does not name its provider fails; a probe cannot pass without it.
        for i, missing in enumerate((None, '', 17)):
            e = self.failure(self.adapter([ok(provider=missing)]), f's1-001:m{i}')
            self.assertEqual(e.category, 'provider_missing'); self.assertIn(e.category, orp.INTEGRITY)
        self.assertEqual(self.failure(self.adapter([{k: v for k, v in ok().items() if k != 'provider'}]), 's1-001:m9').category, 'provider_missing')

    def test_missing_credential(self):
        with patch.dict(os.environ, {orp.KEY_ENV: ''}):
            with self.assertRaises(orp.CallFailure) as cm: self.adapter([])
        self.assertEqual(cm.exception.category, 'missing_credential_alias')

    def test_input_size_limit_is_refused_before_any_reservation(self):
        api = self.adapter([])
        with self.assertRaises(orp.CallFailure) as cm: api.call('SYS', 'U' * 50000, 's1-001:big', validate)
        self.assertEqual(cm.exception.category, 'input_size_limit'); self.assertEqual(self.sent, [])
        self.assertEqual(self.ledger.transact()['attempted_calls'], 0)


class Answers(Base):
    def category(self, response, call_id='s1-001:a'):
        return self.failure(self.adapter([response]), call_id)

    def test_answer_failure_categories_are_distinct_and_never_retried(self):
        cases = {
            'refusal': ok(finish='content_filter'),
            'truncated_output': ok(finish='length'),
            'empty_answer': ok(content='   '),
            'invalid_json': ok(content='{"answer": 7'),
            'invalid_json ': ok(content='{"answer": 7, "answer": 8}'),
            'invalid_answer': ok(content='{"answer": "seven"}'),
            'answer_too_long': ok(content='{"answer": 7}' + ' ' * 5000),
            'nonterminal_output': ok(finish='tool_calls'),
            'missing_usage': ok(usage={}),
            'unexpected_reasoning_tokens': ok(usage={'prompt_tokens': 10, 'completion_tokens': 5,
                                                     'completion_tokens_details': {'reasoning_tokens': 3}}),
        }
        for want, response in cases.items():
            self.sent.clear()
            e = self.category(response, 's1-001:' + want.replace(' ', '2'))
            self.assertEqual(e.category, want.strip()); self.assertEqual(len(self.sent), 1, want)
            self.assertEqual(e.accounting['attempts'], 1)
        # More than 8,000 input tokens (the request must be that large for the byte-based reservation to hold).
        api = self.adapter([ok(usage={'prompt_tokens': 8001, 'completion_tokens': 5})])
        with self.assertRaises(orp.CallFailure) as cm: api.call('SYS', 'U' * 9000, 's1-001:ceiling', validate)
        self.assertEqual(cm.exception.category, 'input_ceiling_exceeded')
        refused = ok(); refused['choices'][0]['message']['refusal'] = 'I cannot help with that.'
        self.assertEqual(self.category(refused, 's1-001:r2').category, 'refusal')
        none = ok(); none['choices'] = []
        self.assertEqual(self.category(none, 's1-001:r3').category, 'empty_answer')

    def test_invalid_answers_keep_the_text_for_reading(self):
        e = self.category(ok(content='{"answer": "seven"}'))
        self.assertEqual(e.accounting['answer_text'], '{"answer": "seven"}')
        self.assertTrue(e.accounting['usage_reported'])

    def test_zero_reasoning_tokens_are_fine(self):
        api = self.adapter([ok(usage={'prompt_tokens': 10, 'completion_tokens': 5, 'completion_tokens_details': {'reasoning_tokens': 0}})])
        api.call('SYS', 'USER', 's1-001:a', validate)


class Transport(Base):
    def test_http_error_keeps_status_body_and_request_id_and_no_secret(self):
        e = self.failure(self.adapter([http(500, '{"error":{"message":"upstream exploded"}}', {'x-request-id': 'req_1'})]))
        self.assertEqual(e.category, 'http_500'); self.assertEqual(len(self.sent), 1)
        self.assertEqual((e.accounting['http_status'], e.accounting['request_id']), (500, 'req_1'))
        self.assertIn('upstream exploded', e.accounting['error_body'])
        self.assertNotIn(KEY, json.dumps(e.accounting)); self.assertNotIn('Bearer', json.dumps(e.accounting))
        self.assertNotIn(KEY, (Path(self.tmp.name) / 'ledger.jsonl').read_text())

    def test_body_is_truncated(self):
        e = self.failure(self.adapter([http(400, 'x' * 9000)]))
        self.assertEqual(len(e.accounting['error_body']), 2000); self.assertEqual(e.category, 'http_400')

    def test_retry_only_on_429_and_overload(self):
        api = self.adapter([http(429), ok()])
        _, acct = api.call('SYS', 'USER', 's1-001:a', validate)
        self.assertEqual(acct['attempts'], 2); self.assertEqual(self.clock.sleeps, [2])
        self.assertEqual(acct['earlier_http_status'], 429)       # evidence of the recovered attempt is kept
        self.clock.sleeps.clear()
        api = self.adapter([http(503), http(529), ok()])
        _, acct = api.call('SYS', 'USER', 's1-001:b', validate)
        self.assertEqual(acct['attempts'], 3); self.assertEqual(self.clock.sleeps, [2, 6])
        e = self.failure(self.adapter([http(429), http(429), http(429)]), 's1-001:c')
        self.assertEqual((e.category, e.accounting['attempts']), ('http_429', 3))
        for status in (400, 401, 403, 404, 408, 500):
            self.sent.clear()
            e = self.failure(self.adapter([http(status)]), f's1-001:s{status}')
            self.assertEqual((e.category, len(self.sent)), (f'http_{status}', 1))

    def test_retry_after_is_honoured_and_capped(self):
        api = self.adapter([http(429, headers={'retry-after': '9'}), http(429, headers={'retry-after': '300'}), ok()])
        api.call('SYS', 'USER', 's1-001:a', validate)
        self.assertEqual(self.clock.sleeps, [9, 20])

    def test_timeouts_and_other_transport_errors_are_never_retried(self):
        for exc, want in ((socket.timeout('t'), 'timeout'), (TimeoutError('t'), 'timeout'),
                          (urllib.error.URLError(socket.timeout('t')), 'timeout'),
                          (urllib.error.URLError('refused'), 'transport_URLError'),
                          (ConnectionResetError('reset'), 'transport_ConnectionResetError')):
            self.sent.clear()
            e = self.failure(self.adapter([exc]), 's1-001:' + want + str(id(exc)))
            self.assertEqual((e.category, len(self.sent)), (want, 1))

    def test_retries_stay_inside_the_request_timeout(self):
        config = json.loads(json.dumps(CONFIG)); config['budget']['request_timeout_seconds'] = 5
        e = self.failure(self.adapter([http(429), http(429)], config))
        self.assertEqual((e.category, e.accounting['attempts']), ('http_429', 2))    # 2 s, then 6 s would pass the deadline

    def test_error_object_in_a_200_response(self):
        api = self.adapter([{'error': {'code': 502, 'message': 'provider returned error'}}, ok()])
        _, acct = api.call('SYS', 'USER', 's1-001:a', validate)
        self.assertEqual(acct['attempts'], 2)
        e = self.failure(self.adapter([{'error': {'code': 400, 'message': 'bad request'}}]), 's1-001:b')
        self.assertEqual(e.category, 'http_400'); self.assertIn('bad request', e.accounting['error_body'])
        e = self.failure(self.adapter([{'error': {'message': 'no code'}}]), 's1-001:c')
        self.assertEqual(e.category, 'provider_error_200')

    def test_malformed_body(self):
        e = self.failure(self.adapter([b'<html>gateway</html>']))
        self.assertEqual(e.category, 'malformed_provider_response'); self.assertIn('gateway', e.accounting['error_body'])


class Billing(Base):
    CREDIT = '{"error":{"code":402,"message":"Insufficient credits. Add more using https://openrouter.ai/credits"}}'

    def test_detection(self):
        self.assertTrue(orp.is_billing_error(402, ''))
        self.assertTrue(orp.is_billing_error(400, 'Your credit balance is too low'))
        self.assertTrue(orp.is_billing_error(403, 'Key limit exceeded: insufficient Balance'))
        for status, body in ((400, 'This request would exceed your usage limits'), (429, 'You have reached your spend limit'),
                             (429, 'Rate limit exceeded: free-models-per-day'), (403, 'Billing is not enabled'),
                             (400, 'Insufficient funds'), (429, "You're out of usage credits")):
            self.assertTrue(orp.is_billing_error(status, body), body)
        self.assertFalse(orp.is_billing_error(400, 'invalid request')); self.assertFalse(orp.is_billing_error(429, 'Too many requests'))
        self.assertFalse(orp.is_billing_error(500, 'credit')); self.assertFalse(orp.is_billing_error(429, ''))

    def test_outage_then_success_is_one_pause_and_no_failed_call(self):
        api = self.adapter([http(402, self.CREDIT)] * 3 + [ok()])
        answer, acct = api.call('SYS', 'USER', 's1-001:a', validate)
        self.assertEqual(answer, {'answer': 7}); self.assertEqual(acct['attempts'], 4)
        self.assertEqual(self.clock.sleeps, [60, 60, 60])
        self.assertEqual(api.billing, {'billing_pauses': 1, 'billing_pause_seconds': 180.0, 'billing_affected_calls': 1})
        self.assertFalse(api.billing_stopped()); self.assertTrue(acct['billing_paused'])
        t = self.ledger.transact()
        self.assertEqual((t['attempted_calls'], t['transport_attempts'], t['usage_reported_calls']), (1, 4, 1))

    def test_credit_error_reported_as_400_or_inside_a_200(self):
        api = self.adapter([http(400, '{"error":{"message":"Your credit balance is too low"}}'),
                            {'error': {'code': 402, 'message': 'Insufficient credits'}}, ok()])
        _, acct = api.call('SYS', 'USER', 's1-001:a', validate)
        self.assertEqual(acct['attempts'], 3); self.assertEqual(api.billing['billing_pauses'], 1)

    def test_outage_outlasting_the_limit_stops_with_the_distinct_category(self):
        api = self.adapter([http(402, self.CREDIT)] * 40)
        e = self.failure(api)
        self.assertEqual(e.category, orp.BILLING_STOP); self.assertEqual(e.category, 'provider_credit_balance_low')
        self.assertEqual(sum(self.clock.sleeps), 1200); self.assertEqual(e.accounting['attempts'], 21)
        self.assertTrue(api.billing_stopped()); self.assertEqual(api.billing['billing_pause_seconds'], 1200.0)
        before = len(self.sent)
        e2 = self.failure(api, 's1-001:next')                       # nothing further is sent or reserved
        self.assertEqual(e2.category, orp.BILLING_STOP); self.assertEqual(len(self.sent), before)
        self.assertFalse(e2.accounting['attempted'])
        # The unanswered call's reservation is voided: no model ran, so it frees its place under the caps.
        t = self.ledger.transact()
        self.assertEqual((t['attempted_calls'], t['voided_calls'], t['calls_by_stage'].get('S1', 0), t['committed_usd']), (0, 1, 0, 0.0))
        self.assertTrue(e.accounting['voided'])
        with self.assertRaises(orp.CallFailure) as cm: self.ledger.transact({'type': 'reserve', 'call_id': 's1-001:a', 'micro_usd': 1})
        self.assertEqual(cm.exception.category, 'duplicate_call_refused')       # the same call id is never reused
        self.ledger.transact({'type': 'reserve', 'call_id': 's1-001-r1:a', 'micro_usd': 1})   # its continuation is admitted

    def test_a_limit_refusal_on_429_pauses_instead_of_failing_the_call(self):
        limit = '{"error":{"message":"This request would exceed your usage limits"}}'
        api = self.adapter([http(429, limit), http(429, limit), http(429, limit), http(429, limit), ok()])
        _, acct = api.call('SYS', 'USER', 's1-001:a', validate)
        self.assertEqual(acct['attempts'], 5); self.assertEqual(self.clock.sleeps, [60, 60, 60, 60])
        self.assertEqual(api.billing['billing_pauses'], 1)

    def test_retry_rule_applies_again_after_the_outage(self):
        api = self.adapter([http(402, self.CREDIT), http(429), ok()])
        _, acct = api.call('SYS', 'USER', 's1-001:a', validate)
        self.assertEqual(acct['attempts'], 3); self.assertEqual(self.clock.sleeps[0], 60)

    def test_other_calls_wait_during_the_pause_and_then_complete(self):
        gate = threading.Event(); order = []
        lock = threading.Lock(); state = {'credit': 2}
        def opener(request, timeout):
            user = json.loads(request.data)['messages'][1]['content']
            with lock:
                order.append(user)
                if state['credit'] > 0:
                    state['credit'] -= 1
                    raise http(402, self.CREDIT)
            return Resp(json.dumps(ok()).encode())
        def sleep(seconds):
            gate.wait(2)                                         # the owner's wait: until the second call has arrived
        ledger = orp.Ledger(Path(self.tmp.name) / 'ledger.jsonl', CONFIG['budget'])
        api = orp.OpenRouter(ledger, CONFIG, opener, sleep=sleep)
        results = {}
        def run(name):
            try: results[name] = api.call('SYS', name, 's1-001:' + name, validate)[1]
            except orp.CallFailure as exc: results[name] = exc
        first = threading.Thread(target=run, args=('one',)); first.start()
        while not order: pass
        second = threading.Thread(target=run, args=('two',)); second.start()
        gate.set(); first.join(10); second.join(10)
        self.assertFalse(first.is_alive() or second.is_alive())
        for name in ('one', 'two'):
            self.assertIsInstance(results[name], dict, results[name]); self.assertTrue(results[name]['usage_reported'])
        self.assertEqual(api.billing['billing_pauses'], 1)
        self.assertEqual(ledger.transact()['usage_reported_calls'], 2)


class LedgerRules(Base):
    def test_caps_and_duplicates(self):
        b = json.loads(json.dumps(CONFIG['budget'])); b['max_calls'] = {'P0': 1, 'Q0': 2, 'S1': 3}; b['max_attempted_calls'] = 5
        b['max_transport_attempts'] = 2
        ledger = orp.Ledger(Path(self.tmp.name) / 'l.jsonl', b)
        def reserve(call, usd=1): return ledger.transact({'type': 'reserve', 'call_id': call, 'micro_usd': usd})
        def refused(call, usd=1):
            with self.assertRaises(orp.CallFailure) as cm: reserve(call, usd)
            return cm.exception.category
        reserve('p0-001:a'); self.assertEqual(refused('p0-001:a'), 'duplicate_call_refused')
        self.assertEqual(refused('p0-001:b'), 'stage_call_cap_reached')
        self.assertEqual(refused('s2-001:a'), 'stage_call_cap_reached')          # unknown stage has no allowance
        reserve('q0-001:a'); reserve('q0-001:b'); reserve('s1-001:a')
        self.assertEqual(refused('s1-001:big', 2_000_001), 'aggregate_budget_exhausted')
        reserve('s1-001-r1:b')                                                    # a continuation batch counts as S1
        self.assertEqual(refused('s1-001:c'), 'study_call_cap_reached')
        with self.assertRaises(orp.CallFailure) as cm: ledger.transact({'type': 'attempt', 'call_id': 'nope'})
        self.assertEqual(cm.exception.category, 'attempt_without_reservation')
        ledger.transact({'type': 'attempt', 'call_id': 'p0-001:a'}); ledger.transact({'type': 'attempt', 'call_id': 'p0-001:a'})
        with self.assertRaises(orp.CallFailure) as cm: ledger.transact({'type': 'attempt', 'call_id': 'p0-001:a'})
        self.assertEqual(cm.exception.category, 'transport_attempt_cap_reached')
        t = ledger.transact()
        self.assertEqual(t['calls_by_stage'], {'P0': 1, 'Q0': 2, 'S1': 2}); self.assertEqual(t['transport_attempts'], 2)

    def test_settled_cost_replaces_the_reservation(self):
        ledger = orp.Ledger(Path(self.tmp.name) / 'l.jsonl', CONFIG['budget'])
        ledger.transact({'type': 'reserve', 'call_id': 's1-001:a', 'micro_usd': 1_500_000})
        with self.assertRaises(orp.CallFailure): ledger.transact({'type': 'reserve', 'call_id': 's1-001:b', 'micro_usd': 600_000})
        ledger.transact({'type': 'response', 'call_id': 's1-001:a', 'actual_micro_usd': 100, 'input_tokens': 5, 'output_tokens': 1})
        ledger.transact({'type': 'reserve', 'call_id': 's1-001:b', 'micro_usd': 600_000})
        self.assertAlmostEqual(ledger.transact()['committed_usd'], 0.6001)

    def test_ledger_file_is_private_and_a_corrupt_line_fails_closed(self):
        path = Path(self.tmp.name) / 'l.jsonl'
        ledger = orp.Ledger(path, CONFIG['budget']); ledger.transact({'type': 'reserve', 'call_id': 's1-001:a', 'micro_usd': 1})
        self.assertEqual(oct(path.stat().st_mode & 0o777), '0o600')
        with path.open('a') as f: f.write('{"type": "reser')
        with self.assertRaises(Exception): ledger.transact()

    def test_stage_caps_are_per_batch_family_and_the_study_cap_is_global(self):
        b = json.loads(json.dumps(CONFIG['budget'])); b['max_calls'] = {'P0': 1, 'Q0': 2, 'S1': 3}; b['max_attempted_calls'] = 6
        ledger = orp.Ledger(Path(self.tmp.name) / 'f.jsonl', b)
        def reserve(call): return ledger.transact({'type': 'reserve', 'call_id': call, 'micro_usd': 1})
        def refused(call):
            with self.assertRaises(orp.CallFailure) as cm: reserve(call)
            return cm.exception.category
        reserve('p0-001:a'); reserve('q0-001:a'); reserve('q0-001:b')
        self.assertEqual(refused('q0-001:c'), 'stage_call_cap_reached')
        reserve('p0-002:a'); reserve('q0-002:a')                       # a repair attempt has its own allowance
        self.assertEqual(refused('p0-002:b'), 'stage_call_cap_reached')
        reserve('q0-002:b')
        self.assertEqual(refused('s1-002:a'), 'study_call_cap_reached')  # the study cap counts every attempt
        self.assertEqual(ledger.transact()['calls_by_batch'], {'p0-001': 1, 'q0-001': 2, 'p0-002': 1, 'q0-002': 2})
        self.assertEqual([orp.family_of(x) for x in ('s1-001:a', 's1-001-r1:a', 's1-001-r12:b', 'q0-002:c')], ['s1-001', 's1-001', 's1-001', 'q0-002'])

    def test_void_rules(self):
        ledger = orp.Ledger(Path(self.tmp.name) / 'v.jsonl', CONFIG['budget'])
        ledger.transact({'type': 'reserve', 'call_id': 's1-001:a', 'micro_usd': 5})
        ledger.transact({'type': 'response', 'call_id': 's1-001:a', 'actual_micro_usd': 2, 'input_tokens': 1, 'output_tokens': 1})
        for call in ('s1-001:a', 's1-001:never'):                                 # answered or unknown calls cannot be voided
            with self.assertRaises(orp.CallFailure) as cm: ledger.transact({'type': 'void', 'call_id': call})
            self.assertEqual(cm.exception.category, 'void_refused')

    def test_stage_of(self):
        self.assertEqual([orp.stage_of(x) for x in ('p0-001:a', 'q0-002:b', 's1-001-r2:c')], ['P0', 'Q0', 'S1'])


if __name__ == '__main__':
    unittest.main()

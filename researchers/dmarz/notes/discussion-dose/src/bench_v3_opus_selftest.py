"""Offline checks for bench_v3_opus: worlds, request contract, response parsing, chain gating. No network."""
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import urllib.error

os.environ.setdefault('SWARM_MODEL_API_KEY', 'offline-test-key')
import bench_v3_opus as bo
from providers import ProviderFailure


class FakeResponse(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False


def reply(content, stop='end_turn', model=bo.MODEL, usage=None):
    body = {'model': model, 'stop_reason': stop, 'content': content,
            'usage': usage or {'input_tokens': 1000, 'output_tokens': 200}}
    return FakeResponse(json.dumps(body).encode())


class FakeHub:
    def __init__(self): self.events = []; self.known = []
    def runs(self, experiment, limit=5000): return list(self.known)
    def register(self, experiment, **spec): self.events.append(('register', experiment))
    def start(self, experiment, run, params, message):
        self.known.append({'run': run}); hub = self
        class Run:
            def progress(self, *a, **k): hub.events.append(('progress', run, k.get('message')))
            def artifact(self, *a, **k): return {}
            def done(self, **k): hub.events.append(('done', run, k))
            def fail(self, **k): hub.events.append(('fail', run, k))
        return Run()


class Tests(unittest.TestCase):
    def test_worlds_fresh_and_balanced(self):
        q0 = bo.stage_cases('q0'); s1 = bo.stage_cases('s1')
        ids = [c['id'] for c in q0 + s1]
        self.assertEqual(len(ids), len(set(ids)))
        for bad in (range(20001, 20007), range(30000, 30024), range(40001, 40013), range(50001, 50007), range(52001, 52013), range(10002, 10008)):
            self.assertFalse(set(ids) & set(bad))
        self.assertEqual(bo.planned_calls('q0'), 636)
        self.assertEqual(bo.planned_calls('s1'), 2436)
        for cases, n in ((q0, 3), (s1, 12)):
            res = [c for c in cases if c['stratum'] == 'resolvable']
            self.assertEqual(len(res), n)
            self.assertEqual(sorted(c['family'] for c in res), sorted(c['family'] for c in cases if c['stratum'] == 'ambiguous'))

    def test_request_contract(self):
        p = bo.Opus(5, 10.0)
        request, _ = bo.probe_request()
        body = p.request_body(request)
        self.assertEqual(body['model'], 'claude-opus-5-5')
        for banned in ('temperature', 'top_p', 'top_k', 'tool_choice', 'fallbacks'):
            self.assertNotIn(banned, body)
        self.assertEqual(body['thinking'], {'type': 'adaptive'})
        self.assertEqual(body['output_config']['effort'], 'high')
        self.assertEqual(body['output_config']['format']['type'], 'json_schema')
        self.assertEqual(body['max_tokens'], 16000)
        self.assertEqual(body['messages'][-1]['role'], 'user')

    def test_parses_text_after_thinking(self):
        p = bo.Opus(5, 10.0)
        request, _ = bo.probe_request()
        with mock.patch('urllib.request.urlopen', return_value=reply([{'type': 'thinking', 'thinking': ''}, {'type': 'text', 'text': '{"value": 51}'}])):
            self.assertEqual(p.complete(request), {'value': 51})
        acct = p.accounting()
        self.assertEqual(acct['input_tokens'], 1000); self.assertAlmostEqual(acct['cost_usd'], (1000 * 4 + 200 * 20) / 1e6)
        self.assertEqual(acct['usage_missing_calls'], 0)

    def test_refusal_mismatch_truncation_http(self):
        request, _ = bo.probe_request()
        cases = [(reply([{'type': 'text', 'text': '{}'}], stop='refusal'), 'provider_schema_refusal'),
                 (reply([{'type': 'text', 'text': '{"value": 1}'}], stop='max_tokens'), 'provider_incomplete'),
                 (reply([{'type': 'text', 'text': '{"value": 1}'}], model='claude-sonnet-4-6'), 'provider_model_mismatch'),
                 (reply([{'type': 'text', 'text': 'x' * 9000}]), 'provider_incomplete'),
                 (reply([{'type': 'text', 'text': '{"value": 1}'}, {'type': 'text', 'text': '{"value": 2}'}]), 'provider_schema_refusal')]
        for response, reason in cases:
            p = bo.Opus(5, 10.0)
            with mock.patch('urllib.request.urlopen', return_value=response):
                with self.assertRaises(ProviderFailure) as ctx: p.complete(request)
            self.assertEqual(ctx.exception.public_reason, reason)
        p = bo.Opus(5, 10.0)
        err = urllib.error.HTTPError('u', 400, 'bad', {}, io.BytesIO(b'{"error":{"message":"thinking disabled"}}'))
        with mock.patch('urllib.request.urlopen', side_effect=err):
            with self.assertRaises(ProviderFailure) as ctx: p.complete(request)
        self.assertEqual(ctx.exception.public_reason, 'provider_http_400')
        p = bo.Opus(5, 10.0)
        with mock.patch('urllib.request.urlopen', return_value=reply([{'type': 'text', 'text': '{}'}], stop='refusal')):
            with self.assertRaises(ProviderFailure): p.complete(request)
        self.assertEqual(p.refusals, 1)

    def test_call_and_cost_caps(self):
        request, _ = bo.probe_request()
        p = bo.Opus(1, 10.0)
        with mock.patch('urllib.request.urlopen', return_value=reply([{'type': 'text', 'text': '{"value": 1}'}])):
            p.complete(request)
        with self.assertRaises(ProviderFailure): p.complete(request)
        p = bo.Opus(5, 0.01)
        with self.assertRaises(ProviderFailure) as ctx: p.complete(request)
        self.assertEqual(ctx.exception.public_reason, 'provider_local_limit')

    def test_transport_retry_rules(self):
        request, _ = bo.probe_request()
        def http(code, retry_after=None):
            headers = {'retry-after': retry_after} if retry_after else {}
            return urllib.error.HTTPError('u', code, 'x', headers, io.BytesIO(b'{}'))
        ok = lambda: reply([{'type': 'text', 'text': '{"value": 1}'}])
        # 429 then success: one retry, two attempts reserved, one logical call.
        p = bo.Opus(5, 10.0); p.sleep = lambda s: None
        with mock.patch('urllib.request.urlopen', side_effect=[http(429, '1'), ok()]):
            self.assertEqual(p.complete(request), {'value': 1})
        a = p.accounting(); self.assertEqual((a['calls'], a['attempts'], a['transport_retries']), (1, 2, 1))
        one = p.reserved_usd / 2
        self.assertGreater(one, 0)
        # 529 three times: two retries then fail closed.
        p = bo.Opus(5, 10.0); p.sleep = lambda s: None
        with mock.patch('urllib.request.urlopen', side_effect=[http(529), http(529), http(529), ok()]):
            with self.assertRaises(ProviderFailure) as ctx: p.complete(request)
        self.assertEqual(ctx.exception.public_reason, 'provider_http_529'); self.assertEqual(p.attempts, 3)
        # 500 and 400 are never retried.
        for code in (500, 400, 408):
            p = bo.Opus(5, 10.0); p.sleep = lambda s: None
            with mock.patch('urllib.request.urlopen', side_effect=[http(code), ok()]):
                with self.assertRaises(ProviderFailure): p.complete(request)
            self.assertEqual(p.attempts, 1)
        # A model answer (refusal, truncation) is never retried.
        p = bo.Opus(5, 10.0); p.sleep = lambda s: None
        with mock.patch('urllib.request.urlopen', side_effect=[reply([{'type': 'text', 'text': '{}'}], stop='refusal'), ok()]):
            with self.assertRaises(ProviderFailure): p.complete(request)
        self.assertEqual(p.attempts, 1)
        # Attempt cap binds retries.
        p = bo.Opus(5, 10.0); p.sleep = lambda s: None; p.max_attempts = 1
        with mock.patch('urllib.request.urlopen', side_effect=[http(429), ok()]):
            with self.assertRaises(ProviderFailure) as ctx: p.complete(request)
        self.assertEqual(p.attempts, 1)
        # Retry must fit inside the request timeout window.
        p = bo.Opus(5, 10.0); p.sleep = lambda s: None; p.timeout = 2
        with mock.patch('urllib.request.urlopen', side_effect=[http(429, '30'), ok()]):
            with self.assertRaises(ProviderFailure): p.complete(request)
        self.assertEqual(p.attempts, 1)

    def test_clean_first_order(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'q0'
            bo.run_stage(out, 'q0', bo.Scripted())
            events = [json.loads(l) for l in (out / 'events.jsonl').read_text().splitlines()]
            starts = [e['label'] for e in events if e['kind'] == 'call_start']
            gate_index = next(i for i, e in enumerate(events) if e['kind'] == 'early_gate')
            before = [e['label'] for e in events[:gate_index] if e['kind'] == 'call_start']
            self.assertEqual(len(before), 66)
            self.assertTrue(all(l.split(':')[1] == '0' and l.split(':')[2] in ('acquisition', 'report_snapshot', 'reports', 'diagnostic') for l in before))
            self.assertEqual(len(starts), 636)
            self.assertTrue(events[gate_index]['passed'])

    def test_scripted_q0_runs_and_audits(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'q0'
            summary = bo.run_stage(out, 'q0', bo.Scripted())
            self.assertTrue(summary['qualification']['execution_complete'])
            self.assertFalse(summary['qualification']['model_qualified'])  # scripted is never scientific
            self.assertTrue(bo.audit(out)['ok'])

    def test_chain_stops_on_failed_probe(self):
        with tempfile.TemporaryDirectory() as d:
            launch = self.launch(Path(d))
            hub = FakeHub()
            err = urllib.error.HTTPError('u', 400, 'bad', {}, io.BytesIO(b'{}'))
            with mock.patch('urllib.request.urlopen', side_effect=err):
                state = bo.chain(hub, launch, Path(d) / 'out', 'test')
            self.assertEqual(state['stopped'], 'probe failed')
            self.assertFalse(any(e[0] == 'register' for e in hub.events))

    def test_chain_stops_on_failed_q0_gate(self):
        with tempfile.TemporaryDirectory() as d:
            launch = self.launch(Path(d)); hub = FakeHub()
            calls = {'n': 0}
            def fake(req, timeout):
                calls['n'] += 1
                # Probe passes; every Q0 call fails -> execution complete but not qualified.
                if calls['n'] == 1: return reply([{'type': 'text', 'text': json.dumps(self.probe_answer())}])
                return reply([{'type': 'text', 'text': '{}'}], stop='refusal')
            with mock.patch('urllib.request.urlopen', side_effect=fake):
                state = bo.chain(hub, launch, Path(d) / 'out', 'test')
            self.assertEqual(state['stopped'], 'Q0 gate failed; S1 not started')
            self.assertNotIn('s1', state['stages'])
            # Clean-first: the gate is decided after 66 calls and the rest is never dispatched.
            self.assertEqual(state['stages']['q0']['accounting']['refusals'], 66)
            self.assertEqual(calls['n'], 67)
            self.assertTrue(any(e[0] == 'done' and 'stopped early' in e[2]['message'] for e in hub.events))

    def probe_answer(self):
        request, expected = bo.probe_request()
        source = request['context']['memory'][0]['sources']
        return {'value': expected, 'sources': source}

    def test_probe_accepts_valid_parent_answer_and_rejects_bad(self):
        with tempfile.TemporaryDirectory() as d:
            p = bo.Opus(1, 1.0)
            with mock.patch('urllib.request.urlopen', return_value=reply([{'type': 'thinking', 'thinking': ''}, {'type': 'text', 'text': json.dumps(self.probe_answer())}])):
                ok, record = bo.run_probe(p, Path(d))
            self.assertTrue(ok, record)
        with tempfile.TemporaryDirectory() as d:
            p = bo.Opus(1, 1.0)
            with mock.patch('urllib.request.urlopen', return_value=reply([{'type': 'text', 'text': '{"value": 51, "sources": ["not-a-source"]}'}])):
                ok, record = bo.run_probe(p, Path(d))
            self.assertFalse(ok)

    def launch(self, folder):
        evidence = folder / 'auth.md'; evidence.write_text('owner waiver')
        import hashlib
        record = {'status': 'owner-waived-opus-chain', 'experiment': bo.EXPERIMENT, 'model': bo.MODEL,
                  'configuration': bo.CONFIG, 'source_hashes': bo.source_hashes(),
                  'stages': {'q0': {'max_calls': 636, 'max_cost_usd': 1000}, 's1': {'max_calls': 2436, 'max_cost_usd': 2000}},
                  'owner_authorization': {'path': 'auth.md', 'sha256': hashlib.sha256(evidence.read_bytes()).hexdigest()}}
        path = folder / 'launch.json'; path.write_text(json.dumps(record)); return path


if __name__ == '__main__': unittest.main(verbosity=1)

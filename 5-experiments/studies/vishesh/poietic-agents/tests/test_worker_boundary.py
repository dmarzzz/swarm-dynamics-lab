"""Rehearse worker failure closeout with fake transport/reporting and development worlds."""
import io
import json
import contextlib
from pathlib import Path
import sqlite3
import sys
import tempfile
import threading
import time
from types import SimpleNamespace
import unittest
import urllib.error
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE/'src'))
import launch
from common import canonical
from qualification import make_case


class WorkerBoundaryTests(unittest.TestCase):
    def rehearse(self, provider_result, expected_settlement='uncertain', expected_nano=None):
        dispatches = []
        completions = []

        class FakeProvider:
            def open(self, request, **kwargs):
                dispatches.append(json.loads(request.data))
                if isinstance(provider_result, Exception):
                    raise provider_result
                return io.BytesIO(canonical(provider_result).encode())

        class FakeRun:
            def __init__(self, run_id, *args):
                self.run_id = run_id
                self._alive = threading.Event()

            def progress(self, *args, **kwargs):
                return True

            def artifact(self, *args, **kwargs):
                return {'spooled': False}

            def done(self, **kwargs):
                completions.append((self.run_id, 'done'))

            def fail(self, **kwargs):
                completions.append((self.run_id, 'failed'))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root/'config.json'
            config.write_text(json.dumps({
                'attempt': 'S0-02', 'source_commit': 'fixture', 'file_hashes': {},
                'allocation': {'host': 'fixture', 'allocated_usd_per_hour': .1},
                'authorization': {'deadline': time.time()+120},
                'credential': {'relay_url': 'http://127.0.0.1:1/invoke'},
                'condition_tldrs': {role: 'SCRIPTED OFFLINE FIXTURE' for role in launch.ROLES},
            }))

            def private_path(value):
                return root/'authority' if value == '/srv/swarm/poietic-agents-authority' else Path(value)

            fake_reporter = SimpleNamespace(Run=FakeRun, report=lambda *args, **kwargs: True)
            # Only admission/network/reporting dependencies are mocked. The actual run loop,
            # response parser, reservations, assigned reconciliation and final rendering execute.
            with patch.object(launch, 'verify'), patch.object(launch, 'source_check'), \
                 patch.object(launch, 'verify_public', return_value={}), \
                 patch.object(launch, 'verify_catalog', return_value={}), \
                 patch.object(launch, 'verify_relay_health'), \
                 patch.object(launch, 'read_json', return_value={}), \
                 patch.object(launch.urllib.request, 'build_opener', return_value=FakeProvider()), \
                 patch.object(launch, 'Path', side_effect=private_path), \
                 patch.object(launch, 'make_case', side_effect=lambda case: make_case(case, development=True)), \
                 patch.dict(sys.modules, {'swarm_report': fake_reporter}), \
                 patch.dict(launch.os.environ, {}):
                with contextlib.redirect_stdout(io.StringIO()):
                    launch.run(config, root/'out')

            records = json.loads((root/'out/records.json').read_text())
            summary = json.loads((root/'out/summary.json').read_text())
            starts = (root/'out/call-starts.jsonl').read_text().splitlines()
            with contextlib.closing(sqlite3.connect(root/'authority/budget.sqlite')) as db:
                charges = db.execute('SELECT status,settled FROM charges').fetchall()
            self.assertEqual(len(dispatches), 1)
            self.assertEqual(len(starts), 1)
            self.assertEqual(charges, [(expected_settlement, expected_nano)])
            self.assertEqual(len(records), 144)
            self.assertEqual(sum(r.get('started', False) for r in records), 1)
            self.assertEqual(sum(r['status'] == 'not_started' for r in records), 143)
            self.assertEqual(summary['terminal'], 144)
            self.assertFalse(summary['qualification_passed'])
            self.assertEqual(summary['stop_reason'], 'interface_failure_guard')
            self.assertEqual([status for _, status in completions], ['failed']*3)
            self.assertTrue((root/'out/final_frame.png').exists())
            return records[0]

    def test_http_rejection_stops_after_one_call_and_preserves_denominator(self):
        error = urllib.error.HTTPError('http://127.0.0.1:1/invoke', 502, 'fixture', {},
                                      io.BytesIO(b'{"error_type":"provider_http","http_status":400}'))
        row = self.rehearse(error)
        self.assertEqual(row['failure_code'], 'http_502')
        self.assertEqual(row['relay_diagnostic']['http_status'], 400)

    def test_invalid_native_action_stops_and_retains_preparse_response(self):
        model = json.loads((BASE/'models.json').read_text())['models']['generalist']
        raw = {'model': model['accepted_response_model_ids'][0], 'provider': model['provider_name'],
               'choices': [{'finish_reason': 'stop', 'message': {'content': 'invalid JSON'}}],
               'usage': {'prompt_tokens': 10, 'completion_tokens': 5, 'cost': .00004}}
        row = self.rehearse(raw, 'known', 40000)
        self.assertEqual(row['status'], 'invalid')
        self.assertEqual(row['raw_response'], raw)
        self.assertEqual(row['billing_receipt']['cost_usd'], .00004)

    def test_fenced_nested_action_preserves_known_usage_and_schema_failure(self):
        model = json.loads((BASE/'models.json').read_text())['models']['generalist']
        raw = {'model': model['accepted_response_model_ids'][0], 'provider': model['provider_name'],
               'choices': [{'finish_reason': 'stop', 'message': {
                   'content': '```json\n{"fetch":{"endpoint":"inventory","entities":["fixture"]}}\n```'}}],
               'usage': {'prompt_tokens': 565, 'completion_tokens': 41, 'cost': .00077}}
        row = self.rehearse(raw, 'known', 770000)
        self.assertEqual(row['status'], 'invalid')
        self.assertFalse(row['schema_valid'])
        self.assertTrue(row['checked']['transport_normalization']['removed_json_fence'])
        self.assertEqual(row['raw_response'], raw)

    def test_invalid_usage_preserves_full_reservation(self):
        model = json.loads((BASE/'models.json').read_text())['models']['generalist']
        raw = {'model': model['accepted_response_model_ids'][0], 'provider': model['provider_name'],
               'choices': [{'finish_reason': 'stop', 'message': {'content': '{"type":"directory"}'}}],
               'usage': {'prompt_tokens': 0, 'completion_tokens': 1, 'cost': .00001}}
        row = self.rehearse(raw)
        self.assertEqual(row['failure_code'], 'token_usage')
        self.assertNotIn('billing_receipt', row)


if __name__ == '__main__':
    unittest.main()

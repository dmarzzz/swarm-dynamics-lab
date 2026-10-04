import copy
import json
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import urllib.error
import successor_run as s
import reading_rule as r
from test_reading_rule import InstrumentTests


class SuccessorTests(unittest.TestCase):
    def setUp(self):
        self.data = r.build_input()
        self.a = self.data['assignments'][0]

    def test_frozen_input_and_carry_forward(self):
        self.assertEqual(r.digest((r.ROOT / 'input.json').read_bytes()), s.FROZEN_INPUT)
        self.assertEqual(sum(x['reservation_usd'] for x in s.historical() if x['event'] == 'start'), .05)
        self.assertLessEqual(157 * r.RESERVE, s.CAP)
        s.admission([], self.a, '2026-10-04T20:00:00+00:00')
        with self.assertRaisesRegex(AssertionError, 'cumulative USD8 cap'):
            s.admission([{'event': 'start', 'id': 'other', 'reservation_usd': 7.95}], self.a,
                        '2026-10-04T20:00:00+00:00')
        with self.assertRaisesRegex(AssertionError, 'durable stop latch'):
            s.admission([{'event': 'terminal', 'halt': 'http_400'}], self.a)

    def test_provider_receipt_and_unmodified_behavior(self):
        response = InstrumentTests().response()
        self.assertEqual(s.score(response)['reason'], 'missing_provider_identity')
        response['provider'] = 'OpenAI'
        self.assertEqual(s.score(response), r.score(response))
        rows = []
        hs = {h['id']: h for h in self.data['histories']}
        for a in self.data['assignments']:
            if a['stage'] == 'S0':
                body = InstrumentTests().response(hs[a['history']]['majority'])
                body['provider'] = 'OpenAI'
                rows.append({'event': 'terminal', 'id': a['id'], 'response': body})
        self.assertTrue(s.qualify(self.data, rows)['pass'])
        self.assertFalse(s.qualify(self.data, rows[:-1])['pass'])

    def test_http400_and_429_stop_after_durable_reservation(self):
        for code in (400, 429):
            with self.subTest(code=code), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / 'results').mkdir()
                key = root / '.moltbot/secrets/openrouter.key'
                key.parent.mkdir(parents=True)
                key.write_text('OFFLINE-DUMMY-NOT-A-KEY')
                output = root / 'results-r2'
                def fail(request, timeout):
                    rows = r.read_journal(output / 'journal.jsonl')
                    self.assertEqual(len(rows), 1)
                    self.assertEqual(rows[0]['event'], 'start')
                    self.assertEqual(rows[0]['reservation_usd'], .05)
                    raise urllib.error.HTTPError(r.ENDPOINT, code, 'offline fixture', {'Retry-After': '60'}, None)
                with patch.object(s, 'ROOT', root), patch.object(s, 'RESULTS', output), \
                     patch.object(s, 'preflight', return_value=self.data), \
                     patch.object(s, 'historical', return_value=[{'event': 'start', 'id': 'v1/old', 'reservation_usd': .05}]), \
                     patch.object(Path, 'home', return_value=root), \
                     patch.object(r, 'now', return_value='2026-10-04T20:00:00+00:00'), \
                     patch.object(s.urllib.request, 'urlopen', side_effect=fail) as native:
                    s.run('S0', 'a' * 40)
                    self.assertEqual(native.call_count, 1)
                    rows = s.read_journal()
                    self.assertEqual(rows[-1]['halt'], 'http_' + str(code))
                    if code == 429:
                        self.assertEqual(rows[-1]['retry_after'], '60')
                    with self.assertRaisesRegex(AssertionError, 'durable stop latch'):
                        s.admission(rows, self.a)


if __name__ == '__main__':
    unittest.main()

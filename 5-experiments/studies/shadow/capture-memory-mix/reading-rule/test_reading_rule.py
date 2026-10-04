import copy
import math
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import reading_rule as r

class InstrumentTests(unittest.TestCase):
    def setUp(self):
        self.data = r.build_input()
        self.a = self.data['assignments'][0]

    def test_assignment_and_history_counts(self):
        self.assertEqual(len(self.data['histories']), 26)
        self.assertEqual(len(self.data['assignments']), 156)
        self.assertEqual(len({a['id'] for a in self.data['assignments']}), 156)
        scientific = [h for h in self.data['histories'] if h['stage'] == 'S1']
        self.assertEqual(sum(h['majority'] == 'Cedar' for h in scientific), 12)
        self.assertEqual(sum(h['conflict'] for h in scientific), 12)

    def test_lossless_and_matched_all_conditions(self):
        for h in self.data['histories']:
            for rep, order in r.CONDITIONS:
                payload = r.representation(h, rep, order)
                self.assertEqual(r.reconstruct(payload), h['events'])
                for group in payload.get('counts_and_positions', []):
                    self.assertEqual(group['count'], len(group['event_indices']))

    def test_request_bounds_and_offline_admission(self):
        for a in self.data['assignments']:
            r.admission([], a, '2026-10-04T16:00:00+00:00')
        self.assertLessEqual(156 * r.RESERVE, r.CAP)
        with self.assertRaises(AssertionError):
            r.admission([], self.a, r.DEADLINE)

    def test_duplicate_budget_call_and_drift_guards(self):
        start = {'event': 'start', 'id': self.a['id'], 'reservation_usd': .05}
        with self.assertRaises(AssertionError):
            r.admission([start], self.a, '2026-10-04T16:00:00+00:00')
        with self.assertRaises(AssertionError):
            r.admission([dict(start, id='other', reservation_usd=12)], self.a, '2026-10-04T16:00:00+00:00')
        with self.assertRaises(AssertionError):
            r.admission([dict(start, id=str(i)) for i in range(156)], self.a, '2026-10-04T16:00:00+00:00')
        bad = copy.deepcopy(self.a)
        bad['body']['model'] = 'unauthorized'
        with self.assertRaises(AssertionError):
            r.admission([], bad, '2026-10-04T16:00:00+00:00')

    def response(self, name='Cedar'):
        return {'model': r.MODEL, 'choices': [{'message': {'content': name}, 'logprobs': {'content': [{'top_logprobs': [
            {'token': 'C', 'logprob': math.log(.9)}, {'token': 'R', 'logprob': math.log(.1)}]}]}}]}

    def test_known_answer_negative_and_missing_scorer(self):
        self.assertAlmostEqual(r.score(self.response())['p']['Cedar'], .9)
        self.assertFalse(r.score(self.response('unknown'))['valid'])
        self.assertFalse(r.score({})['valid'])
        bad = self.response()
        bad['model'] = 'wrong'
        self.assertEqual(r.score(bad)['reason'], 'model_mismatch')
        bad = self.response()
        bad['choices'][0]['logprobs']['content'][0]['top_logprobs'] = [{'token': 'C', 'logprob': math.log(.1)}]
        self.assertFalse(r.score(bad)['valid'])

    def test_qualification_all_assignments_and_failures(self):
        hs = {h['id']: h for h in self.data['histories']}
        rows = [{'event': 'terminal', 'id': a['id'], 'response': self.response(hs[a['history']]['majority'])}
                for a in self.data['assignments'] if a['stage'] == 'S0']
        self.assertTrue(r.qualify(self.data, rows)['pass'])
        self.assertFalse(r.qualify(self.data, rows[:-1])['pass'])
        self.assertFalse(r.qualify(self.data, [])['pass'])

    def test_ambiguous_start_persists_and_blocks_replay(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'journal.jsonl'
            with p.open('a') as f:
                r.append(f, {'event': 'start', 'id': self.a['id'], 'reservation_usd': .05})
            with self.assertRaises(AssertionError):
                r.admission(r.read_journal(p), self.a, '2026-10-04T16:00:00+00:00')

    def test_public_preflight_rejects_noncommit(self):
        with self.assertRaises(AssertionError):
            r.preflight('main', 'S0')

if __name__ == '__main__':
    unittest.main()

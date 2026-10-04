import copy
import json
import unittest
from reassess_s0 import BASE, analyze, references

class ReassessmentTests(unittest.TestCase):
    def setUp(self):
        p = BASE / 'results/QM-S0-02'
        self.m = json.loads((p/'manifest.json').read_text())
        self.r = [json.loads(s) for s in (p/'receipts.jsonl').read_text().splitlines()]

    def test_known_conflict(self):
        reports = [{'report_id': str(i), 'visible_root': 'r0' if i < 7 else 'r'+str(i-6),
                    'bit': int(i < 7), 'q': .8} for i in range(9)]
        self.assertEqual(references(reports), ('ONE', 'ZERO'))
        reports[1]['bit'] = 0
        with self.assertRaisesRegex(ValueError, 'inconsistent'):
            references(reports)

    def test_saved_reconciliation(self):
        result = analyze(self.m, self.r)
        self.assertEqual(result['totals']['model_correct'], 29)
        self.assertEqual(result['totals']['count_all_correct'], 24)
        self.assertEqual(result['strata']['conflict'], {'calls': 8, 'model_correct': 5})
        self.assertEqual(len(result['cases']), 16)

    def test_duplicate_receipt(self):
        self.r[-1] = copy.deepcopy(self.r[0])
        with self.assertRaisesRegex(ValueError, 'duplicate receipt'):
            analyze(self.m, self.r)

    def test_tampered_request(self):
        self.m['assignments'][0]['request']['state']['reports'][0]['bit'] = 1
        with self.assertRaisesRegex(ValueError, 'digest'):
            analyze(self.m, self.r)

    def test_wrong_frozen_label(self):
        self.m['assignments'][0]['expected'] = 'ONE'
        with self.assertRaisesRegex(ValueError, 'label mismatch'):
            analyze(self.m, self.r)

    def test_missing_receipt(self):
        with self.assertRaisesRegex(ValueError, '32 assignments'):
            analyze(self.m, self.r[:-1])

    def test_invalid_scores(self):
        self.r[0]['response']['answers']['decision']['probabilities']['ZERO'] = float('nan')
        with self.assertRaisesRegex(ValueError, 'invalid scores'):
            analyze(self.m, self.r)

if __name__ == '__main__':
    unittest.main()

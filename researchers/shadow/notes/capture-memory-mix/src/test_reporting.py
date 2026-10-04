"""Offline regression checks for the retrospective reporting correction."""
import unittest
from collections import Counter
from pathlib import Path
import lineage
from worker import metrics

ROOT = Path(__file__).resolve().parents[1]

class ReportingTests(unittest.TestCase):
    def test_mp3_denominators(self):
        raw = lineage.read_records(ROOT / 'results/pilot-mp3')
        selected, cells = lineage.select(raw)
        totals = Counter()
        for cell in cells.values():
            totals.update(cell)
        self.assertEqual([totals[k] for k in ('raw_records', 'raw_invalid', 'selected_records', 'selected_valid', 'first_observed_valid')], [327, 127, 180, 178, 54])
        self.assertEqual(len(selected), 180)

    def test_selection_unchanged(self):
        for name in ('pilot-mp', 'pilot-mp2', 'pilot-mp3'):
            raw = lineage.read_records(ROOT / 'results' / name)
            key = lambda r: (r['_file'], r['_line'])
            selected, _ = lineage.select(raw)
            self.assertEqual(set(map(key, selected)), set(map(key, lineage.legacy_select(raw))))

    def test_incomplete_later_attempt_does_not_replace_complete(self):
        raw = lineage.read_records(ROOT / 'results/pilot-mp3')
        selected, _ = lineage.select(raw)
        complete = [dict(x) for x in selected[:3]]
        for x in complete:
            x['validity'] = {'ok': True}
        partial = dict(complete[0], _line=99999)
        result, _ = lineage.select(complete + [partial])
        self.assertEqual(len(result), 3)
        self.assertNotIn(99999, [x['_line'] for x in result])

    def test_capture_fraction_with_unequal_valid_arm_counts(self):
        stats = {str(n): dict(n=n, captured=n, frac_T=0, delta=0, invalid=0, calls=0, usd=0) for n in (2, 3, 4)}
        self.assertEqual(metrics(stats)['captured'], 1)
        for s in stats.values():
            s['n'] = s['captured'] = 0
        self.assertIsNone(metrics(stats)['captured'])

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
import unittest

from uncertainty import metrics, quantile, resample


class UncertaintyTests(unittest.TestCase):
    def test_quantile_interpolation(self):
        self.assertEqual(quantile([4, 0, 2], .25), 1)
        self.assertEqual(quantile([3], .975), 3)

    def test_paired_invariant(self):
        result = resample([[10, 4, 2], [20, 8, 4]], 100, 1)
        self.assertEqual(result['conditional_95pct_ci']['ratio'], [2, 2])
        self.assertEqual(result['leave_one_page_out_range']['ratio'], [2, 2])
        self.assertEqual(result['point']['difference'], .2)
        self.assertEqual(result['replicates_valid'], 100)

    def test_seed_reproducibility(self):
        pages = [[10, 7, 1], [20, 9, 3], [5, 4, 2]]
        self.assertEqual(resample(pages, 100, 9), resample(pages, 100, 9))

    def test_zero_denominator(self):
        with self.assertRaises(ValueError):
            metrics([0, 0, 0])
        with self.assertRaises(ValueError):
            metrics([2, 1, 0])
        result = resample([[1, 1, 1], [1, 0, 0]], 100, 3)
        self.assertGreater(result['replicates_rejected'], 0)
        self.assertEqual(result['replicates_valid'] + result['replicates_rejected'], 100)
        self.assertEqual(result['leave_one_out_rejected'], 1)

    def test_leave_one_out_known_answer(self):
        result = resample([[10, 8, 4], [20, 10, 2]], 100, 4)
        self.assertEqual(result['leave_one_page_out_range']['ratio'], [2, 5])
        self.assertEqual(result['leave_one_page_out_range']['difference'], [.4, .4])


if __name__ == '__main__':
    unittest.main()

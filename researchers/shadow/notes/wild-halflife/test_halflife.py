#!/usr/bin/env python3
"""Offline synthetic checks for halflife.py. Run: python3 test_halflife.py"""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import halflife as H  # noqa: E402


def rec(t, a, units, cluster=None, b=None):
    return dict(t=float(t), a=a, b=b or a, cluster=cluster or f"c{t}{a}",
                units={"url": set(units), "line": set(), "host": set()})


class T(unittest.TestCase):
    def test_units(self):
        self.assertEqual(H.url_units("see [https://X.org/A%2F?q=1 name] and http://y.io/b."),
                         {"https://x.org/a%2f?q=1", "http://y.io/b"})
        self.assertEqual(H.norm_line("  * Hello   WORLD this is a long enough line"),
                         "hello world this is a long enough line")
        self.assertEqual(H.line_units(["short", "Beschreibe hier die neue Seite."]), set())

    def test_repeat_writer_and_ties(self):
        recs = [rec(0, "A", ["u"]), rec(0, "B", ["u"]), rec(5, "A", ["u"]), rec(10, "C", ["u"]),
                rec(20, "D", ["v"])]
        table, t_end, a_end, _ = H.adoption_table(recs, "url", "a")
        self.assertEqual([e[2] for e in table["u"]], ["A", "B", "C"])  # A's repeat ignored
        iv = H.unit_intervals(table["u"], t_end, a_end, clock=1)
        # A and B tie at origin -> j starts at 2; C arrives at activity 3 (3 earlier records)
        self.assertEqual(iv, [(2, 3.0, 1), (3, 5.0 - 3.0, 0)])

    def test_censoring(self):
        recs = [rec(0, "A", ["u"]), rec(3600, "B", ["x"]), rec(7200, "C", ["x"])]
        table, t_end, a_end, _ = H.adoption_table(recs, "url", "a")
        iv = H.unit_intervals(table["u"], t_end, a_end, clock=0)
        self.assertEqual(iv, [(1, 2.0, 0)])

    def test_km(self):
        dur = np.array([1., 2., 3., 4.])
        obs = np.array([1, 0, 1, 1])
        F, _, _ = H.weighted_km(dur, obs, np.ones(4), [1, 2.5, 4])
        # S: after t=1 3/4; t=2 censored; t=3 at risk 2 -> 3/4*1/2; t=4 -> 0
        np.testing.assert_allclose(F, [0.25, 0.25, 1.0])
        F2, _, _ = H.weighted_km(dur, obs, np.array([2., 1, 1, 1]), [1])
        np.testing.assert_allclose(F2, [0.4])

    def test_slope(self):
        mids = np.array([1, 2, 3.5, 7, 14.5, 30.])
        X = np.ones(6) * 100
        E = mids * 3  # rate proportional to j
        self.assertAlmostEqual(H.wls_slope(E, X, mids), 1.0, places=9)
        self.assertAlmostEqual(H.wls_slope(np.ones(6) * 5, X, mids), 0.0, places=9)

    def test_analyse_runs(self):
        rng = np.random.default_rng(0)
        recs = []
        for i in range(60):
            recs.append(rec(i, f"id{i % 7}", [f"u{i % 9}", f"w{i}"], cluster=f"p{i % 5}"))
        table, t_end, a_end, _ = H.adoption_table(recs, "url", "a")
        H.N_BOOT = 20
        r = H.analyse(table, t_end, a_end, rng, "synthetic")
        self.assertEqual(r["units"], 69)
        self.assertEqual(r["units_ge2"], 9)
        self.assertTrue(0 <= r["activity"]["km_adopted_frac"][-1] <= 1)


if __name__ == "__main__":
    unittest.main()

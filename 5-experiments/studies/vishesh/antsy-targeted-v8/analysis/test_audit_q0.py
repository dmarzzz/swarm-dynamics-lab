import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from test_native import fixture
from qualification import summarize
from audit_q0 import audit, wilson


class AuditTests(unittest.TestCase):
    def test_qualified(self):
        r, j = fixture()
        self.assertTrue(audit(r, j, summarize(r, j))["qualified"])

    def test_missing_denominator_is_unknown(self):
        r, j = fixture()
        a = audit(r, j, summarize(r, j))
        self.assertIsNone(
            a["conditional"]["checker_correct_given_primary_wrong"]["wilson95"]
        )

    def test_partial(self):
        r, j = fixture()
        a = audit(r[:2], j[:8], summarize(r[:2], j[:8]))
        self.assertEqual(a["unstarted"], 36)
        self.assertFalse(a["qualified"])

    def test_summary_corruption(self):
        r, j = fixture()
        s = summarize(r, j)
        s["arms"]["primary"]["correct"] -= 1
        with self.assertRaises(ValueError):
            audit(r, j, s)

    def test_duplicate_and_orphan(self):
        r, j = fixture()
        with self.assertRaises(ValueError):
            audit(r, j + j[:1], summarize(r, j))
        with self.assertRaises(ValueError):
            audit(r, j[1:], summarize(r, j))

    def test_zero_errors_not_zero_risk(self):
        self.assertAlmostEqual(wilson(0, 20)[1], 0.161125, places=5)
        self.assertIsNone(wilson(0, 0))


if __name__ == "__main__":
    unittest.main()

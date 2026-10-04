import tempfile, unittest
from pathlib import Path
from core import evaluate, diversity
from study import audit
from visuals import render, wilson, intervals


def fixture():
    records = []
    for i, vs in enumerate(
        [
            [10, 10, 10, 11, 11],
            [None, 10, None, 10, 10],
            [11, 11, 10, 10, 10],
            [None] * 5,
        ]
    ):
        records.append(
            {
                "id": i,
                "image_sha256": str(i),
                "gold": {"status": "ok", "value": 10},
                "workers": {
                    k: {
                        "id": k,
                        "family": k[0],
                        "origin": k,
                        "valid": True,
                        "wall_s": 1.0,
                        "candidate": {
                            "status": "ok" if v is not None else "missing",
                            "value": v,
                        },
                    }
                    for k, v in zip(["T0", "T1", "T2", "R0", "R1"], vs)
                },
            }
        )
    return records


class StudyTests(unittest.TestCase):
    def test_audit_reconciles_and_detects_corruption(self):
        r = fixture()
        o, s = evaluate(r)
        self.assertTrue(audit(r, o, s, list(range(4)))["passed"])
        s["arms"]["mixed/majority"]["correct"] += 1
        with self.assertRaises(AssertionError):
            audit(r, o, s, list(range(4)))

    def test_wilson_and_paired_identity(self):
        self.assertIsNone(wilson(0, 0))
        lo, hi = wilson(0, 10)
        self.assertAlmostEqual(lo, 0)
        self.assertGreater(hi, 0.2)
        r = fixture()
        o, s = evaluate(r)
        x = intervals(o, s)
        self.assertEqual(x, intervals(o, s))

    def test_all_artifacts_render_from_measured_outcomes(self):
        r = fixture()
        o, s = evaluate(r)
        with tempfile.TemporaryDirectory() as td:
            render(td, r, o, s, diversity(r))
            for f in [
                "outcomes.png",
                "same-wrong.png",
                "decision-map.png",
                "observed-traces.gif",
                "uncertainty.json",
                "arm-key.json",
            ]:
                self.assertGreater((Path(td) / f).stat().st_size, 30)


if __name__ == "__main__":
    unittest.main()

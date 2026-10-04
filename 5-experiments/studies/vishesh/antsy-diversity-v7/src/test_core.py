import copy, itertools, unittest
from core import (
    extract,
    decide,
    payload,
    pair_stats,
    evaluate,
    diversity,
    grade,
    digest,
)


def item(i, v, origin=None, family="tess"):
    return {
        "id": i,
        "family": family,
        "origin": origin or i,
        "candidate": {
            "status": "ok" if v is not None else "missing",
            "value": v,
            "confidence": 0.8,
            "regions": [],
        },
        "wall_s": 1.0,
        "valid": True,
    }


def record(i, vals, gold="10.00"):
    return {
        "id": i,
        "gold": {"status": "ok" if gold is not None else "missing", "value": gold},
        "workers": {
            k: item(k, v, family="rapid" if k.startswith("R") else "tess")
            for k, v in zip(["T0", "T1", "T2", "R0", "R1"], vals)
        },
    }


class CoreTests(unittest.TestCase):
    def test_legitimate_labels(self):
        for s in [
            "TOTAL 10",
            "GrandTotal 10",
            "TOTAL. 10",
            "AMOUNT DUE 10",
            "DUE 10",
            "10 Total.",
        ]:
            self.assertEqual(extract([{"text": s}])["value"], "10.00")

    def test_reject_salvage_and_other_fields(self):
        for s in [
            "SUB-TOTAL 10",
            "SUB TOTAL 10",
            "TOTAL QTY 10",
            "TOTAL CASH 10",
            "TOTAL TAX 10",
            "TOTAL -10",
            "TOTAL 1O",
            "TOTAL USD 10",
            "TOTAL 10 20",
            "garbage TOTAL 10",
            "TOTAL 10.",
            "TOTAL .10",
        ]:
            self.assertIsNone(extract([{"text": s}])["value"])

    def test_conflicting_totals(self):
        self.assertEqual(
            extract([{"text": "TOTAL 10"}, {"text": "TOTAL 20"}])["status"], "ambiguous"
        )

    def test_wrong_majority_dissent(self):
        xs = [item("a", "9"), item("b", "9"), item("c", "10")]
        self.assertEqual(decide(xs, "majority")["value"], "9")
        self.assertIsNone(decide(xs, "provenance-dissent")["value"])

    def test_duplicate_cannot_manufacture_quorum(self):
        a = item("a", "10")
        b = copy.deepcopy(a)
        b["id"] = "fake"
        self.assertIsNone(decide([a, b], "provenance-dissent")["value"])
        self.assertEqual(decide([a, b], "majority")["value"], "10")

    def test_duplicate_invariance(self):
        xs = [item("a", "10"), item("b", "10")]
        expected = decide(xs, "provenance-dissent")
        self.assertEqual(
            expected, decide(xs + [dict(xs[0], id="alias")] * 10, "provenance-dissent")
        )

    def test_conflicting_origin_rejected(self):
        with self.assertRaises(ValueError):
            decide(
                [item("a", "10", "same"), item("b", "20", "same")], "provenance-dissent"
            )

    def test_permutation_invariance(self):
        xs = [item("a", "10"), item("b", "10"), item("c", None)]
        for p in itertools.permutations(xs):
            self.assertEqual(
                decide(list(p), "provenance-dissent"), decide(xs, "provenance-dissent")
            )

    def test_missing_not_dissent_or_evidence(self):
        self.assertIsNone(
            decide([item("a", "10"), item("b", None)], "provenance-dissent")["value"]
        )

    def test_actor_truth_exclusion(self):
        r = record(1, ["10"] * 5)
        a = payload(r, ["T0", "R0"])
        r["gold"] = {"value": "secret"}
        r["workers"]["T0"]["gold"] = "secret"
        self.assertEqual(a, payload(r, ["T0", "R0"]))
        self.assertNotIn("gold", str(a))

    def test_unknown_not_correct(self):
        self.assertFalse(grade(None, {"status": "missing", "value": None})["correct"])

    def test_pair_denominators(self):
        rs = [
            record(0, ["10.00", "10.00", None, None, None]),
            record(1, ["9", "9", None, None, None]),
            record(2, [None, "10.00", None, None, None]),
            record(3, [None, None, None, None, None], None),
        ]
        p = pair_stats(rs, "T0", "T1")
        self.assertEqual(
            (
                p["assigned"],
                p["scorable"],
                p["co_answered"],
                p["same_wrong"],
                p["double_wrong"],
                p["joint_noncorrect"],
            ),
            (4, 3, 2, 1, 1, 1),
        )
        self.assertEqual(p["answer_agreement"], 1)
        self.assertEqual(p["b_correct_a_not"], 1)

    def test_degenerate_correlation_is_null(self):
        p = pair_stats([record(0, ["10.00"] * 5)], "T0", "T1")
        self.assertIsNone(p["correctness_phi"])

    def test_shared_missing_not_wrong_acceptance(self):
        p = pair_stats([record(0, [None] * 5)], "T0", "T1")
        self.assertEqual(p["joint_noncorrect"], 1)
        self.assertEqual(p["double_wrong"], 0)
        self.assertIsNone(p["answer_agreement"])

    def test_unique_correct_information(self):
        d = diversity([record(0, [None, None, None, "10.00", None])])
        self.assertEqual(d["workers"]["R0"]["unique_correct"], 1)
        self.assertEqual(d["candidate_oracle"], 1)

    def test_complete_outcome_denominator(self):
        out, s = evaluate([record(0, ["10.00"] * 5), record(1, [None] * 5, None)])
        self.assertEqual(len(out), 22)
        self.assertEqual(s["assigned"], 2)
        self.assertEqual(s["scorable"], 1)

    def test_family_not_independence(self):
        d = decide([item("a", "10"), item("b", "10")], "provenance-dissent")
        self.assertEqual(d["support_families"], ["tess"])
        self.assertEqual(len(d["support_origins"]), 2)


if __name__ == "__main__":
    unittest.main()

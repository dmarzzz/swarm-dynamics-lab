import unittest
from unittest.mock import patch
import contract as c


def cand(v, status="ok", confidence=0.8):
    return {"value": v, "status": status, "confidence": confidence}


def lines(*ss):
    return [{"text": s, "confidence": 0.8} for s in ss]


class ContractTests(unittest.TestCase):
    def test_valid_numbers(self):
        for raw, expected in [
            ("0", "0.00"),
            ("Rp 45.000", "45000.00"),
            ("45,000", "45000.00"),
            ("12.50", "12.50"),
            ("12,50", "12.50"),
            ("1.234,56", "1234.56"),
            ("1,234.56", "1234.56"),
            ("IDR 007", "7.00"),
        ]:
            with self.subTest(raw=raw):
                self.assertEqual(c.amount(raw), expected)

    def test_reject_unsafe(self):
        for s in [
            "-10",
            "1O00",
            "1,23,456",
            "12.3456",
            "1..000",
            "NaN",
            "Infinity",
            "",
            "12 000",
            "12.3",
        ]:
            with self.subTest(raw=s):
                self.assertIsNone(c.amount(s))

    def test_total_anchors(self):
        for s in [
            "TOTAL 45,000",
            "GRAND TOTAL Rp 45.000",
            "TOTAL BAYAR 45000",
            "JUMLAH BAYAR 45000",
        ]:
            self.assertEqual(c.extract(lines(s))["value"], "45000.00")

    def test_reject_other_fields(self):
        for s in [
            "SUBTOTAL 45,000",
            "SUB TOTAL 45,000",
            "TOTAL QTY 2",
            "TOTAL TAX 1000",
            "TOTAL CASH 50000",
            "CHANGE 5000",
        ]:
            self.assertEqual(c.extract(lines(s))["status"], "missing")

    def test_conflicts_abstain(self):
        self.assertEqual(
            c.extract(lines("TOTAL 100", "TOTAL 200"))["status"], "ambiguous"
        )

    def test_missing_not_zero(self):
        self.assertIsNone(c.extract(lines("TOTAL unreadable"))["value"])
        self.assertEqual(c.extract(lines("TOTAL 0"))["value"], "0.00")

    def test_multinumber_line_abstains(self):
        self.assertEqual(c.extract(lines("TOTAL 100 200"))["status"], "missing")

    def test_negative_not_positive(self):
        self.assertEqual(c.extract(lines("TOTAL -100"))["status"], "missing")

    def test_no_numeric_salvage(self):
        for text in [
            "TOTAL (100)",
            "TOTAL - 100",
            "TOTAL USD 100",
            "TOTAL abc 100",
            "TOTAL 1O00",
        ]:
            self.assertEqual(c.extract(lines(text))["status"], "missing")

    def test_reference_missing_unscorable(self):
        self.assertFalse(
            c.grade(
                {"action": "refer", "value": None}, c.reference({"valid_line": []})
            )["scorable"]
        )

    def test_reference_conflict_unscorable(self):
        gt = {"gt_parse": {"total": {"total_price": ["100", "200"]}}}
        self.assertEqual(c.reference(gt)["status"], "ambiguous")

    def test_subtotal_not_gold(self):
        self.assertEqual(
            c.reference(
                {
                    "valid_line": [
                        {
                            "category": "sub_total.subtotal_price",
                            "words": [{"text": "100"}],
                        }
                    ]
                }
            )["status"],
            "missing",
        )

    def test_real_cord_schema(self):
        gt = {
            "gt_parse": {
                "total": {"total_price": "1,591,600", "cashprice": "2,000,000"}
            },
            "valid_line": [
                {
                    "category": "total.total_price",
                    "words": [
                        {"text": "Grand"},
                        {"text": "Total"},
                        {"text": "1,591,600"},
                    ],
                }
            ],
        }
        self.assertEqual(c.reference(gt), {"status": "ok", "value": "1591600.00"})

    def test_reference_cannot_fall_back_to_cash(self):
        self.assertEqual(
            c.reference({"gt_parse": {"total": {"cashprice": "100"}}})["status"],
            "missing",
        )

    def test_reference_malformed_structure(self):
        self.assertEqual(
            c.reference({"gt_parse": {"total": [{"total_price": "100"}]}})["status"],
            "ambiguous",
        )

    def test_agreement_requires_distinct_sources(self):
        self.assertIsNone(c.consensus({"A": cand("1.00")}))

    def test_tied_agreement_abstains(self):
        self.assertIsNone(
            c.consensus({k: cand(v) for k, v in zip("ABCD", ["1", "1", "2", "2"])})
        )

    def test_null_cannot_add_support(self):
        a = {"A": cand("1")}
        a["D"] = cand(None, "missing")
        self.assertIsNone(c.consensus(a))

    def test_selective_stop(self):
        a = {k: cand("1") for k in "ABC"}

        def no_call(k):
            raise AssertionError("unnecessary checker")

        self.assertEqual(c.run_policy(a, no_call, "selective-check")["checks"], [])

    def test_selective_continue_and_stop(self):
        a = {k: cand(v) for k, v in zip("ABC", ["1", "2", "3"])}
        r = c.run_policy(a, lambda k: cand("2"), "selective-check")
        self.assertEqual(r["checks"], ["D"])
        self.assertEqual(r["value"], "2")

    def test_missing_checks_preserve_prior(self):
        a = {k: cand(v) for k, v in zip("ABC", ["1", "2", "3"])}
        r = c.run_policy(a, lambda k: cand(None, "missing"), "selective-check")
        self.assertEqual(r["checks"], ["D", "E"])
        self.assertEqual(r["action"], "refer")

    def test_wrong_consensus_is_wrong(self):
        r = c.run_policy(
            {k: cand("1") for k in "ABC"}, lambda k: cand("1"), "agreement"
        )
        self.assertTrue(c.grade(r, {"status": "ok", "value": "2"})["wrong"])

    def test_abstention_not_accuracy(self):
        g = c.grade({"action": "refer", "value": None}, {"status": "ok", "value": "2"})
        self.assertFalse(g["correct"])
        self.assertTrue(g["refer"])

    def test_actor_whitelist(self):
        r = {
            "pipelines": {
                k: {"candidate": cand("1"), "secret_truth": "BAD"} for k in "ABCDE"
            },
            "gold": {"value": "secret"},
        }
        self.assertEqual(set(c.actor(r)), set("ABC"))
        self.assertNotIn("gold", str(c.actor(r)))
        r["gold"]["value"] = "mutated"
        self.assertEqual(c.actor(r), {k: cand("1") for k in "ABC"})

    def test_mutation_reject_subtotal_bug(self):
        with patch.object(c, "EXCLUDE", __import__("re").compile(r"NEVERMATCH")):
            self.assertEqual(c.extract(lines("SUB TOTAL 100"))["value"], "100.00")

    def test_mutation_null_vote_bug_detectable(self):
        # Deliberate faulty oracle is rejected by the distinct-source contract fixture.
        bad = lambda xs: next(iter(xs.values()))["value"]
        self.assertNotEqual(bad({"A": cand("1")}), c.consensus({"A": cand("1")}))


if __name__ == "__main__":
    unittest.main()

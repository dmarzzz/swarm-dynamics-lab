import unittest
from fields import extract, policy


def words(parts):
    return [
        {
            "text": t,
            "x": x,
            "y": y,
            "h": h,
            "box": [x, y - h / 2, max(12, len(t) * 8), h],
            "confidence": 0.9,
        }
        for t, x, y, h in parts
    ]


def candidate(v):
    return {"value": v, "status": "ok" if v is not None else "missing"}


class Fields(unittest.TestCase):
    def test_dotted_subtotal(self):
        self.assertIsNone(
            extract(words([("SUB.TOTAL", 0, 20, 20), ("22,727", 200, 20, 20)]))["value"]
        )

    def test_unresolved_grand_total_blocks_generic_quantity(self):
        r = extract(
            words(
                [
                    ("TOTAL", 0, 20, 20),
                    ("5", 200, 20, 20),
                    ("GRAND TOTAL", 0, 70, 20),
                    ("illegible", 200, 70, 20),
                ]
            )
        )
        self.assertIsNone(r["value"])
        self.assertIn("unresolved_explicit_final_total", r["reasons"])

    def test_baseline_mismatch(self):
        self.assertEqual(
            extract(words([("TOTAL", 0, 20, 24), ("30,000", 200, 28, 14)]))["value"],
            "30000.00",
        )

    def test_adjacent_row_not_total(self):
        self.assertIsNone(
            extract(words([("TOTAL", 0, 20, 20), ("30,000", 200, 42, 20)]))["value"]
        )

    def test_decorated_total_and_decimal_space(self):
        self.assertEqual(
            extract(
                words(
                    [
                        ("Total.", 0, 20, 20),
                        ("»", 90, 20, 20),
                        ("35.000,00", 120, 20, 20),
                    ]
                )
            )["value"],
            "35000.00",
        )
        self.assertEqual(
            extract(words([("TOTAL", 0, 20, 20), ("30, 000", 200, 20, 20)]))["value"],
            "30000.00",
        )

    def test_excluded_semantics(self):
        for t in [
            "SUB TOTAL",
            "SUB-TOTAL",
            "TOTAL ITEMS",
            "TOTAL CASH",
            "TOTAL TAX",
            "TOTAL VOID",
            "TOTAL DISCOUNT",
        ]:
            with self.subTest(t=t):
                self.assertIsNone(
                    extract(words([(t, 0, 20, 20), ("100", 200, 20, 20)]))["value"]
                )

    def test_multiple_or_bad_numbers(self):
        for t in ["100 200", "100/200", "A100", "100A", "-100", "1,00,0", "100 000"]:
            with self.subTest(t=t):
                self.assertIsNone(
                    extract(words([("TOTAL", 0, 20, 20), (t, 200, 20, 20)]))["value"]
                )

    def test_unrecognized_gap(self):
        self.assertIsNone(
            extract(
                words(
                    [("TOTAL", 0, 20, 20), ("fee", 100, 20, 20), ("100", 200, 20, 20)]
                )
            )["value"]
        )

    def test_conflicting_totals(self):
        r = extract(
            words(
                [
                    ("TOTAL", 0, 20, 20),
                    ("100", 200, 20, 20),
                    ("GRAND TOTAL", 0, 60, 20),
                    ("200", 200, 60, 20),
                ]
            )
        )
        self.assertEqual(r["status"], "ambiguous")

    def test_no_anchor_no_numeric_salvage(self):
        self.assertIsNone(
            extract(words([("OTHER", 0, 20, 20), ("100", 200, 20, 20)]))["value"]
        )

    def test_bad_digit_is_not_corrected(self):
        self.assertEqual(
            extract(words([("TOTAL", 0, 20, 20), ("13,450", 200, 20, 20)]))["value"],
            "13450.00",
        )

    def test_policy_no_weak_veto(self):
        self.assertEqual(
            policy(candidate("100"), candidate("900"), "targeted-fallback")["value"],
            "100",
        )
        self.assertIsNone(
            policy(candidate("100"), candidate("900"), "agreement")["value"]
        )

    def test_fallback_not_corroboration(self):
        r = policy(candidate(None), candidate("100"), "targeted-fallback")
        self.assertEqual(r["value"], "100")
        self.assertFalse(r["corroborated"])

    def test_always_targeted_same_decisions(self):
        for p in [None, "100", "200"]:
            for c in [None, "100", "200"]:
                self.assertEqual(
                    policy(candidate(p), candidate(c), "targeted-fallback")["value"],
                    policy(candidate(p), candidate(c), "always-fallback")["value"],
                )


if __name__ == "__main__":
    unittest.main()

import copy, datetime, unittest
from admission import validate, UTC


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime(2026, 10, 4, 6, tzinfo=UTC)
        self.r = {
            "experiment": "antsy-diversity-v7",
            "run": "S0-a1",
            "stage": "S0",
            "source": "abc",
            "plan_sha256": "hash",
            "verified_utc": "2026-10-04T05:59:00Z",
            "expires_utc": "2026-10-04T07:00:00Z",
            "claim_expires_utc": "2026-10-04T08:00:00Z",
            "public_page_verified": True,
            "exclusive_claim_verified": True,
            "host": "sim-vishesh",
            "claim": "vishesh-antsy-diversity-v7",
            "max_model_calls": 0,
            "new_charge_cap_usd": 0,
            "max_ocr_calls": 100,
            "public_content_url": "https://raw.githubusercontent.com/dmarzzz/swarm-lab/abc/researchers/vishesh/notes/antsy-diversity-v7/PLAN.md",
        }

    def test_valid(self):
        self.assertTrue(validate(self.r, "S0", "S0-a1", "abc", "hash", self.now))

    def test_failed_gate_blocks(self):
        for k, v in [
            ("source", "bad"),
            ("public_page_verified", False),
            ("exclusive_claim_verified", False),
            ("max_model_calls", 1),
            ("max_ocr_calls", 101),
            ("new_charge_cap_usd", 1),
            ("plan_sha256", "bad"),
            ("run", "duplicate"),
            ("stage", "S1"),
            ("public_content_url", "https://example.com"),
        ]:
            r = dict(self.r, **{k: v})
            with self.subTest(k=k), self.assertRaises(AssertionError):
                validate(r, "S0", "S0-a1", "abc", "hash", self.now)

    def test_stale_and_expired_block(self):
        for key in ["verified_utc", "expires_utc", "claim_expires_utc"]:
            r = dict(self.r, **{key: "2026-10-04T04:00:00Z"})
            with self.subTest(key=key), self.assertRaises(AssertionError):
                validate(r, "S0", "S0-a1", "abc", "hash", self.now)


if __name__ == "__main__":
    unittest.main()

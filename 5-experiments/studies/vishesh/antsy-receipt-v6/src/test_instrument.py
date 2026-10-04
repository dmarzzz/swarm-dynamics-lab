import json, tempfile, unittest
from pathlib import Path
from test_eval import record
from measure import lines_from_tsv
from study import evaluate
from audit import audit
from analyze import analyze, wilson


class InstrumentTests(unittest.TestCase):
    def test_tsv_quotes_are_literal_not_multiline_csv(self):
        raw = 'left\ttop\theight\tconf\ttext\n0\t0\t10\t80\t"\n0\t30\t10\t90\tTOTAL\n60\t30\t10\t90\t100\n'
        rows = lines_from_tsv(raw)
        self.assertEqual([r["text"] for r in rows], ['"', "TOTAL 100"])

    def fixture(self):
        p = Path(tempfile.mkdtemp(prefix="antsy6-eval-test-"))
        records = [record(0), record(1, "2.00"), record(2, None)]
        for r in records:
            r["image_sha256"] = str(r["id"])
        rows, s = evaluate(records)
        (p / "records.jsonl").write_text("".join(json.dumps(r) + "\n" for r in records))
        (p / "manifest.json").write_text(
            json.dumps(
                {"complete": True, "ids": [0, 1, 2], "ocr_calls": 15, "invalid_ocr": 0}
            )
        )
        (p / "summary.json").write_text(json.dumps(s))
        (p / "outcomes.json").write_text(json.dumps(rows))
        return p

    def test_reparse_preserves_parent_and_measured_cost(self):
        from reparse import reparse
        from unittest.mock import patch

        p = self.fixture()
        m = json.loads((p / "manifest.json").read_text())
        m["source"] = "original-source"
        (p / "manifest.json").write_text(json.dumps(m))
        rs = [json.loads(x) for x in (p / "records.jsonl").read_text().splitlines()]
        (p / "private").mkdir()
        for r in rs:
            r["split"] = "train"
            for tool in "ABCDE":
                (p / "private" / f"train-{r['id']}-{tool}.tsv").write_text(
                    "left\ttop\theight\tconf\ttext\n0\t0\t10\t90\tSUB-TOTAL\n100\t0\t10\t90\t1\n"
                )
        (p / "records.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rs))
        before = (p / "records.jsonl").read_bytes()
        with patch("reparse.render"):
            result = reparse(p, p / "repaired")
        self.assertEqual(result["new_ocr_calls"], 0)
        self.assertEqual(result["candidate_changes"], 15)
        self.assertEqual((p / "records.jsonl").read_bytes(), before)
        fixed = [
            json.loads(x)
            for x in (p / "repaired/records.jsonl").read_text().splitlines()
        ]
        self.assertEqual(fixed[0]["pipelines"]["A"]["wall_s"], 0.5)
        self.assertIsNone(fixed[0]["pipelines"]["A"]["candidate"]["value"])
        with self.assertRaises(FileExistsError):
            reparse(p, p / "repaired")

    def test_all_unscorable_cannot_pass(self):
        p = self.fixture()
        rs = [json.loads(x) for x in (p / "records.jsonl").read_text().splitlines()]
        for r in rs:
            r["gold"] = {"status": "missing", "value": None}
        out, s = evaluate(rs)
        (p / "records.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rs))
        (p / "outcomes.json").write_text(json.dumps(out))
        (p / "summary.json").write_text(json.dumps(s))
        with self.assertRaisesRegex(AssertionError, "zero scorable"):
            audit(p)

    def test_measurement_timeout_retained(self):
        import io, subprocess
        from PIL import Image
        from unittest.mock import patch
        from measure import measure

        b = io.BytesIO()
        Image.new("RGB", (20, 20), "white").save(b, format="PNG")
        with (
            tempfile.TemporaryDirectory() as d,
            patch(
                "measure.subprocess.run",
                side_effect=subprocess.TimeoutExpired("tesseract", 30),
            ),
        ):
            r = measure(
                {
                    "image": {"bytes": b.getvalue()},
                    "ground_truth": json.dumps(
                        {"gt_parse": {"total": {"total_price": "100"}}}
                    ),
                },
                0,
                "train",
                Path(d),
            )
        self.assertEqual(r["gold"]["value"], "100.00")
        self.assertEqual(len(r["pipelines"]), 5)
        self.assertTrue(
            all(
                not p["valid"] and p["candidate"]["status"] == "error"
                for p in r["pipelines"].values()
            )
        )

    def test_scoring_audit_passes(self):
        self.assertTrue(audit(self.fixture())["passed"])

    def test_score_mutation_rejected(self):
        p = self.fixture()
        s = json.loads((p / "summary.json").read_text())
        s["arms"]["agreement"]["correct"] += 1
        (p / "summary.json").write_text(json.dumps(s))
        with self.assertRaises(AssertionError):
            audit(p)

    def test_duplicate_assignment_rejected(self):
        p = self.fixture()
        rows = json.loads((p / "outcomes.json").read_text())
        rows[0] = rows[1]
        (p / "outcomes.json").write_text(json.dumps(rows))
        with self.assertRaises(AssertionError):
            audit(p)

    def test_missing_assignment_rejected(self):
        p = self.fixture()
        rows = json.loads((p / "outcomes.json").read_text())
        (p / "outcomes.json").write_text(json.dumps(rows[:-1]))
        with self.assertRaises(AssertionError):
            audit(p)

    def test_zero_observed_errors_is_not_zero_risk(self):
        self.assertAlmostEqual(wilson(0, 10)[1], 0.2775328, places=6)
        self.assertIsNone(wilson(0, 0))

    def test_reference_unknown_bounds(self):
        r = analyze(self.fixture())
        self.assertEqual(
            r["uncertain_reference_bounds"]["agreement"]["error_rate_bounds"],
            [1 / 3, 2 / 3],
        )

    def test_spatial_rows_ignore_annotation(self):
        t = "level\tleft\ttop\twidth\theight\tconf\ttext\n5\t0\t10\t30\t10\t90\tTOTAL\n5\t100\t11\t30\t10\t80\t100\n5\t0\t40\t30\t10\t70\tCASH\n"
        r = lines_from_tsv(t)
        self.assertEqual(r[0]["text"], "TOTAL 100")
        self.assertEqual(r[1]["text"], "CASH")


if __name__ == "__main__":
    unittest.main()

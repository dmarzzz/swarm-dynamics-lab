import copy, json, tempfile, unittest
from pathlib import Path
from native import validate, ROOT, DOCS, sha
from qualification import summarize


def fixture():
    rr = []
    jj = []
    for i in range(60, 80):
        rr.append(
            {
                "id": i,
                "gold": {"status": "ok", "value": 100},
                "workers": {
                    w: {
                        "valid": True,
                        "candidate": {"status": "ok", "value": 100},
                        "wall_s": 1,
                    }
                    for w in ["P", "C"]
                },
            }
        )
        for w in ["P", "C"]:
            jj.extend(
                [
                    dict(id=i, worker=w, status="started"),
                    dict(id=i, worker=w, status="valid"),
                ]
            )
    return rr, jj


class QualificationTests(unittest.TestCase):
    def test_positive_and_threshold_boundary(self):
        r, j = fixture()
        self.assertTrue(summarize(r, j)["qualified"])
        for x in r[:10]:
            x["workers"]["C"]["candidate"] = {"status": "missing", "value": None}
        self.assertTrue(summarize(r, j)["qualified"])
        r[10]["workers"]["C"]["candidate"] = {"status": "missing", "value": None}
        self.assertFalse(summarize(r, j)["qualified"])

    def test_wrong_acceptance_limit(self):
        r, j = fixture()
        r[0]["workers"]["C"]["candidate"]["value"] = 200
        self.assertTrue(summarize(r, j)["qualified"])
        r[1]["workers"]["C"]["candidate"]["value"] = 200
        self.assertFalse(summarize(r, j)["qualified"])

    def test_duplicate_missing_and_error_journal(self):
        for change in ["duplicate", "missing", "error"]:
            r, j = fixture()
            if change == "duplicate":
                j += j[:2]
            elif change == "missing":
                j.pop()
            else:
                j[-1]["status"] = "error"
            self.assertFalse(summarize(r, j)["qualified"])

    def test_unknown_reference_is_not_correct(self):
        r, j = fixture()
        for x in r[:5]:
            x["gold"] = {"status": "unknown", "value": None}
        s = summarize(r, j)
        self.assertFalse(s["qualified"])
        self.assertEqual(s["arms"]["primary"]["unknown_accepted"], 5)

    def test_incomplete_assignments(self):
        r, j = fixture()
        s = summarize(r[:3], j[:12])
        self.assertFalse(s["qualified"])
        self.assertEqual(s["unstarted"], 34)

    def test_fallback_does_not_repair_confident_error(self):
        r, j = fixture()
        r[0]["workers"]["P"]["candidate"]["value"] = 200
        s = summarize(r, j)
        self.assertEqual(s["arms"]["targeted-fallback"]["wrong"], 1)
        self.assertEqual(s["paired"]["checker_correct_primary_wrong"], 1)

    def test_visual_artifacts(self):
        from native_visuals import render
        from PIL import Image

        r, j = fixture()
        with tempfile.TemporaryDirectory() as t:
            p = Path(t)
            render(p, r[:3], j[:12])
            with Image.open(p / "final_frame.png") as im:
                self.assertEqual(im.size, (1600, 900))
            with Image.open(p / "observed-replay.gif") as im:
                self.assertEqual(im.n_frames, 4)


class AdmissionTests(unittest.TestCase):
    def receipt(self):
        return dict(
            experiment="antsy-targeted-v8",
            attempt="Q0-attempt-1",
            source="a" * 40,
            runtime_sha256="b" * 64,
            verified_at=1000,
            claim_expires_at=5000,
            exclusive_claim_verified=True,
            approved_team_verified=True,
            host_idle_verified=True,
            public_page_verified=True,
            budget_reconciled=True,
            max_ocr_calls=40,
            max_model_calls=0,
            new_charge_cap_usd=0,
            claim="vishesh-antsy-targeted-v8",
            host="fixture-host",
            documents={p: sha(ROOT / p) for p in DOCS},
        )

    def test_valid_receipt(self):
        self.assertTrue(validate(self.receipt(), "a" * 40, "b" * 64, 1000))

    def test_missing_or_changed_gate(self):
        changes = {
            "experiment": "other",
            "attempt": "Q0-attempt-2",
            "source": "c" * 40,
            "runtime_sha256": "c" * 64,
            "verified_at": -1000,
            "claim_expires_at": 1100,
            "exclusive_claim_verified": False,
            "approved_team_verified": False,
            "host_idle_verified": False,
            "public_page_verified": False,
            "budget_reconciled": False,
            "max_ocr_calls": 41,
            "max_model_calls": 1,
            "new_charge_cap_usd": 1,
            "claim": "old",
            "host": "",
            "documents": {},
        }
        for k, v in changes.items():
            with self.subTest(k=k):
                r = self.receipt()
                r[k] = v
                with self.assertRaises(ValueError):
                    validate(r, "a" * 40, "b" * 64, 1000)

    def test_future_receipt(self):
        r = self.receipt()
        r["verified_at"] = 1001
        with self.assertRaises(ValueError):
            validate(r, "a" * 40, "b" * 64, 1000)


if __name__ == "__main__":
    unittest.main()


class RunnerTests(unittest.TestCase):
    def run_fixture(self, failure=False, duplicate=False):
        import argparse, contextlib, io, sys, time, types
        from unittest.mock import patch
        import native

        reports = []
        calls = []
        sr = types.SimpleNamespace(
            runs=lambda *a, **k: [{"run": native.RUN}] if duplicate else [],
            report=lambda *a, **k: reports.append(a[0]),
            upload=lambda *a: None,
        )
        runtime = {w: {"fixture": "SCRIPTED NOT MODEL EVIDENCE"} for w in ["P", "C"]}
        rows = [
            {
                "image": {"bytes": str(i).encode()},
                "ground_truth": json.dumps(
                    {"gt_parse": {"total": {"total_price": "100"}}}
                ),
            }
            for i in range(80)
        ]
        old = types.SimpleNamespace(
            REV="fixture", load_dataset=lambda *a: (rows, {"sha256": "fixture"})
        )

        def process(argv, **kw):
            # Pixel-only dispatch contract: no annotation, gold value or peer answer.
            self.assertNotIn("--gold", argv)
            self.assertNotIn("--reference", argv)
            calls.append(argv)
            dest = Path(argv[argv.index("--out") + 1])
            if failure:
                return types.SimpleNamespace(returncode=1, stderr=b"scripted fault")
            dest.write_text(
                json.dumps(
                    {"candidate": {"status": "ok", "value": "100.00"}, "raw_words": []}
                )
            )
            return types.SimpleNamespace(returncode=0, stderr=b"")

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "Q0-attempt-1"
            receipt = AdmissionTests().receipt()
            receipt.update(
                runtime_sha256=native.digest(runtime),
                verified_at=time.time(),
                claim_expires_at=time.time() + 7200,
            )
            ap = Path(tmp) / "admission.json"
            ap.write_text(json.dumps(receipt))
            args = argparse.Namespace(
                repo=Path(tmp),
                admission=ap,
                out=out,
                primary_python=Path("fixture-P"),
                checker_python=Path("fixture-C"),
                models=Path(tmp),
            )

            def urlopen(url, **kw):
                return io.BytesIO(
                    (native.ROOT / url.split("/antsy-targeted-v8/")[1]).read_bytes()
                )

            with (
                patch.dict(sys.modules, swarm_report=sr),
                patch.object(native, "source", return_value="a" * 40),
                patch.object(native, "runtimes", return_value=runtime),
                patch.object(native, "prior_hashes", return_value=(old, set())),
                patch.object(native.urllib.request, "urlopen", side_effect=urlopen),
                patch.object(native.subprocess, "run", side_effect=process),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                if duplicate:
                    with self.assertRaises(ValueError):
                        native.execute(args)
                    self.assertFalse(out.exists())
                    self.assertFalse(calls)
                    return
                native.execute(args)
            result = json.loads((out / "summary.json").read_text())
            self.assertTrue((out / "observed-replay.gif").exists())
            if failure:
                self.assertEqual(len(calls), 1)
                self.assertEqual(result["unstarted"], 39)
                self.assertFalse(result["qualified"])
                self.assertEqual(reports[-1], "fail")
                self.assertTrue((out / "partial-record.json").exists())
            else:
                self.assertEqual(len(calls), 40)
                self.assertTrue(result["qualified"])
                self.assertEqual(reports[-1], "done")

    def test_complete_scripted_path(self):
        self.run_fixture()

    def test_stop_on_first_error(self):
        self.run_fixture(failure=True)

    def test_duplicate_hub_run_blocked_before_dispatch(self):
        self.run_fixture(duplicate=True)

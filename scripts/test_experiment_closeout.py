"""Offline terminal, crash recovery, privacy and immutable post-mortem tests."""
import contextlib
import io
import json
from pathlib import Path
import sqlite3
import unittest
from unittest.mock import patch

from experiment_ops import closeout, core
import test_experiment_operations as fixtures


class CloseoutTests(unittest.TestCase):
    setUp = fixtures.OperationsTests.setUp
    put = fixtures.OperationsTests.put
    packet = fixtures.OperationsTests.packet
    dispatch = fixtures.OperationsTests.dispatch

    def report(self, root, entry, source, output):
        output.mkdir(parents=True)
        (output / "summary.json").write_text(json.dumps({
            "recorded_events": 2, "expected_events": 2, "audit_mismatch_count": 0,
            "qualification_passed": False,
            "call_accounting": {"reserved_dispatches": 2, "durable_results": 2, "unfinished_or_ambiguous": 0,
                                "reserved_usd": 0.2, "actual_usd_with_usage": 0.1, "secret": "FAKE_PRIVATE_MARKER"},
            "raw_receipt": "FAKE_PRIVATE_MARKER"}))
        print("FAKE_PRIVATE_MARKER")
        return {"status": "reported", "model_calls": 0}

    def run_result(self, status):
        def run(root, entry, prepared, receipt, output):
            output.mkdir(parents=True)
            (output / "manifest.json").write_text('{"private_fixture":"FAKE_PRIVATE_MARKER"}')
            if status == "interrupt":
                raise KeyboardInterrupt("FAKE_PRIVATE_MARKER")
            return {"status": status, "exit_code": 0 if status == "completed" else 1,
                    "qualification_passed": False, "raw_error": "FAKE_PRIVATE_MARKER"}
        return run

    def test_all_terminal_paths_write_closeout_without_claiming_scientific_review(self):
        for index, status in enumerate(("completed", "failed", "blocked", "interrupt")):
            packet = self.packet(f"attempt-{index}", f"packet-{index}.json")
            self.put("receipt.json", json.dumps({"receipt": index}))
            stdout = io.StringIO()
            with patch.object(core, "adapter_for", return_value=self.adapter), patch.object(self.adapter, "run", side_effect=self.run_result(status)), patch.object(self.adapter, "report", side_effect=self.report), contextlib.redirect_stdout(stdout):
                result = self.dispatch(packet, f"run-{index}")
            self.assertEqual(result["status"], "ambiguous" if status == "interrupt" else status)
            self.assertEqual(result["closeout_status"], "written_review_required")
            handoff = core.read_json(self.root / result["closeout"]["handoff_path"])
            self.assertEqual(handoff["scientific_review"], "unresolved")
            self.assertEqual(handoff["saved_analysis"]["qualification_passed"], False)
            self.assertNotIn("FAKE_PRIVATE_MARKER", json.dumps(result) + json.dumps(handoff) + stdout.getvalue())
            postmortem = (self.root / handoff["postmortem_path"]).read_text()
            self.assertIn("not a completed scientific review", postmortem)
            self.assertIn("Owner approval", postmortem)

    def test_closeout_failure_does_not_change_native_result_and_recovers_idempotently(self):
        packet = self.packet()
        with patch.object(core, "adapter_for", return_value=self.adapter), patch.object(self.adapter, "run", side_effect=self.run_result("completed")), patch.object(self.adapter, "report", side_effect=self.report), patch.object(closeout, "publish_file", side_effect=OSError("FAKE_PRIVATE_MARKER")):
            result = self.dispatch(packet)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["closeout_status"], "failed")
        self.assertNotIn("FAKE_PRIVATE_MARKER", json.dumps(result))
        with patch.object(core, "adapter_for", return_value=self.adapter), patch.object(self.adapter, "report", side_effect=self.report), patch.object(self.adapter, "run", side_effect=AssertionError("must not redispatch")):
            recovered = closeout.finalize(self.root, self.entry, "attempt-one")
            repeated = closeout.finalize(self.root, self.entry, "attempt-one")
        self.assertEqual(recovered, repeated)
        self.assertEqual(recovered["native_outcome"], "completed")

    def test_partial_closeout_publication_recovers_without_overwriting_first_file(self):
        packet = self.packet()
        original = closeout.publish_file
        written = []
        def fail_after_first(path, content):
            if written:
                raise OSError("fixture interruption")
            original(path, content)
            written.append((path, path.stat().st_mtime_ns, content))
        with patch.object(core, "adapter_for", return_value=self.adapter), patch.object(self.adapter, "run", side_effect=self.run_result("failed")), patch.object(self.adapter, "report", side_effect=self.report), patch.object(closeout, "publish_file", side_effect=fail_after_first):
            result = self.dispatch(packet)
        self.assertEqual(result["closeout_status"], "failed")
        with patch.object(core, "adapter_for", return_value=self.adapter), patch.object(self.adapter, "report", side_effect=self.report):
            recovered = closeout.finalize(self.root, self.entry, "attempt-one")
        self.assertEqual(recovered["closeout_status"], "written_review_required")
        self.assertEqual(written[0][0].stat().st_mtime_ns, written[0][1])
        self.assertEqual(written[0][0].read_bytes(), written[0][2])

    def test_crashed_journal_recovery_retains_ambiguity_and_cannot_fake_completion(self):
        with contextlib.closing(core.open_journal(self.root)) as connection, connection:
            connection.execute("INSERT INTO attempts(study,attempt,packet,admission,status,output,started_at) VALUES(?,?,?,?,?,?,?)",
                               (self.entry["id"], "crashed", "packet", "receipt", "dispatching", core.STATE + "/missing-output", core.now()))
        with self.assertRaisesRegex(core.OperationError, "may still be running"):
            closeout.finalize(self.root, self.entry, "crashed", outcome="completed")
        self.assertEqual(core.journal_status(self.root, self.entry["id"])[0]["status"], "dispatching")
        result = closeout.finalize(self.root, self.entry, "crashed", outcome="completed", worker_stopped=True)
        self.assertEqual(result["native_outcome"], "ambiguous")
        self.assertEqual(core.read_json(self.root / result["handoff_path"])["outcome_source"], "interrupted_journal_recovery")
        self.assertEqual(core.read_json(self.root / result["handoff_path"])["context"]["worker_stop_attestation"], "operator_attestation_not_independently_verified")
        with self.assertRaisesRegex(core.OperationError, "cannot replace"):
            closeout.finalize(self.root, self.entry, "crashed", outcome="completed")

    def test_manual_study_is_operator_assertion_and_later_evidence_creates_new_snapshot(self):
        entry = dict(self.entry, adapter=None)
        path = self.root / "manual-results"
        path.mkdir()
        first = closeout.finalize(self.root, entry, "manual", path, "failed")
        document = self.root / first["handoff_path"]
        original = document.read_bytes()
        handoff = json.loads(original)
        self.assertEqual(handoff["outcome_source"], "operator_assertion")
        self.assertEqual(handoff["saved_analysis"]["status"], "unresolved")
        (path / "later-evidence.json").write_text('{"raw":"FAKE_PRIVATE_MARKER"}')
        second = closeout.finalize(self.root, entry, "manual")
        self.assertNotEqual(first["handoff_path"], second["handoff_path"])
        self.assertEqual(document.read_bytes(), original)
        self.assertNotIn("FAKE_PRIVATE_MARKER", (self.root / second["handoff_path"]).read_text())

    def test_latest_completion_uses_recorded_time_not_attempt_name_or_recovery_time(self):
        entry = dict(self.entry, adapter=None)
        path = self.root / "manual-results"
        path.mkdir()
        with patch.object(core, "now", return_value="2026-10-04T01:00:00+00:00"):
            closeout.finalize(self.root, entry, "z-earlier", path, "completed")
        with patch.object(core, "now", return_value="2026-10-04T02:00:00+00:00"):
            closeout.finalize(self.root, entry, "a-later", path, "failed")
        closeout.finalize(self.root, entry, "z-earlier")
        latest = closeout.latest_handoff(self.root, entry["id"])
        self.assertEqual(latest["attempt"], "a-later")
        self.assertEqual(latest["native_outcome"], "failed")

    def test_latest_handoff_requires_complete_untampered_artifacts(self):
        path = self.root / "manual-results"
        path.mkdir()
        entry = dict(self.entry, adapter=None)
        result = closeout.finalize(self.root, entry, "manual", path, "failed")
        handoff = self.root / result["handoff_path"]
        handoff.write_text(handoff.read_text() + " ")
        latest = closeout.latest_handoff(self.root, entry["id"])
        self.assertEqual(latest["closeout_status"], "missing_or_incomplete")
        self.assertNotIn("handoff_sha256", latest)

    def test_historical_postmortem_requires_next_plan_even_with_empty_local_journal(self):
        entry = dict(self.entry, owner="vishesh", postmortem_path="historical-postmortem.md")
        self.assertEqual(core.journal_status(self.root, entry["id"]), [])
        self.assertTrue(core.needs_updated_plan(self.root, entry))

    def test_finalize_cannot_inventory_its_own_artifact_tree(self):
        for relative in (core.STATE, core.STATE + "/closeouts", core.STATE + "/closeouts/prior"):
            with self.subTest(relative=relative), self.assertRaisesRegex(core.OperationError, "generated closeout"):
                closeout.finalize(self.root, dict(self.entry, adapter=None), "manual", self.root / relative, "completed")
        self.assertEqual(core.journal_status(self.root, self.entry["id"]), [])

    def test_cli_closeout_failure_is_nonzero_without_relabeling_native_success(self):
        self.packet()
        stdout = io.StringIO()
        with patch.object(core, "adapter_for", return_value=self.adapter), patch.object(self.adapter, "run", side_effect=self.run_result("completed")), patch.object(closeout, "publish_file", side_effect=OSError("FAKE_PRIVATE_MARKER")), contextlib.redirect_stdout(stdout):
            code = core.main(["run", "test-study", "--packet", core.STATE + "/packet.json", "--receipt", "receipt.json", "--output", core.STATE + "/run"], root=self.root)
        result = json.loads(stdout.getvalue())
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["closeout_status"], "failed")

    def test_legacy_journal_is_inspectable_without_migration_and_finalizable(self):
        path = core.safe_path(self.root, core.STATE + "/attempts.sqlite")
        path.parent.mkdir(parents=True)
        with contextlib.closing(sqlite3.connect(path)) as connection, connection:
            connection.execute("CREATE TABLE attempts(study TEXT,attempt TEXT,packet TEXT,admission TEXT,status TEXT,output TEXT)")
            connection.execute("INSERT INTO attempts VALUES(?,?,?,?,?,?)", (self.entry["id"], "legacy", "p", "r", "failed", "missing"))
        self.assertEqual(core.journal_status(self.root, self.entry["id"])[0]["closeout_status"], None)
        result = closeout.finalize(self.root, self.entry, "legacy")
        self.assertEqual(result["closeout_status"], "written_review_required")
        self.assertEqual(result["native_outcome"], "failed")


class MechanicalReviewTests(unittest.TestCase):
    def test_observed_defects_flag_gaps_without_inventing_scientific_passes(self):
        rows = closeout.rubric({"counts": {"recorded_events": 3, "expected_events": 4, "audit_mismatch_count": 1},
                                "qualification_passed": False, "call_accounting": {"usage_missing": 1},
                                "instrument_binding": "differs_from_prepared"}, {})
        statuses = {row["dimension"]: row["status"] for row in rows}
        for key in ("data_integrity", "measurement", "capability", "resources", "reproducibility"):
            self.assertEqual(statuses[key], "gap")
        self.assertEqual(statuses["scenarios"], "unknown")
        self.assertNotIn("pass", statuses.values())
        self.assertTrue(all(row["status"] == "unknown" for row in closeout.rubric({}, {})))


if __name__ == "__main__":
    unittest.main()

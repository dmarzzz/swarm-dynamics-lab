"""Offline safety checks for preparation, lineage and single-checkout dispatch."""
from concurrent.futures import ThreadPoolExecutor
import contextlib
import io
import json
import multiprocessing
import os
from pathlib import Path
import sqlite3
import tempfile
import threading
import unittest
from unittest.mock import patch

from experiment_ops import core


class FakeAdapter:
    def prepare(self, root, entry, stage, config_path, qualification_path):
        inputs = {"instrument.py": core.file_hash(root / "instrument.py")}
        if qualification_path is not None and qualification_path.is_dir():
            inputs.update({path.relative_to(root).as_posix(): core.file_hash(path) for path in qualification_path.iterdir() if path.is_file()})
        return {"stage": stage, "input_files": inputs,
                "assignments": [{"unit": "root-1"}], "cost_envelope": {"maximum_physical_calls": 2}}

    def run(self, root, entry, prepared, receipt_path, output_path):
        return {"status": "completed", "exit_code": 0}

    def report(self, root, entry, result_path, output_path):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result_path.read_text())
        return {"status": "reported", "model_calls": 0}


def die_after_claim(root, entry, packet):
    class CrashingAdapter:
        def run(self, *args):
            os._exit(19)
    root = Path(root)
    with patch.object(core, "adapter_for", return_value=CrashingAdapter()):
        core.dispatch(root, entry, packet, root / "receipt.json", root / core.STATE / "crashed")


class OperationsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.entry = {"id": "test-study", "title": "Test", "owner": "alice", "study_path": "5-experiments/studies/alice/study",
                      "setup_path": None, "postmortem_path": None, "adapter": "theseus-v2", "checked_at": "2026-10-04",
                      "checked_commit": "a" * 40, "next_action": "Read setup"}
        (self.root / self.entry["study_path"]).mkdir(parents=True)
        (self.root / "lab/researchers/alice").mkdir(parents=True)
        self.put(core.REGISTRY, json.dumps({"schema_version": 1, "studies": [self.entry]}))
        self.put("5-experiments/toolkit/agent-experiments/templates/experiment-setup.md", "# [study ID / version]\n[Runbook](../EXPERIMENT-SETUP.md)\n[Operations](../OPERATIONS.md)\n[fill]\n")
        self.put("5-experiments/toolkit/agent-experiments/templates/protocol.md", "# Protocol\n[fill]\n")
        for name in ("agent-definition.json", "context-access.json", "run-config.json"):
            self.put("5-experiments/toolkit/agent-experiments/templates/" + name, '{}')
        self.put("instrument.py", "# frozen instrument\n")
        self.put("receipt.json", '{"admission":"fixture-only"}')
        for relative in ("scripts/experiment.py", "scripts/experiment_ops/__init__.py", "scripts/experiment_ops/core.py", "scripts/experiment_ops/theseus.py", "scripts/experiment_ops/closeout.py", "scripts/experiment_ops/iteration.py"):
            self.put(relative, "# fixture launcher\n")
        self.adapter = FakeAdapter()

    def put(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def packet(self, attempt="attempt-one", output="packet.json"):
        target = self.root / core.STATE / output
        with patch.object(core, "adapter_for", return_value=self.adapter):
            core.prepare(self.root, self.entry, "S0", attempt, None, None, target)
        return core.read_json(target)

    def dispatch(self, packet, output="run"):
        return core.dispatch(self.root, self.entry, packet, self.root / "receipt.json", self.root / core.STATE / output)

    def test_paths_reject_escape_symlinks_and_nonprivate_artifacts(self):
        for value in ("../outside", "/tmp/outside", "one/../two", "one//two", "one/./two", "one\\two"):
            with self.subTest(value=value), self.assertRaises(core.OperationError):
                core.safe_path(self.root, value)
        (self.root / "linked").symlink_to(self.root / "lab/researchers", target_is_directory=True)
        with self.assertRaises(core.OperationError):
            core.safe_path(self.root, "linked/alice")
        with self.assertRaises(core.OperationError):
            core.artifact_path(self.root, "lab/researchers/alice/receipt.json")
        self.assertEqual(core.artifact_path(self.root, core.STATE + "/receipt.json"), self.root / core.STATE / "receipt.json")

    def test_prepare_freezes_inputs_and_does_not_call_run(self):
        with patch.object(self.adapter, "run", side_effect=AssertionError("no dispatch")):
            packet = self.packet()
        core.verify_packet(self.root, self.entry, packet)
        self.put("instrument.py", "# changed instrument\n")
        with patch.object(core, "adapter_for", return_value=self.adapter), patch.object(self.adapter, "run") as run:
            with self.assertRaisesRegex(core.OperationError, "changed"):
                self.dispatch(packet)
            run.assert_not_called()
        self.assertFalse((self.root / core.STATE / "attempts.sqlite").exists())

    def test_qualification_directory_is_frozen_as_manifest_files(self):
        evidence = self.put("qualification/manifest.json", '{"fixture":true}')
        output = self.root / core.STATE / "qualified-packet.json"
        with patch.object(core, "adapter_for", return_value=self.adapter):
            core.prepare(self.root, self.entry, "S1", "qualified", None, evidence.parent, output)
        packet = core.read_json(output)
        self.assertIn("qualification/manifest.json", packet["input_files"])
        core.verify_packet(self.root, self.entry, packet)
        evidence.write_text('{"fixture":false}')
        with self.assertRaisesRegex(core.OperationError, "changed"):
            core.verify_packet(self.root, self.entry, packet)
        self.assertEqual(output.stat().st_mode & 0o777, 0o600)
        self.assertEqual(output.parent.stat().st_mode & 0o777, 0o700)

    def test_packet_mutation_and_adapter_drift_rejected_but_navigation_is_not(self):
        packet = self.packet()
        newer_entry = dict(self.entry, next_action="Updated prose", checked_at="2026-10-05")
        core.verify_packet(self.root, newer_entry, packet)
        packet["attempt"] = "renamed"
        with self.assertRaisesRegex(core.OperationError, "modified"):
            core.verify_packet(self.root, self.entry, packet)
        packet = self.packet("another", "packet-two.json")
        self.put("scripts/experiment_ops/theseus.py", "# changed adapter\n")
        with self.assertRaisesRegex(core.OperationError, "changed"):
            core.verify_packet(self.root, self.entry, packet)

    def test_prepare_and_iteration_never_overwrite(self):
        self.packet()
        with self.assertRaisesRegex(core.OperationError, "already exists"):
            self.packet()
        base = self.put("base.json", '{"model":"fixture", "sampling":{"temperature":0,"seed":1}}')
        changes = self.put("changes.json", '{"sampling":{"seed":2}}')
        output = self.root / core.STATE / "config.json"
        core.iterate(self.root, self.entry, base, changes, output)
        with self.assertRaisesRegex(core.OperationError, "already exists"):
            core.iterate(self.root, self.entry, base, changes, output)

    def test_iteration_lineage_is_deterministic_and_copies_no_authority(self):
        base = self.put("base.json", '{"model":"fixture", "sampling":{"temperature":0,"seed":1},"remove":true}')
        changes = self.put("changes.json", '{"sampling":{"seed":2},"remove":null}')
        targets = [self.root / core.STATE / name for name in ("config-one.json", "config-two.json")]
        for target in targets:
            core.iterate(self.root, self.entry, base, changes, target)
        self.assertEqual(targets[0].read_bytes(), targets[1].read_bytes())
        self.assertEqual(Path(str(targets[0]) + ".lineage.json").read_bytes(), Path(str(targets[1]) + ".lineage.json").read_bytes())
        lineage = core.read_json(Path(str(targets[0]) + ".lineage.json"))
        self.assertEqual(lineage["changed_fields"], ["/remove", "/sampling/seed"])
        self.assertIn("not transferred", lineage["authorization_status"])
        self.assertEqual(core.read_json(base)["sampling"]["seed"], 1)
        for field in ("authorization", "owner_authorization_ref", "spending_authorization", "authorized_total_usd", "claim_id", "receipt_path"):
            changes.write_text(json.dumps({field: "fixture"}))
            with self.subTest(field=field), self.assertRaisesRegex(core.OperationError, "authorization"):
                core.iterate(self.root, self.entry, base, changes, self.root / core.STATE / "bad.json")

    def test_concurrent_duplicate_dispatch_is_exactly_once(self):
        packet = self.packet()
        calls = []
        lock = threading.Lock()
        def run(*args):
            with lock:
                calls.append(1)
            return {"status": "completed", "exit_code": 0}
        def invoke():
            try:
                return self.dispatch(packet)["status"]
            except core.OperationError:
                return "duplicate"
        with patch.object(core, "adapter_for", return_value=self.adapter), patch.object(self.adapter, "run", side_effect=run):
            with ThreadPoolExecutor(max_workers=2) as executor:
                outcomes = list(executor.map(lambda _: invoke(), range(2)))
        self.assertEqual(sorted(outcomes), ["completed", "duplicate"])
        self.assertEqual(len(calls), 1)

    def test_same_native_admission_cannot_be_renamed_into_new_dispatch(self):
        first = self.packet()
        second = self.packet("different-attempt", "packet-two.json")
        with patch.object(core, "adapter_for", return_value=self.adapter):
            self.dispatch(first)
            with self.assertRaisesRegex(core.OperationError, "already claimed"):
                self.dispatch(second, "other-run")

    def test_nonzero_and_exception_are_retained_and_not_retried(self):
        packet = self.packet()
        with patch.object(core, "adapter_for", return_value=self.adapter), patch.object(self.adapter, "run", return_value={"status": "failed", "exit_code": 7}):
            self.assertEqual(self.dispatch(packet)["exit_code"], 7)
            with self.assertRaisesRegex(core.OperationError, "already claimed"):
                self.dispatch(packet)
        with contextlib.closing(core.open_journal(self.root)) as connection:
            self.assertEqual(connection.execute("SELECT status FROM attempts").fetchone()[0], "failed")

    def test_hard_process_exit_keeps_ambiguous_dispatch_consumed(self):
        packet = self.packet()
        process = multiprocessing.get_context("spawn").Process(target=die_after_claim, args=(str(self.root), self.entry, packet))
        process.start()
        process.join(timeout=10)
        if process.is_alive():
            process.kill()
            process.join()
            self.fail("fixture dispatch did not exit")
        self.assertEqual(process.exitcode, 19)
        with contextlib.closing(core.open_journal(self.root)) as connection:
            self.assertEqual(connection.execute("SELECT status FROM attempts").fetchone()[0], "dispatching")
        row = core.journal_status(self.root, self.entry["id"])[0]
        self.assertEqual({key: row[key] for key in ("attempt", "status", "output", "automatic_redispatch")}, {"attempt": "attempt-one", "status": "dispatching", "output": core.STATE + "/crashed", "automatic_redispatch": False})
        with patch.object(core, "adapter_for", return_value=self.adapter), self.assertRaisesRegex(core.OperationError, "already claimed"):
            self.dispatch(packet)

    def test_journal_inspection_does_not_create_state(self):
        self.assertEqual(core.journal_status(self.root, self.entry["id"]), [])
        self.assertFalse((self.root / core.STATE).exists())

    def test_scaffold_and_report_make_no_dispatch_and_resume_is_unsupported(self):
        output = io.StringIO()
        with patch.object(core, "adapter_for", return_value=self.adapter), patch.object(self.adapter, "run", side_effect=AssertionError("no models")):
            result = core.scaffold(self.root, "new-study", "alice", "New study")
            self.assertEqual(result["model_calls"], 0)
            setup = (self.root / result["study_path"] / "SETUP.md").read_text()
            self.assertEqual(result["study_path"], "5-experiments/studies/alice/new-study")
            self.assertIn("../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md", setup)
            self.assertIn("../../../toolkit/agent-experiments/OPERATIONS.md", setup)
            self.assertEqual(core.read_json(self.root / result["study_path"] / "spec/run-config.json")["execution"]["request_retries"], 0)
            saved = self.put("saved.json", '{"result":"already acquired"}')
            with contextlib.redirect_stdout(output):
                self.assertEqual(core.main(["report", "test-study", "--results", "saved.json", "--output", core.STATE + "/report.json"], root=self.root), 0)
                self.assertEqual(core.main(["resume", "test-study"], root=self.root), 2)
            self.assertEqual((self.root / core.STATE / "report.json").read_bytes(), saved.read_bytes())
        self.assertIn("unsupported", output.getvalue())

    def test_unexpected_error_and_child_exception_values_are_not_printed(self):
        packet = self.packet()
        output = io.StringIO()
        with patch.object(core, "adapter_for", return_value=self.adapter), patch.object(self.adapter, "run", side_effect=RuntimeError("FAKE_SECRET_MUST_STAY_PRIVATE")):
            with contextlib.redirect_stdout(output):
                status = core.main(["run", "test-study", "--packet", core.STATE + "/packet.json", "--receipt", "receipt.json", "--output", core.STATE + "/run"], root=self.root)
        self.assertEqual(status, 2)
        self.assertNotIn("FAKE_SECRET", output.getvalue())
        with contextlib.closing(core.open_journal(self.root)) as connection:
            self.assertEqual(connection.execute("SELECT status FROM attempts").fetchone()[0], "ambiguous")

    def test_fixed_adapter_admission_code_is_blocked_and_visible(self):
        from experiment_ops.theseus import AdapterError
        packet = self.packet()
        with patch.object(core, "adapter_for", return_value=self.adapter), patch.object(self.adapter, "run", side_effect=AdapterError("native_budget_history_missing")):
            result = self.dispatch(packet)
            self.assertEqual({key: result[key] for key in ("attempt", "status", "reason")}, {"attempt": "attempt-one", "status": "blocked", "reason": "native_budget_history_missing"})
        with contextlib.closing(core.open_journal(self.root)) as connection:
            self.assertEqual(connection.execute("SELECT status FROM attempts").fetchone()[0], "blocked")
        self.assertIsNone(core.adapter_error_code(AdapterError("must not print arbitrary error!")))


if __name__ == "__main__":
    unittest.main()

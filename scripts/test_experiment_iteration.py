"""Offline checks that successor approval cannot drift into another experiment."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from experiment_ops import core, iteration


class IterationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.entry = {"id": "study", "owner": "vishesh"}
        self.evidence = self.put("data/evidence.json", {"fixture": True})
        self.parent = self.put("data/handoff.json", {"study_id": "study", "attempt": "first"})
        self.latest = {"attempt": "first", "handoff_path": "data/handoff.json", "handoff_sha256": core.file_hash(self.parent)}
        self.review = {"schema_version": 1, "study_id": "study", "assessor": "fixture", "assessed_at": "2026-10-04T00:00:00Z", "attempt": "first",
                       "parent_handoff_sha256": core.file_hash(self.parent),
                       "verdict": "diagnostic", "outcome_interpretation": "Valid negative pilot; measure uncertainty.",
                       "assessments": [{"dimension": dimension, "status": "pass", "finding": "Fixture supported.",
                                        "evidence": [self.ref(self.evidence)]} for dimension in iteration.DIMENSIONS]}
        self.review_path = self.put("data/review.json", self.review)
        self.config = self.put("data/config.json", {"model": "fixture-model", "source_commit": "a" * 40, "temperature": 0})
        self.prepared = {"stage": "S0", "instrument_sha256": "1" * 64, "assignments": [{"world": 1}, {"world": 2}],
                         "config_path": "data/config.json", "sample_size_summary": {"worlds": 2},
                         "cost_envelope": {"maximum_calls": 4, "maximum_reserved_usd": 0.5},
                         "initialization_contract": {"memory": "fresh"}}
        self.plan = {"schema_version": 1, "study_id": "study", "parent_handoff": self.ref(self.parent),
                     "scientific_review": self.ref(self.review_path), "question": "Does the diagnostic discriminate?",
                     "changes": ["Add a matched control"], "acceptance_checks": ["Recompute against fixture truth"],
                     "sample_size": {"independent_unit": "world", "planned_units": 2,
                                     "rationale": "Feasibility only; no efficacy claim.", "allocation": "Two paired worlds",
                                     "analysis_plan": "Report both paired outcomes", "stopping_rule": "Complete fixed assignments"},
                     "scenarios": {"families": ["fixture"], "construction": "Frozen inputs", "challenge": "Known oracle ceiling",
                                   "realism": "Synthetic limitation", "controls": "Matched baseline", "holdout_policy": "Disjoint fixtures"},
                     "data_collection": {"records": ["assignments", "outcomes"], "missingness": "Retain every unit",
                                         "validation": "Independent fixture arithmetic", "privacy": "No secrets"},
                     "implementation": {"change_summary": "One comparison", "offline_validation": "Fixture tests pass"},
                     "resources": {"maximum_calls": 4, "maximum_cost_usd": 0.5, "machine_count": 1, "allocation_required": True,
                                   "cumulative_budget_ref": "original-authority", "machine_requirements": "Dedicated existing fleet host"}}
        self.plan_path = self.put("data/plan.json", self.plan)
        self.mock_latest = patch("experiment_ops.closeout.latest_handoff", side_effect=lambda *args: self.latest)
        self.mock_latest.start()
        self.addCleanup(self.mock_latest.stop)

    def put(self, relative, value):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value))
        return path

    def ref(self, path):
        return {"path": path.relative_to(self.root).as_posix(), "sha256": core.file_hash(path)}

    def freeze(self):
        return iteration.freeze_next_plan(self.root, self.entry, self.prepared, self.plan_path)

    def approval(self, binding):
        self.record = {"schema_version": 1, "study_id": "study", "decision": "approved", "approver_role": "owner",
                       "plan_sha256": binding["plan"]["sha256"], "execution_sha256": binding["execution_sha256"],
                       "authorization_ref": "fixture-owner-decision", "scopes": ["launch", "provision"],
                       "recorded_at": "2026-10-04T00:00:00Z"}
        return self.put("data/approval.json", self.record)

    def test_matching_approval_and_source_metadata_refresh_preserve_scope(self):
        binding = self.freeze()
        approval = self.approval(binding)
        packet = {"prepared": self.prepared, "next_run": binding}
        result = iteration.validate_update_approval(self.root, self.entry, packet, approval)
        self.assertTrue(result["approval_is_operator_attestation"])
        self.put("data/config.json", {"model": "fixture-model", "source_commit": "b" * 40, "temperature": 0})
        iteration.validate_update_approval(self.root, self.entry, packet, approval)

    def test_existing_valid_allocation_needs_no_new_provision_scope(self):
        self.plan["resources"]["allocation_required"] = False
        self.put("data/plan.json", self.plan)
        binding = self.freeze()
        approval = self.approval(binding)
        self.record["scopes"] = ["launch"]
        self.put("data/approval.json", self.record)
        iteration.validate_update_approval(self.root, self.entry, {"prepared": self.prepared, "next_run": binding}, approval)

    def test_changed_model_assignments_or_context_invalidates_approval(self):
        binding = self.freeze()
        approval = self.approval(binding)
        for key, value in [("assignments", [{"world": 99}]), ("initialization_contract", {"memory": "inherited"}), ("adapter_runtime", {"python_version": "changed"})]:
            changed = copy.deepcopy(self.prepared)
            changed[key] = value
            with self.subTest(key=key), self.assertRaises(core.OperationError):
                iteration.validate_update_approval(self.root, self.entry, {"prepared": changed, "next_run": binding}, approval)
        self.put("data/config.json", {"model": "different-model", "source_commit": "a" * 40, "temperature": 0})
        with self.assertRaises(core.OperationError):
            iteration.validate_update_approval(self.root, self.entry, {"prepared": self.prepared, "next_run": binding}, approval)

    def test_pending_wrong_study_and_launch_only_approval_cannot_allocate(self):
        binding = self.freeze()
        approval = self.approval(binding)
        for key, value in [("decision", "pending"), ("study_id", "other"), ("scopes", ["launch"]),
                           ("plan_sha256", "0" * 64), ("approver_role", "researcher")]:
            record = dict(self.record, **{key: value})
            self.put("data/approval.json", record)
            with self.subTest(key=key), self.assertRaises(core.OperationError):
                iteration.validate_update_approval(self.root, self.entry, {"prepared": self.prepared, "next_run": binding}, approval)

    def test_no_approval_no_plan_and_newer_closeout_are_blocked(self):
        with self.assertRaises(core.OperationError):
            iteration.freeze_next_plan(self.root, self.entry, self.prepared, None)
        binding = self.freeze()
        with self.assertRaises(core.OperationError):
            iteration.validate_update_approval(self.root, self.entry, {"prepared": self.prepared, "next_run": binding}, None)
        self.latest = {"handoff_path": "newer/handoff.json", "handoff_sha256": "0" * 64}
        with self.assertRaises(core.OperationError):
            self.freeze()

    def test_missing_quality_unknown_without_action_and_stale_evidence_block(self):
        for mutate in (lambda r: r["assessments"].pop(),
                       lambda r: r["assessments"][0].update(status="unknown"),
                       lambda r: r.update(verdict="complete_valid_result")):
            review = copy.deepcopy(self.review)
            mutate(review)
            self.put("data/review.json", review)
            self.plan["scientific_review"] = self.ref(self.review_path)
            self.put("data/plan.json", self.plan)
            with self.assertRaises(core.OperationError):
                self.freeze()
        self.put("data/review.json", self.review)
        self.plan["scientific_review"] = self.ref(self.review_path)
        self.put("data/plan.json", self.plan)
        self.put("data/evidence.json", {"fixture": "changed"})
        with self.assertRaises(core.OperationError):
            self.freeze()

    def test_sample_and_resource_understatement_block(self):
        for section, key, value in [("sample_size", "planned_units", 1), ("resources", "maximum_calls", 3),
                                    ("resources", "maximum_cost_usd", 0.1), ("resources", "maximum_cost_usd", float("nan"))]:
            plan = copy.deepcopy(self.plan)
            plan[section][key] = value
            self.put("data/plan.json", plan)
            with self.subTest(key=key), self.assertRaises(core.OperationError):
                self.freeze()

    def test_live_attempt_blocks_next_plan_even_with_older_completed_handoff(self):
        with patch.object(core, "journal_status", return_value=[{"status": "dispatching"}]), self.assertRaises(core.OperationError):
            self.freeze()


if __name__ == "__main__":
    unittest.main()

"""Bind a successor run to its assessed predecessor and owner-approved update.

Approval is a private operator attestation of an actual owner decision, not an
authentication service. This module never issues approvals or allocates hosts.
"""
from datetime import datetime
import math

from .core import OperationError, SHA256, digest, file_hash, read_json, safe_path

DIMENSIONS = ("question", "scenarios", "controls", "capability", "measurement",
              "sample_size", "agent_context", "data_integrity", "resources",
              "reproducibility", "visualization")


def require(condition, message):
    if not condition:
        raise OperationError(message)


def text(value):
    return isinstance(value, str) and bool(value.strip()) and value.strip().lower() not in {
        "todo", "tbd", "unresolved", "[fill]"}


def strings(value):
    return isinstance(value, list) and bool(value) and all(text(item) for item in value)


def number(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def reference(root, value):
    require(isinstance(value, dict) and isinstance(value.get("sha256"), str)
            and SHA256.fullmatch(value["sha256"]), "next-run evidence reference requires a SHA-256")
    path = safe_path(root, value.get("path"), exists=True)
    require(path.is_file() and file_hash(path) == value["sha256"], "next-run evidence changed or is not a file")
    return path


def execution_contract(root, prepared):
    # Harmless source-commit and receipt-URL refreshes do not change the approved
    # scientific contract. Native source/admission checks still verify them.
    config = {}
    if prepared.get("config_path"):
        config = read_json(safe_path(root, prepared["config_path"], exists=True))
        require(isinstance(config, dict), "next-run effective configuration must be an object")
        config = {key: value for key, value in config.items() if key not in {
            "source_commit", "plan_url", "pre_run_review_url", "prospective_repair_review_url",
            "pricing_verified_epoch"}}
    return {"stage": prepared.get("stage"),
            "instrument_sha256": prepared.get("instrument_sha256"),
            "assignment_sha256": digest(prepared.get("assignments", [])),
            "effective_config_sha256": digest(config),
            "sample_size_summary": prepared.get("sample_size_summary"),
            "cost_envelope": prepared.get("cost_envelope", prepared.get("cost")),
            "adapter_runtime": prepared.get("adapter_runtime"),
            "initialization_contract": prepared.get("initialization_contract")}


def freeze_next_plan(root, entry, prepared, path):
    from .closeout import latest_handoff
    from .core import journal_status
    require(not any(row["status"] == "dispatching" for row in journal_status(root, entry["id"])),
            "reconcile the unfinished local attempt before planning its successor")
    require(path is not None, "assess the previous post-mortem and supply --next-plan before preparing a successor")
    path = safe_path(root, path.relative_to(root).as_posix(), exists=True)
    plan = read_json(path)
    require(isinstance(plan, dict) and plan.get("schema_version") == 1
            and plan.get("study_id") == entry["id"], "next-run plan targets a different study or schema")
    latest = latest_handoff(root, entry["id"])
    require(latest and latest.get("handoff_path") and latest.get("handoff_sha256"),
            "finalize the preceding attempt before preparing its successor")
    parent = plan.get("parent_handoff")
    reference(root, parent)
    require(parent["path"] == latest["handoff_path"] and parent["sha256"] == latest["handoff_sha256"],
            "next-run plan does not use the latest local closeout")
    review_ref = plan.get("scientific_review")
    review = read_json(reference(root, review_ref))
    require(isinstance(review, dict) and review.get("schema_version") == 1
            and review.get("study_id") == entry["id"]
            and review.get("parent_handoff_sha256") == parent["sha256"],
            "scientific post-mortem must bind this study and predecessor")
    require(text(review.get("assessor")) and text(review.get("assessed_at"))
            and review.get("attempt") == latest.get("attempt"),
            "scientific post-mortem requires assessor, date and matching parent attempt")
    require(review.get("verdict") in {"advance", "repair", "diagnostic"},
            "post-mortem must justify a next run; blocked or complete findings do not authorize continuation")
    require(text(review.get("outcome_interpretation")), "post-mortem requires a scoped interpretation")
    assessments = review.get("assessments")
    require(isinstance(assessments, list) and len(assessments) == len(DIMENSIONS)
            and all(isinstance(row, dict) for row in assessments)
            and {row.get("dimension") for row in assessments} == set(DIMENSIONS),
            "post-mortem must assess every run-quality dimension exactly once")
    for row in assessments:
        require(row.get("status") in {"pass", "gap", "unknown", "not_applicable"}
                and text(row.get("finding")), "quality assessments require a status and reason")
        evidence = row.get("evidence", [])
        require(isinstance(evidence, list), "quality evidence must be a list of pinned references")
        if row["status"] == "pass":
            require(bool(evidence), "a passing quality assessment needs pinned evidence")
        for item in evidence:
            reference(root, item)
        if row["status"] in {"gap", "unknown"}:
            require(text(row.get("next_action")) and text(row.get("acceptance_check")),
                    "every unresolved quality gap needs an action and acceptance check")
    require(text(plan.get("question")) and strings(plan.get("changes"))
            and strings(plan.get("acceptance_checks")), "next-run question, changes and acceptance checks are required")
    sections = {
        "sample_size": ("independent_unit", "rationale", "allocation", "analysis_plan", "stopping_rule"),
        "scenarios": ("construction", "challenge", "realism", "controls", "holdout_policy"),
        "data_collection": ("missingness", "validation", "privacy"),
        "implementation": ("change_summary", "offline_validation"),
        "resources": ("cumulative_budget_ref", "machine_requirements"),
    }
    for section, fields in sections.items():
        require(isinstance(plan.get(section), dict) and all(text(plan[section].get(key)) for key in fields),
                "next-run plan is missing required design, collection or resource details")
    require(strings(plan["scenarios"].get("families")) and strings(plan["data_collection"].get("records")),
            "next-run scenarios and collection records must be explicit")
    sample, resources = plan["sample_size"], plan["resources"]
    require(type(sample.get("planned_units")) is int and sample["planned_units"] > 0,
            "next-run independent sample count must be a positive integer")
    require(type(resources.get("maximum_calls")) is int and resources["maximum_calls"] >= 0
            and number(resources.get("maximum_cost_usd"))
            and type(resources.get("machine_count")) is int and resources["machine_count"] >= 0
            and type(resources.get("allocation_required")) is bool
            and (not resources["allocation_required"] or resources["machine_count"] > 0),
            "next-run resource ceilings must be finite nonnegative numbers")
    planned = prepared.get("sample_size_summary", {})
    if "worlds" in planned:
        require(sample["planned_units"] == planned["worlds"], "planned sample count differs from prepared world assignments")
    cost = prepared.get("cost_envelope", {})
    if "maximum_calls" in cost:
        require(resources["maximum_calls"] >= cost["maximum_calls"], "proposal call ceiling is below prepared calls")
    if "maximum_reserved_usd" in cost:
        require(resources["maximum_cost_usd"] >= cost["maximum_reserved_usd"], "proposal cost ceiling is below prepared exposure")
    contract = execution_contract(root, prepared)
    return {"plan": {"path": path.relative_to(root).as_posix(), "sha256": file_hash(path)},
            "scientific_review": review_ref, "parent_handoff": parent,
            "execution_contract": contract, "execution_sha256": digest(contract),
            "provisioning_requested": resources["allocation_required"],
            "approval_status": "owner_decision_required"}


def validate_update_approval(root, entry, packet, path):
    binding = packet.get("next_run")
    require(isinstance(binding, dict), "successor packet lacks a reviewed next-run plan")
    plan_path = reference(root, binding.get("plan"))
    current = freeze_next_plan(root, entry, packet["prepared"], plan_path)
    require(current == binding, "successor evidence or execution contract changed; prepare the updated proposal")
    require(path is not None, "owner approval of this update is required before allocation or launch")
    record = read_json(path)
    require(isinstance(record, dict) and record.get("schema_version") == 1
            and record.get("study_id") == entry["id"] and record.get("decision") == "approved"
            and record.get("approver_role") == "owner", "an explicit owner approval record is required")
    require(record.get("plan_sha256") == binding["plan"]["sha256"]
            and record.get("execution_sha256") == binding["execution_sha256"],
            "owner approval does not match this proposal and execution contract")
    require(text(record.get("authorization_ref")), "approval must reference the actual owner decision")
    scopes = record.get("scopes")
    require(isinstance(scopes, list) and all(isinstance(item, str) for item in scopes)
            and "launch" in scopes and (not binding["provisioning_requested"] or "provision" in scopes),
            "owner approval does not cover the proposed allocation and launch")
    try:
        when = datetime.fromisoformat(record.get("recorded_at", "").replace("Z", "+00:00"))
        require(when.tzinfo is not None, "approval timestamp requires a timezone")
    except (ValueError, TypeError, AttributeError):
        raise OperationError("approval timestamp is invalid") from None
    return {"approval_record_sha256": file_hash(path), "plan_sha256": binding["plan"]["sha256"],
            "execution_sha256": binding["execution_sha256"], "approval_is_operator_attestation": True}

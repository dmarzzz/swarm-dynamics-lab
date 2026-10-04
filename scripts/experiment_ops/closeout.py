"""Offline, immutable operational post-mortems; never a substitute for scientific review."""
from contextlib import closing, redirect_stderr, redirect_stdout
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile

from . import core, trace_receipts


OUTCOMES = {"completed", "failed", "blocked", "ambiguous"}
COUNT_FIELDS = ("worlds", "scenario_families", "trajectories", "primary_worlds", "planned_calls")
COST_FIELDS = ("maximum_calls", "maximum_input_bytes_per_call", "maximum_output_tokens_per_call",
               "maximum_reserved_usd", "native_study_cap_usd", "native_study_call_cap", "concurrency", "automatic_retries")
ACCOUNTING_FIELDS = ("reserved_dispatches", "durable_results", "unfinished_or_ambiguous", "reserved_usd",
                     "actual_usd_with_usage", "usage_missing", "input_tokens_known", "output_tokens_known")


def numbers(value, keys):
    if not isinstance(value, dict):
        return {}
    return {key: value[key] for key in keys if type(value.get(key)) in (int, float) and math.isfinite(value[key]) and value[key] >= 0}


def prepared_context(packet):
    prepared = packet.get("prepared", {})
    sample = numbers(prepared.get("sample_size_summary"), COUNT_FIELDS)
    context = {"planned_sample": sample, "planned_cost": numbers(prepared.get("cost_envelope"), COST_FIELDS)}
    if isinstance(prepared.get("assignments"), list):
        context["planned_assignment_count"] = len(prepared["assignments"])
    for key in ("packet_sha256", "assignment_sha256", "instrument_sha256", "config_sha256"):
        value = packet.get(key, prepared.get(key))
        if isinstance(value, str) and core.SHA256.fullmatch(value):
            context[key] = value
    return context


def safe_result(result):
    safe = {"status": result["status"] if result.get("status") in OUTCOMES else "ambiguous"}
    if type(result.get("exit_code")) is int:
        safe["exit_code"] = result["exit_code"]
    if type(result.get("qualification_passed")) is bool:
        safe["qualification_passed"] = result["qualification_passed"]
    return safe


def saved_context(value):
    if not isinstance(value, dict):
        return {}
    context = {"planned_sample": numbers(value.get("planned_sample"), COUNT_FIELDS),
               "planned_cost": numbers(value.get("planned_cost"), COST_FIELDS)}
    if type(value.get("planned_assignment_count")) is int and value["planned_assignment_count"] >= 0:
        context["planned_assignment_count"] = value["planned_assignment_count"]
    for key in ("packet_sha256", "assignment_sha256", "instrument_sha256", "config_sha256"):
        if isinstance(value.get(key), str) and core.SHA256.fullmatch(value[key]):
            context[key] = value[key]
    if isinstance(value.get("native_result"), dict):
        context["native_result"] = safe_result(value["native_result"])
    if value.get("worker_stop_attestation") == "operator_attestation_not_independently_verified":
        context["worker_stop_attestation"] = value["worker_stop_attestation"]
    return context


def inventory(path):
    if not path.exists():
        return {"status": "missing", "file_count": 0}
    if not path.is_dir() or path.is_symlink():
        raise core.OperationError("closeout evidence must be an ordinary directory")
    entries, size = [], 0
    for child in sorted(path.rglob("*")):
        if child.is_symlink():
            raise core.OperationError("closeout evidence contains an unsupported symlink")
        if child.is_file():
            digest = hashlib.sha256()
            with child.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
                    size += len(chunk)
            entries.append([child.relative_to(path).as_posix(), digest.hexdigest()])
    # Filenames and raw source contents never enter the generated report.
    return {"status": "inventoried", "sha256": core.digest(entries), "file_count": len(entries), "bytes": size}


def saved_analysis(root, entry, result_path):
    if not result_path.is_dir():
        return {"status": "unavailable", "reason": "saved_result_directory_missing"}
    if not entry.get("adapter"):
        return {"status": "unresolved", "reason": "manual_study_requires_explicit_scientific_analysis"}
    try:
        parent = core.safe_path(root, core.STATE)
        core.private_parents(parent)
        with tempfile.TemporaryDirectory(prefix="closeout-analysis-", dir=parent) as temporary:
            output = Path(temporary) / "report"
            with open(os.devnull, "w") as sink, redirect_stdout(sink), redirect_stderr(sink):
                adapter = core.adapter_for(entry)
                validation = adapter.analysis_fingerprint(root, entry) if hasattr(adapter, "analysis_fingerprint") else {}
                adapter.report(root, entry, result_path, output)
            summary = core.read_json(output / "summary.json")
        result = {"status": "recomputed_from_saved_evidence", "model_calls": 0,
                  "counts": numbers(summary, ("recorded_events", "expected_events", "audit_mismatch_count")),
                  "call_accounting": numbers(summary.get("call_accounting"), ACCOUNTING_FIELDS),
                  "cost_scope": "saved per-call usage only; cumulative budget reconciliation remains unresolved",
                  "unknown_exposure": "retain native reservations; closeout issues no refunds or new authority"}
        if type(summary.get("qualification_passed")) is bool:
            result["qualification_passed"] = summary["qualification_passed"]
        if isinstance(validation.get("instrument_sha256"), str) and core.SHA256.fullmatch(validation["instrument_sha256"]):
            result["analysis_instrument_sha256"] = validation["instrument_sha256"]
        return result
    except Exception:
        return {"status": "unresolved", "reason": "saved_analysis_not_available_or_not_validated"}


def rubric(analysis, context):
    rows = [
        {"dimension": "question", "status": "unknown",
         "next_action": "State what decision the result informs and which plausible mechanisms remain unidentified; justify the value of another run."},
        {"dimension": "scenarios", "status": "unknown",
         "next_action": "Identify missing realistic challenge regimes and scenario families; specify held-out generation, leakage controls and competence checks for each change."},
        {"dimension": "controls", "status": "unknown",
         "next_action": "Audit paired assignment, competent reference policies, matched information and resources, and targeted ablations."},
        {"dimension": "capability", "status": "unknown",
         "next_action": "Interpret qualification separately from treatment effects; distinguish an instrument defect, capability failure and valid adverse result."},
        {"dimension": "measurement", "status": "unknown",
         "next_action": "Check endpoint definitions, scorer correctness, denominator consistency, effect uncertainty and missing-outcome bounds."},
        {"dimension": "sample_size", "status": "unknown",
         "next_action": "Separate independent roots from agents, calls and repeats; choose the next sample count using a stated effect or precision target and cumulative cost."},
        {"dimension": "agent_context", "status": "unknown",
         "next_action": "Compare delivered-context and startup receipts with the frozen definition; document role differences, memory resets, truncation and deviations."},
        {"dimension": "data_integrity", "status": "unknown",
         "next_action": "Reconcile all assigned, started, terminal, graded and missing outcomes; preserve failed attempts and audit exclusion or transport-retry decisions."},
        {"dimension": "resources", "status": "unknown",
         "next_action": "Reconcile actual and reserved spend, unresolved exposure and remaining cumulative authority; estimate the next total cost without resetting the ledger."},
        {"dimension": "reproducibility", "status": "unknown",
         "next_action": "Bind source, configuration, assignment and analysis versions; verify deterministic initialization and distinguish replay from fresh model sampling."},
        {"dimension": "visualization", "status": "unknown",
         "next_action": "Check that tables and plots reconcile to saved evidence and expose uncertainty, failed outcomes, denominators and claim boundaries."},
    ]
    by_dimension = {row["dimension"]: row for row in rows}
    counts = analysis.get("counts", {})
    recorded, expected = counts.get("recorded_events"), counts.get("expected_events")
    if recorded is not None and expected is not None and recorded != expected:
        by_dimension["data_integrity"].update(status="gap", finding=f"Saved analysis counted {recorded} events against {expected} expected; reconcile the missing or excess records.")
    if counts.get("audit_mismatch_count", 0) > 0:
        by_dimension["measurement"].update(status="gap", finding="Saved reference-score audit reports mismatches; do not rely on the affected estimates until reconciled.")
    if analysis.get("qualification_passed") is False:
        by_dimension["capability"].update(status="gap", finding="The saved native qualification result is false; broader stage admission remains closed pending diagnosis.")
    accounting = analysis.get("call_accounting", {})
    if accounting.get("unfinished_or_ambiguous", 0) > 0 or accounting.get("usage_missing", 0) > 0:
        by_dimension["resources"].update(status="gap", finding="Saved call records contain uncertain completion or missing usage; retain reservations and reconcile exposure.")
    if analysis.get("instrument_binding") == "differs_from_prepared":
        by_dimension["reproducibility"].update(status="gap", finding="Saved-data analysis used a different instrument fingerprint; identify it as a revised analysis, not the original run result.")
    trace = analysis.get("trace_receipts", {})
    if trace and trace.get("status") != "verified_declared_coverage":
        by_dimension["data_integrity"].update(status="gap", trace_status=trace.get("status", "unavailable"))
        by_dimension["data_integrity"]["next_action"] += " Inspect trace_receipts coverage; missing manifests are not complete tracing."
    # Other dimensions remain unknown; passing these mechanical checks alone
    # does not establish scenario quality, causal validity or a scientific pass.
    return rows


def markdown(payload):
    lines = ["# Automated operational post-mortem", "",
             "This deterministic closeout records retained evidence and unresolved questions. It is not a completed scientific review or an approved next-run plan.", "",
             f"- Study: `{payload['study_id']}`", f"- Attempt: `{payload['attempt']}`",
             f"- Native execution outcome: **{payload['native_outcome']}**",
             f"- Outcome source: `{payload['outcome_source']}`",
             f"- Saved evidence inventory: `{payload['evidence_inventory']['status']}`",
             f"- Saved-data analysis: `{payload['saved_analysis']['status']}`", "",
             "## Retained quantitative evidence", "",
             "Counts below are mechanical observations or declared planning metadata. Planned units are not completed observations, and calls or agents are not independent samples.", "",
             "```json", json.dumps({"planning_context": payload["context"], "saved_analysis": payload["saved_analysis"]}, indent=2, sort_keys=True), "```", "",
             "## Run-quality gaps to resolve", ""]
    for row in payload["rubric"]:
        lines.extend([f"### {row['dimension'].replace('_', ' ').capitalize()} — {row['status']}", "", row.get("finding", "No automated scientific judgment is available."), "", row["next_action"], ""])
    lines.extend(["## Required next-session workflow", ""])
    lines.extend(f"{index}. {text}" for index, text in enumerate(payload["required_next_session_steps"], 1))
    lines.extend(["", "Owner approval of an updated plan must precede provisioning and the next launch. Existing researcher-review decisions and cumulative budget/account boundaries retain their scope; this record grants no authority.", ""])
    return "\n".join(lines)


def publish_file(path, content):
    """Atomic no-clobber publication; recover an interrupted multi-file publication."""
    if path.exists():
        if path.is_symlink() or not path.is_file() or path.read_bytes() != content:
            raise core.OperationError("immutable closeout artifact differs; preserve it and investigate")
        return
    core.private_parents(path.parent)
    descriptor, temporary = tempfile.mkstemp(prefix=".closeout-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError:
            if path.read_bytes() != content:
                raise core.OperationError("concurrent immutable closeout mismatch") from None
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        os.unlink(temporary)


def result_directory(root, path):
    path = core.safe_path(root, path.relative_to(root).as_posix())
    output_root = core.safe_path(root, core.STATE + "/closeouts")
    if output_root.is_relative_to(path) or path.is_relative_to(output_root):
        raise core.OperationError("result evidence must not contain or be generated closeout artifacts")
    return path


def finalize(root, entry, attempt, result_path=None, outcome=None, worker_stopped=False):
    if not isinstance(attempt, str) or not core.SLUG.fullmatch(attempt) or outcome is not None and outcome not in OUTCOMES:
        raise core.OperationError("finalize requires a valid attempt and terminal outcome")
    if result_path is not None:
        result_path = result_directory(root, result_path)
    with closing(core.open_journal(root)) as connection:
        row = connection.execute("SELECT status,output,context_json,outcome_source FROM attempts WHERE study=? AND attempt=?", (entry["id"], attempt)).fetchone()
        if row is None:
            if result_path is None or outcome is None:
                raise core.OperationError("manual finalize requires results and an explicitly reported outcome")
            relative = result_path.relative_to(root).as_posix()
            identity = "manual:" + core.digest({"study": entry["id"], "attempt": attempt})
            with connection:
                connection.execute("INSERT INTO attempts(study,attempt,packet,admission,status,output,started_at,completed_at,context_json,outcome_source,closeout_status) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                    (entry["id"], attempt, identity, identity, outcome, relative, None, core.now(), "{}", "operator_assertion", "pending"))
            row = (outcome, relative, "{}", "operator_assertion")
        native_outcome, relative, context_json, outcome_source = row
        if result_path is not None and result_path.relative_to(root).as_posix() != relative:
            raise core.OperationError("finalize results do not match the retained attempt")
        if outcome is not None and native_outcome != "dispatching" and outcome != native_outcome:
            raise core.OperationError("finalize cannot replace a retained native outcome")
        if native_outcome == "dispatching":
            if worker_stopped is not True:
                raise core.OperationError("attempt may still be running; stop and verify its worker before attesting --worker-stopped")
            native_outcome = "ambiguous"
            outcome_source = "interrupted_journal_recovery"
            retained_context = saved_context(json.loads(context_json or "{}"))
            retained_context["worker_stop_attestation"] = "operator_attestation_not_independently_verified"
            context_json = json.dumps(retained_context, sort_keys=True)
            with connection:
                connection.execute("UPDATE attempts SET status=?,completed_at=?,outcome_source=?,context_json=? WHERE study=? AND attempt=?",
                    (native_outcome, core.now(), outcome_source, context_json, entry["id"], attempt))
        result_path = result_directory(root, core.safe_path(root, relative))
        try:
            context = saved_context(json.loads(context_json or "{}"))
            before = inventory(result_path)
            analysis = saved_analysis(root, entry, result_path)
            analysis["trace_receipts"] = trace_receipts.audit(result_path, study=entry["id"], attempt=attempt)
            if analysis.get("analysis_instrument_sha256") and context.get("instrument_sha256"):
                analysis["instrument_binding"] = "matches_prepared" if analysis["analysis_instrument_sha256"] == context["instrument_sha256"] else "differs_from_prepared"
            else:
                analysis["instrument_binding"] = "unresolved"
            if inventory(result_path) != before:
                raise core.OperationError("saved evidence changed during closeout; retry after the writer stops")
            payload = {"schema_version": 1, "kind": "automated_operational_post_mortem", "study_id": entry["id"],
                       "attempt": attempt, "native_outcome": native_outcome, "outcome_source": outcome_source or "legacy_native_journal",
                       "context": context, "evidence_inventory": before, "saved_analysis": analysis,
                       "scientific_review": "unresolved", "rubric": rubric(analysis, context),
                       "required_next_session_steps": [
                           "Read this post-mortem and the retained evidence before proposing another attempt.",
                           "Evaluate every unresolved quality dimension and record evidence-linked conclusions, including what the run cannot establish.",
                           "Write a concrete updated plan: question, controls, independent sample counts and justification, scenario changes, data checks, context policy, stopping rules and cumulative cost.",
                           "Obtain the owner's explicit approval bound to the updated plan before provisioning or launching; approval is not inherited from this closeout.",
                           "Refresh public registration, qualification, budget and approved-account/allocation evidence required by the native launcher."]}
            snapshot = core.digest(payload)
            directory = core.artifact_path(root, f"{core.STATE}/closeouts/{entry['id']}/{attempt}/{snapshot}")
            postmortem = markdown(payload).encode()
            handoff = {**payload, "snapshot_sha256": snapshot,
                       "postmortem_path": (directory / "POST-MORTEM.md").relative_to(root).as_posix(),
                       "postmortem_sha256": hashlib.sha256(postmortem).hexdigest()}
            handoff_bytes = (json.dumps(handoff, indent=2, sort_keys=True) + "\n").encode()
            manifest = {"schema_version": 1, "snapshot_sha256": snapshot, "postmortem_sha256": handoff["postmortem_sha256"],
                        "handoff_sha256": hashlib.sha256(handoff_bytes).hexdigest()}
            publish_file(directory / "POST-MORTEM.md", postmortem)
            publish_file(directory / "handoff.json", handoff_bytes)
            publish_file(directory / "COMPLETE.json", (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode())
            handoff_path = (directory / "handoff.json").relative_to(root).as_posix()
            with connection:
                connection.execute("UPDATE attempts SET closeout_status='written_review_required',closeout_path=? WHERE study=? AND attempt=?",
                                   (handoff_path, entry["id"], attempt))
            return {"closeout_status": "written_review_required", "handoff_path": handoff_path,
                    "handoff_sha256": manifest["handoff_sha256"], "native_outcome": native_outcome, "model_calls": 0}
        except BaseException:
            with connection:
                connection.execute("UPDATE attempts SET closeout_status='failed' WHERE study=? AND attempt=?", (entry["id"], attempt))
            return {"closeout_status": "failed", "native_outcome": native_outcome,
                    "reason": "closeout_generation_failed; retained native outcome is unchanged", "model_calls": 0}


def latest_handoff(root, study_id):
    attempts = core.journal_status(root, study_id)
    completed = [row for row in attempts if row["status"] != "dispatching"]
    if not completed:
        return None
    row = completed[-1]
    result = {"attempt": row["attempt"], "completed_at": row.get("completed_at"), "native_outcome": row["status"],
              "closeout_status": row.get("closeout_status", "missing"), "handoff_path": row.get("closeout_path")}
    if result["handoff_path"] and result["closeout_status"] == "written_review_required":
        try:
            path = core.safe_path(root, result["handoff_path"], exists=True)
            manifest_path = core.safe_path(root, (path.parent / "COMPLETE.json").relative_to(root).as_posix(), exists=True)
            manifest = core.read_json(manifest_path)
            handoff = core.read_json(path)
            postmortem = core.safe_path(root, handoff["postmortem_path"], exists=True)
            actual = core.file_hash(path)
            if manifest.get("handoff_sha256") != actual or core.file_hash(postmortem) != manifest.get("postmortem_sha256") or handoff.get("study_id") != study_id or handoff.get("attempt") != row["attempt"]:
                raise core.OperationError("closeout integrity mismatch")
            result["handoff_sha256"] = actual
        except Exception:
            result["closeout_status"] = "missing_or_incomplete"
    return result

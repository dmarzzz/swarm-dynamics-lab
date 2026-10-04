"""Standard-library operations shell. Native adapters retain all launch gates.

The SQLite journal is a single-checkout duplicate-dispatch guard, not a budget
ledger or distributed lock. A claimed attempt remains consumed after failure or
interruption. There is deliberately no reset, retry, force, or approval command.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sqlite3


REGISTRY = "tooling/agent-experiments/operations.json"
STATE = "data/experiment-operations"
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
FORBIDDEN_COPY = {"authorization", "authorization_receipt", "admission_receipt",
                  "approval", "approvals", "results", "qualification_result"}


class OperationError(Exception):
    """Only fixed, public-safe messages belong in this exception."""


def now():
    return datetime.now(timezone.utc).isoformat()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_path(root, value, *, exists=False):
    """Require an ordinary repository-relative path, rejecting every symlink."""
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise OperationError("invalid repository-relative path")
    parts = PurePosixPath(value)
    if parts.is_absolute() or any(p in {".", ".."} for p in value.split("/")):
        raise OperationError("path traversal is not permitted")
    if value.endswith("/") or "//" in value:
        raise OperationError("path must use a canonical repository-relative spelling")
    root = Path(root).resolve()
    target = root.joinpath(*parts.parts)
    if not target.is_relative_to(root) or target == root:
        raise OperationError("path is outside the repository")
    cursor = root
    for part in parts.parts:
        cursor /= part
        if cursor.is_symlink():
            raise OperationError("symlink paths are not supported")
    if exists and not target.exists():
        raise OperationError("required local input is missing")
    return target


def artifact_path(root, value):
    target = safe_path(root, value)
    if not target.is_relative_to(safe_path(root, STATE)) or target == safe_path(root, STATE):
        raise OperationError("operational artifacts must be under data/experiment-operations")
    return target


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError):
        raise OperationError("could not read a valid local JSON input") from None


def write_new_json(path, value):
    private_parents(path.parent)
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError:
        raise OperationError("output already exists; choose a fresh artifact path") from None


def private_parents(directory):
    missing = []
    while not directory.exists():
        missing.append(directory)
        directory = directory.parent
    for path in reversed(missing):
        path.mkdir(mode=0o700, exist_ok=True)


def registry(root):
    data = read_json(safe_path(root, REGISTRY, exists=True))
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("studies"), list):
        raise OperationError("unsupported operations registry schema")
    seen = set()
    for entry in data["studies"]:
        if not isinstance(entry, dict) or not SLUG.fullmatch(entry.get("id", "")) or entry["id"] in seen:
            raise OperationError("invalid or duplicate registry study id")
        seen.add(entry["id"])
        for field in ("title", "owner", "checked_at", "checked_commit", "next_action"):
            if not isinstance(entry.get(field), str) or not entry[field]:
                raise OperationError("registry entry is missing descriptive metadata")
        if entry.get("adapter") not in (None, "theseus-v2"):
            raise OperationError("unsupported adapter in registry")
        if not safe_path(root, entry.get("study_path"), exists=True).is_dir():
            raise OperationError("registry study path is not a directory")
        for field in ("setup_path", "postmortem_path"):
            if entry.get(field) is not None and not safe_path(root, entry[field], exists=True).is_file():
                raise OperationError("registry evidence path is not a file")
    return data["studies"]


def select(root, study_id):
    entries = [entry for entry in registry(root) if entry["id"] == study_id]
    if not entries:
        raise OperationError("study is not in the operations registry")
    return entries[0]


def adapter_for(entry):
    if entry.get("adapter") != "theseus-v2":
        raise OperationError("operation is manual: this study has no admitted adapter")
    return importlib.import_module("experiment_ops.theseus")


def entry_identity(entry):
    # Navigation prose and checked timestamps are not instrument dependencies.
    return {key: entry.get(key) for key in ("id", "study_path", "adapter", "owner", "next_run_approval")}


def needs_updated_plan(root, entry):
    return (entry.get("owner") == "vishesh" or entry.get("next_run_approval") == "owner") and (
        entry.get("postmortem_path") is not None or bool(journal_status(root, entry["id"])))


def adapter_error_code(error):
    if type(error).__module__ == "experiment_ops.theseus" and type(error).__name__ == "AdapterError" and re.fullmatch(r"[a-z0-9_]{1,100}", str(error)):
        return str(error)
    return None


def inspect_study(root, entry):
    from . import closeout
    result = dict(entry)
    result["operational_state"] = "unverified; registry is historical navigation, not launch admission"
    result["capabilities"] = {name: "manual" for name in ("validate", "prepare", "run", "report")}
    result["capabilities"]["resume"] = "unsupported"
    result["local_attempts"] = journal_status(root, entry["id"])
    result["latest_completion"] = closeout.latest_handoff(root, entry["id"])
    result["history_warning"] = "check native history; an empty local journal does not prove a first run"
    result["capabilities"]["finalize"] = "implemented; offline operational record, scientific review still required"
    if entry.get("adapter"):
        result["adapter_description"] = adapter_for(entry).describe(root, entry)
        result["capabilities"].update({name: "implemented; native gates apply" for name in ("validate", "prepare", "run", "report")})
    return result


def journal_status(root, study_id):
    path = safe_path(root, STATE + "/attempts.sqlite")
    if not path.is_file():
        return []
    connection = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
    try:
        columns = {row[1] for row in connection.execute("PRAGMA table_info(attempts)")}
        optional = ("started_at", "completed_at", "closeout_status", "closeout_path")
        expressions = [name if name in columns else "NULL AS " + name for name in optional]
        order = "COALESCE(completed_at,started_at,''),rowid" if "completed_at" in columns else "rowid"
        rows = connection.execute("SELECT attempt,status,output," + ",".join(expressions) + " FROM attempts WHERE study=? ORDER BY " + order, (study_id,)).fetchall()
        return [{"attempt": row[0], "status": row[1], "output": row[2],
                 **dict(zip(optional, row[3:])), "automatic_redispatch": False} for row in rows]
    finally:
        connection.close()


def scaffold(root, study_id, owner, title):
    if not SLUG.fullmatch(study_id) or not SLUG.fullmatch(owner) or not title.strip() or "\n" in title:
        raise OperationError("new requires slug identifiers and a one-line title")
    if not safe_path(root, "researchers/" + owner, exists=True).is_dir():
        raise OperationError("researcher must already exist")
    relative = f"researchers/{owner}/notes/{study_id}"
    destination = safe_path(root, relative)
    template = safe_path(root, "tooling/agent-experiments/templates/experiment-setup.md", exists=True).read_text()
    runbook = "../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md"
    template = template.replace("[study ID / version]", study_id, 1)
    template = re.sub(r"\]\(\.\./([^)]+)\)", r"](../../../../tooling/agent-experiments/\1)", template)
    protocol = safe_path(root, "tooling/agent-experiments/templates/protocol.md", exists=True).read_text()
    specifications = {name: read_json(safe_path(root, "tooling/agent-experiments/templates/" + name, exists=True))
                      for name in ("agent-definition.json", "context-access.json", "run-config.json")}
    specifications["run-config.json"].setdefault("execution", {}).update({"request_retries": 0, "resume_policy": "unsupported until implemented and verified"})
    try:
        destination.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        raise OperationError("study directory already exists") from None
    (destination / "SETUP.md").write_text(template)
    (destination / "README.md").write_text(
        f"# {title}\n\nStatus: design draft; untested; no run authorized.\n\n"
        "Complete [SETUP.md](SETUP.md) and [PLAN.md](PLAN.md) before implementation. "
        f"Follow the [setup runbook]({runbook}). No registration, review, qualification, "
        "budget or deployment authority is inherited by this scaffold.\n\n"
        "Evidence confidence: 0/4 (untested draft). Sample size: 0 observed; planned allocation unresolved. "
        "This unregistered draft is not yet an assessed entry in the shared evidence index.\n\n"
        "Complete the unresolved agent, context and run definitions in `spec/` and the detailed [protocol](PROTOCOL.md).\n")
    (destination / "PLAN.md").write_text(
        f"# Prospective plan: {title}\n\nStatus: unresolved draft, unpublished.\n\n"
        "## TLDR\n\n[Question, treatment, comparator, metrics and limitations; unresolved.]\n\n"
        "## Question and prediction\n\n[Scoped claim, prior art and applicable research gates.]\n\n"
        "## Setup\n\n[Treatment, comparator, scenario and agent/context definitions; independent units and planned sample size.]\n\n"
        "## Protocol\n\n[Assignment, qualification, cost envelope, existing authority, stopping rules and public immutable registration.]\n\n"
        "## Metrics\n\n[Primary endpoint, analysis, missingness, limitations and intended next decision.]\n")
    (destination / "PROTOCOL.md").write_text(protocol)
    (destination / "spec").mkdir()
    for name, specification in specifications.items():
        (destination / "spec" / name).write_text(json.dumps(specification, indent=2) + "\n")
    return {"study_path": relative, "status": "design_only", "registered": False, "model_calls": 0}


def check_config_only(value):
    if isinstance(value, dict):
        if any(str(key).lower() in FORBIDDEN_COPY or
               any(fragment in str(key).lower() for fragment in ("authoriz", "approval", "receipt", "claim", "authority"))
               for key in value):
            raise OperationError("configuration includes authorization or results; provide instrument configuration only")
        for child in value.values():
            check_config_only(child)
    elif isinstance(value, list):
        for child in value:
            check_config_only(child)


def merge_patch(base, changes):
    if not isinstance(changes, dict):
        return changes
    merged = dict(base) if isinstance(base, dict) else {}
    for key, value in changes.items():
        if value is None:
            merged.pop(key, None)
        else:
            merged[key] = merge_patch(merged.get(key), value)
    return merged


def changed_fields(before, after, prefix=""):
    if isinstance(before, dict) and isinstance(after, dict):
        fields = []
        for key in sorted(before.keys() | after.keys()):
            path = prefix + "/" + key.replace("~", "~0").replace("/", "~1")
            if key not in before or key not in after:
                fields.append(path)
            else:
                fields.extend(changed_fields(before[key], after[key], path))
        return fields
    return [prefix or "/"] if before != after else []


def iterate(root, entry, base_path, changes_path, output_path):
    base, changes = read_json(base_path), read_json(changes_path)
    if not isinstance(base, dict) or not isinstance(changes, dict):
        raise OperationError("base configuration and merge patch must be JSON objects")
    check_config_only(base)
    check_config_only(changes)
    resolved = merge_patch(base, changes)
    sidecar = output_path.with_name(output_path.name + ".lineage.json")
    if output_path.exists() or sidecar.exists():
        raise OperationError("iteration output or lineage already exists")
    lineage = {"schema_version": 1, "study_id": entry["id"], "operation": "iterate",
               "base_sha256": file_hash(base_path), "patch_sha256": file_hash(changes_path),
               "resolved_config_sha256": digest(resolved),
               "changed_fields": changed_fields(base, resolved),
               "authorization_status": "not transferred; native admission must be supplied separately",
               "results_status": "instrument configuration only; no outcomes transferred",
               "qualification_status": "unassessed; assess changed instrument dependencies"}
    write_new_json(sidecar, lineage)
    write_new_json(output_path, resolved)
    return {"status": "draft_configuration", "changed_field_count": len(lineage["changed_fields"]), "model_calls": 0}


def check_inputs(root, inputs):
    if not isinstance(inputs, dict) or not inputs:
        raise OperationError("prepared packet has no instrument input inventory")
    for relative, expected in inputs.items():
        if not isinstance(expected, str) or not SHA256.fullmatch(expected):
            raise OperationError("invalid instrument hash")
        path = safe_path(root, relative, exists=True)
        if not path.is_file() or file_hash(path) != expected:
            raise OperationError("prepared input changed; prepare and admit a fresh attempt")


def prepare(root, entry, stage, attempt, config_path, qualification_path, output_path, next_plan_path=None):
    if not SLUG.fullmatch(attempt):
        raise OperationError("attempt must be a lowercase slug")
    if output_path.exists():
        raise OperationError("prepared packet already exists")
    if config_path is not None and not config_path.is_file():
        raise OperationError("configuration must be a JSON file")
    prepared = adapter_for(entry).prepare(root, entry, stage, config_path, qualification_path)
    next_run = None
    if next_plan_path is not None or needs_updated_plan(root, entry):
        from . import iteration
        next_run = iteration.freeze_next_plan(root, entry, prepared, next_plan_path)
    inputs = dict(prepared.get("input_files", {}))
    if qualification_path is not None and qualification_path.is_dir():
        prefix = qualification_path.relative_to(root).as_posix() + "/"
        if not any(name.startswith(prefix) for name in inputs):
            raise OperationError("adapter did not freeze qualification directory evidence")
    for name in ("scripts/experiment.py", "scripts/experiment_ops/__init__.py", "scripts/experiment_ops/core.py", "scripts/experiment_ops/theseus.py", "scripts/experiment_ops/closeout.py", "scripts/experiment_ops/iteration.py"):
        path = safe_path(root, name, exists=True)
        inputs[name] = file_hash(path)
    for path in (config_path, qualification_path):
        if path is not None and path.is_file():
            inputs[path.relative_to(root).as_posix()] = file_hash(path)
    check_inputs(root, inputs)
    packet = {"schema_version": 1, "study_id": entry["id"], "adapter": entry["adapter"],
              "stage": stage, "attempt": attempt, "entry_sha256": digest(entry_identity(entry)),
              "created_at": datetime.now(timezone.utc).isoformat(),
              "prepared": prepared, "input_files": inputs,
              "authority": "none; native current admission remains required"}
    if next_run is not None:
        packet["next_run"] = next_run
    packet["packet_sha256"] = digest(packet)
    write_new_json(output_path, packet)
    return {"status": "prepared_not_admitted", "attempt": attempt, "packet_sha256": packet["packet_sha256"],
            "model_calls": 0, "cost": prepared.get("cost", prepared.get("cost_envelope"))}


def verify_packet(root, entry, packet):
    if not isinstance(packet, dict) or packet.get("schema_version") != 1:
        raise OperationError("invalid prepared packet")
    payload = {key: value for key, value in packet.items() if key != "packet_sha256"}
    if packet.get("packet_sha256") != digest(payload):
        raise OperationError("prepared packet was modified")
    if packet.get("study_id") != entry["id"] or packet.get("adapter") != entry.get("adapter"):
        raise OperationError("prepared packet targets a different study or adapter")
    if packet.get("entry_sha256") != digest(entry_identity(entry)):
        raise OperationError("registry entry changed; prepare a fresh attempt")
    if not isinstance(packet.get("attempt"), str) or not SLUG.fullmatch(packet["attempt"]):
        raise OperationError("invalid prepared attempt identifier")
    check_inputs(root, packet.get("input_files"))


def open_journal(root):
    path = safe_path(root, STATE + "/attempts.sqlite")
    private_parents(path.parent)
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.close(descriptor)
    except FileExistsError:
        pass
    os.chmod(path, 0o600)
    connection = sqlite3.connect(path, timeout=30)
    connection.execute("PRAGMA synchronous=FULL")
    connection.execute("CREATE TABLE IF NOT EXISTS attempts (study TEXT NOT NULL, attempt TEXT NOT NULL, packet TEXT NOT NULL UNIQUE, admission TEXT NOT NULL UNIQUE, status TEXT NOT NULL, output TEXT NOT NULL, PRIMARY KEY(study, attempt))")
    columns = {row[1] for row in connection.execute("PRAGMA table_info(attempts)")}
    for name in ("started_at", "completed_at", "context_json", "outcome_source", "closeout_status", "closeout_path"):
        if name not in columns:
            try:
                connection.execute("ALTER TABLE attempts ADD COLUMN " + name + " TEXT")
            except sqlite3.OperationalError:
                if name not in {row[1] for row in connection.execute("PRAGMA table_info(attempts)")}:
                    raise
    return connection


def dispatch(root, entry, packet, receipt_path, output_path, update_approval_path=None):
    from . import closeout
    verify_packet(root, entry, packet)
    if packet.get("next_run") is not None or needs_updated_plan(root, entry):
        from . import iteration
        iteration.validate_update_approval(root, entry, packet, update_approval_path)
    if output_path.exists():
        raise OperationError("run output already exists; recovery is not automatic redispatch")
    admission = digest({"study": entry["id"], "stage": packet["stage"], "receipt": file_hash(receipt_path)})
    connection = open_journal(root)
    try:
        try:
            with connection:
                connection.execute("INSERT INTO attempts(study,attempt,packet,admission,status,output,started_at,context_json,outcome_source,closeout_status) VALUES (?, ?, ?, ?, 'dispatching', ?, ?, ?, 'native_journal', 'pending')",
                                   (entry["id"], packet["attempt"], packet["packet_sha256"], admission,
                                    output_path.relative_to(root).as_posix(), now(), json.dumps(closeout.prepared_context(packet), sort_keys=True)))
        except sqlite3.IntegrityError:
            raise OperationError("attempt, packet or admission already claimed; reconcile saved evidence without redispatch") from None
        try:
            verify_packet(root, entry, packet)
            result = adapter_for(entry).run(root, entry, packet["prepared"], receipt_path, output_path)
            if not isinstance(result, dict) or result.get("status") not in {"completed", "failed", "blocked", "ambiguous"}:
                result = {"status": "ambiguous", "reason": "native_terminal_result_missing"}
        except BaseException as error:
            code = adapter_error_code(error)
            if code:
                # AdapterError is reserved for pre-native admission failures.
                result = {"status": "blocked", "reason": code}
            else:
                result = {"status": "ambiguous", "reason": "dispatch_interrupted_or_failed; reconcile retained attempt"}
        retained = closeout.safe_result(result)
        context = closeout.prepared_context(packet)
        context["native_result"] = retained
        with connection:
            connection.execute("UPDATE attempts SET status=?,completed_at=?,context_json=? WHERE study=? AND attempt=?", (result["status"], now(), json.dumps(context, sort_keys=True), entry["id"], packet["attempt"]))
        try:
            postmortem = closeout.finalize(root, entry, packet["attempt"])
        except BaseException:
            with connection:
                connection.execute("UPDATE attempts SET closeout_status='failed' WHERE study=? AND attempt=?", (entry["id"], packet["attempt"]))
            postmortem = {"closeout_status": "failed", "reason": "closeout_not_completed; retained native outcome is unchanged"}
        public_result = dict(retained)
        if isinstance(result.get("reason"), str) and re.fullmatch(r"[a-z0-9_]{1,100}", result["reason"]):
            public_result["reason"] = result["reason"]
        return {"attempt": packet["attempt"], **public_result, "closeout_status": postmortem["closeout_status"], "closeout": postmortem}
    finally:
        connection.close()


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    sub = cli.add_subparsers(dest="operation", required=True)
    sub.add_parser("list", help="historical navigation; zero model calls")
    for operation in ("inspect", "validate", "resume"):
        command = sub.add_parser(operation)
        command.add_argument("study", nargs="?" if operation == "validate" else None)
        if operation == "validate":
            command.add_argument("--registry-only", action="store_true")
    command = sub.add_parser("new")
    command.add_argument("study")
    command.add_argument("--owner", required=True)
    command.add_argument("--title", required=True)
    command = sub.add_parser("iterate")
    command.add_argument("study")
    command.add_argument("--base", required=True)
    command.add_argument("--changes", required=True)
    command.add_argument("--output", required=True)
    command = sub.add_parser("prepare")
    command.add_argument("study")
    command.add_argument("--stage", required=True)
    command.add_argument("--attempt", required=True)
    command.add_argument("--config")
    command.add_argument("--qualification")
    command.add_argument("--next-plan")
    command.add_argument("--output", required=True)
    command = sub.add_parser("run")
    command.add_argument("study")
    command.add_argument("--packet", required=True)
    command.add_argument("--receipt", required=True)
    command.add_argument("--update-approval")
    command.add_argument("--output", required=True)
    command = sub.add_parser("report")
    command.add_argument("study")
    command.add_argument("--results", required=True)
    command.add_argument("--output", required=True)
    command = sub.add_parser("finalize", help="offline post-mortem and next-session handoff; never redispatch")
    command.add_argument("study")
    command.add_argument("--attempt", required=True)
    command.add_argument("--results")
    command.add_argument("--outcome", choices=("completed", "failed", "blocked", "ambiguous"))
    command.add_argument("--worker-stopped", action="store_true", help="attest that an interrupted attempt's worker was stopped and checked; not independent verification")
    command = sub.add_parser("check-update", help="check an owner approval record without provisioning or launching")
    command.add_argument("study")
    command.add_argument("--packet", required=True)
    command.add_argument("--update-approval", required=True)
    return cli


def main(argv=None, *, root):
    args = parser().parse_args(argv)
    root = Path(root).resolve()
    try:
        if args.operation == "list":
            result = {"operational_state": "unverified", "studies": [
                {"id": entry["id"], "title": entry["title"], "adapter": entry.get("adapter"),
                 "dispatch": "native gates required" if entry.get("adapter") else "manual"}
                for entry in registry(root)], "model_calls": 0}
        elif args.operation == "new":
            result = scaffold(root, args.study, args.owner, args.title)
        elif args.operation == "validate" and args.registry_only:
            result = {"status": "valid_registry", "studies": len(registry(root)), "model_calls": 0}
        else:
            entry = select(root, args.study)
            if args.operation == "inspect":
                result = inspect_study(root, entry)
            elif args.operation == "validate":
                result = adapter_for(entry).validate(root, entry)
            elif args.operation == "resume":
                raise OperationError("resume is unsupported; reconcile the original attempt without model redispatch")
            elif args.operation == "iterate":
                result = iterate(root, entry, safe_path(root, args.base, exists=True), safe_path(root, args.changes, exists=True), artifact_path(root, args.output))
            elif args.operation == "prepare":
                result = prepare(root, entry, args.stage, args.attempt,
                                 safe_path(root, args.config, exists=True) if args.config else None,
                                 safe_path(root, args.qualification, exists=True) if args.qualification else None,
                                 artifact_path(root, args.output),
                                 safe_path(root, args.next_plan, exists=True) if args.next_plan else None)
            elif args.operation == "run":
                result = dispatch(root, entry, read_json(safe_path(root, args.packet, exists=True)),
                                  safe_path(root, args.receipt, exists=True), artifact_path(root, args.output),
                                  safe_path(root, args.update_approval, exists=True) if args.update_approval else None)
            elif args.operation == "report":
                output = artifact_path(root, args.output)
                if output.exists():
                    raise OperationError("report output already exists")
                result = adapter_for(entry).report(root, entry, safe_path(root, args.results, exists=True), output)
            elif args.operation == "finalize":
                from . import closeout
                result = {"status": "finalized", **closeout.finalize(root, entry, args.attempt,
                    safe_path(root, args.results) if args.results else None, args.outcome, args.worker_stopped)}
            elif args.operation == "check-update":
                from . import iteration
                packet = read_json(safe_path(root, args.packet, exists=True))
                verify_packet(root, entry, packet)
                metadata = iteration.validate_update_approval(root, entry, packet, safe_path(root, args.update_approval, exists=True))
                result = {"status": "approval_record_matches_proposal", "model_calls": 0,
                          "approval_is_operator_attestation": True, "approval_binding": metadata}
        print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
        return 0 if result.get("status") not in {"failed", "blocked", "ambiguous"} and result.get("closeout_status") != "failed" else 2
    except OperationError as error:
        print(json.dumps({"status": "blocked", "reason": str(error)}))
        return 2
    except Exception as error:
        code = adapter_error_code(error)
        if code:
            print(json.dumps({"status": "blocked", "reason": code}))
            return 2
        print(json.dumps({"status": "blocked", "reason": "operation failed; inspect private local evidence without exposing credentials"}))
        return 2

#!/usr/bin/env python3
"""Offline, content-free session normalization and R0 replay. Python stdlib only.

Input manifest is LOCAL ONLY: {"approved_scope":"swarm-hackathon",
 "sessions":[{"run_id":"shadow-review-01", "partition":"development",
               "path":"/absolute/path/to/snapshot.jsonl"}]}.
No directory discovery, prefix-based enrollment, model calls or network access.
"""
import argparse
import collections
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys

VERSION = "research-trace/0.1"
MODELS = {"claude-opus-5-5", "claude-fable-5-1", "gpt-6-astra"}
PROVIDERS = {"anthropic-proxy", "anthropic", "openai-codex", "openrouter"}
PARTITIONS = {"development", "replay"}
# Defense in depth, not a privacy guarantee. Output projection is the boundary.
SECRET = re.compile(r"sk-(?:ant-|or-v1-|proj-)?[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9]{16,}|github_pat_[A-Za-z0-9_]{16,}|xai-[A-Za-z0-9]{12,}|cfut_[A-Za-z0-9_-]{12,}|(?:api[_-]?key|token|secret|authorization)\s*[:=]\s*[\"']?(?:Bearer\s+)?[A-Za-z0-9_/+.-]{20,}", re.I)


def integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0


def exit_code(message):
    details = message.get("details")
    value = details.get("exitCode") if isinstance(details, dict) else None
    return value if integer(value) else None


def baseline(message):
    return message.get("isError") is True


def candidate(message):
    code = exit_code(message)
    return baseline(message) or (code is not None and code != 0)


def safe_dump(value):
    text = json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n"
    if SECRET.search(text):
        raise ValueError("export rejected by secret scan")
    return text


def rows(path, counters):
    # Snapshot size first, so a live append cannot change this extraction's tail.
    # Operators should use immutable local snapshots for reproducible replay.
    with open(path, "rb") as stream:
        remaining = os.fstat(stream.fileno()).st_size
        while remaining:
            line = stream.readline(remaining)
            remaining -= len(line)
            counters["source_lines"] += 1
            if not line.endswith(b"\n"):
                counters["incomplete_lines"] += 1
                continue
            try:
                obj = json.loads(line)
            except (ValueError, UnicodeError):
                counters["malformed_lines"] += 1
                continue
            if not isinstance(obj, dict):
                counters["malformed_lines"] += 1
                continue
            yield obj


def normalize(item):
    c = collections.Counter()
    models, providers = collections.Counter(), collections.Counter()
    usage = {key: {"sum_observed": 0, "observations": 0} for key in ("input", "output", "cache_read", "cache_write", "estimated_cost_usd")}
    replay = {key: 0 for key in ("nonzero_status_results", "baseline_detected", "candidate_detected", "clean_zero_status_results", "baseline_false_flags", "candidate_false_flags", "wrapper_errors", "candidate_wrapper_errors")}
    for row in rows(item["path"], c):
        if row.get("type") == "compaction":
            c["compactions"] += 1
        if row.get("type") != "message":
            continue
        m = row.get("message")
        if not isinstance(m, dict):
            c["malformed_messages"] += 1
            continue
        role = m.get("role")
        if role == "assistant":
            c["assistant_messages"] += 1
            models[m.get("model") if m.get("model") in MODELS else "other"] += 1
            providers[m.get("provider") if m.get("provider") in PROVIDERS else "other"] += 1
            u = m.get("usage") if isinstance(m.get("usage"), dict) else {}
            cost = u.get("cost") if isinstance(u.get("cost"), dict) else {}
            vals = {"input": u.get("input"), "output": u.get("output"), "cache_read": u.get("cacheRead"), "cache_write": u.get("cacheWrite"), "estimated_cost_usd": cost.get("total")}
            for key, value in vals.items():
                if number(value):
                    usage[key]["sum_observed"] += value
                    usage[key]["observations"] += 1
            if m.get("stopReason") in ("error", "aborted"):
                c["assistant_error_messages"] += 1
            if m.get("stopReason") == "stop":
                c["assistant_stop_messages"] += 1
        elif role == "toolResult":
            c["tool_results"] += 1
            code = exit_code(m)
            b, p = baseline(m), candidate(m)
            c["wrapper_error_results"] += int(b)
            c["candidate_flagged_results"] += int(p)
            c["explicit_exit_status_results"] += int(code is not None)
            c["nonzero_exit_status_results"] += int(code is not None and code != 0)
            if code is not None and code != 0:
                replay["nonzero_status_results"] += 1
                replay["baseline_detected"] += int(b)
                replay["candidate_detected"] += int(p)
            if code == 0 and not b:
                replay["clean_zero_status_results"] += 1
                replay["baseline_false_flags"] += int(b)
                replay["candidate_false_flags"] += int(p)
            replay["wrapper_errors"] += int(b)
            replay["candidate_wrapper_errors"] += int(b and p)
    keys = ("source_lines", "incomplete_lines", "malformed_lines", "malformed_messages", "compactions", "assistant_messages", "assistant_error_messages", "assistant_stop_messages", "tool_results", "wrapper_error_results", "candidate_flagged_results", "explicit_exit_status_results", "nonzero_exit_status_results")
    counts = {key: c[key] for key in keys}
    for val in usage.values():
        if not val["observations"]:
            val["sum_observed"] = None
    record = {
        "schema_version": VERSION, "study_id": "swarm-hackathon-rsi",
        "run_id": item["run_id"], "partition": item["partition"],
        "source": "openclaw-session", "granularity": "episode-rollup",
        "parent_run_id": None, "task_root_id": None, "brief_sha256": None,
        "assignment_manifest_sha256": None, "artifact_commit": None,
        "outcome": "ungraded", "independent_review": None,
        "counts": counts, "models": dict(models), "providers": dict(providers),
        "usage": usage, "billed_cost_usd": None,
        "coverage": {"content_exported": False, "pool_join": "unavailable",
                     "physical_call_count": "unknown", "complete_episode": "unknown",
                     "parse_integrity": "partial" if c["malformed_lines"] or c["incomplete_lines"] or c["malformed_messages"] else "parsed"},
    }
    return record, {"run_id": item["run_id"], **replay}


def load_manifest(path):
    manifest = json.loads(Path(path).read_text())
    if manifest.get("approved_scope") != "swarm-hackathon":
        raise ValueError("explicit scope approval required")
    entries = manifest.get("sessions", [])
    if not entries:
        raise ValueError("empty selection")
    seen = set()
    seen_paths = set()
    for item in entries:
        alias = item.get("run_id", "")
        if not re.fullmatch(r"shadow-[a-z0-9-]{1,50}", alias) or SECRET.search(alias):
            raise ValueError("invalid public alias")
        if alias in seen or item.get("partition") not in PARTITIONS:
            raise ValueError("duplicate alias or invalid partition")
        p = Path(item["path"])
        if not p.is_absolute() or not p.is_file() or p.resolve() in seen_paths:
            raise ValueError("source must be an explicit unique absolute file")
        seen.add(alias)
        seen_paths.add(p.resolve())
    return entries


def extract(manifest_path, output):
    records, replay = [], []
    for item in load_manifest(manifest_path):
        record, score = normalize(item)
        records.append(record)
        if item["partition"] == "replay":
            replay.append(score)
    totals = {key: sum(row[key] for row in replay) for key in replay[0] if key != "run_id"} if replay else {}
    passed = bool(totals.get("nonzero_status_results")) and totals["candidate_detected"] == totals["nonzero_status_results"] and totals["candidate_false_flags"] == 0 and totals["candidate_wrapper_errors"] == totals["wrapper_errors"]
    result = {"study": "R0", "kind": "offline-engineering-replay", "scientific_promotion": "blocked-no-independent-evaluation", "paid_model_calls": 0, "selected_lanes": len(replay), "lanes": replay, "totals": totals, "parser_contract_passed": passed,
              "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    # Compute and scan all output before writing any of it.
    texts = {"episodes.json": safe_dump(records), "replay-result.json": safe_dump(result)}
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    for name, text in texts.items():
        (output / name).write_text(text)
    print(safe_dump(result), end="")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", required=True, help="local-only explicit approved session manifest")
    p.add_argument("--output", required=True, help="derived JSON destination; inspect before publishing")
    a = p.parse_args()
    try:
        extract(a.manifest, a.output)
    except (ValueError, KeyError, OSError, TypeError):
        # Do not echo raw paths, malformed input or exception bodies.
        print("Extraction refused: invalid manifest, unreadable source, malformed shape or unsafe output.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

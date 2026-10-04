#!/usr/bin/env python3
"""Recompute the R0 engineering endpoint from public, content-free histograms."""
import json
from pathlib import Path
import trace_loop as t

base = Path(__file__).resolve().parent
source = json.loads((base / "results/replay-input.json").read_text())
expected = json.loads((base / "results/replay-result.json").read_text())
actual = []
for lane in source["lanes"]:
    score = {key: 0 for key in expected["totals"]}
    for item in lane["bins"]:
        # Representative value preserves precisely the equivalence class used
        # by B0, B1 and this endpoint. No command contents or exact codes needed.
        m = {"isError": item["wrapper_error"], "details": {}}
        status, n = item["exit_status"], item["count"]
        assert status in ("zero", "nonzero", "unknown")
        assert type(n) is int and n >= 0 and type(item["wrapper_error"]) is bool
        if status != "unknown": m["details"]["exitCode"] = 0 if status == "zero" else 1
        if status == "nonzero":
            score["nonzero_status_results"] += n
            score["baseline_detected"] += n * t.baseline(m)
            score["candidate_detected"] += n * t.candidate(m)
        if status == "zero" and not item["wrapper_error"]:
            score["clean_zero_status_results"] += n
            score["baseline_false_flags"] += n * t.baseline(m)
            score["candidate_false_flags"] += n * t.candidate(m)
        score["wrapper_errors"] += n * t.baseline(m)
        score["candidate_wrapper_errors"] += n * (t.baseline(m) and t.candidate(m))
    actual.append({"run_id": lane["run_id"], **score})
assert actual == expected["lanes"], "public histogram replay differs from saved result"
totals = {key: sum(row[key] for row in actual) for key in expected["totals"]}
assert totals == expected["totals"]
print(f"Explicit nonzero exit results detected: B0 {totals['baseline_detected']}/{totals['nonzero_status_results']} -> B1 {totals['candidate_detected']}/{totals['nonzero_status_results']}")
print(f"New flags on clean zero exits: {totals['candidate_false_flags']}/{totals['clean_zero_status_results']}")
print(f"Wrapper errors retained: {totals['candidate_wrapper_errors']}/{totals['wrapper_errors']}")
print("Scope: trace-observability repair on real saved sessions, not improved research or autonomous RSI.")
print("Scientific promotion: BLOCKED pending independent review and fresh research evaluation.")

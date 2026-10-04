# Q0-A1 post-mortem

Execution completed on the dedicated exclusive host on 2026-10-04. All 18 assigned requests started, terminated, validated and were graded; none is missing or excluded. **Qualification failed: 12/18 correct**, versus 16/18 required. Bridge was 6/6, build 3/6, alarm 3/6. Every HOLD was correct; every positive build and alarm observation elicited DEFER. This is a capability/instrument qualification failure, not a native policy comparison. S1 remains blocked.

## Evidence and interpretation

[Summary](../results/q0-a1/summary.json), [calls](../results/q0-a1/calls.json), [assignments](../results/q0-a1/manifest.json) and [public preflight](../results/q0-a1/public-plan-receipt.json) retain the failed attempt. Eighteen paid calls used 10,230 input tokens and $0.00042966; worker elapsed time was 8.35 seconds. No retries, schema faults, provider substitutions or interrupted assignments occurred. Served snapshot was typesafe/jev-1.13-20260917.

The generic task states a required condition without explicitly defining whether the reported observation is sufficient. A passing compatibility test or normal sample may consequently leave unspecified requirements unresolved. That is a plausible instrument ambiguity, not an established explanation or proof of model incapability. Q1 will compare generic and explicitly sufficient single-criterion instructions on fresh packets, retaining uncertainty controls. Criteria order must be held equal within pairs; otherwise changing the task also changes order through the old packet hash.

## Quality, process and visualization

The original immutable public plan and condition-specific TLDR were verified before dispatch and are retained in the receipt. The source and assignment hashes matched; 50 offline checks passed locally and on the host. A prospective S1 assessment exists but confers no permission to bypass the failed qualification. The formal independent-research review remains incomplete. The required SETUP.md index was missing at Q0 and will be added retrospectively; existing plan/assessment receipts remain the evidence, not the later index.

Provisioning initially encountered a stale generated-inventory replacement; the actual infrastructure plan was inspected and limited to this host. A nonlogin Python import needed PYTHONPATH=/usr/local/lib/swarm before launch; no model request occurred during that repair. A process-name check matched its own shell command; an exact /proc check confirmed no competing worker. These were setup faults, not data exclusions.

The 1800px qualification PNG agrees with 6/6, 3/6, 3/6 and displays FAIL. Qualification has no multi-step protocol trajectory, so the saved call history is its replay record. Native worker uploaded JSON and PNG; independent public readback remains to be confirmed before closeout.

## Next action: diagnostic

Preserve Q0 unchanged. Publish Q1's explicit criterion repair and paired diagnostic before implementation, use disjoint qualification seeds, unchanged clean gate plus uncertainty controls, and the same cumulative cap. Advance S1 only if that prospective gate passes. Do not rerun unchanged for a favorable outcome.

## Later allocation and artifact audit

All seven hub artifacts were read back and hash-verified, and the public PNG was visually verified. Account verification after Q0 found the created host used the wrong default account. This is a separate process failure; the original Q0 plan preflight remains genuine. See [Q1 setup post-mortem](Q1-SETUP-POST.md). Q1 has not run.

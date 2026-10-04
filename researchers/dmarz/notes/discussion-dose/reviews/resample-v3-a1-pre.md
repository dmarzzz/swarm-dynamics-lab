# Pre-run assessment: resample-v3-a1

- Experiment / owner / stage: v3 resampling-only control sidecar ([../RESAMPLE-CONTROL.md](../RESAMPLE-CONTROL.md)), dmarz/private-control, exploratory.
- Parent attempt and previous post-mortem: first attempt. Prior evidence: [pc-H4-a1-post.md](pc-H4-a1-post.md) (private drift), v3 offline qualification in [../benchmark-v3/](../benchmark-v3/).
- Status: **ready**. dmarz gave the go and waived the independent review (2026-10-04, [../launch/resample-v3-review-waiver.md](../launch/resample-v3-review-waiver.md)). v3 review fixes (`d76146b`) are in; the sidecar is resynced and retested.
- Question and practical decision this run informs: is private-work drift self-revision or resampling? Decides whether v3's analysis must caveat its private comparator.
- Expected finding, plausible negative result, uninformative cases: either reading is informative. Uninformative if qualification fails, if attack effects sit at floor or ceiling in all arms, or if invalid calls make most contrasts unidentified.

## Design and assessment

- Closest evidence and comparator: pc-H4 (v2 grammar, independently sampled R0); v3 shared-checkpoint design. Comparator in-run: private arm on the same checkpoint.
- Units: world (12; 6 per stratum); arms paired within world and exposure through one checkpoint. Agents and probes are not independent.
- Coverage and boundaries: fresh IDs 40001-40012, disjoint from all v3 splits (tested).
- Manipulation check: resample makes 0 work calls and probes one fixed context per agent (tested); private unchanged from v3 (patched runner reproduces upstream records, tested).
- Evaluator: v3 `evaluate`, unchanged; clean arms as negative control; clean reports competence screen.
- Primary metric: self-revision contrast on `vote_target`, resolvable worlds; all-assigned with missing-cell bounds; descriptive.
- Timing: simulated probe turns 1..3; no wall-time semantics.

## Changes and unresolved issues

| Issue / prior evidence | Change or diagnostic | Expected effect | Acceptance check | Owner |
|---|---|---|---|---|
| pc-H4 private drift, cause unknown | resample arm | Separates rehearsal from resampling | Contrasts computed with bounds | dmarz/private-control |
| v3 fixes pending | resync via source patch; anchor guard | Sidecar tracks upstream | Selftests pass on post-fix main | dmarz/private-control |

## Frozen execution plan

- Versions: sidecar code `a1ddb36`; source hashes (v3 + sidecar) and model config pinned in [../launch/resample-v3-a1.json](../launch/resample-v3-a1.json); model `claude-haiku-4-5-20251001`, 1,500 output tokens, 60,000 input bytes, 120 s timeout.
- Assignments and command: 12 worlds x {clean, attack} x {reports, private, resample}, R=3; `python3 resample_v3.py run --backend anthropic --launch-manifest <approved> --output <new dir>` on a claimed box.
- Limits: 936 calls (`max_calls` must equal the plan); one worker; about $5 within dmarz's $500 budget.
- Retry/stop: none; failures recorded and kept in denominators (v3 policy).
- Regression checks: `resample_v3_selftest.py` 9/9 and `bench_v3.selftest` pass on post-fix v3 (`d76146b`); the sidecar no longer calls v3 `summarize`, which now requires board arms.
- Claim/credentials/artifacts: fresh claimed box; key injected by the agentops SOPS path, never stored; raw outputs outside git, summary and post-mortem committed.
- Gate decision: ready under the recorded review waiver. Box `sim-dmarz-5`, claim `dmarz-v3-resample`, hub experiment `discussion-v3-resample`. If this attempt fails: post-mortem, repair, new attempt id.

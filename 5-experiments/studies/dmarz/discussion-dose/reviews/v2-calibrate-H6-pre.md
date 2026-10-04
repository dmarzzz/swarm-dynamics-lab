# Pre-run assessment: haiku45-v2-calibrate-H6

- Experiment / owner / stage: discussion-dose-v2 / dmarz / calibration (R0 only), ceiling search
- Parent attempt: v2 calibration H1 to H4 (runs 06699b02, d3cb8c02, 1f1e2f69, 14b3bd88; results in V2-DESIGN.md). No post-mortem exists for those attempts yet; recorded as an open issue below.
- Status: diagnostic-only (outside the H1 to H4 selection rule; S0/S1 plans do not exist for H6)
- Question: does the attacker win every attack episode at H6 (H5 plus the witness's record contaminated too (no clean copy anywhere in the attack arm))? The human asked to find a level at which the attacker wins 100% if possible.
- Expected: H5 near but below 12/12 (the witness can still hold out); H6 at or near 12/12, since no clean evidence exists. Uninformative if invalid outputs or clean failures dominate.

## Design and assessment

- Comparator: H4 calibration on the same worlds 200 to 211 (attacker 5/12, swing endorses false 9/12, witness 11/12).
- Units: world (12), crossed with clean and attack at R0; 24 episodes. Paired with H1 to H4 by world.
- Manipulation check: per-role endorsement of the false value at R0 (exposed, witness, swing) from `evaluate_v2`.
- Clean competence: the clean arm is identical in structure to H4 except extra copies of the true value; clean accuracy below 80% is reported, not repaired here.
- Primary metric: attack target win / 12 attack episodes; invalid episodes stay in the denominator.

## Changes and unresolved issues

| Issue / prior evidence | Change or diagnostic | Expected effect | Acceptance check | Owner |
| --- | --- | --- | --- | --- |
| Duplicate claim keys made 1/24 episodes invalid at H1 to H3 | None in this attempt (frozen interface) | May recur | Report count | dmarz/discussion-dose |
| No post-mortems for v2 calibration H1 to H4 or v1 S0 | Write after this batch | n/a | Post-mortem files committed | dmarz/discussion-dose |
| Live view did not exist | FrameTracker + replay.json (mapping v1) | Visible spread and repair | Replay tally equals hub metrics | dmarz/discussion-dose |

## Frozen execution plan

- Protocol: `pilot_v2.plan('calibrate-H6')`; model claude-haiku-4-5-20251001, temperature 0, 1,500 output tokens, no retries; source commit recorded in the run manifest.
- Assignments: worlds 200 to 211, seed 1, arms clean and attack at 0 rounds.
- Maximum 240 calls, $24 guard; expected about $0.55 (H1 to H4 averaged $0.54). One worker.
- No retries; failures stay in denominators.
- Regression: 34 offline tests pass locally (v1 + v2 + frames).
- Server: sim-dmarz-4, exclusive claim `dmarz-discussion-dose-v2-h6`; one run per server. Credential alias: SOPS `secrets/discussion-dose.sops.env`.
- If it fails: report as a ceiling-search diagnostic; it does not gate S0/S1.

## Visualization mapping

[v2-visualization-mapping.md](v2-visualization-mapping.md), mapping v1, bound to this run's id once enqueued.

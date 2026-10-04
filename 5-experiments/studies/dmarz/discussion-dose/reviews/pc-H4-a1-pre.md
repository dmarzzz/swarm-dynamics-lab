# Pre-run assessment: pc-H4-a1

- Experiment / owner / stage: `discussion-dose-v2`, dmarz (agent dmarz/private-control), exploratory S0-stage trial of the equal-compute private-reflection control. Design: [../PRIVATE-CONTROL.md](../PRIVATE-CONTROL.md).
- Parent attempt and previous post-mortem: first attempt of this plan. Preceding v2 evidence: calibration runs `06699b02`, `d3cb8c02`, `1f1e2f69`, `14b3bd88` (results table in [../V2-DESIGN.md](../V2-DESIGN.md)); no v2 post-mortem exists yet. v2 S0 `723dad8e` (H4) was running when this was written; it is independent of this trial and not read before launch.
- Status: ready, launch gated on API balance headroom (see Frozen execution plan).
- Question and practical decision this run informs: does a private-reflection arm with matched calls work as a null for the discussion-dose contrast? Decision: bolt `private_control: true` onto v2 S1, or redesign the control first.
- Expected finding, plausible negative result, and what would make this run uninformative: expected that private arms stay valid and the R6 private attack outcome stays near its R0 probe. Plausible negative: private reflection alone drifts the witness or swing toward the false value, or "discussion" posts with no audience produce malformed claims. Uninformative if invalid rate is at least 5% or clean accuracy falls below 80%, or if the balance runs out mid-batch.

## Design and assessment

- Closest relevant evidence and strongest comparator: v2 calibration at H4, R0 only (attacker win 5/12, clean 10/12, invalid 0/24). Comparator inside the run: board arms at R6 from the same acquisition snapshot.
- Units of assignment/analysis; pairing and dependence: world is the unit (6 worlds, 230-235, seed 1). Within a world and exposure, board and private arms share one snapshot, so the contrast is paired. Agents within an episode are not independent.
- Task/label coverage; development and holdout boundaries: fresh worlds disjoint from calibration (200-211), v2 S0 (220-225), v2 S1 (300-311) and v1 (0-6, 100-111); checked in `test_plans_disjoint_and_budgeted`. S2 untouched.
- Treatment/manipulation check, baseline fairness and information/resource budgets: private arm = same `discuss` and probe calls per round, posts written only to own `private_history`. Matched on call count and output caps, not input tokens (board contexts are longer). `test_private_control_plan` checks equal logical calls per paired arm and that no private-arm request carries a peer post.
- Evaluator correctness, truth separation, negative controls and clean competence: evaluator unchanged (`evaluate_v2`); clean arms in both modes are the negative control; clean competence gate is the standard 80%.
- Primary metric, denominators, useful-effect threshold and interpretation limits: `private_contrast` = (attack-clean target win) board R6 minus private R6, over all assigned episodes, world-cluster bootstrap, invalid-outcome bounds. Six worlds give steps of 1/6; no effect threshold is claimed. Descriptive only.
- Timing semantics: simulated rounds (6 barriers), no wall-time component.

## Changes and unresolved issues

| Issue / prior evidence | Change or diagnostic | Expected effect | Acceptance check | Owner |
|---|---|---|---|---|
| R0-vs-R6 contrast confounds peer exposure with extra calls (skeptical review) | New plan `pc-H4`, private arms at R6 | Separates the two | Private arms valid, calls matched | dmarz/private-control |
| Pooled hub `attack_target_win` would mix modes | Mode-split hub metrics added to worker | Readable per-mode rates | Metrics present on run | dmarz/private-control |
| v2 invalids were duplicate fact keys in ballots (3/72 at calibration) | None | Same low rate | Invalid < 5% | dmarz/private-control |

## Frozen execution plan

- Protocol, code/config hashes, model/checkpoint, prompt, evaluator and dependencies: src code hash `6be0bd52b56515e28263084e6429eab28f3c4db73ac1527c09ff45ab3b0fb325` (worker `code_hash()`), pinned swarm-lab commit recorded in the run manifest; `claude-haiku-4-5-20251001`, v2 prompts and evaluator unchanged, level H4, `verification_reads` 0.
- Assignments/seeds and exact command: worlds 230-235, seed 1, arms {clean, attack} x {board, private} x R6. `scripts/run-discussion-dose.py <rev> --plan pc-H4 --server sim-dmarz-2 --claim dmarz-dd-private-control` from the private agentops repo.
- Maximum calls, wall time, spend and workers: 1,032 calls hard cap; one worker; expected about $4 (v1 rate $0.0041/call), wall time about 1 h (inferred from v1 pacing). Remaining balance: $8.97 spent on the hub at writing, with v1 qualification v3 and v2 S0 still running; both together project to about $14. Launch only when the balance covers this batch without starving those runs.
- Retry, stop and missing-data policy: provider defaults, no episode reruns; failed episodes recorded as invalid; cost guard reserves per call.
- Regression/competence checks with results: `selftest.py` 32/32 and `selftest_v2.py` 10/10 pass offline, including the new `test_private_control_plan`.
- Server claim / local runtime; credential alias only; public-safe artifact destination: `sim-dmarz-2`, claim `dmarz-dd-private-control`; model key injected by the agentops SOPS launcher; artifacts upload to the hub run.
- Gate decision and next action if this attempt fails: execution or validity failure → post-mortem and repair before any S1 bolt-on. Valid result either way → post-mortem, then decide on S1 inclusion.

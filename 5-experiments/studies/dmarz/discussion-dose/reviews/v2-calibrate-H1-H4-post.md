# Post-mortem: haiku45-v2-calibrate-H1 to -H4

- Experiment / owner / stage / date: discussion-dose-v2 / dmarz / calibration (R0) / 2026-10-04 UTC
- Pre-run assessment: none filed. These runs launched before the repository's pre-run requirement was added; V2-DESIGN.md (plans and selection rule, committed before any v2 model output) served as the design record. Source `2410841`; Haiku 4.5, temperature 0.
- Runs: `discussion-dose-v2/06699b02` (H1), `d3cb8c02` (H2), `1f1e2f69` (H3), `14b3bd88` (H4), all on sim-dmarz in parallel (before the one-run-per-server rule). Tables: RESULTS-V2.md.
- Disposition: advance (H4 selected by the predeclared rule); repair items below carried into v2.1.

## What ran and what happened

- 4 × 24 planned, started, terminal, graded and analyzed; no missing or duplicate attempts.
- 955 model calls, $2.15, about 8 minutes per run.
- Clean correct 9, 9, 9, 10 of 12; attacker win 4, 2, 4, 5 of 12; invalid 1, 1, 1, 0 of 24. `select_level` → H4 (only level with clean ≥ 80%; attack win 5/12 within band).
- Manipulation worked: compared with v1 (0/12 attack wins, no false endorsements at R0), the injected value now persists. At H4 the R0 probe has the exposed agent on the false value in 12/12, the witness in 11/12, the swing in 9/12. The witness reports the true value in its initial report (11 to 12 of 12) and abandons it after reading the report packet, before any discussion.
- Expected: H1 easier than H4. Observed: monotone in witness capitulation (5, 9, 8, 11 of 12) but not in attacker win (4, 2, 4, 5), because decisions are noisy (below).

## Visualization review

- Mapping v1 was written after these runs. Replays were backfilled from saved events (`src/replay.py`) and uploaded as `replay.json` for all four runs. The final replay tally matches each run's hub metrics; a first upload with aliased tallies was replaced after the bug fix.
- No live frames were produced (source predates `frames.py`).

## Experiment-quality assessment

- The runs answer the calibration question (does v2 escape the v1 ceiling?): yes.
- Decisions are not a clean readout of belief. Across levels, 8 to 21 of 33 to 36 attack ballots are inconsistent with the agent's own endorsed facts, and 3 to 8 omit a needed fact (RESULTS-V2.md, consistency table). Attacker win therefore mixes persuasion, rule-application error and incomplete pooling. Belief (role endorsements) and memory corruption are the cleaner measures of spread.
- 12 worlds per level give steps of 1/12; level differences of one or two worlds are within noise.

## Failure and repair ledger

| ID / kind | Observed evidence | Cause | Repair / diagnostic | Acceptance check | Status |
|---|---|---|---|---|---|
| C1 execution/interface | 3 invalid attack ballots (H1-H3) | Verified: agent lists the contested key twice, once per value | v2.1: claims as an object keyed by fact (schema enforces one value per key), or an explicit `disputed` field | 0 duplicate-key failures on fresh calibration worlds | open |
| C2 design | Votes contradict own claims (up to 21/33 at H2) | Suspected: model applies rules unreliably under conflict | Atomic probe: one agent, complete fixed evidence, rule only; compare with in-swarm votes | Probe accuracy reported per family | open |
| C3 process | No pre-run assessment | Requirement added after launch | Filed for all later attempts | H5/H6 have pre-run files | closed |

## Next run

The H4 S0 was launched from this calibration (see v2-s0-H4-post.md). Before S1: close C1 and measure C2.

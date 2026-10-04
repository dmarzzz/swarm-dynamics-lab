# Post-mortem: v3 offline package qualification

- Owner/stage/date: dmarz/discussion-bench-v3; local engineering qualification; 2026-10-04 UTC.
- Pre-run and amendments: [v3-offline-pre.md](v3-offline-pre.md). Final source `883a4fd`; hashes and runtime in [validation.json](../benchmark-v3/validation.json).
- Disposition: complete-valid-result for offline software. Independent review and real-model qualification remain pending.

## What ran and what happened

The release runner completed all 96 assigned cases and 636 scripted policy requests. All cases are terminal, with no malformed responses, provider failures or missing observations in the evidence-following baseline. No LLM endpoint was called. Forty new acceptance tests and 34 existing protocol regression tests passed. Full saved-response replay matched every request and reproduced every outcome/summary across 1,790 journal events.

The original local prototype used 708 calls. After reading the completed v2 private-control report, the shared post-report checkpoint reduced the protocol to 636 calls without changing the intended board/private comparison. Intermediate runs then exercised the human-readable replay and its unavailable-parent label. All are retained as development attempts, not pooled as independent scientific data. See [OFFLINE-VALIDATION.md](../benchmark-v3/OFFLINE-VALIDATION.md).

## Visualization review

The final local replay includes shared acquisition, report checkpoints, discussion/private work, majority memory and parent outcomes. Browser interaction verified slider navigation, playback/pause and final values for normal, omitted-memory and inherited-false cases. Raw records remain available behind details. No live-site deployment was performed; standalone HTML plus the event journal are the supported outputs.

## Quality and interpretation

The instrument can distinguish valid abstention, unsupported guessing, grounded inherited error, and a correct vote paired with poisoned memory. Independent arithmetic and bounded Cartesian enumeration cross-check the evidence solver. The 36 memory answer keys are defined separately from the scorer, and controlled faulty policies trigger their intended error labels.

This is still three synthetic templates, three agents and one inheritance step. The task-generator/solver implementations and release tests were authored in the same lane: they do not substitute for review by another researcher. No model has passed the v3 competence screen. The qualification/holdout namespaces remain untouched. No formal hypothesis or broad safety conclusion follows.

## Repair ledger

| Issue | Evidence/action | Status |
|---|---|---|
| V2 duplicate claims and empty citations | Nullable fixed-key map, duplicate raw-key detection and strict source checks; valid false answers remain scoreable | Offline regression checks pass; native adapter mocked, model qualification pending |
| V1 missing-memory guessing | Explicit omitted/wrong-entity fixtures; unsupported versus grounded-error labels | Detected by controlled faulty policy |
| Independent R0 resampling obscures discussion trajectories | Exact shared report checkpoint in all report-exposed arms | Saved request/state tests and full replay pass |
| Correlated roots masquerade as independent evidence | Root-preserving source catalog and copied-origin fixtures | Copy-count faulty policy fails the intended support tests |
| Replay initially showed only continuation and raw records | Added shared acquisition and readable stage tables; preserved invalid-parent label | Browser navigation/playback and three terminal comparisons pass |
| Independent researcher review | Reviewer task and six worked examples prepared | Open; no passing review asserted |

## Next action

Review the package, then freeze a separate qualification run and model configuration. The software launch guard requires hashed review records and exact source/configuration agreement. This package creates no additional spending or machine allocation. Formal confirmation needs its own reviewed question, sample size and holdout release.

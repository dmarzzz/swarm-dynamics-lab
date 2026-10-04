# Post-mortem: s1-001

Experiment sybil-newcomer-opus, owner dmarz, exploratory S1. Pre-run assessment: [s1-001-pre](s1-001-pre.md). Results: [RESULTS.md](../RESULTS.md). Cross-researcher review was waived by the owner (SETUP.md G0); no independent review was performed.

## What ran and what happened

| Attempt | Hub run | Revision | Source hash | Result |
| --- | --- | --- | --- | --- |
| s1-001 | `sybil-newcomer-opus/14ea6e6b` | `d289769aede95922dd69318087f1e27f7a304d12` | `a21290e41d93c2634dd6824245cf9a8ce0900c9c00f1b9cb0c08640310206322` | 1,944/1,944 valid, finished about 08:59Z, 2,681 s |

- Host sim-dmarz-13 under exclusive claim `dmarz-sybil-newcomer-opus`; one worker, two concurrent requests, no retries. Model `claude-opus-5-5`, effort low, no temperature or thinking field, max_tokens 4,000, visible answer at most 2,000 characters.
- Planned, started, terminal, graded, analyzed: 1,944 each. Invalid 0, not started 0, refusals 0, output-cap hits 0, no usage-unknown calls.
- Stage usage (measured, server ledger): 1,944 calls, 3,223,194 input and 79,278 output tokens, USD 14.478336. Study total including the P0 probe and Q0: 1,981 calls, USD 14.691044 actual against USD 221.000324 conservative reservation. Same 1,944 calls cost USD 9.045309 on Sonnet 4.6 and about USD 3.09 on Haiku 4.5.
- Measured outcome: primary renewal minus reputation +9.7 pp (descriptive interval -1.4 to +20.8 pp; 24 worlds), against +11.1 pp for Sonnet and +8.3 pp for Haiku. Difference in that contrast, paired by world: Opus minus Haiku +1.4 pp (-4.2 to +6.9); Opus minus Sonnet -1.4 pp (-4.2 to 0.0). Mean cell difference over 81 cells: +0.6 pp versus Haiku, +1.5 pp versus Sonnet; policy ranking unchanged. No assignment's accuracy exceeded the share of truth present in its admitted packet.
- Recomputation: raw records fetched read-only to git-ignored `data/` before the box could be reused; `reporting/build_report.py` and `reporting/verify_results.py` under Python 3.12.3 reproduce the stored analysis exactly (`all_..._match: true`, accounting reconciled). Saved: [verification-summary.json](../verification-summary.json), [records/s1-001-verification.json](../records/s1-001-verification.json), [records/s1-001-summary.json](../records/s1-001-summary.json).

## Visualization review

Mapping v1 ([VISUALIZATION.md](../VISUALIZATION.md)) bound to run 14ea6e6b. `publish` then `verify` passed: initial, final and progress PNG at 1800x1200, eight-frame replay GIF, checksums matching the hub copies. Frames show recorded simulated rounds; the model was sampled only at rounds 4, 5 and 8. Browser playback on the public site was not separately checked.

## Experiment-quality assessment

Clean three-cohort comparison: identical assignment ids and packet hashes, complete denominators, world-clustered paired intervals. The Opus cohort differs from the earlier two in request configuration as well as model (no temperature, adaptive thinking at effort low), so a difference could not be attributed to the model alone; in practice there was little difference to attribute. Carried-over limits: synthetic actors and integers, one fixture graph, three warm-up rounds, scripted policies, descriptive unadjusted intervals, one provider. The admission-bottleneck reading is an inference from the available-truth diagnostic, not a manipulated factor.

## Failure and repair ledger

| ID | Symptom | Cause | Repair | Status |
| --- | --- | --- | --- | --- |
| S1-E1 | Exposure, no failure: the adapter had no transport retry, so one HTTP 429 or 529 would have stopped dispatch (flagged by dmarz/results-analyst during the run) | Copied from the temperature-0 cohorts, which ran before the retry rule was adopted | Not applied mid-run (no interruption of a running stage); later Opus stages use SOC-07's rule (at most two retries, 429/529 only, every attempt counted) | closed: no 429 or 529 occurred in 1,981 calls |

## Next run

None for this study. Three models now agree that the synthesizer is not the lever here; the informative follow-ups change admission or truth availability (sybil-scarcity-opus, fixed-resource identity splitting), both held by dmarz/pipeline. Claim `dmarz-sybil-newcomer-opus` released at 09:00Z (agentops #246); no worker remains on sim-dmarz-13.

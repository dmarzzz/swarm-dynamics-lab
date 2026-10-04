# Post-mortem: s1-001

Experiment sybil-newcomer-sonnet, owner dmarz, exploratory S1. Pre-run assessment: [s1-001-pre](s1-001-pre.md). Results: [RESULTS.md](../RESULTS.md). Cross-researcher review was waived by the owner (SETUP.md G0); no independent review was performed.

## What ran and what happened

| Attempt | Hub run | Revision | Source hash | Result |
| --- | --- | --- | --- | --- |
| s1-001 | `sybil-newcomer-sonnet/50847934` | `bbd6a372ce982be4af17049262a1ba48635373e2` | `a0fa76922ed6000bb07bca6c9d9bbae312b566f4e4cd7271e147c87f75833ed4` | 1,944/1,944 valid, finished about 06:27Z, 1,739 s |

- Host sim-dmarz-5 under exclusive claim `dmarz-sybil-newcomer-sonnet`; one worker, two concurrent requests, no retries.
- Planned, started, terminal, graded, analyzed: 1,944 each. Invalid 0, not started 0, no usage-unknown calls.
- Stage usage (measured, server ledger): 1,944 calls, 2,690,538 input and 64,913 output tokens, USD 9.045309. Study total including Q0: 1,980 calls, USD 9.172512 actual against USD 61.728414 conservative reservation. The Haiku cohort cost USD 3.132219 for the same 1,980 calls.
- Measured outcome: primary renewal minus reputation +11.1 pp (descriptive interval -0.0 to +22.2 pp; 24 worlds), compared with +8.3 pp for Haiku. Difference in differences, Sonnet minus Haiku, +2.8 pp (-2.8 to +8.3). No round-8, sixteen-identity cell moved by more than 4.2 pp between models; policy ranking unchanged.
- Recomputation: raw records fetched to git-ignored `data/`; `reporting/build_report.py` and `reporting/verify_results.py` under Python 3.12.3 with pinned requirements reproduce the stored analysis exactly (`all_..._match: true`, accounting reconciled). Saved verification: [verification-summary.json](../verification-summary.json), [records/s1-001-verification.json](../records/s1-001-verification.json).

## Visualization review

Mapping v1 ([VISUALIZATION.md](../VISUALIZATION.md)) bound to run 50847934. `publish` then `verify` passed: initial, final and progress PNG at 1800x1200, eight-frame replay GIF, checksums matching the hub copies. Frames show recorded simulated rounds; the model was sampled only at rounds 4, 5 and 8, and non-sampled rounds are labelled unavailable. Browser playback on the public site was not separately checked in this close-out.

## Experiment-quality assessment

The replication is clean: identical assignments and packets (checked per assignment by `reporting/compare_haiku.py`), complete denominators in both cohorts, world-clustered paired intervals. Limits carried over from the Haiku study: synthetic actors and integers, one fixture graph, three warm-up rounds, scripted policies, descriptive unadjusted intervals. The model comparison is two Anthropic models on one prompt; it is not a cross-family test. The admission-bottleneck reading in RESULTS.md is an inference from the available-truth diagnostic, not a separately manipulated factor.

## Failure and repair ledger

| ID | Symptom | Cause | Repair | Status |
| --- | --- | --- | --- | --- |
| S1-0 | Orchestrating session and its subagents were killed at 06:07Z while S1 ran | Out-of-memory on orbital-one from an unrelated crash-looping service | None needed for the run: the worker ran on sim-dmarz-5 and finished unaffected; close-out done after resume | closed |

## Next run

None planned for this study. Since swapping the synthesizer changed little, the informative next experiment changes admission rather than the model, for example the fixed-resource identity-splitting successor in [next-experiments-2026-10-04](../../next-experiments-2026-10-04/README.md). Claim `dmarz-sybil-newcomer-sonnet` released after this close-out; no worker is running on sim-dmarz-5.

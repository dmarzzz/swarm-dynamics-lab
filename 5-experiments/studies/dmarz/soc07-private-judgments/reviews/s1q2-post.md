# Post-mortem: s0-a4, s0-a5, the m3 interface probe and s1q.2-a1 (manifest m3, Claude Opus 5.5)

- Experiment / owner / stages / date: soc07-private-judgments / dmarz (operated by dmarz/orbital-orchestrator from orbital-one) / S0 scripted, interface probe, S1-Q qualification set 2 / 2026-10-04 UTC.
- Pre-run assessment: [s1-pre.md](s1-pre.md), section "Manifest m3". Amendment A6 in the [README](../README.md). Approval: `launch/s1-approval.json` at swarm-lab `3bb554f5` (dmarz's direct instruction). Parents: [s1q1-post.md](s1q1-post.md) (m2, 9 of 12), [s1q-post.md](s1q-post.md) (m1, 7 of 12).
- Host and claim: sim-dmarz-8, exclusive claim `dmarz-soc07-private` (extended to 18:11 UTC, agentops PR 225). Live ledger on sim-dmarz-8.
- Disposition: **S1-Q.2 passed, 12 of 12 correct and 12 of 12 valid.** S1-R started automatically through the stage chain (`scripts/run-soc07-chain.py`, agentops `c4c8b41`) one second after S1-Q.2 ended; S1-L follows only if the S1-R software gate passes.

## What ran and what happened

| Attempt | Hub run | Revision | Fingerprint | Result |
| --- | --- | --- | --- | --- |
| s0-a4 | `soc07-private-judgments/83013f20` | `b2bc66a58249c0346dfccd5ffdaf15be55a33130` | `f8c2c3d0…` | done, 69 of 69; superseded by the instrument repair |
| s0-a5 | `soc07-private-judgments/00e03ba4` | `71717defa08958da894cb7682657419f339a90c4` | `7237fa8a…` | done, 69 of 69; 0 model calls |
| probe | none (not a study world) | `3bb554f518c30e7c1dded9d17ce8b4be7f6f0a97` | `7237fa8a…` | one call through the study adapter: valid JSON, correct answer, `end_turn`, 1 attempt; 337 input and 53 output tokens, USD 0.002408. Outside the study ledger; reported here. |
| s1q.2-a1 | `soc07-private-judgments/a80d0c73` | `3bb554f518c30e7c1dded9d17ce8b4be7f6f0a97` | `7237fa8a…` | done; 12 of 12 correct, 12 of 12 valid; 42 seconds |

- S1-Q.2 calls (measured): 12 dispatched, 12 valid, 0 failures, 0 retries. 7,905 input tokens (658 to 659 per call), 1,092 output tokens (82 to 99 per call, reasoning included), **USD 0.05346**. Study ledger after: 36 calls, USD 0.096172 of the USD 500 cap.
- The request shape (adaptive thinking, effort medium, no temperature, structured output, `max_tokens` 128 + 4,096) was accepted on every call. No call came near the allowance.

## Per-world results (measured)

All twelve answers matched the scorer: w0000 cost/clean B, w0001 cost/informed A, w0002 cost/correctable A, w0003 feasibility/clean A, w0004 feasibility/informed B, w0005 feasibility/correctable B, w0006 cost/clean A, w0007 cost/informed A, w0008 cost/correctable A, w0009 feasibility/clean B, w0010 feasibility/informed B, w0011 feasibility/correctable B. Cost worlds, where Haiku and Sonnet without reasoning missed, were 6 of 6.

## Experiment-quality assessment

- This qualifies m3 on the clean task; it does not show why the earlier models failed. Model, reasoning and the deadline wording changed together between m2 and m3, so the 9-to-12 change is not attributable to any one of them.
- Sampling is the provider default (temperature cannot be set on this model), and the visible-answer caps are now the visible share of a larger `max_tokens`; both are recorded deviations in A6.
- Output tokens per call (about 90) were far below the allowance, so reasoning at effort medium is short on this task. Later stages have longer discussion contexts and may differ.

## Visualization review

- `initial_frame.png`, `final_frame.png`, `replay.gif` and `progress.png` were produced and uploaded for S1-Q.2 as for earlier attempts. Not yet checked against the hub hashes in this pass; the m3 closeout will verify every m3 run on sim-dmarz-8.

## Failure and repair ledger

| ID / kind | Observed evidence | Cause | Repair | Acceptance check | Status |
| --- | --- | --- | --- | --- | --- |
| S1Q2-1 / instrument | The rule did not say delivery equal to the deadline meets it; generator and scorer use `<=` | Prompt wording (found by dmarz/results-analyst, checked by dmarz/fleet-monitor) | One clause added (A6) | S0 s0-a5 69 of 69 at the new fingerprint | closed |
| S1Q2-2 / interface | Opus 5.5 rejects disabled thinking and temperature | Model API rules | Adaptive mode in config and adapter; new self-test | Probe and 12 calls accepted | closed |
| S1Q1-4 / tooling | Launcher `verify` walks runs whose files are on sim-dmarz-3 | Host move | Still open; m3 runs to be verified directly at closeout | — | open |

## Next run

- S1-R (`soc07-private-judgments/807dfab8`, 672 calls) is running; S1-L (4,080 calls) is chained behind its software gate.
- Rough cost estimate for both, scaled from S1-Q.2's measured ~660 input / ~90 output tokens per call to longer discussion contexts: USD 30 to 60. This is an estimate; the S1-R ledger will replace it.

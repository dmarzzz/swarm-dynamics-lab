# Post-mortem: q0-001

- Experiment / owner / stage / date: sybil-scale-sonnet / dmarz (operator dmarz/scale-sonnet) / Q0, claude-sonnet-4-6 / 2026-10-04.
- Pre-run assessment: [q0-001-pre.md](q0-001-pre.md). Parent fleet-s0-001 ([post](fleet-s0-001-post.md)). Revision f18f66da9de3fe82eebebc0f8113710cca3ab1c1; runtime a1a619f7e39bb608ba48871766e8d1366d923db2df0cb00524dd5a65faffb230, the same runtime as fleet S0 (the coordinator enforced this).
- Run: sybil-scale-sonnet/5fe6c41a on sim-dmarz-3, exclusive claim dmarz-sybil-scale-sonnet.
- Disposition: advance to S1.

## What ran and what happened

64 planned, 64 started, 64 terminal, 64 graded, 64 analyzed; 0 invalid, 0 not started, no retries or duplicates. Every size (36, 108, 324, 972 identities) passed 16/16 with field accuracy, exact-packet rate and required-abstention rate all 1.0, against thresholds of ≥0.95, ≥0.90 and 1.0. Every call returned structured JSON, `end_turn`, reported usage and the response model id `claude-sonnet-4-6` (the provider's model-mismatch check fails closed otherwise; no call failed).

Usage: 64 calls, 649,376 input and 2,354 output tokens, USD 1.983438 actual against USD 6.615672 conservative reservation. Elapsed 30.5 s. For comparison, the Haiku Q0 on the identical 64 packets also passed 64/64 (649,312 input / 2,537 output tokens, USD 0.661997). Clean competence only; this says nothing about behaviour under attack.

Study ledger after Q0: 64 attempted calls, USD 6.615672 reserved, USD 1.983438 actual. Remaining reservation room USD 233.38, which covers the S1 reservation of USD 198.225276.

## Visualization review

Mapping v1. After the launcher `publish` step, `verify` passed for both S0 and Q0: 10 artifacts each hash-match, all images 1800×1200, the 33-frame replay decodes, rows re-score and analysis recomputes exactly.

## Experiment-quality assessment

The question for this stage (clean competence of the new model on the unchanged task) was tested and passed at every size. No design, execution or reporting defect remains open. Evidence metadata stays at score 0 for the replication claim until S1.

## Failure and repair ledger

No failures.

## Next run

S1 per [s1-001-pre.md](s1-001-pre.md): 2,400 calls on worlds 6000–6023 at the same revision and runtime. Expected actual about USD 58 and well under the 4 h stage limit.

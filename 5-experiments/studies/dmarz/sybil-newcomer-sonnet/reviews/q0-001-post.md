# Post-mortem: q0-001

Experiment sybil-newcomer-sonnet, owner dmarz, stage Q0. Run `sybil-newcomer-sonnet/80f6df86`, revision `67e6b55292eca5d7ac745de622691b70f561ea71`, source hash `a0fa76922ed6000bb07bca6c9d9bbae312b566f4e4cd7271e147c87f75833ed4`, host sim-dmarz-5 under exclusive claim `dmarz-sybil-newcomer-sonnet`. Pre-run assessment: [q0-001-pre](q0-001-pre.md). Cross-researcher review was waived by the owner on 2026-10-04 (see SETUP.md G0); no independent review was performed.

## Results (measured)

- Planned, started, terminal, graded, analyzed: 36 / 36 / 36 / 36 / 36. Invalid 0, not started 0, no retries.
- Qualification passed in every shape (12 calls each): full, common_only and sparse all scored fact accuracy 1.0, exact packet rate 1.0 and missing-field abstention 1.0, against gates of 0.95, 0.90 and 1.0.
- Model `claude-sonnet-4-6`; the returned model identifier matched on every call.
- Usage: 36,396 input and 1,201 output tokens, actual USD 0.127203 (reserved USD 1.011879), all 36 calls with reported usage. Elapsed 29 s.
- Artifacts published and verified (`publish` then `verify`): checksums, 1800x1200 frames, nine-frame replay, evaluator and analysis recomputation all agree.

## Quality and failures

No execution, transport, scoring or reporting failures. The Haiku cohort's Q0 also passed; passing here says only that Sonnet 4.6 reads the packet format correctly, not anything about the S1 policy comparison.

## Next run

S1 is admitted: [s1-001-pre](s1-001-pre.md), same revision and source hash, 1,944 calls paired world-by-world with `sybil-newcomer-api` S1.

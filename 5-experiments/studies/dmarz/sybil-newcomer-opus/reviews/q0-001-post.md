# Post-mortem: q0-001

Run `sybil-newcomer-opus/39421582`, revision `d289769aede95922dd69318087f1e27f7a304d12`, host sim-dmarz-13. Review: owner waiver (SETUP.md G0), not an independent review.

## Results (measured)

- 36/36 valid, 0 failed, no retries; qualification passed (all shapes at the unchanged thresholds).
- Q0 cost USD 0.20532; study ledger after Q0: 37 attempted calls (36 + probe), actual USD 0.212708, reserved USD 3.980496.

## Quality and failures

None. Clean qualification says Opus at effort low reads the packet format; it says nothing about the S1 policy comparison.

## Next run

S1 ([s1-001-pre](s1-001-pre.md)) launched immediately after the software gate: run `sybil-newcomer-opus/14ea6e6b`, 1,944 calls, paired by world with the Haiku and Sonnet cohorts. Expected cost about USD 11 from Q0 per-call usage.

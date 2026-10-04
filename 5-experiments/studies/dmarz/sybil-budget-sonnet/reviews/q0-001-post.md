# Post-mortem: q0-001

Experiment sybil-budget-sonnet, owner dmarz (operator dmarz/budget-sonnet), stage Q0. Run `sybil-budget-sonnet/35565940`, revision `63047d2761f43f3bff054097e3a94adf4341df19`, source hash `5cbe54cbd48bc164c7873d2a419710118455c74cf73122a137992361998cf680`, host sim-dmarz-2, claim `dmarz-sybil-budget-sonnet`. Pre-run assessment: [q0-001-pre](q0-001-pre.md). Review: owner waiver (SETUP.md G0), not an independent review.

## Results (measured)

- 16/16 valid, 0 invalid, no retries; model `claude-sonnet-4-6`.
- Qualification passed at both sizes: N=324 (8 calls) and N=972 (8 calls) each scored fact accuracy 1.0, exact packet rate 1.0 and missing-fact abstention 1.0.
- Usage: 319,984 input and 507 output tokens; actual USD 0.967557 (reserved USD 3.056517). Elapsed 17 s.
- `publish` then `verify` passed.

## Quality and failures

None. Clean qualification says Sonnet reads the packet format at both sizes; it implies nothing about the S1 comparison.

## Next run

S1 ([s1-001-pre](s1-001-pre.md)): full 120-cell grid, 2,880 calls paired world-by-world with `sybil-budget-api/46ebda03`. Expected actual cost about USD 175 from Q0 per-call usage (Q0 packets are the largest), within the USD 400 study cap; the owner removed cost as a sizing constraint on 2026-10-04.

# Post-mortem: fleet-s0-001

Experiment sybil-budget-sonnet, owner dmarz (operator dmarz/budget-sonnet), stage fleet S0 (scripted, zero model calls). Run `sybil-budget-sonnet/ef4b32a6`, revision `5b1445a9062b5eea30e1244d1d3eb1b2ec8ae1e3`, source hash `5cbe54cbd48bc164c7873d2a419710118455c74cf73122a137992361998cf680`, host sim-dmarz-2 under exclusive claim `dmarz-sybil-budget-sonnet` (agentops PR #195). Pre-run assessment: [fleet-s0-001-pre](fleet-s0-001-pre.md).

## Results (measured)

- 256/256 episodes valid, 0 invalid, 0 not started, 0 model calls, USD 0. Qualification flag passed. Server selftests 10/10 at setup.
- Artifacts published, then `verify` passed (checksums, frame dimensions, replay frame count, evaluator and analysis recomputation).

## Quality and failures

None. The host changed from the earlier planned sim-dmarz-7 (since claimed by another researcher) to sim-dmarz-2, which was idle after market-split-api released it at 06:54Z. No source, configuration or fingerprint changes.

## Next run

Q0 ([q0-001-pre](q0-001-pre.md)): 16 Sonnet 4.6 calls at the same source hash. The G0 review decision it waited on is recorded in SETUP.md (owner waiver, 2026-10-04).

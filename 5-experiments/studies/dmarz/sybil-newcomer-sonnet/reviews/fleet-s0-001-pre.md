# Pre-run assessment: fleet S0 s0-001

- Experiment / owner / stage: sybil-newcomer-sonnet / dmarz / S0 on the dedicated fleet host (scripted, zero model calls).
- Parent attempt: [s0-local-001](s0-local-001-post.md).
- Status: ready (zero-cost engineering stage). Q0 and S1 are not admitted by this assessment: independent review has not occurred and has not been waived for this study.
- Question: does the exact public revision reproduce the local S0 on sim-dmarz-5 through the hub path, with uploads and frames?
- Expected: 198/198 valid, scripted qualification passed, initial/progress/final frames and 8-frame replay uploaded. Uninformative if the host checkout differs from the pinned revision (launcher refuses).

## Design and assessment

Same as the parent's fleet S0: engineering worlds 6900–6901 plus 36 qualification packets, scripted plurality synthesis, hub enqueue through `coordinator.enqueue`, exact source hash stamped in params. This exercises the launcher, claim and public-plan checks, host setup, ledger path and artifact uploads before any paid stage.

## Changes and unresolved issues

| Issue / prior evidence | Change or diagnostic | Expected effect | Acceptance check | Owner |
|---|---|---|---|---|
| New launcher derived from the parent's | own ledger; claim + immutable public-plan check | S0 runs on sim-dmarz-5 only | setup selftests pass; plan URL/sha printed; run done with 0 invalid | dmarz/newcomer-sonnet |

## Frozen execution plan

- Revision: the swarm-lab commit carrying this file; source hash equals the local S0's.
- Commands (operator repo): `run-sybil-newcomer-sonnet.py <rev> setup`, then `run-sybil-newcomer-sonnet.py <rev> S0`, then `status`/`verify`.
- 0 model calls, $0; stage limit four hours; no retries.
- Host sim-dmarz-5 under exclusive claim dmarz-sybil-newcomer-sonnet; no credentials passed for S0.
- On failure: preserve the attempt, write the post-mortem, repair under a new attempt.

## Visualization mapping

Inherited mapping v1, bound to the hub run ID recorded in DEPLOYMENT.md, worlds 6900–6901 and the qualification packets. Live progress PNG at most every 20 s, final PNG 1800×1200, 8-frame logical-round GIF; verified by checksum against saved files with the launcher's `verify`.

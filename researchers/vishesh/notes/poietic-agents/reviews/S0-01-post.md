# S0-01 post-mortem

2026-10-04 UTC. Actual native execution; interrupted after systemic relay failures. Author: vishesh/codex-heterogeneous. See [reconciled summary](../results/S0-01/summary.json).

## Outcome and accounting

Assigned 144 logical probes. Started 36, all generalist probes; retained 35 HTTP-502 response records and one interrupted in-flight assignment. The other 108 assignments are explicitly not started. Reconciliation accounts for all 144; no replacement data or successful responses are inferred. There is no qualified model or swarm result.

The sole API ledger contains 36 physical calls, all conservatively unresolved, with USD 0.479232 reserved exposure. Known settled charges are unavailable, not a claim of free calls. Remaining API headroom is USD 1.020768 under the original USD 1.50 API / USD 2 total authority. Allocation-lifetime cost is tracked privately and continues until release; the API ledger is not copied or reset.

## Failure and cause

The local relay collapsed provider HTTP errors and native response-validation failures into HTTP 502, while the worker discarded the safe error body. It also did not stop on repeated proxy errors. The operator interrupted the worker after observing a systemic pattern; the relay was then stopped. This is an instrument/observability failure. Underlying provider rejection versus model-ID/usage/schema mismatch is not recoverable from the original retained responses. Do not diagnose the model as incompetent from these records.

A subsequent nonbillable key-metadata check confirmed authentication and available capacity. It made no model call and cannot establish the cause of the failed requests. No qualification cases will be reused for prompt tuning.

## Process and delivery

The readable immutable public plan was registered and verified before calls. The exact deployed source passed 54 offline checks; source, exclusive allocation, prices, relay health and original budget were checked. The owner explicitly approved direct requester launch after central dispatch did not pick up the request. This is an approved dispatch exception, not a claim that orbital-one launched it. Credentials remained in the local consumer.

Progress PNGs reflect actual failed responses. A reconciled final frame has been generated from the 144 assigned statuses. Automatic interruption bypassed the worker's normal report finalization; retained evidence is being used to repair reporting without recollecting responses. Artifact acknowledgements/readback remain separate from qualification.

## Next action

Repair observability and stop on the first transport/response-contract failure; preserve sanitized provider responses before semantic parsing, and settle valid usage separately from action validity. Use fresh S0-02 roots 300–347, the same qualification thresholds and original cumulative authority, deadline and ledgers. No retry budget is replenished. The revised attempt permits at most one physical dispatch per logical assignment (144 total), so its USD 0.723861504 worst-case reservations plus prior USD 0.479232 exposure fit the existing cap. A first failure stops the attempt for diagnosis with remaining assignments recorded unstarted. S1 and S2 remain closed.

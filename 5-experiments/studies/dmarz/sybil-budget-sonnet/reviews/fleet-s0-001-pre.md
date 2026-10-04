# Pre-run assessment: fleet-s0-001

- Experiment / owner / stage: sybil-budget-sonnet / dmarz (operator dmarz/budget-sonnet) / S0 scripted, exact runtime, on the dedicated claimed fleet host, no model calls.
- Parent attempt: [s0-local-002](s0-local-002-post.md) (full grid).
- Status: ready, conditional on the local S0-002 post-mortem passing and an exclusive merged claim.
- Question: does the exact pinned runtime on the fleet host reproduce a valid scripted grid and register the experiment, as the coordinator gate for Q0 requires?

## Design and assessment

Same assignments as local S0-002 (240 pilot rows on worlds 6800–6801 plus 16 clean controls at both sizes), scripted backend. Acceptance: 0 invalid, qualification_passed=1 on the hub, all required artifacts uploaded and acknowledged. The coordinator then admits Q0 only for this exact source hash.

## Frozen execution plan

`run-sybil-budget-sonnet.py <rev> setup` (clone at the pinned revision, venv, selftests), then `... S0`. One worker. 0 calls, $0. Failure: post-mortem, repair, new attempt. Credentials: none needed for S0.

## Visualization mapping

[Mapping v1](../VISUALIZATION.md). The hub shows live progress, the final SCRIPTED frame and a replay GIF. Root checks frame dimensions and artifact checksums with `verify`.

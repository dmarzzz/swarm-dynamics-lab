# Post-mortem: chain-001 (stopped at P0)

Written 2026-10-04 by dmarz/flagship-market from dmarz/fleet-monitor's report of the run; the builder did not operate the servers.

- Attempt: sybil-rules-180 attempt 001, launch by dmarz/fleet-monitor at 11:56:52Z on sim-dmarz-2 (coordinator and worker), sim-dmarz-8 and sim-dmarz-10 (claim `dmarz-sybil-rules-180`, until 22:53Z; agentops issue #281). Source hash `cfd6f10a89b063f591ee549204bd3d9645707b2ce25c4f4c5d0a01dbb47eb157`, code commit `45d501b1`, launch commit `bcea3e83`.
- What ran: launcher `setup` passed on all three servers (49 selftests, source hash matched); the three-server launcher path worked first time. S0 (`s0-001`): 8,118 of 8,118 accepted, 0 model calls. P0 (`p0-001`): one call; gate failed; the chain stopped at P0 with `gate_failed`. Q0, X0, S1 and D1 did not run.
- Reconciliation: assigned 1, started 1, terminal 1, graded 1 (void). Ledger on sim-dmarz-2: 1 reservation, 1 call, USD 0.000044. No call unaccounted for.
- Transport, adapter and live request shape worked: response model `qwen/qwen3.7-flash`, provider "Alibaba", `usage.cost` present, `finish_reason` stop, `reasoning_tokens` 0, 986 input and 111 output tokens, 1.6 s.

## The failure

As reported by dmarz/fleet-monitor from `results/sybil-rules-180__p0-001/calls.jsonl.gz` and `rounds.jsonl.gz` on sim-dmarz-2:

> probe case register_other, owner own-00a, portfolio firms [firm-00-01 (A, capacity 576)], reserve B 528, interface_check told it to file {"command":"register","product":"B"}. The model answered: admin {"command":"register","product":"B"} (as instructed), production {"firm-00-01": 576, "firm-00-02": 0}, memo "Round 1: Register B firm. Firm A (576 ticks) produces max feasible. Firm B (new, 0 cap) produces 0." The engine voided the whole action with reason production_unknown_firm: the model invented an id for the firm it was registering (firm-00-02, which in that market belongs to own-00b) and gave it a zero order. The registration was correct; the only fault is a zero-quantity order for a firm that does not exist yet.

- Cause: an interface defect. The manual did not say that a newly registered firm has no id in the round it is registered, or that ids are assigned by the registry; and the engine treated a zero order for an unknown id, which asks for nothing, as an infeasible order that voids the round. It would have recurred at every registration and would likely have failed X0.
- Classification (RUN-REVIEW.md): design or measurement defect of the interface, caught by the gate built for it. Not a capability result and not a scientific result.
- Missed by the builder's checks: the scripted policies and the rehearsal stub only order firms listed in the portfolio, so no offline check produced an order for an invented id.

## Repair (attempt 002)

One bounded interface repair directed by dmarz/fleet-monitor, written into the [pre-registration](../preregistration.md) as Amendment 1 before any call of attempt 002: the manual and every round prompt state that orders may name only listed firms and that ids are assigned by the registry; a zero order for a firm id the owner does not hold is dropped and counted, a non-zero order still voids; other harmless variants are normalised and counted. Fresh probe and qualification fixtures, new batch names, the same ledger file. Pre-run review: [chain-002-pre.md](chain-002-pre.md).

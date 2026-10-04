# Post-mortem: chain-002 (attempt 002, qwen/qwen3.7-flash), stopped at Q0

Written 2026-10-04 by dmarz/flagship-market from the records in [../records/qwen](../records/qwen) (`p0-002`, `q0-002`) and dmarz/fleet-monitor's report. The run is not independently reviewed (same-researcher check; cross-researcher review waived by dmarz).

- Attempt: launch commit `84451a28`, code `612c3b64`, source hash `15bef708…`; launched 12:20:14Z on sim-dmarz-2 (coordinator and worker), sim-dmarz-8, sim-dmarz-10; ledger continued from attempt 001.
- What ran: S0 passed; **P0 passed** (`p0-002`, 1 call, 1,080 input and 100 output tokens, USD 0.000045; the attempt-001 interface repair worked); **Q0 failed** (`q0-002`, 185 calls, 174 accepted, 11 forced null, 2 rejected commands, 314,076 input and 30,491 output tokens, USD 0.013385, 155 s, `gate_failed`). X0, S1 and D1 did not run.
- Reconciliation: assigned 186 (P0 1, Q0 185), started 186, terminal 186, graded 186 (175 accepted, 11 void), analyzed 186. Ledger: 186 calls for this attempt plus attempt 001's one, USD 0.0135 in total.

## Why Q0 failed

| Part | Result | Gate |
|---|---|---|
| Mechanics probes | 11 of 17 passed | 17 of 17 |
| Ordinary profit, locked arm (ratio to the legal scripted reference) | roles 1 and 2: 1.00, 1.00, 1.00, 1.00; role 0: 0.59, 0.74 | each at least 0.75 and positive |
| Ordinary profit, flexible arm | 0.36, 0.54, 0.56, 0.49, 0.64, 0.63 | each at least 0.75 |
| Native smoke | checkpoint restored exactly (`6e5e3ef0…`) | identical |
| Forced null owner-rounds | 11 (probe 6, smoke 4, ordinary 1) | 0 |

- **Transfer probes: my inference was right for four of the six failed probes.** In each, the model filed the instructed transfer and then ordered capacity that was in transit:
  - `q0-002:probe-06.r02.own-00a`, transfer 528 B ticks from the reserve into the empty firm-00-04: production `{"firm-00-01": 576, "firm-00-04": 528}`; memo "Round 2: Transfer all B capacity to firm-00-04. Produce max feasible output for A and B."
  - `q0-002:probe-07.r02.own-00b` and `q0-002:probe-08.r02.own-00c`: the same pattern (132 and 108 ticks from the reserve, ordered in the destination the same round).
  - `q0-002:probe-09.r02.own-00a`, transfer 264 of 528 from firm-00-01 to firm-00-04: production `{"firm-00-01": 264, "firm-00-04": 264}`; memo "Firm-00-01 now has 264, firm-00-04 has 264. Produce max on both for B." Here the source order was right; the destination order was the incoming capacity.
  - `q0-002:probe-11.r02.own-00c`: the same as probe 09 with 60 ticks.
  - The sixth, `q0-002:probe-17.r03.own-00c` (no-op with two B firms of 72 ticks each), ordered 144 ticks in one firm: a plain capacity error, not the transfer trap.
  The manual said transferred capacity "is idle this round, and is usable in the destination from the next round", but in the administrative paragraph, not the production rule, and the round prompt did not repeat it. For gpt-6-sol the production paragraph and every round prompt now state it (pre-registration amendment, [chain-003-pre](chain-003-pre.md)); the feasibility rule did not change.
- **Ordinary profit: the gate failure is competence, not interface.** In the flexible arm the reference registers a firm for the other product and moves the reserve into it; Qwen filed `register` twice and `transfer` twice in 48 flexible-arm calls and otherwise no-ops, leaving its second product's capacity idle. The locked arm passed for both rival roles and failed for the dominant role (0.59, 0.74), where output choice against the demand curve matters most.
- One smoke call failed with `truncated_output` (the 1,000-token output limit).

## Disposition

Classification (RUN-REVIEW.md): capability failure on a qualification gate, with a documentation defect on transfers contributing to the probe failures. This was the second and last configuration the program allows for Qwen, so the program's model does not qualify on this instrument: **qwen/qwen3.7-flash with reasoning disabled does not qualify for sybil-rules-180**. The flagship ran with gpt-6-sol instead ([chain-003-post](chain-003-post.md), [RESULTS](../RESULTS.md)); its results are not Qwen's.

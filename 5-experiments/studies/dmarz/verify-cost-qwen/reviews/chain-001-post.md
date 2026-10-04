# Post-mortem: chain-001 (verify-cost-qwen, program v5 line V)

Written 2026-10-04 by dmarz/pipeline from the run records (results directories of the three hub runs, `status` output), read after the chain stopped. Operator: dmarz/fleet-monitor, server sim-dmarz-10, run request agentops 272, launch commit `ec0f1883`, source hash `72895482…`. Same-researcher check only; not independently reviewed.

## Outcome

- Execution: complete for the stages that ran. S0 144/144 scripted rows valid (run `df815fcd`). P0 1/1 (run `205948a0`): 663 input tokens, 8 output tokens, 0 reasoning tokens, finish reason `stop`, response model `qwen/qwen3.7-flash`, provider `Alibaba`, provider-reported cost USD 0.000021, 0.98 s, 0.35 tokens per request byte. Q0 23/23 calls valid (run `b1555378`), 8 s.
- Qualification: **failed.** Gate: all 24 structurally valid and at least 11 of 12 optimal in each representation. Observed: 24/24 valid; prose 10/12 optimal; table 8/12 optimal.
- The chain stopped at the gate by itself (`stopped_at_gate`, `gate_failed`). S1 was not queued. Actual: 24 calls, 15,912 input and 234 output tokens, USD 0.000504. No retry, no failed call, no billing pause. Claim released by the operator.
- Scientific conclusion: none about the table-versus-prose contrast (S1 did not run). The qualification result is a finding about the model configuration: see below.

## Every miss (rendered request and returned text read for all 24)

Every answer was the bare JSON object and nothing else (8 to 12 output tokens). Expected cost of checking is U, of exploring is e.

| Fixture | e (report wrong) | U (UNKNOWN cost) | Optimal | Chosen | Position of chosen cell |
|---|---:|---:|---|---|---|
| `qa-2808-e01-u65-prose` | 0.01 | 0.65 | explore | check | first listed |
| `qa-2810-e03-u70-prose` | 0.03 | 0.70 | explore | check | first listed |
| `qa-2809-e15-u85-table` | 0.15 | 0.85 | explore | check | second listed |
| `qa-2800-e90-u05-table` | 0.90 | 0.05 | check | explore | second listed |
| `qa-2801-e95-u15-table` | 0.95 | 0.15 | check | explore | first listed |
| `qa-2804-e99-u05-table` | 0.99 | 0.05 | check | explore | second listed |

The other 18 choices were optimal (prose: 4 of 6 explore cases and 6 of 6 check cases; table: 5 of 6 explore cases and 3 of 6 check cases). Each of the 6 missed fixtures was answered correctly in the other representation of the same layout and case (2808 and 2810 in the table; 2809, 2800, 2801 and 2804 in prose), so no layout is unreadable.

## Classification

- Not a format problem: 24 of 24 answers parsed, had exactly the key `inspect` and named an allowed cell.
- Not an instrument defect found: I re-read the two formats of two missed fixtures in full (`qa-2804-e99-u05-table`, `qa-2808-e01-u65-prose`). Each states the report's error probability, the cost of UNKNOWN, and the outcome, probability and cost of every affected cell under each action; the analytic optimum follows from two products (for 2804: checking costs 0.05, exploring costs 0.99). The margins of the missed fixtures are 0.64 to 0.94 expected-cost units.
- **Capability failure of this configuration**: with reasoning disabled and an answer of one key, the model has no place to compute the two expected costs and answers at once. Overall 18 of 24 optimal (75%) on choices where one action dominates by at least 0.60. The misses are not one constant habit (they fall on both actions and both list positions), which is what an unreliable single-step judgment looks like. Observed fact: the pattern of misses. Suspected cause: no working space. Not verified: nothing was run to test the cause.

## Issue ledger

| Id | Evidence | Kind | Cause confidence | Repair | Acceptance | Status |
|---|---|---|---|---|---|---|
| V-1 | 6 of 24 clear-dominance choices wrong, all structurally valid | capability / qualification failure | suspected (single-step answer with reasoning disabled) | proposed to dmarz/fleet-monitor: the one pre-registered bounded repair, attempt 002 on the second frozen fixture set, thresholds unchanged, same model | attempt 002's Q0 gate | open; nothing is built until the fleet monitor says go |

## Next action

`repair-and-rerun` at most once, as the program pre-registered (one bounded repair, repeat on disjoint fixtures, thresholds unchanged, no model change; a failed repeat ends the line). The proposal and its limits are recorded in the fleet monitor's thread and will be written into a new pre-run review if it is approved. Preserved: the three hub runs of this attempt, their records and the ledger.

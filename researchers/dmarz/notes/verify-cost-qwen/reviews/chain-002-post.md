# Post-mortem: chain-002 (verify-cost-qwen, program v5 line V, attempt 002: the one bounded repair)

Written 2026-10-04 by dmarz/pipeline from the run records ([records/attempt-002](../records/attempt-002/): chain status, stage summaries, every assignment, request and answer row of P0 and Q0), read after the chain stopped. Operator: dmarz/fleet-monitor, server sim-dmarz-13, run request agentops 272 (recorded there as attempt 002), launch commit `7e043086`, code commit `35404c24`, source hash `ef40246d…`. [Pre-run review](chain-002-pre.md). Same-researcher check only; not independently reviewed. Previous: [chain-001-post.md](chain-001-post.md).

## Outcome

- Execution: complete for the stages that ran, 12:30:17Z to 12:30:34Z. S0 144/144 scripted rows valid (run `05d5448d`). P0 1/1 passed its interface gate (run `0a09ff39`): 761 input and 36 output tokens, 0 reasoning tokens, finish reason `stop`, response model `qwen/qwen3.7-flash`, provider `Alibaba`, provider-reported cost USD 0.000028, 0.93 s, 0.34 tokens per request byte. Q0 23/23 calls valid (run `d45666da`).
- Qualification: **failed.** Gate: all 24 structurally valid and at least 11 of 12 optimal in each representation, over P0's row and Q0's 23. Observed: 24/24 valid; prose 6/12 optimal; table 4/12 optimal. Attempt 001 (answer-only, fixture set a): prose 10/12, table 8/12.
- The chain stopped at the gate by itself (`stopped_at_gate`, `gate_failed`). S1 was not queued. Actual: 24 calls, 24 transport attempts, 18,264 input and 914 output tokens, USD 0.000674. No retry, no failed call, no billing pause. Claim released by the operator.
- **As pre-registered, this failed repeat ends the Qwen route of this line.** No further attempt on `qwen/qwen3.7-flash` exists, thresholds were not lowered, and attempt 001 and attempt 002 are not pooled. No conclusion about the table-versus-prose contrast: S1 never ran on this model.
- First real use of the launcher's fresh-ledger declaration (`ledger: fresh`): setup ran 87 selftests with a matching source hash and the chain started with its own ledger on a fresh server, as reported by the operator.

## Every row (rendered request and returned object read for all 24)

All 24 answers were one bare JSON object with `cost_if_inspect` before `inspect`, both costs written as numbers, no extra key, no tolerated variant (33 to 50 output tokens). The analytic expected cost of checking (inspecting the reported cell) is U; of exploring (inspecting the cell without evidence) is e. "Written" is the model's cost for check / explore.

| Fixture | e | U | Optimal | Written check / explore | True check / explore | Written costs | Chosen | Choice is the smaller of its own two numbers | Result |
|---|---:|---:|---|---|---|---|---|---|---|
| `qb-2900-e92-u08-prose` | 0.92 | 0.08 | check | 0.92 / 0.08 | 0.08 / 0.92 | swapped | explore | yes | miss |
| `qb-2901-e97-u12-prose` | 0.97 | 0.12 | check | 0.12 / 0.97 | 0.12 / 0.97 | correct | check | yes | optimal |
| `qb-2902-e88-u22-prose` | 0.88 | 0.22 | check | 1.88 / 2.1 | 0.22 / 0.88 | other | check | yes | optimal |
| `qb-2903-e94-u28-prose` | 0.94 | 0.28 | check | 0.28 / 0.94 | 0.28 / 0.94 | correct | check | yes | optimal |
| `qb-2904-e98-u02-prose` | 0.98 | 0.02 | check | 0.98 / 0.02 | 0.02 / 0.98 | swapped | explore | yes | miss |
| `qb-2905-e75-u06-prose` | 0.75 | 0.06 | check | 0.06 / 0.75 | 0.06 / 0.75 | correct | check | yes | optimal |
| `qb-2906-e04-u92-prose` | 0.04 | 0.92 | explore | 0.04 / 0.92 | 0.92 / 0.04 | swapped | check | yes | miss |
| `qb-2907-e08-u82-prose` | 0.08 | 0.82 | explore | 0.08 / 0.82 | 0.82 / 0.08 | swapped | check | yes | miss |
| `qb-2908-e02-u68-prose` | 0.02 | 0.68 | explore | 0.02 / 0.68 | 0.68 / 0.02 | swapped | check | yes | miss |
| `qb-2909-e12-u88-prose` | 0.12 | 0.88 | explore | 0.88 / 0.12 | 0.88 / 0.12 | correct | explore | yes | optimal |
| `qb-2910-e06-u72-prose` | 0.06 | 0.72 | explore | 0.06 / 0.72 | 0.72 / 0.06 | swapped | check | yes | miss |
| `qb-2911-e07-u97-prose` | 0.07 | 0.97 | explore | 0.97 / 0.07 | 0.97 / 0.07 | correct | explore | yes | optimal |
| `qb-2900-e92-u08-table` | 0.92 | 0.08 | check | 0.92 / 0 | 0.08 / 0.92 | swapped, smaller value written as 0 | explore | yes | miss |
| `qb-2901-e97-u12-table` | 0.97 | 0.12 | check | 0.12 / 0.97 | 0.12 / 0.97 | correct | check | yes | optimal |
| `qb-2902-e88-u22-table` | 0.88 | 0.22 | check | 0.22 / 0.88 | 0.22 / 0.88 | correct | check | yes | optimal |
| `qb-2903-e94-u28-table` | 0.94 | 0.28 | check | 0.94 / 0.28 | 0.28 / 0.94 | swapped | check | no | optimal |
| `qb-2904-e98-u02-table` | 0.98 | 0.02 | check | 0.98 / 0 | 0.02 / 0.98 | swapped, smaller value written as 0 | explore | yes | miss |
| `qb-2905-e75-u06-table` | 0.75 | 0.06 | check | 0.75 / 0.06 | 0.06 / 0.75 | swapped | explore | yes | miss |
| `qb-2906-e04-u92-table` | 0.04 | 0.92 | explore | 0.04 / 0.92 | 0.92 / 0.04 | swapped | check | yes | miss |
| `qb-2907-e08-u82-table` | 0.08 | 0.82 | explore | 0.08 / 0.82 | 0.82 / 0.08 | swapped | check | yes | miss |
| `qb-2908-e02-u68-table` | 0.02 | 0.68 | explore | 0 / 0.68 | 0.68 / 0.02 | swapped, smaller value written as 0 | check | yes | miss |
| `qb-2909-e12-u88-table` | 0.12 | 0.88 | explore | 0 / 0.88 | 0.88 / 0.12 | swapped, smaller value written as 0 | check | yes | miss |
| `qb-2910-e06-u72-table` | 0.06 | 0.72 | explore | 0.72 / 0.06 | 0.72 / 0.06 | correct | explore | yes | optimal |
| `qb-2911-e07-u97-table` | 0.07 | 0.97 | explore | 0.07 / 0.97 | 0.97 / 0.07 | swapped | check | yes | miss |

Counts over the 24 rows (recomputed from the rows; they agree with `summary.json` `work`, which covers Q0's 23 rows, plus P0's row):

- Both costs correct within 0.005: **8 of 24** (prose 5, table 3). All 8 choices optimal.
- Costs exactly swapped (the number written for checking is e and the number written for exploring is U): **11 of 24** (prose 6, table 5).
- Swapped with the smaller value written as 0: **4 of 24** (all table).
- Other: 1 (`qb-2902-e88-u22-prose`: 1.88 and 2.1, neither a cost of this task, but in the right order).
- So the written arithmetic is wrong in **16 of 24** rows, and in 15 of those 16 the larger number sits on the wrong action.
- The choice is the action with the smaller of the model's own two numbers in **23 of 24** rows. The one contradiction (`qb-2903-e94-u28-table`: swapped costs, then the action its own numbers say is dearer) is counted optimal.
- All 14 misses have swapped costs (10 exact, 4 with a zero) and follow the model's own numbers. The 10 optimal rows are the 8 with correct costs, the one with wrong numbers in the right order, and the one contradiction.
- Misses fall on both actions (5 where checking is optimal, 9 where exploring is optimal) and both list positions (6 with the chosen cell listed first, 8 second).

## What the rows show

- **Asking this model to write its expected costs made its choices worse, not better.** 10 of 24 optimal with the written costs against 18 of 24 without them. The two attempts used different fixture sets of the same construction (set a and set b: twelve layouts each, six check-optimal and six explore-optimal cases, margin at least 0.60), so this is a comparison of two batches of 24, not a paired one; as a description, a difference this large between two batches of 24 would be unusual if the two configurations were equally good (Fisher exact, two-sided, p = 0.04, computed after the fact and not pre-registered).
- **The failure is in forming the numbers, not in comparing them.** The model compares its two numbers correctly almost every time (23 of 24) and picks the smaller. In 15 of 24 rows the numbers are attached to the wrong action: under each cell it wrote the cost that the request attaches to that cell when it is left uninspected (e for the reported cell, U for the cell without evidence), which is the cost of the other action. Choosing the smaller of those selects the dearer action, so a model that did this in every row and followed its numbers would score 0 of 24; the 8 rows with correct costs are the ones where it attached the numbers to the actions.
- The working fields did what they were built for: they show where the one-step answer goes wrong. In attempt 001 the same error could not be seen, only its effect on 6 of 24 choices.

## Classification

- Not a format problem: 24 of 24 valid, no tolerated variant needed.
- Instrument: I re-read the system message and the two representations of two missed fixtures in full (`qb-2900-e92-u08-prose`, `qb-2908-e02-u68-table`). The instruction asks for "the expected total cost of the final map for each of the two allowed actions"; CONSEQUENCES lists, per action, every affected cell with its probability and cost, so each cost is one product read from the lines of that action. I found no error in the request. One alternative explanation is not excluded: the answer key `cost_if_inspect` with cell names as sub-keys may invite writing "the cost of this cell" under each cell name; a format keyed by action, or one that asks for the cost in words per action, might behave differently. That was not tested and, for this model, will not be: the pre-registration allows no further repair.
- **Capability failure of this configuration, now located**: with reasoning disabled, `qwen/qwen3.7-flash` attaches each risk to the cell it describes instead of to the action that incurs it, in 15 of 24 one-step answers. Observed fact: the swapped numbers. Suspected cause: no reasoning step between reading the consequences and writing the numbers. Not verified.

## Issue ledger

| Id | Evidence | Kind | Cause confidence | Repair | Acceptance | Status |
|---|---|---|---|---|---|---|
| V-1 (from chain-001) | attempt 001: 6 of 24 clear-dominance choices wrong | capability / qualification failure | suspected | attempt 002: write the two costs before choosing | attempt 002's Q0 gate | **closed, repair failed**: 14 of 24 wrong; the Qwen route ends |
| V-2 | 15 of 24 answers attach each cost to the wrong action; 23 of 24 choices follow the model's own numbers | capability of the no-reasoning configuration; an effect of the answer key's shape is not excluded | observed pattern, cause suspected | none on this model (no repair remains) | — | recorded as the result |
| V-3 | the launcher refused a repaired attempt on a fresh server (`missing_prior_ledger`) before launch | launcher gap, found in review | verified | `ledger: fresh` declaration (agentops `7560167`, contract paragraph in READY-CHAIN.md) | this launch started with its own ledger | closed |

## Next action

- `qwen/qwen3.7-flash`: none. The line's result for this model is two failed qualifications, reported side by side and never pooled: answer-only 18 of 24 optimal (set a), costs-then-choice 10 of 24 optimal (set b).
- A second pre-registered model, `gpt-6-luna` through the OpenAI API with `reasoning_effort: low`, runs the original attempt-001 instrument (answer `{"inspect": "<cell>"}` only) as its own chain 003 with its own ledger, probe, qualification and review. It was pre-registered at `1790b88c` before this result was known; dmarz/fleet-monitor decided at 12:38Z, after this result was known, that its qualification uses fixture set a instead of set b, so that its 24 qualification requests are byte-identical to the ones Qwen answered in attempt 001; the preregistration is to record that as a dated amendment before any run on that model. It is a different actor configuration and is compared with the Qwen attempts descriptively only.
- Preserved: the three hub runs of this attempt, their records in [records/attempt-002](../records/attempt-002/), and the ledger totals in `chain-status.json`.

# Results: verify-cost-qwen (research program v5, line V)

Written 2026-10-04 by dmarz/pipeline-verify from the saved run records. Exploratory. Operated by dmarz/fleet-monitor through the private launcher; cross-researcher review waived by dmarz; dmarz/fleet-monitor's check is a same-researcher check; nothing here is independently reviewed or replicated. Every number below was recomputed from the saved rows ([records](records/README.md), [records/chain-003](records/chain-003/README.md)); the three chains are separate records and are never pooled.

## What ran

| Chain | Model and setting | Answer the model returns | Qualification set | Qualification (24 valid of 24 in all three) | Main stage | Calls | Dollars |
|---|---|---|---|---|---|---:|---:|
| Attempt 001 | `qwen/qwen3.7-flash`, reasoning disabled | `{"inspect": "<cell>"}` | a | prose 10 of 12, table 8 of 12 optimal: **failed** (needs 11 of 12 each) | not run | 24 | 0.000504 |
| Attempt 002 (the one pre-registered repair) | `qwen/qwen3.7-flash`, reasoning disabled | the expected cost of each action, then `inspect` | b | prose 6 of 12, table 4 of 12: **failed**; the Qwen route ended | not run | 24 | 0.000674 |
| Chain 003 (second pre-registered model) | `gpt-6-luna`, `reasoning_effort: low` | `{"inspect": "<cell>"}`, the attempt-001 instrument byte for byte | a (the same 24 requests as attempt 001) | prose 12 of 12, table 12 of 12: **passed** | 576 of 576 valid, 0 failed | 600 | 0.061279 |

Post-mortems: [chain-001-post.md](reviews/chain-001-post.md), [chain-002-post.md](reviews/chain-002-post.md), [chain-003-post.md](reviews/chain-003-post.md).

## The question the study could answer, and the one it could not

The primary question was whether a structured action-consequence table changes an agent's one-step choice between checking a report and exploring an unexamined cell, relative to explicit prose with the same objective, facts and consequences.

- For `qwen/qwen3.7-flash` it was never measured: the model did not qualify in either answer configuration, so its main stage did not run.
- For `gpt-6-luna` it was measured and the answer is **no measurable difference, at ceiling**: 288 of 288 optimal choices with the prose, 287 of 288 with the table. The pre-registration named this outcome in advance as a ceiling, not as evidence that the two renderings are equivalent for models in general.

## Primary measure (chain 003, gpt-6-luna)

Per layout, the mean over the twelve cases of expected regret with the table minus expected regret with the prose. 24 layouts, all complete (24 of 24 units valid in each).

- 23 layouts: exactly 0. One layout (3018): +0.0208 (one miss, regret 0.25, divided by twelve cases).
- Mean **+0.00087** expected-loss units per decision (the table arm is worse by one choice in 288). Standard error 0.00087; descriptive 95% t interval over layouts **−0.00093 to +0.00266**; range 0 to +0.0208; leave-one-layout-out range 0 to +0.00091. With 23 values at exactly zero the t interval is a formality: it describes one miss.
- The pre-registered practical marker was 0.03 and the predicted direction negative. Observed: 35 times smaller than the marker, and positive. No missing unit, so the bounds over all assigned layouts equal the estimate.
- The design could show a contrast as large as ±0.3208. The model left it no room: mean regret 0.0000 with the prose and 0.0009 with the table, against 0.1500 for always-check and 0.1708 for always-explore.

## All twelve strata (chain 003)

Expected regret per decision; 24 layouts per cell. "Always check" and "always explore" are the offline comparators: the regret of that constant policy in the case.

| e | U | Optimal action | Prose: optimal of 24 | Prose: mean regret | Table: optimal of 24 | Table: mean regret | Table minus prose | Always check | Always explore |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 0.05 | 0.10 | explore | 24 | 0.0000 | 24 | 0.0000 | +0.0000 | 0.05 | 0.00 |
| 0.05 | 0.25 | explore | 24 | 0.0000 | 24 | 0.0000 | +0.0000 | 0.20 | 0.00 |
| 0.05 | 0.75 | explore | 24 | 0.0000 | 24 | 0.0000 | +0.0000 | 0.70 | 0.00 |
| 0.20 | 0.10 | check | 24 | 0.0000 | 24 | 0.0000 | +0.0000 | 0.00 | 0.10 |
| 0.20 | 0.25 | explore | 24 | 0.0000 | 24 | 0.0000 | +0.0000 | 0.05 | 0.00 |
| 0.20 | 0.75 | explore | 24 | 0.0000 | 24 | 0.0000 | +0.0000 | 0.55 | 0.00 |
| 0.50 | 0.10 | check | 24 | 0.0000 | 24 | 0.0000 | +0.0000 | 0.00 | 0.40 |
| 0.50 | 0.25 | check | 24 | 0.0000 | 24 | 0.0000 | +0.0000 | 0.00 | 0.25 |
| 0.50 | 0.75 | explore | 24 | 0.0000 | 23 | 0.0104 | +0.0104 | 0.25 | 0.00 |
| 0.80 | 0.10 | check | 24 | 0.0000 | 24 | 0.0000 | +0.0000 | 0.00 | 0.70 |
| 0.80 | 0.25 | check | 24 | 0.0000 | 24 | 0.0000 | +0.0000 | 0.00 | 0.55 |
| 0.80 | 0.75 | check | 24 | 0.0000 | 24 | 0.0000 | +0.0000 | 0.00 | 0.05 |
| all | | | 288 of 288 | 0.0000 | 287 of 288 | 0.0009 | +0.0009 | 0.1500 | 0.1708 |

- The only miss: `m-3018-e50-u75-table` (e 0.50, U 0.75, exploring optimal by 0.25): the model inspected the reported cell, which was listed first in that layout.
- Reliable-source strata (e ≤ 0.20, six cases): 24 of 24 optimal in every cell of both renderings. No regression of the table against the prose; the pre-registered flag (a drop of 3 or more of 24) is not raised anywhere.
- The two cells that correspond to PC5's conditions (e 0.20 and e 0.80 at U 0.25): 24 of 24 in both renderings. PC5 reported 21 of 32 and 24 of 32 optimal with its explicit prose contract on a different model (`typesafe/jev-1.13`); that is a descriptive reference, not a comparison.
- Position: the first-listed cell was chosen in 144 of 288 prose answers and 145 of 288 table answers, which is what the balanced design gives a policy that ignores position.
- Realized scripted loss (secondary, under each layout's seeded truth draw): 0.2090 with the prose and 0.2082 with the table.

## The three-way picture on qualification

Twelve clear-dominance choices (one action better by at least 0.60 in expected loss) in each of two renderings; both actions legal.

| Configuration | Set | Prose | Table | Total |
|---|---|---:|---:|---:|
| Qwen, answer only, reasoning disabled (attempt 001) | a | 10 of 12 | 8 of 12 | 18 of 24 |
| Qwen, writes both expected costs first, reasoning disabled (attempt 002) | b | 6 of 12 | 4 of 12 | 10 of 24 |
| gpt-6-luna, answer only, `reasoning_effort: low` (chain 003) | a | 12 of 12 | 12 of 12 | 24 of 24 |

- Rows one and three are answers to the same 24 requests: the request hashes of chain 003's P0 and Q0 equal those of attempt 001 (checked from the saved rows, and proved in the selftest against attempt 001's manifest). Fixture by fixture:

| Fixture | e | U | Optimal | gpt-6-luna (chain 003) | Qwen (attempt 001) |
|---|---:|---:|---|---|---|
| `qa-2800-e90-u05-prose` | 0.90 | 0.05 | check | check | check |
| `qa-2801-e95-u15-prose` | 0.95 | 0.15 | check | check | check |
| `qa-2802-e85-u20-prose` | 0.85 | 0.20 | check | check | check |
| `qa-2803-e90-u30-prose` | 0.90 | 0.30 | check | check | check |
| `qa-2804-e99-u05-prose` | 0.99 | 0.05 | check | check | check |
| `qa-2805-e70-u05-prose` | 0.70 | 0.05 | check | check | check |
| `qa-2806-e02-u90-prose` | 0.02 | 0.90 | explore | explore | explore |
| `qa-2807-e10-u80-prose` | 0.10 | 0.80 | explore | explore | explore |
| `qa-2808-e01-u65-prose` | 0.01 | 0.65 | explore | explore | check (miss) |
| `qa-2809-e15-u85-prose` | 0.15 | 0.85 | explore | explore | explore |
| `qa-2810-e03-u70-prose` | 0.03 | 0.70 | explore | explore | check (miss) |
| `qa-2811-e10-u95-prose` | 0.10 | 0.95 | explore | explore | explore |
| `qa-2800-e90-u05-table` | 0.90 | 0.05 | check | check | explore (miss) |
| `qa-2801-e95-u15-table` | 0.95 | 0.15 | check | check | explore (miss) |
| `qa-2802-e85-u20-table` | 0.85 | 0.20 | check | check | check |
| `qa-2803-e90-u30-table` | 0.90 | 0.30 | check | check | check |
| `qa-2804-e99-u05-table` | 0.99 | 0.05 | check | check | explore (miss) |
| `qa-2805-e70-u05-table` | 0.70 | 0.05 | check | check | check |
| `qa-2806-e02-u90-table` | 0.02 | 0.90 | explore | explore | explore |
| `qa-2807-e10-u80-table` | 0.10 | 0.80 | explore | explore | explore |
| `qa-2808-e01-u65-table` | 0.01 | 0.65 | explore | explore | explore |
| `qa-2809-e15-u85-table` | 0.15 | 0.85 | explore | explore | check (miss) |
| `qa-2810-e03-u70-table` | 0.03 | 0.70 | explore | explore | explore |
| `qa-2811-e10-u95-table` | 0.10 | 0.95 | explore | explore | explore |

- gpt-6-luna answered correctly all six fixtures that Qwen missed, and all eighteen that Qwen got right.
- Row two is on other fixtures and another answer format. Its post-mortem found that in 15 of 24 answers Qwen wrote each cost under the wrong action and then followed its own numbers; asking that model to write intermediate values made it worse, not better.
- What the three rows do not separate: rows one and three differ in model, provider and reasoning setting at once (`gpt-6-luna` used a mean of 57 reasoning tokens per call, between 0 and 146; Qwen ran with reasoning disabled). The observation is that this instrument is passable as written; why one configuration passes and the other does not is not identified.

## The reading the program left open

The program asked that both renderings carry "the same objective, facts and full action consequences". This package read that as: for each action, the outcome, probability and cost of every affected cell, and **not** the expected loss of the action. Neither rendering prints an expected loss, a comparison or a recommendation; the agent has to form e × 1 and compare it with U itself. All results above hold under that reading. If the expected loss of each action had been printed, the task would have been a comparison of two printed numbers; that variant was not run, and nothing here says how either model would behave on it.

## What can and cannot be said

- Observed: `gpt-6-luna` at low reasoning effort chooses the minimum-loss action in 575 of 576 one-step decisions across twelve risk and cost cases in which the best action changes, in both renderings. Always-check and always-explore would each be wrong in half the cases.
- Observed: `qwen/qwen3.7-flash` with reasoning disabled fails clear-dominance versions of the same decision in two answer configurations (18 of 24 and 10 of 24).
- Not supported: any effect of a table over prose. Where it could be measured, both arms were at ceiling. For a model that struggles, the comparison was never made.
- Not supported: any claim about multi-step sensing, learned source reliability or a group of agents. This is a one-step policy assay with stated calibrated probabilities and scripted consequences, on 24 synthetic layouts that randomize coordinates, labels and listing order within twelve authored cases.
- Units: 24 layouts are the independent units of the primary; 576 calls are not 576 independent tasks.

## Execution and cost (chain 003)

600 calls, 600 transport attempts, 0 failed, 0 retries, 0 billing pauses. 378,900 input tokens (630 to 633 per call), 46,354 output tokens, of which 34,366 reasoning tokens. USD 0.061279 computed from usage at the pinned prices (cap USD 5); S1 alone USD 0.058810. Wall time 4 min 21 s for the chain (S1 3 min 56 s, mean 1.53 s per call, four in flight). The whole line (three chains): 648 calls, USD 0.0625.

## Verification of the records

`chain.py verify` through the launcher returned exit 1 with `chain_status_is_for_another_model`. That is not a discrepancy in the data: the launcher ran `status` and `verify` without `STUDY_MODEL`, the code then selected the first model of its ladder (Qwen), and the verify step refuses a chain status written for another model before it checks anything. Run offline on the saved records with the model set, every check that needs no hub passes for all four stages: every unit has one row, requests regenerate to their recorded hashes and to the committed manifest, every saved answer re-validates and regrades to the saved evaluation, the analysis, totals, gates and pass flags recompute to the saved values, call caps respected ([offline-verify.json](records/chain-003/offline-verify.json)). The four hub comparisons (artifact checksums and metrics on the hub) were not re-run and remain unchecked. An independent recomputation from the request texts and returned answers, without the study's scorer, gives the same grades, strata and primary ([recompute.json](records/chain-003/recompute.json)).

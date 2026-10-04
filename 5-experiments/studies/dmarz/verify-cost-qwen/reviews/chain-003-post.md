# Post-mortem: chain 003 (verify-cost-qwen on gpt-6-luna, the second pre-registered model)

Written 2026-10-04 by dmarz/pipeline-verify (the builder of the package) from the run records delivered by the operator: [records/chain-003](../records/chain-003/README.md) (chain status, the summary, analysis, failure report, assignments, requests and rows of all four stages, the ledger, the launcher's `status` and `verify` outputs). Operator: dmarz/fleet-monitor, server sim-dmarz-9, launch commit `61a7269f`, code commit `c74da5bc`, source hash `b1b15d25…`. [Pre-run review](chain-003-pre.md). Same-researcher check only; not independently reviewed. Previous: [chain-001-post.md](chain-001-post.md), [chain-002-post.md](chain-002-post.md). Results in full: [RESULTS.md](../RESULTS.md).

## Outcome

- Execution: complete, 17:40:21Z to 17:44:42Z. All four stages `done`, chain state `completed`, exit 0 as recorded in the chain status. The launcher's setup ran 123 selftests on the server with a matching source hash (operator's report).
- Qualification: **passed.** 24 of 24 valid; 12 of 12 optimal with the prose and 12 of 12 with the table, on the same 24 set-a requests on which Qwen scored 10 and 8 in attempt 001.
- Main stage: 576 of 576 valid, 0 failed, 0 not started. 575 of 576 choices optimal.
- Primary (per-layout mean table-minus-prose expected regret, 24 complete layouts): **+0.00087**, descriptive 95% t interval −0.00093 to +0.00266; 23 layouts at exactly 0 and one at +0.0208. Mean regret 0.0000 with the prose and 0.0009 with the table. Both renderings are at ceiling for this model; the pre-registration named that outcome in advance.
- Scientific status: a valid, completed result with no measurable contrast. It is a ceiling, not evidence of equivalence for other models, and not a failure to repair.

## Reconcile the recorded facts

| Quantity | Assigned or planned | Observed | Missing, partial or uncertain | Evidence |
|---|---|---|---|---|
| Independent layouts and paired arms | 24 layouts × 12 cases × 2 renderings | 24 complete layouts, 576 units | none | `results/…80380bb4…/episodes.jsonl.gz`, `recompute.json` |
| Started / terminal / graded / analyzed units | S0 144, P0 1, Q0 23, S1 576 | 144 / 1 / 23 / 576 in each column | none | stage summaries; `offline-verify.json` (`every_unit_has_one_row`) |
| Model calls, including retries | caps 1 / 23 / 576, 600 total, 760 transport attempts | 1 / 23 / 576 calls, 600 transport attempts, 0 re-sends, 0 billing pauses, 0 voided reservations | none | ledger: 600 reservations, 600 attempts, 600 responses |
| Tokens | not capped per call beyond 8,000 in and 1,500 out | 378,900 input (630 to 633 per call), 46,354 output of which 34,366 reasoning (0 to 146 per call), 0 cached | none | rows' accounting; ledger totals agree |
| Spend | cap USD 5 | USD 0.061279 computed from usage at the pinned prices (P0 0.000099, Q0 0.002370, S1 0.058810); no open reservation left | the provider reports no cost; this is the adapter's computation | ledger `actual_usd`, stage summaries |
| Wall time and concurrency | 4 in flight; chain timeout 7,200 s | 4 min 21 s for the chain; S1 3 min 56 s; mean 1.53 s per call, longest 3.56 s | none | chain status timestamps; rows' `latency_seconds` |
| Projection gates before S1 | cost and input ceiling | projected USD 0.0594 against USD 4.9975 remaining; 632 projected input tokens against 8,000 | none | chain status `projection` |

Pre-run estimates against actuals: cost predicted USD 0.06 to 0.16, observed 0.061; S1 time predicted 2.5 to 12 minutes, observed 3.9; reasoning tokens assumed 50 to 400 per call, observed mean 57.

## The launcher's `verify` exit 1: not a discrepancy

Saved output: `{"ok": false, "reason": "chain_status_is_for_another_model"}`.

- Cause, read from the saved outputs and the code: the launcher's `status` and `verify` actions ran `chain.py` without `STUDY_MODEL` in the environment. The saved `status` output shows it: its top-level `model` is `qwen/qwen3.7-flash` and its ledger line shows `cap_usd: 2`, while the chain status inside it says `model: gpt-6-luna`. With no `STUDY_MODEL` the code selects the first model of its frozen ladder (Qwen). `chain.py verify` then meets a chain status written for `gpt-6-luna` and refuses before checking anything. That refusal is the guard added in this package so that one model's records are never verified against another model's manifest.
- So the exit 1 is a check that was run for the wrong model, not a failed check. The chain itself ran with the right model: its batches, hub params, adapter, prices and cap (the ledger was opened with USD 5 during the run) are all gpt-6-luna's.
- What was verified instead, offline, on the delivered records with the model set ([offline_verify.py](../records/chain-003/offline_verify.py), [offline-verify.json](../records/chain-003/offline-verify.json)): for S0, P0, Q0 and S1, every check of `chain.py verify` that needs no hub passes: one row per unit; assignments and requests regenerate to the recorded hashes; the stage digests equal the committed manifest (which for this chain equals attempt 001's manifest); every saved answer re-validates from the object as returned and regrades to the saved evaluation; analysis, totals, gate and pass flag recompute to the saved values; source hash current; call caps respected; for S1 every unit exactly once and no unit answered twice.
- What remains unchecked: the four comparisons against the hub (run status, artifact list, artifact checksums, hub metrics). They need the hub and were not re-run. Running the launcher's `verify` with `STUDY_MODEL=gpt-6-luna` in the environment would cover them.
- Defect to fix (owner: builder for the code, the launcher's owner for the launcher): either the launcher passes `STUDY_MODEL` to `status` and `verify` as it does to `chain`, or `chain.py status` and `verify` take the model from the chain status file instead of the environment. The second is the smaller change and is the right behaviour for read-only commands; it changes the source hash, so it belongs to a later revision, not to this run.

## Native trace audit

| Artifact | Expected units | Retained / inspected | Missing or excluded and why |
|---|---|---|---|
| Requests (system and user text) | 144 + 1 + 23 + 576 | all retained; hashes regenerate; P0 and Q0 hashes equal attempt 001's saved rows (24 of 24) | none |
| Returned answer and parsed action | 600 | all retained as returned; every one is the bare object `{"inspect": "r,c"}` (18 characters); no tolerated variant was needed (0 extra keys, 0 respaced) | none |
| Independent grade | 600 | recomputed from request text and answer without the study's scorer: identical to the saved grades | none |
| Transport, usage, terminal receipt | 600 | response model `gpt-6-luna` and finish reason `stop` on every call; usage on every call | frames and replay GIF were not in the delivered archive; the chain log was not copied |

The one miss, read in full: `m-3018-e50-u75-table`. Report wrong with probability 0.50, UNKNOWN costs 0.75; exploring costs 0.50 in expectation and checking 0.75. The model inspected the reported cell (listed first in that layout). The same layout and case in prose was answered correctly, and the other 23 layouts answered this case correctly in the table. Margin 0.25: not the smallest margin of the grid (four cases have 0.05 or 0.10 and were all answered correctly). One event; no pattern can be read from it.

## Interpret the result

- The instrument is passable as written: a model with a small reasoning allowance reads either rendering and compares e with U correctly in 599 of 600 paid decisions (24 qualification, 576 main, one miss).
- The table-versus-prose question has no answer from this line. Where the comparison ran, both arms were at ceiling (the pre-registration's "uninformative about the contrast" case); where a model struggled (Qwen with reasoning disabled), it did not qualify and the comparison was not run. The design did not include a difficulty dial that would have put a qualified model between floor and ceiling (lessons item 9); that is the main design limit.
- Across the line: Qwen answer-only 18 of 24 on qualification, Qwen with written costs 10 of 24, gpt-6-luna 24 of 24 on the same requests as the first. The first and third differ in model, provider and reasoning setting together.
- Reading left open by the program, and used here: both renderings give the outcome, probability and cost of each affected cell per action, without the expected loss of the action. The variant that prints the expected loss was not run.

## Assess experiment quality

| Dimension | Status | Finding and evidence | Next action |
|---|---|---|---|
| question | met in part | one-step decision assay as specified; the format contrast is unanswered | a harder variant if the question is kept |
| scenarios | limited | twelve authored cases, 24 synthetic layouts; clear arithmetic, no noise | cases with smaller margins or more cells at risk |
| controls | good | analytic optimum, always-check, always-explore, position balance; equal information proved for every request | none |
| capability | qualified (gpt-6-luna); failed twice (Qwen) | 24 of 24; 18 of 24; 10 of 24 | none |
| measurement | sound, at ceiling | 575 of 576 optimal; contrast +0.00087 | difficulty dial |
| sample_size | as planned | 24 layouts; interval is descriptive and reflects one miss | none |
| agent_context | clean | stateless calls; no truth, seed or optimum in any request (checked in S0) | none |
| data_integrity | good, hub comparisons unchecked | offline verify passes; independent recomputation agrees | rerun `verify` with the model set |
| resources | far inside caps | 600 calls, USD 0.061 of 5 | none |
| reproducibility | good | pinned commit, source hash, manifest, saved requests and rows, two scripts | none |
| visualization | not retained | frames were produced on the server (no reporting error in the summaries) but were not in the delivered archive | rebuild from the rows if wanted |

## Resolve issues and prior suggestions

| Issue | Decision | Evidence | Status |
|---|---|---|---|
| V-1, V-2 (Qwen fails clear-dominance choices; writes costs under the wrong action) | recorded as results of attempts 001 and 002; the Qwen route ended as pre-registered | chain-001 and chain-002 post-mortems | closed |
| V-4: is the instrument itself at fault? | no: a second model passes it unchanged, 24 of 24 on the identical requests | this run | closed |
| V-5: `status` and `verify` select the model from the environment | take the model from the chain status file, or have the launcher pass `STUDY_MODEL` | saved launcher outputs | open; does not affect the result |
| V-6: both arms at ceiling for the qualified model | reported as the result; no rerun to obtain an effect | RESULTS.md | closed for this run |
| Concern before the run: reasoning tokens could exhaust the 1,500-token allowance | did not happen: at most 146 reasoning tokens in a call | rows | closed |

## Closeout and handoff

- Decision: **complete_valid_result** for chain 003. The line is closed: no further attempt is pre-registered on either model, thresholds were never changed, nothing was rerun, and the three chains are not pooled.
- If the question is taken up again it needs a new plan, not a rerun: a version of the decision in which a qualified model is not at ceiling (several reports and several unknown cells with one inspection, smaller margins, or probabilities that must be combined), with the same equal-information discipline, and a qualification that screens for competence without guaranteeing a ceiling.
- Records: [records/chain-003](../records/chain-003/README.md), scanned before committing (no credential, header, hub or server address). Server and claim: released by the operator (operator's statement; not checked by the builder).

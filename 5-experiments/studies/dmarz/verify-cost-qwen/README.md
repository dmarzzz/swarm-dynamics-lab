# When is verification worth its cost? (program v5 line V, Qwen3.7 Flash)

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/pipeline-verify; source `9781739c` ([registry](../../../evidence-metadata.json), [rubric](../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — In a one-step choice between checking a report and exploring an unknown cell, with the outcome, probability and cost of each action stated and no expected loss printed, gpt-6-luna at low reasoning effort chooses the minimum-loss action in both an explicit-prose and an action-consequence-table rendering (575 of 576), so the table-minus-prose expected regret is +0.00087 (95% interval -0.00093 to +0.00266): no measurable effect of the table, at ceiling. Basis: Exploratory. The format contrast was measurable only where both arms were at ceiling, so it does not show whether a table helps a model that struggles; qwen3.7-flash with reasoning disabled failed qualification twice (18 of 24 and 10 of 24 optimal) and its comparison never ran. One model in the main stage, twelve authored cases on synthetic layouts, scripted consequences; the three chains differ in model, provider and reasoning setting and are not pooled. Builder's own assessment; hub comparisons of verify not re-run; not independently reviewed or replicated.
- **sample_size_summary:** Observed: 24 paired synthetic layouts × 12 authored cases × 2 renderings = 576/576 valid gpt-6-luna choices, 0 failed; separate qualification 24/24 valid and optimal. Qwen3.7 Flash: two qualification-only attempts, 24/24 valid each, 18 and 10 optimal, main stage not run. Layouts are the units, not calls.
<!-- experiment-evidence:end -->

**Status, 2026-10-04: the line has run and is closed.** Results: [RESULTS.md](RESULTS.md). Three separate chains, never pooled. (1) `qwen/qwen3.7-flash`, reasoning disabled, answer `{"inspect": "<cell>"}`: stopped at the qualification gate, 10 of 12 optimal with the prose and 8 of 12 with the table (threshold 11 of 12 each; [post-mortem](reviews/chain-001-post.md)). (2) The one pre-registered repair, the same model writing the expected cost of each action before choosing: stopped at the gate again, 6 of 12 and 4 of 12 ([post-mortem](reviews/chain-002-post.md)); that ended the Qwen route. (3) `gpt-6-luna` at `reasoning_effort: low` on the original instrument, byte for byte, qualifying on the same 24 requests as (1): 12 of 12 and 12 of 12, then the main stage 576 of 576 valid with 575 optimal choices ([post-mortem](reviews/chain-003-post.md)). Primary, per-layout mean table-minus-prose expected regret over 24 layouts: +0.00087 (descriptive 95% interval −0.00093 to +0.00266): both renderings are at ceiling for that model, so the study shows no measurable effect of the table and cannot say whether one exists for a model that struggles. 648 calls and USD 0.0625 in total. The sections below are the prospective plan as written before the runs. Exploratory; owner dmarz; built by dmarz/pipeline-verify; not independently reviewed.

It implements line V of research program v5 ("When is verification worth its cost?") as a [ready-chain](../pipeline/READY-CHAIN.md) package. The program's files are in [`../overnight-program-2026-10-04/`](../overnight-program-2026-10-04/) ([program.json](../overnight-program-2026-10-04/program.json), [SETUP.md](../overnight-program-2026-10-04/SETUP.md), [selected-model.json](../overnight-program-2026-10-04/selected-model.json)).

Authority and review status, recorded 2026-10-04 as relayed to this builder by dmarz/pipeline: dmarz directed this program himself (research program v5, written with him by a Codex session on 2026-10-04; his instruction to ship it was relayed by dmarz/fleet-monitor). The design is the program's; this package implements line V as specified there. Cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check and nothing more; the run is not independently reviewed. The run is launched only by the orchestrator from the private run queue. S2 is disabled. It is not an accepted hypothesis and makes no novelty claim.

Implementation note, 2026-10-04: the program describes five sessions and one shared reservation authority. That arrangement is replaced by the ready-chain: one package per line, one server per line, its own ledger and caps. The program's design for this line (sample, cases, representations, primary measure, qualification thresholds, call counts) is unchanged.

Source instrument: Vishesh's phantom-coast PC5 study, [`5-experiments/studies/vishesh/phantom-coast/pc5/`](../../vishesh/phantom-coast/pc5/README.md), copied at commit `61307ac19d9af2d8119736f9886e85683ce7e21d` (`src/contract.py`, `src/design.py`, `src/engine.py`). The copy in `src/` is dmarz-owned and parameterized; nothing in `lab/researchers/vishesh/` was edited, moved or run. PC5's own [next-iteration note](../../vishesh/phantom-coast/pc5/NEXT-ITERATION.md) proposed this threshold study and did not start it.

## TLDR

An agent has one inspection left. It can check a report that may be wrong, or explore a cell nobody has looked at. Checking is worth it only when the report's error probability is larger than the cost of leaving the other cell UNKNOWN. PC5 found that stating the scoring rule improved the average choice but made choices worse when the report was reliable (28 of 32 optimal fell to 21 of 32). This study asks whether the form of the same information matters: explicit prose against a structured action-consequence table, across twelve cases in which the better action changes. 24 layouts × 12 cases × 2 representations = 576 calls to `qwen/qwen3.7-flash`, one stateless call each. The measure is expected regret against the analytic minimum-loss action. This is a one-step policy assay. It is not learned multi-step sensing and it does not claim that typography repairs a live swarm.

## Question and prediction

Can an agent choose checking versus exploration when the optimal action changes with report reliability and the cost of leaving territory unknown, and does a structured action-consequence table change the choice relative to explicit prose carrying the same objective, facts and consequences?

Primary measure: for each layout, the mean over the twelve cases of expected regret with the table minus expected regret with the prose. That gives 24 paired layout-level values. Prediction, written before any outcome exists: the mean is negative (the table lowers regret). Practical marker: 0.03 expected-loss units per decision. The largest difference the design can show is 0.3208 (the mean of |e − U| over the twelve cases). A difference near zero, or a positive one, is a valid result and triggers no tuning and no rerun.

Anchors from PC5, measured on a different model (`typesafe/jev-1.13`) with a prose contract and 32 layouts; none is an outcome of this study: at report reliability 0.8 and UNKNOWN cost 0.25 (exploring optimal) 21 of 32 choices were optimal with the explicit contract; at reliability 0.2 (checking optimal) 24 of 32. Those two cases are the cells e = 0.20 and e = 0.80 at U = 0.25 of this grid.

## Setup

- **The decision.** A 6 × 6 map. 34 cells have a noiseless current measurement. One cell has only an older report (LAND or WATER) that is wrong with stated probability e. One cell has no evidence. The agent may inspect exactly one of those two cells; both are always legal. A fixed rule then completes the map: the inspected cell gets a correct measurement; an uninspected report is kept; an uninspected cell without evidence is returned as UNKNOWN. A wrong label costs 1, UNKNOWN costs U, a correct label costs 0.
- **Analytic optimum.** Checking the report costs U for certain. Exploring costs 1 with probability e, so e in expectation. The minimum-loss action is to check when e > U and to explore when e < U. Expected regret of a choice is its expected loss minus min(e, U). No case has e = U.
- **Cases.** e in {0.05, 0.20, 0.50, 0.80} crossed with U in {0.10, 0.25, 0.75}: twelve cases. Checking is optimal in six and exploring in six, so a policy that always checks or always explores is wrong in half of them. Always-check has mean regret 0.1500 and always-explore 0.1708; both are offline comparators, never model arms.
- **Representations.** Both requests carry the same map, evidence, objective and the same consequence records for each of the two actions (which cell ends in which state, with which probability and at which cost). `prose` writes the records as sentences; `table` writes them as rows of an action-consequence table. Everything outside the consequence block is byte-identical. Neither states an expected loss, a comparison or a recommendation. A test parses each block back into the records and proves that both hold exactly the same facts and numbers and nothing else.
- **Layouts.** A layout fixes the two cells, the report's label, the 34 measurements and the order in which the two legal cells are listed. Within a layout these are identical in all 24 requests; only e, U and the representation change. The order (report first or unexplored cell first) and the label are balanced over the 24 layouts by construction. Main layouts 3000 to 3023, qualification 2800 to 2811 (set a) and 2900 to 2911 (set b), engineering 2600 to 2603. Every seed stream carries the prefix `verify-cost-qwen`, so no layout repeats a phantom-coast root.
- **Model.** `qwen/qwen3.7-flash` through OpenRouter, provider pinned to Alibaba, `allow_fallbacks: false`, `require_parameters: true`, reasoning disabled, JSON-object mode, `max_tokens` 1,000. The request body is the program's frozen template plus `messages` and nothing else. No other model and no fallback. Reasoning is disabled, so effort does not apply; `effort: low` appears in `READY.yaml` and `design.yaml` only because the launcher requires the field.
- **Answer.** Attempt 002: `{"cost_if_inspect": {"<first allowed cell>": <number>, "<second allowed cell>": <number>}, "inspect": "<row>,<column>"}`: the model writes the expected total cost of each allowed action, then its choice. Only `inspect` is graded; the written costs are reported (absolute error against the analytic cost; how often the choice contradicts the model's own numbers) and never gated. Reasoning stays disabled at the provider. The provider gives no schema guarantee, so the answer is validated locally by rules fixed in advance: valid when the text parses as one JSON object and `inspect` is a string naming one of the two legal cells after trimming whitespace and spaces around the comma; numeric strings, integers, extra decimals, respaced keys, missing or non-numeric costs, extra keys and key order are tolerated and counted; text that is not one JSON object, a missing or other `inspect`, and a repeated key are failed calls. No repair call and no answer retry. (Attempt 001: `{"inspect": "<row>,<column>"}` and nothing else.)
- **Frozen files.** [design.yaml](design.yaml), [preregistration.md](preregistration.md), [manifest.json](manifest.json) (assignment ids and request hashes per stage). The source hash covers `design.yaml`, `experiment.yaml`, `requirements.txt` and `src/*.py`.
- **Code.** `src/sim.py` is the parameterized copy of PC5's `contract.py` (layouts, facts, consequence records, scorer); `src/study.py` holds the two renderings, validation, assignments and gates (PC5's `design.py`); `src/worker.py` runs a stage (PC5's `engine.py`) on `src/provider.py`, the pipeline's reference OpenRouter adapter and ledger, copied unchanged from main `639e9501`; `src/analyze.py` is the scorer's analysis and failure report; `src/render.py` draws the regret and cost panel.

## Protocol

Four stages run as one chain on one server. Each stage is one hub run. A stage is queued only if the previous stage finished `done` at the same source hash with no invalid row and its gate passed. A failed stage stops the chain and nothing further is queued.

1. **S0, scripted, 0 calls.** The four engineering layouts through the whole grid (96 rows) and both qualification sets (24 + 24 rows), answered by the analytic minimum-loss policy: 144 rows. S0 passes only if every row is valid, the scripted qualification passes on both sets, and every invariant holds: both actions legal in every request; the two representations hold the same facts; within a layout only e, U and the representation change; no request contains a truth value, a seed, an expected loss or the optimal action; the optimum is `check` in six cases and `explore` in six; always-check, always-explore, always-first and always-second each fail the qualification gate and have positive regret on the engineering layouts; every qualification fixture has one action better by at least 0.60 in expected loss; a scripted pair of policies that differs between the representations produces the contrast the scorer should report.
2. **P0, 1 call.** The first of the 24 qualification fixtures. It checks the interface: the response parses, the model slug and provider match, usage is reported, the finish reason is `stop`, no reasoning tokens are billed and the answer is structurally valid. Its measured input tokens per request byte are written to its summary and to the hub.
3. **Q0, 23 calls.** The other 23 qualification fixtures (attempt 002: set b, layouts 2900 to 2911; attempt 001 used set a). The gate is evaluated over all 24 rows (P0's saved row plus Q0's 23): 24 of 24 structurally valid and at least 11 of 12 optimal in each representation. These are twelve clear-dominance choices with both actions legal, which repairs PC5's screen (its qualification offered one legal cell). A failed qualification stops the chain.
4. **S1, 576 calls.** 24 layouts × 12 cases × 2 representations, one stateless call each, four requests in flight, the 24 requests of a layout in a seeded order. Before S1 is queued the chain stops with reason `projection_exceeds_cap` if 576 × Q0's measured cost per call does not fit in the remaining dollar cap, and with reason `input_ceiling_projection` if P0's measured tokens per byte times the largest S1 request exceeds 8,000 tokens.

Call caps in the ledger: P0 1, Q0 23, S1 576, 600 in total (attempt 002 runs on a fresh server with a fresh ledger; no further repair exists). Dollar cap USD 2 of settled cost plus open reservations. There is no token-counting endpoint on this route; each reservation is 10 times a byte-based upper bound (input tokens ≤ request bytes, plus the full output limit, at the snapshot prices), about USD 0.002 per call, so part 2 of the failure-handling rule (token counting) does not apply. Expected spend is about USD 0.02; the arithmetic is in the [pre-run review](reviews/chain-002-pre.md).

Failure handling (ready-chain rule of 2026-10-04): every failed request keeps its HTTP status, response body (2,000 characters) and request id; S1 continues past failed calls until more than 6 have failed (the larger of 3 and 1% of 576); integrity failures stop dispatch at once; a credit or balance error pauses the stage, re-sends the same call every 60 s for up to 20 minutes and then stops with `provider_credit_balance_low`, after which `chain.py resume` continues the not-started units at the same source hash inside the same S1 cap (the reservation of a call that no model answered is voided). S0, P0 and Q0 stay strict.

The one permitted repair after a failed qualification is a new attempt (`attempt: '002'`, qualification set b, new source hash, its own pre-run review) after reading the failing answers. That repair is attempt 002, now prepared. A failed repeat ends the line. Thresholds are never lowered.

Analysis: the independent randomized units are the 24 layouts within twelve authored cases, not 576 independent tasks. All 24 layouts stay in the primary analysis. A unit without a valid answer keeps its place with its regret bounded between 0 and |e − U|; the contrast is then reported as bounds over all 24 layouts together with the complete-case estimate and its denominator. Nothing is dropped, imputed or re-run. All twelve strata are reported for both representations, with the optimal-choice counts, and the reliable-source strata (e ≤ 0.20) are checked for regressions of the table against the prose.

## Metrics

| Measure | Definition |
|---|---|
| **Table-minus-prose expected regret (primary)** | Per layout, the mean over the twelve cases of regret(table) − regret(prose). 24 paired values; mean, standard error, descriptive 95% t interval, range, leave-one-layout-out range. Negative favours the table. |
| Expected regret | Expected loss of the chosen action (U for check, e for explore) minus min(e, U). Uses the stated probabilities, not the realized draw. |
| Strata | For each of the twelve (e, U) cases and each representation: valid, optimal, check and explore counts out of 24, mean regret, and the paired difference. |
| Reliable-source regression | In each stratum with e ≤ 0.20: optimal count with the table minus optimal count with the prose. A drop of 3 or more of 24 is flagged. |
| Offline comparators | Always-check and always-explore regret per case and on average; the analytic policy has regret 0. |
| Position | Share of choices of the first-listed cell, per representation. |
| Realized scripted loss | Loss under the layout's seeded truth draw. Secondary; it does not define the optimal action. |
| Qualification | Valid rows of 24; optimal of 12 per representation. |
| Written costs (attempt 002; reported, never gated) | Per representation and overall: rows with both costs written; rows with both within 0.005 of the analytic costs; mean absolute error of each; choices that contradict the model's own two numbers; counts of each tolerated format variant. |
| Failure report | Every unit without a valid answer: category, HTTP status, response body, request id, returned text. |
| Resources | Calls, transport attempts, input and output tokens, dollars from reported usage, billing pauses. |

## Visualization

[VISUALIZATION.md](VISUALIZATION.md): 1800×1200 frames with the regret and cost panel (mean expected regret per case for prose and table, the 24 layout-level contrasts with their mean and interval, each case against the offline comparators, calls, tokens, dollars and failures), an initial, progress and final frame, and a completion-progress GIF.

## Offline evidence (no model call, no server)

Run by the builder on 2026-10-04 at the chain-003 code commit named in the [pre-run review](reviews/chain-003-pre.md): `python3 src/selftest.py` 123 tests OK; offline S0 144 of 144 rows valid, 0 invariant violations, for both models; `python3 src/manifest.py --check` current; the rehearsal against a throwaway local hub and stubbed model endpoints passes all eight chains, including the gpt-6-luna chain on an OpenAI-shaped stub. Operator steps: [RUN.md](RUN.md). Gate status: [SETUP.md](SETUP.md).

Scripted reference values on the four engineering layouts (expected regret per decision; not model evidence; `python3 src/analyze.py calibration`):

| e | U | Optimal action | Analytic policy | Always check | Always explore |
|---|---|---|---|---|---|
| 0.05 | 0.10 | explore | 0 | 0.05 | 0 |
| 0.05 | 0.25 | explore | 0 | 0.20 | 0 |
| 0.05 | 0.75 | explore | 0 | 0.70 | 0 |
| 0.20 | 0.10 | check | 0 | 0 | 0.10 |
| 0.20 | 0.25 | explore | 0 | 0.05 | 0 |
| 0.20 | 0.75 | explore | 0 | 0.55 | 0 |
| 0.50 | 0.10 | check | 0 | 0 | 0.40 |
| 0.50 | 0.25 | check | 0 | 0 | 0.25 |
| 0.50 | 0.75 | explore | 0 | 0.25 | 0 |
| 0.80 | 0.10 | check | 0 | 0 | 0.70 |
| 0.80 | 0.25 | check | 0 | 0 | 0.55 |
| 0.80 | 0.75 | check | 0 | 0 | 0.05 |
| mean | | | 0 | 0.1500 | 0.1708 |

Always choosing the first-listed or the second-listed cell gives 0.1604 each (the listing order is balanced). The analytic policy has regret 0 in both representations by construction, so its table-minus-prose contrast is 0; a scripted pair that is analytic with the table and always-check with the prose gives −0.1500, and the reverse gives +0.1500. The model's cells are not at a floor or a ceiling by construction: any cell can land anywhere between 0 and the case's |e − U|.

## Limits

One model, one synthetic decision with stated calibrated probabilities, scripted consequences, twelve authored cases. Twenty-four layouts randomize coordinates, labels and listing order; they are not twenty-four distinct reasoning tasks. A difference between two renderings of the same information says nothing about multi-step sensing, learned source estimates or a group of agents.

## Results

See [RESULTS.md](RESULTS.md) and the status paragraph at the top. In short: Qwen did not qualify in either answer configuration (18 of 24 and 10 of 24 optimal on clear-dominance choices); gpt-6-luna qualified 24 of 24 and chose optimally in 575 of 576 main decisions, 288 of 288 with the prose and 287 of 288 with the table, so the table-minus-prose contrast is +0.00087 at ceiling. Always-check and always-explore would have had regret 0.1500 and 0.1708.

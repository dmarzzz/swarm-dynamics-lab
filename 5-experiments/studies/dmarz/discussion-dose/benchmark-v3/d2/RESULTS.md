# D2 results: canonical decisions and single-option feasibility checks (v3-d2-a1)

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/v3-d2-opus; source `aef218e8` ([registry](../../../../../../experiments/evidence-metadata.json), [rubric](../../../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — On a compact fact table with a one-field answer, Opus 5.5 answers the six D1 worlds without error (6/6 decisions, 18/18 single-option feasibility checks) while Sonnet 4.6 and Haiku 4.5 each score 5/6 and 16/18 and miss the same two sum-over-budget options. Basis: Measured: 72/72 valid, exact-source audit recomputed all outcomes, known-answer controls discriminate. Limits: six reused dependent world clusters, one response per item with no repeats, only two sum-violating options, and the Opus arm differs from the comparison arms in thinking, effort, sampling and output ceiling.
- **sample_size_summary:** Observed: 72/72 assigned calls valid and analyzed (24 per model: 6 decisions + 18 single-option checks) on 6 reused development world clusters; 3 models on identical items; one response per item; not 72 independent samples. Plus 1 uncounted Opus probe.
<!-- experiment-evidence:end -->

Completed 2026-10-04 08:28 UTC. Attempt `v3-d2-a1`, hub run `discussion-dose-v3/v3-d2-a1`, source commit
`aef218e8fd19470f74aac7bd5749876711a3038f`, frozen manifest `6c772197…f82c`, server `sim-dmarz-3`. Exploratory
diagnostic on six reused development worlds. [Plan and amendment](PLAN.md), [pre-run assessment](../../reviews/v3-d2-a1-pre.md),
[post-run review](../../reviews/v3-d2-a1-post.md), [setup record](SETUP.md). Review was a same-researcher check by
`dmarz/fleet-monitor` under dmarz's waiver; no independent review was performed.

**Opus 5.5, the model under test, passed both screens: 6/6 canonical decisions and 18/18 feasibility checks.
Sonnet 4.6 and Haiku 4.5 each scored 5/6 and 16/18 and failed both screens.** All 72 assigned calls were valid:
no provider failure, refusal, truncation, retry or missing usage. The exact-source audit verified 72 requests and
recomputed 72 outcomes.

Opus was already known to clear the v3 baseline: the separate [D1-Opus run](../../d1-opus/RESULTS.md) passed its
fresh gate 12/12 on D1's original evidence packaging. D2 does not qualify any model. It shows that Opus is also at
ceiling on the compact format, and it narrows where Haiku and Sonnet go wrong.

## Scores

Screens: 6/6 decisions and 18/18 feasibility checks. Answering "infeasible" to every check scores 12/18;
answering "feasible" to every check scores 6/18.

| | Opus 5.5 (under test) | Sonnet 4.6 | Haiku 4.5 | Always-infeasible baseline |
|---|---:|---:|---:|---:|
| Canonical decisions correct, of 6 | **6** | 5 | 5 | n/a |
| Wrong choice of an infeasible option | 0 | 1 | 1 | n/a |
| Abstentions | 0 | 0 | 0 | n/a |
| Feasibility checks correct, of 18 | **18** | 16 | 16 | 12 |
| Feasible options recognized, of 6 | 6 | 6 | 6 | 0 |
| Infeasible options recognized, of 12 | 12 | 10 | 10 | 12 |
| Infeasible options called feasible | 0 | 2 | 2 | 0 |
| Valid responses, of 24 | 24 | 24 | 24 | n/a |
| Decision screen | pass | fail | fail | |
| Feasibility screen | pass | fail | fail | |

By family (two worlds each; decisions of 2, checks of 6):

| Family | Opus decisions / checks | Sonnet decisions / checks | Haiku decisions / checks |
|---|---|---|---|
| Capacity (20001, 20004) | 2 / 6 | 2 / 6 | 1 / 6 |
| Total cost (20002, 20005) | 2 / 6 | 2 / 4 | 2 / 4 |
| Dependency (20003, 20006) | 2 / 6 | 1 / 6 | 2 / 6 |

Paired on identical items (24 per pair): Opus minus Sonnet +3, Opus minus Haiku +3, Sonnet minus Haiku 0. Sonnet and
Haiku gave the same answers on all 18 feasibility checks and differed on two decisions. These are counts on six
dependent world clusters with one response per item. No interval or significance claim is made.

## Per-item table

Feasibility checks. "Rule check" is the arithmetic on the canonical facts. A cell shows the model's answer; a wrong
answer is in bold.

| Item | Rule check | Correct | Opus | Sonnet | Haiku |
|---|---|---|---|---|---|
| 20001 A | power 18 ≥ 16, access 6 ≤ 7 | feasible | feasible | feasible | feasible |
| 20001 B | power 18 ≥ 16, access 8 > 7 | infeasible | infeasible | infeasible | infeasible |
| 20001 C | power 13 < 16 | infeasible | infeasible | infeasible | infeasible |
| 20002 A | 13 + 66 = 79 ≤ 79, 7 days ≤ 7 | feasible | feasible | feasible | feasible |
| 20002 B | 16 + 68 = 84 > 79, 6 days ≤ 7 | infeasible | infeasible | **feasible** | **feasible** |
| 20002 C | 13 + 5 = 18 ≤ 79, 8 days > 7 | infeasible | infeasible | infeasible | infeasible |
| 20003 A | direct 17 < 18, backup 0 | infeasible | infeasible | infeasible | infeasible |
| 20003 B | direct 16 < 18, backup 1 but transfer 5 > 4 | infeasible | infeasible | infeasible | infeasible |
| 20003 C | direct 20 ≥ 18 | feasible | feasible | feasible | feasible |
| 20004 A | power 16 ≥ 14, access 4 > 3 | infeasible | infeasible | infeasible | infeasible |
| 20004 B | power 13 < 14 | infeasible | infeasible | infeasible | infeasible |
| 20004 C | power 17 ≥ 14, access 2 ≤ 3 | feasible | feasible | feasible | feasible |
| 20005 A | 20 + 46 = 66 > 62, 5 days ≤ 6 | infeasible | infeasible | **feasible** | **feasible** |
| 20005 B | 17 + 5 = 22 ≤ 62, 7 days > 6 | infeasible | infeasible | infeasible | infeasible |
| 20005 C | 17 + 43 = 60 ≤ 62, 6 days ≤ 6 | feasible | feasible | feasible | feasible |
| 20006 A | direct 7 < 8, backup 0 | infeasible | infeasible | infeasible | infeasible |
| 20006 B | direct 7 < 8, backup 1 and transfer 2 ≤ 2 | feasible | feasible | feasible | feasible |
| 20006 C | direct 6 < 8, backup 1 but transfer 4 > 2 | infeasible | infeasible | infeasible | infeasible |

Canonical decisions, with the D1-format choices of the same models on the same worlds for reference
([D1](../RESULTS-D1.md), [D1-Opus](../../d1-opus/RESULTS.md)). D1 and D2 are different requests and single responses,
so a change between them is not a measured packaging effect.

| World / family | Correct | Opus D2 | Sonnet D2 | Haiku D2 | Opus D1 format | Sonnet D1 | Haiku D1 |
|---|---|---|---|---|---|---|---|
| 20001 / capacity | A | A | A | A | A | A | B |
| 20002 / total cost | A | A | A | A | A | C | A |
| 20003 / dependency | C | C | **B** | C | C | C | B |
| 20004 / capacity | C | C | C | **B** | C | A | A |
| 20005 / total cost | C | C | C | C | C | B | A |
| 20006 / dependency | B | B | B | B | B | B | B |
| Correct, of 6 | | 6 | 5 | 5 | 6 | 3 | 2 |

Full rows, including call order, tokens and latency per call: [per-item.csv](results/v3-d2-a1/per-item.csv).

## What the errors were

Observed:

- **Both feasibility errors of both comparison models are the same two items**, 20002 B and 20005 A. They are the
  only two of the 18 options whose base plus freight exceeds the budget (84 against 79, 66 against 62); both meet
  the deadline. Sonnet and Haiku answered every other check correctly: all 12 capacity and dependency checks, and
  the four total-cost checks where the sum is within budget.
- **Each comparison model made one wrong decision, on a world where all three of its own feasibility answers were
  correct.** Sonnet chose B in 20003; B has direct 16 against a minimum of 18 and transfer 5 against a maximum of 4.
  Haiku chose B in 20004; B has power 13 against a minimum of 14. Neither model abstained.
- **Composition.** Applying the task's objective and tie-break to each model's own three feasibility answers gives
  the correct option in 6/6 worlds for all three models. In the two worlds where Sonnet and Haiku called a second
  option feasible, the objective still selects the correct one (79 beats 84; 60 beats 66). Each comparison model's
  direct vote disagrees with its own derived choice in one world (Sonnet 20003, Haiku 20004); Opus in none.
- **Opus output size.** On 17 of its 24 items Opus returned 10 or 11 output tokens, the size of the bare answer. On
  7 items it returned 29 to 79: the decisions for 20002, 20003, 20004 and 20005, and the checks 20002 B, 20005 A and
  20005 C. Thinking is billed as output, so Opus spent reasoning tokens on at most those seven items, which include
  both items the comparison models missed.

Inference, not established by this run: the two false positives are consistent with Sonnet and Haiku, answering
without thinking, mishandling a two-term sum against a budget; the wrong votes are consistent with a selection slip
that the same models avoid when asked about one option at a time. One response per item cannot separate a stable
error from run-to-run variation, and no repeat was made.

## Reading under the rule fixed before the run

| Model | Decisions 6/6 | Checks 18/18 | Reading |
|---|---|---|---|
| Opus 5.5 | yes | yes | Passes on the compact representation and contract. With D1-Opus, Opus is at ceiling on both formats on these worlds. D2 qualifies nothing. |
| Sonnet 4.6 | no | no | Inspect predicate, task and interface semantics before another model or a swarm. |
| Haiku 4.5 | no | no | Same. |

The prediction from D2-PLAN, that complete explicit facts and a small contract reduce the D1 decision failures, is
matched in direction for the comparison models (Haiku 2/6 to 5/6, Sonnet 3/6 to 5/6) and not to the 6/6 screen.
Sonnet also got 20003 wrong here after getting it right in D1. The compact format did not fully repair either model,
and the remaining feasibility errors sit on one predicate type.

## Calls, tokens and cost

| | Calls | Valid | Input tokens | Output tokens | Observed cost USD | Summed latency s |
|---|---:|---:|---:|---:|---:|---:|
| Opus 5.5 | 24 | 24 | 15,814 | 551 | 0.074276 | 56.7 |
| Sonnet 4.6 | 24 | 24 | 11,620 | 215 | 0.038085 | 23.7 |
| Haiku 4.5 | 24 | 24 | 11,596 | 216 | 0.012676 | 19.7 |
| Batch | 72 | 72 | 39,030 | 982 | **0.125037** | 100.1 |
| Opus compatibility probe (not a result) | 1 | 1 | 626 | 10 | 0.002704 | 2.9 |
| All inference calls | 73 | 73 | 39,656 | 992 | **0.127741** | |

Cost is provider-reported usage at list prices (USD per million input/output: Opus 4/20, Sonnet 3/15, Haiku 1/5),
not reconciled against an invoice. No cache tokens. The worst-case reservation was USD 3.387356 under a USD 5 cap.
The hub run carries the batch cost once (0.125037); the probe cost is recorded here and in
[accounting.json](results/v3-d2-a1/accounting.json) only. The service ran from 08:26:06 to 08:27:58 UTC, one call at
a time. Every returned model id matched the requested id. Opus requests counted 626 to 742 input tokens against 458
to 550 for the same content on the other two models; the cause was not investigated.

## Limits

- Six reused development worlds, each with exactly one feasible option. Scores on these worlds do not generalize to
  fresh worlds and do not test tie-breaking among several feasible options.
- One response per model and item. There is no estimate of run-to-run variation, and a one-item difference (5/6
  against 6/6) is a single response.
- The Opus arm differs from the comparison arms in model, always-on adaptive thinking at effort `high`, no sampling
  parameter and a 4,000-token output ceiling. An Opus advantage is model and configuration together.
- D2 changed evidence packaging and the response contract together relative to D1. The D1 columns above are
  reference, not a controlled comparison.
- No swarm, discussion treatment, merge defence or holdout is involved. `model_qualified` is false for all three.
- Published here: scores, the one-letter or boolean answer per item, and accounting. Request and response journals
  and raw text stay private.

## Records

[summary.json](results/v3-d2-a1/summary.json) (SHA-256 `28133b82…82a2`), [audit.json](results/v3-d2-a1/audit.json),
[artifact-index.json](results/v3-d2-a1/artifact-index.json), [per-item.csv](results/v3-d2-a1/per-item.csv),
[accounting.json](results/v3-d2-a1/accounting.json), [rehearsal receipt](launches/v3-d2-a1-rehearsal.json). Six
indexed artifacts were downloaded from the hub and matched the server and local bytes; the private archive SHA-256
is `fee5dcdb8166e62bfc6541c7a04516855ec581bb0034765f47268e946ca0387a`.

No successor was started. The claim on `sim-dmarz-3` was released after artifact readback.

# When verification amplifies capture (program v5, line T)

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/pipeline-split; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **0/4** — Placing the credit of a passed check on the passed identity alone, instead of propagating it to neighbours, attenuates the rise in attacker seats between 32 and 108 coverage checks at 324 scripted identities. Basis: Unrun. Plan and frozen design only; no stage has run on a server and no model call has been made.
- **sample_size_summary:** Observed: none. Planned: 24 paired synthetic roots × 21 cells = 504 S1 calls (qwen3.7-flash) at 324 scripted identities and one synthesizer; 24 qualification calls on 8 roots. Roots are the independent units; the primary seat outcome is scripted.
<!-- experiment-evidence:end -->

**Nothing has run.** This directory is a prospective plan and, once the code lands, a launch-ready package. No stage of this study has been executed on a server, no model call has been made and no result exists. Exploratory; owner dmarz; built by dmarz/pipeline-split on 2026-10-04 for the pipeline lead dmarz/pipeline.

This is line T of [research program v5](../overnight-program-2026-10-04/program.json) ([setup record of the program](../overnight-program-2026-10-04/SETUP.md), [selected model](../overnight-program-2026-10-04/selected-model.json)). It extends the instrument of [sybil-budget-api](../sybil-budget-api/RESULTS.md) at 324 identities and follows the [ready-chain contract](../pipeline/READY-CHAIN.md). It is not an accepted hypothesis and makes no novelty claim. S2 is disabled.

**Authority and review status** (as relayed to this builder by dmarz/pipeline, 2026-10-04). dmarz directed this program himself (research program v5, written with him by a Codex session on 2026-10-04; his instruction to ship it was relayed by dmarz/fleet-monitor). The design is the program's; this package implements line T as specified there. Cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check and nothing more; the run is not independently reviewed.

Implementation note, 2026-10-04: the program's five-session and shared-reservation arrangement is replaced by the ready-chain: one package per line, one server per line, its own ledger and caps, launched by the orchestrator from the private run queue.

## TLDR

The earlier budget study found that, at 324 simulated identities with strong checks, the attacker's share of admitted seats rose from 1.98% at 32 coverage checks to 8.51% at 64 and 10.70% at 108, while answer accuracy also rose. In that instrument every identity that passes a check becomes a seed of the trust ranking, so its credit also flows to its neighbours. This study tests whether that flow is what admits the extra attacker identities. For each of 24 fresh roots the audit (which identities are checked, in what order, with what outcome) is generated once and then replayed under three admission rules that differ only in where the credit of a passed check goes: to the passed identity and onward to its neighbours (`propagated`, the earlier behaviour), to the passed identity alone (`direct`), or nowhere (`anchors`). Seats, tie-breaking, badges and packet order are the same. The primary outcome is the number of attacker identities among the 162 seats; it is computed by the scripted admission, not by a model. `qwen/qwen3.7-flash` then reads each admitted packet and answers six values, so answer quality can be reported beside admission. There are 504 comparison calls after a scripted stage and 24 qualification calls. The 324 identities are scripted, not model agents; one graph family, one audit policy and one fabrication type are used.

## Question and prediction

Does propagating a passed identity's trust credit to its neighbours cause extra attacker identities to be admitted as the check budget grows?

Primary contrast, per root, at strong checking (an attacker identity passes a check with probability 0.1): [attacker seats under `propagated` at 108 checks − at 32 checks] − [attacker seats under `direct` at 108 checks − at 32 checks]. Positive means that placing pass credit on the passed identity alone attenuates the rise in attacker seats that comes with a larger budget. It is paired by root over 24 roots.

Prediction, written after the scripted calibration on the 8 engineering roots and before any model call: positive and large. On the engineering roots the `propagated` rule reproduces the direction of the budget study (attacker seats 2.2, 13.2, 15.5 at 32, 64, 108 checks: 1.4%, 8.2%, 9.6% of seats) and the primary is +23.4 seats (every root positive, 12 to 32). That number has a second half the program text does not anticipate: under `direct` and under `anchors` the attacker holds many seats at 32 checks (20.5 and 22.1) and fewer at 108 (10.4 and 6.6). A likely reason, not checked here: without propagated credit the honest specialists near passed identities are not lifted, and outside identities near the bridges, the controller's among them, take the seats that failed core identities vacate. So on these roots `direct` credit removes the budget escalation, and at the small budget it admits more attacker identities than `propagated` does. Both parts are reported; the primary contrast alone would hide the second.

What would count against the candidate mechanism: a primary near zero or negative on the 24 comparison roots. What the model can add: whether answers on rare skills follow the seats (wrong answers where attacker rows outnumber honest ones) or not. A null or adverse result is kept.

## Setup

**World** (the sybil-budget-api instrument at N = 324, unchanged): 162 honest core identities holding three common skills, one honest outside group of 81 specialists holding three rare skills, and one outside group of 81 identities owned by one controller that reports the true value plus 7 on its rare skill. Two core identities are trusted anchors. Honest identities pass a check with probability 0.9; controller identities with probability 0.1 (strong checks) or 0.9 (weak checks). Check outcomes are one uniform draw per identity, so they are coupled across the two strengths.

**Frozen audit.** For each root and check strength the coverage policy of the earlier study picks 108 identities one after another (each time the unchecked identity whose neighbourhood adds most uncovered identities), and each check passes or fails. Failed identities are removed. The sequence depends on the public graph and earlier outcomes only, never on an admission rule. Budgets 32 and 64 are prefixes of the same sequence.

**Three admission rules** on each snapshot, with one transition matrix (an identity spreads its mass equally over its neighbours that have not failed) and one dangling rule (an identity with no such neighbour sends its mass to the two anchors), restart 0.2, 120 iterations: q0 is the personalized PageRank from the two anchors, q1 from the passed identities, alpha = passed / (2 + passed).

- `propagated` = (1 − alpha)·q0 + alpha·q1
- `direct` = (1 − alpha)·q0 + alpha·uniform(passed)
- `anchors` = q0

The top 162 scores are seated, ties broken by identity name. The pass-credit mass is alpha in both of the first two rules; an empty passed set reduces every rule to q0.

**Relation to the earlier implementation.** With no dangling identity, `propagated` is the earlier ranking exactly (the earlier restart vector is uniform over anchors and passed identities, which is the same mixture). The earlier code sends a dangling identity's mass to anchors and passed identities; here it goes to the anchors only, so that q0 holds no pass credit. On the engineering roots 12 of 48 snapshots contain one or two dangling identities; the admitted set equals the earlier one in 42 of 48 snapshots, differs by 6 to 13 seats in the other 6 (all with a dangling identity), and the attacker seat count differs by at most 1. This is an audited difference, not an exact replication.

**Cells.** 3 rules × 3 budgets {32, 64, 108} × 2 strengths = 18 attacked cells per root, plus 3 clean endpoints (the three rules at 108 checks). A clean endpoint keeps the graph and the audit of the weak-check cell (the controller's identities then pass at the honest rate, which is the same draw) and makes every controller report truthful, so its admission is identical to the weak-check cell at 108 checks and only the reported values differ.

**Packet.** The model sees the 162 admitted reports as a compact JSON object: `skills`, `columns` (`id, skill, value, age, activity, check`) and one short array per report, with `check` = `T` (anchor), `P` (passed) or `U`. Rows are ordered by a key drawn once per root and identity. A whole request is 5.9 kB; the design refuses any request over 7,600 bytes, so input stays under the 8,000-token ceiling even at one token per byte. The instruction states the exact JSON shape of the answer, and the answer is validated locally.

**Model.** `qwen/qwen3.7-flash` through OpenRouter, provider pinned to Alibaba, no fallback, reasoning disabled, JSON-object mode, `max_tokens` 1,000. `effort: low` appears in `READY.yaml` only because the launcher requires the field; reasoning is disabled and effort does not apply.

## Protocol

[Pre-registration](preregistration.md), [design](design.yaml), [setup record](SETUP.md).

| Stage | Batch | Calls | What it does | Passes when |
|---|---|---|---|---|
| S0 | `s0-001` | 0 | Reference policy on 8 engineering roots through the whole grid (168 rows) and on both sets of 24 fixtures; invariants in code | every row valid, no invariant violated, both fixture sets pass under the reference, `propagated` reproduces the earlier direction, primary not constant |
| P0 | `p0-001` | 1 | The first of the 24 qualification fixtures | response parses, model and provider match, usage reported, finish reason `stop`, no reasoning tokens, valid structure |
| Q0 | `q0-001` | 23 | The other 23 fixtures | over all 24: every structure valid; at least 7 of 8 exactly right in `full` and in `sparse`; null on the withheld fact in 8 of 8 `missing` packets |
| S1 | `s1-001` | 504 | 24 roots × (18 attacked cells + 3 clean endpoints) | at most 6 failed calls and no integrity failure |

Fixtures: 8 development roots × `full` (18 specialists per rare skill), `sparse` (two per rare skill) and `missing` (one rare skill has no report). All are clean packets of 162 reports in the comparison's format. A second, disjoint set of 24 fixtures is frozen now for the one bounded repair the program allows.

Before S1 the chain stops if the tokens per byte measured in P0 would put the largest S1 request over 8,000 tokens (`input_ceiling_projection`), or if S1's projected cost exceeds what is left under the dollar cap (`projection_exceeds_cap`).

Failure handling: a failed call in S1 is recorded with its HTTP status and response body and dispatch continues until more than 6 calls have failed; integrity failures stop at once; a billing outage pauses the stage and, if it outlasts 20 minutes, stops it in a state that `chain.py resume` can continue.

Roots (all below 10000): engineering 4481-4488, qualification 4591-4598, repair qualification 4650-4657, comparison 9541-9564.

## Metrics

Primary: as above, in seats, with the mean over 24 roots, a root-bootstrap interval (10,000 draws, seed 20261004) and the per-root values. It is computed from scripted admission and is therefore complete whatever happens to model calls.

Reported beside it for every rule, budget and strength: attacker seats and seat share; honest-specialist retention; truth availability (rare skills with at least one honest report admitted) and truth plurality (rare skills where honest reports outnumber the controller's); the model's rare-skill answers as correct, wrong or abstained; the same for the reference plurality rule; the clean endpoints. The same attenuation contrast is reported for weak checks, for `anchors` in place of `direct`, and at 64 checks.

Missing model outcomes stay in their cell's denominator with bounds (each missing answer counted as all wrong or all right); complete-case values are shown with their denominators. Nothing is dropped, imputed or re-run.

## Limits

- The 324 identities are scripted, not model agents. Only the synthesis of the admitted packet is a model call.
- The primary is deterministic given the design and a root; the model does not influence it.
- One graph family, one audit policy (coverage), one fabrication (+7), one population size.
- `direct` and `anchors` are counterfactual admission rules written for this study, not published defenses.
- The dangling rule differs from the earlier implementation as described above.

## Results

Not yet collected.

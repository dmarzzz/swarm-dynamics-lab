# Frozen decision protocol v1

Status: exploratory S0/S1; policies frozen before opening evaluation IDs 30–99. Source code is the executable definition; this file states its assumptions and limitations.

## Estimator and QA tool

For each mode, calibrate an additive bias as mean(regional recall minus regional OCR confidence) over nonempty annotated regions of the first20 receipts. For an unchecked region, estimate clip(confidence+bias,0,1). For a checked region use its revealed recall; if it has no annotated text, omit that region from the average. The mode estimate is the unweighted mean of its available region estimates. Select its maximum; ties A, then B, then C.

The evaluator's whole-receipt recall is weighted by annotated token counts. The selector's region average intentionally has no access to those hidden counts. This approximation can fail when text is unevenly distributed or OCR misses a region. It is a limitation to measure, not a claim that the selector is optimal. A future confidence estimator should be trained on a separate, larger development set; do not fit it to these70 receipts after seeing outcomes.

All deployable check policies select A/B/C; the tool checks the selected mode's lowest-confidence unchecked region, breaking ties top to bottom. This restriction keeps actions compact for Laya and shared across controls. Two checks per receipt; no duplicates or refund for an empty region. QA exposes only regional recall or no-target-text. It does not repair OCR, reveal other regions, or give the correct final selection.

## Arms

| Arm | Rule | Maximum model calls / checks |
|---|---|---|
| best-fixed | Always calibration-best mode | 0 / 0 |
| confidence-only | Highest initial calibrated estimate | 0 / 0 |
| random-checks | Two random mode choices, seed71 keyed by receipt; same region tool | 0 / 2 |
| decision-focused | Twice maximize estimate + 0.25*(1-lowest remaining confidence); same region tool | 0 / 2 |
| single-agent | One fully informed Laya role chooses check or STOP | 2 / 2 |
| swarm-fixed | Five role votes per step; plural check vote, then estimate, then A/B/C; always two checks | 10 / 2 |
| swarm-adaptive | Same ballots/action rule; STOP at 4/5 first step or 3/5 second | 10 / 2 |

STOP votes are ignored when choosing the fixed policy's next check. If every role votes STOP, highest estimate selects the check. This explicitly makes fixed a budget-spending ablation rather than a rational stopping baseline. Single-agent and no-check controls prevent treating fixed's overspending as evidence for a swarm. The 0.25 bonus and quorum thresholds are design choices, not empirically optimal values.

## Agent specification

Runtime: local convaiinnovations/laya, revision55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851, source2e4d9c87e8b1621deb344eac7de5c7258f32f849, CPU eager backend, seed0, two threads. Every input is encoded and checked for truncation and distinct options. Every call records state, question, probability distribution, selected action, token count, hash and latency. No hidden remote inference; Jev/OpenRouter remains a separate future backend comparison.

Roles are layout specialist, text-quality auditor, coverage skeptic, cost controller and verification coordinator. The first three see confidence for A, B or C respectively; the last two see all three. All see the current estimated leader and shared QA. These role names do not confer specialized training or expertise; all use the same checkpoint. The single-agent control receives the full union of observations. Role prompts and exact state builder are in src/policies.py.

They choose only A/B/C/STOP. Their task is choosing a useful verification, not describing a receipt or generating a chain of thought. No interpretation of model internals is made. The four explicit-response interface probes measure basic action adherence; misses must be reported. Valid schemas alone do not establish semantic competence.

## Pairing, validity and audit

Run fixed committee first and retain both potential ballot vectors. Adaptive consumes the same prefix, stopping before later information arrives. This is a common-random-input comparison of stopping rules, not two independent fresh model runs. Count unused fixed ballots as physical compute but not adaptive logical calls. No further memoization.

Every receipt is retained; no cherry-picking by difficulty, OCR confidence or model success. An OCR failure, malformed model output, encoding loss, budget violation or missing receipt blocks escalation. Semantic bad choices are outcomes, not faults to reroll. Report the instrument screen separately. The70 exploratory receipts are one small dataset, not70 heterogeneous production applications.

For each selected output retain all three evaluator scores, checked regions and action history. Report regret above2pp, changes that improve/hurt versus no-check confidence, and adaptive-vs-fixed quality loss/savings on the paired tape. These are observable contrasts. Assigning mental causes such as confusion requires further controlled tests; label those explanations as hypotheses.

An evaluator-only ceiling enumerates0,1,2 arbitrary configuration-region checks with perfect future information and the same selector. Its action space is broader than deployable policies. It is a diagnostic upper bound, not a fair competitor or reachable accuracy promise.

## Robustness and next discriminating tests

This version checks outcome persistence, model encoding, paired budgets, source blindness and measured rendering. It does not establish robustness to annotation errors, malicious agents, alternative OCR versions, noisy humans, broader languages or domain shift. Next tests should change QA accuracy/cost, confidence estimation and private/shared evidence separately; use a new held-out corpus after development. A Jev comparison must preserve the task, budget and logging, and separately account for paid calls. Do not claim general adaptive-quorum superiority from this version.

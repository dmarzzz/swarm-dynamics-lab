# S1 attempt 2 post-mortem and quality assessment

**Execution complete; narrow qualification passed; conditional mechanism result; no general adaptive-quorum or AI advantage established.** All 384 assigned blocks completed, yielding 2,688 policy outcomes across 12 synthetic task clusters. Zero invalid actor/schema outputs. The 25-block interrupted prefix was recovered byte-equivalently at the decoded-record level, once, with no model rerolls. [Integrity checks](../results/S1/integrity.json), [summary](../results/S1/summary.json), [all outcomes](../results/S1/outcomes.csv), [task-paired contrasts](../results/S1/paired-contrasts.json).

## What the results teach

For nine scouts and cutoff six, each condition contains the same twelve tasks:

| Evidence world / arrival | Fixed-two | Fixed-three | Adaptive |
|---|---|---|---|
| Clean / late | 12 correct | 12 correct | 12 correct |
| Clean / stalled | 12 correct | 12 abstain | 12 correct |
| Early wrong / late correction | 12 violations | 12 abstain | 12 correct |
| Early wrong / stalled | 12 violations | 12 abstain | 12 violations |
| Late wrong / late | 12 correct | 12 abstain | 12 violations |
| Late wrong / stalled | 12 correct | 12 abstain | 12 correct |

Copies reproduce the clean condition's terminal choices in this matrix; root counting is invariant, though private delivery can in general change. Adaptive trades caution for action and benefits from timely corrections. The same relaxation becomes harmful when false reports persist or arrive late. Comparing only with fixed-three would overstate its practical benefit: fixed-two already solves clean stalled cases earlier. Full-information central controls also fail when the supplied latest reports are false. Information access is not a truth oracle.

Pooled counts hide this reversal. Majority, fixed-two, adaptive, deadline-vote, central and symbolic central each have 288/384 correct, 96/384 violations, mean loss 0.25. Fixed-three has 48/384 correct, 336/384 abstentions, no violations, mean loss 0.4375 under the declared utility. A different abstention penalty changes this ranking; component rates are the meaningful record. The engineered scenario frequencies are not real deployment frequencies. There is no inferential claim from twelve generator variants or their repeated ballots.

Every hybrid policy choice matched its fully symbolic counterpart. No model eligibility acceptances required guard blocking in S1. Thus the model is **not shown to add decision quality** on this structured task. Q1's retention error remains a caution against delegating hard typed constraints to an unconstrained decision model. The guard regression establishes its behavior; S1 is not a new causal efficacy test of that guard.

## Seven requested quality dimensions

| Dimension | Evidence-based assessment |
|---|---|
| Design | Stronger mechanism test: matched tapes, fixed-two comparator, late correction and late misinformation, stalled/copy controls, both populations/cutoffs. Still synthetic and highly deterministic. |
| Measurement | Reconciled384 unique assignments/2688 outcomes, balanced targets 96 per policy, explicit component loss, actual encoded tokens, source support rather than availability, consumed-prefix costs and receipt references. Per-arm deployment latency is not measured. |
| Visualization | Eight preselected seven-frame 1600px GIFs plus final frames and conditional tradeoff chart. Initial/intermediate/final frames inspected; future decisions hidden. Charts use measured outcomes, not invented spatial motion. |
| Specification | Consolidated protocol, exact agent contract, pins, split IDs, evidence authority, guard/cache semantics and runbook. Historical protocols remain explicitly versioned. |
| Plan | Failed D0/Q1 screens led to bounded diagnosis and new qualification, then a frozen factorial. Rendering failure triggered a real regression and exact-prefix recovery; no scientific rerolls. |
| Controls/robustness | Deliberate controls expose both adaptive benefit and harm, and no incremental model benefit. Source reliability, source-root forgery, asynchronous latency, natural-language extraction and external task diversity remain untested. |
| Agent reproducibility | Exact checkpoint/source/dependencies/prompts, no hidden evaluator inputs, per-call probability/encoding receipts and recorded cache references. Five/nine logical scouts share one deterministic model; not independent experts or autonomous researchers. |

## Operational and resource reconciliation

39 distinct physical model calls across both operational attempts, including 12 restored receipts;88,128 logical predicate invocations. 1,677 actually encoded input tokens and 26.394s total physical inference time. The reported 38.475s recovery elapsed field measures recovery computation up to summary construction and **excludes later rendering/upload**; do not present it as full end-to-end or per-policy latency. First-attempt wall time is also separate. No hosted API spend. Exact source/runtime manifest is linked with results. A tiny memoized input set is another reason not to claim 88,128 independent model tests.

Attempt1's GIF TypeError is retained on the hub. Fixed by correct duration-list construction, nine regression tests including actual GIF encode/decode, and separating rendering after durable outcomes. Attempt2 completed and uploaded full compressed event/invocation/guard histories, receipts, manifests and images. The public dashboard initially hid new stages because actual executions had been tagged `kind: analysis`; reporting metadata was corrected to experiment/qualification/diagnostic without changing scientific data or terminal statuses. This is a reporting repair, not a new replicate.

No failures in the completed recovered execution remain unresolved. Historical failures stay visible. No guarantee of failure-free future runs is warranted. Public artifact reachability and final dashboard rendering are checked separately at handoff.

## Issue closure and remaining limits

R1 missing-versus-ineligible, R2 supporting roots, R4 later-fault contamination, R5 exact encoding and R9 reproducibility: repaired with tests/receipts. R3 tool authority, R6 misleading benchmark label and R7 timing: removed from v3's primary stopping task; historical v2 remains annotated, not silently rescored. R8 model capability: system qualified after explicit architecture change; unconstrained Laya still not qualified for full provider selection. R10 temporal visual integrity: repaired and regression-tested; interrupted GIF attempt preserved. These close the scoped engineering defects, not the external-validity gaps.

Next action: **complete-valid-result** for this engineering study. Do not increase model count or rerun these cases seeking an adaptive win. Before a stronger scientific claim, obtain independent prior-art/hypothesis review, build a held-out corpus of realistic provider-document claims with cited gold facts, vary source reliability/forged ancestry and calibrated latency, and compare learned extraction with the same guarded symbolic pipeline. Jev is a future separately qualified backend. That is a new protocol, not required to disguise this valid conditional/negative result.

## Handoff verification

Clean-browser verification loaded all18 public result images (eight PNG/GIF pairs plus two analysis charts). All GIFs contain seven frames; initial and final frames and an intermediate event frame were inspected. Hub run status is done, progress384/384; all29 expected team artifacts are listed. Gitleaks found no secrets in the contribution; lab check has zero errors and five pre-existing citation warnings. Nine regressions pass. Own active experiment workers: zero.


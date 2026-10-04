# Next practical study: receipt intake with selective review

Prospective design, not executed and not an accepted hypothesis. This follows Dmarz's conditional Antsy recommendation and the v4/v5 engineering diagnostics. It replaces a vague “better OCR” goal with a decision a receipt-processing service actually makes: accept a structured result, pay for another check, or send the receipt to manual review.

## Application contract

Given an original receipt and candidate extractions from three pinned pipelines, return the required fields (total amount, currency when printed, transaction date when printed, merchant), or abstain on each unsupported field. Preserve a distinction between absent, unreadable and conflicting. The primary outcome is an entirely correct required-field decision per assigned receipt at a fixed total resource allowance. Report false confident acceptance and manual referral separately; token recall is a secondary diagnostic.

The actor must receive the OCR candidates and observable pipeline signals; never annotation-aligned crops, reference answers, ground-truth field locations or “correct” flags disguised as tool outputs. A checker must independently inspect an actor-selected crop/field or run a different extraction method. Record the checker output, actual latency and monetary cost; evaluate its errors against withheld annotations afterward. Annotation-perfect checking may remain an explicitly separate diagnostic ceiling.

## Development before evaluation

Use 20 new receipts from separately sampled document/vendor-layout families, disjoint from the previous validation receipts. Before inspecting model-policy outcomes, manually audit the field normalizer and scoring on development examples, including currency/decimal conventions, duplicate TOTAL lines, tips/tax, absent dates and unreadable text. Do not silently convert locale ambiguity into a single “correct” number. Ambiguous reference cases get a prespecified exclusion/abstention rule and retain their assigned denominator in reporting.

Measure whether alternatives actually disagree and whether an available checker changes the correct decision. No quota of intentionally bad agents or hand-assigned winning policies. If the checker cannot improve a meaningful number of decisions, drop that tool/application or keep the no-check pipeline; do not manufacture ambiguity to favor a committee.

## Fair comparisons

- No-check confidence router with an abstention threshold fitted only on development data.
- Cheapest competent single solver with the same initial evidence and tool menu.
- Deterministic expected-value-of-information baseline with calibrated uncertainty.
- Five-role committee, first with matched total inference allowance, then a separately labeled operational-cost condition.
- Same-input repeat voters versus genuinely different evidence partitions, if and only if the basic committee is qualified.

Both STOP and CONTINUE are legitimate. Prices, penalties, review limits and available tools appear explicitly in the task, with prespecified sensitivity ranges. The final policy may abstain rather than accept an unsupported result. False acceptance has a separately stated loss; no claim that normalized loss units are dollars unless measured.

## Promotion gates

1. Independent scoring/field-parsing review passes, including absent/ambiguous reference cases and mutation tests.
2. Measured checker confusion/latency/cost records exist; no truth leakage.
3. Each selected model passes disjoint clean task and stop/continue controls with a prespecified threshold. A formatting pass alone is insufficient.
4. Development establishes real decision headroom; choose evaluation size from paired outcome variability and the proposed useful improvement (5 percentage points at equal resource allowance), not a desired p-value.
5. Freeze vendor/layout-family partitions, agents, evaluator, costs and visualization before opening untouched evaluation. Cluster intervals by receipt/vendor family when dependence warrants it; never count votes or cost settings as new observations.

After the freeze, changes become a new version. Report all assigned cases, invalid outputs, abstentions, failed calls, missing observations and actual costs. If an independent evaluation excludes a useful gain over the cheapest competent baseline, retain that baseline. Wide intervals remain inconclusive.

## Explanation and visualization

A replay should show the actual receipt/crop only when public-data licensing and content review permit it, the candidate fields with disagreement highlighted, a shrinking review budget, each checker response, the reason-coded decision to accept/check/refer, and finally the withheld evaluator result. Do not invent chain-of-thought. Pair the replay with an acceptance-risk versus review-cost frontier and a table of errors that verification introduced, not merely those it repaired. Label preselected examples and post-hoc worst cases separately.

## Current boundary

V5 implements and tests the numerical missing-evidence repair and a development cost-aware baseline. It does not yet implement this field extractor or measure human/checker costs. Launch remains closed until those gates are satisfied. This prevents another synthetic-looking committee demonstration from being presented as practical evidence.

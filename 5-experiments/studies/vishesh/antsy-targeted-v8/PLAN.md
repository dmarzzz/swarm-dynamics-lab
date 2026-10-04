# Antsy v8: verify the field, not the vote

Exploratory design and offline development. No new native qualification or held-out result is claimed. Parent: [v7 post-mortem](../antsy-diversity-v7/reviews/S0-repair-post.md). This plan precedes v8 implementation; the development diagnosis may lead to an explicit amendment, never a rewritten v7 result.

## TLDR

Repair the receipt field-extraction contract on saved, already-used OCR, then test whether a useful checker improves a strong primary reader under an explicit resource budget. Do not lower qualification thresholds, give weak workers votes, or let an arbitrary dissenter veto good evidence. Decompose recognition, label/amount association and aggregation so failures can be located. Current scope: development replay, tested prototype, and prospective qualification/comparison design; no new OCR or hosted-model calls in this work unit.

## Question and prediction

Can localized label-to-amount evidence recover legitimate totals lost by the whole-line parser without accepting unrelated numbers, and can targeted verification add correct completions without additional wrong acceptances at lower measured cost than always checking? Prediction: some v7 abstentions reflect the shared extraction contract rather than engine inability, but repair may expose additional wrong OCR values. A distinct engine is useful only if it adds competent complementary evidence. A valid result may favor the primary singleton. These are separate extraction and decision-policy questions, not a pure causal estimate of diversity.

## Setup

Development: saved OCR from v7 S0-repair-1, train40–59 only. Twenty used receipts,19 scorable. Raw OCR remains private. Replay is not new sampling. Gold is read by the evaluator only after candidate generation. Preserve original v7 artifacts and source.

Proposed fresh Q0: CORD-v2 pinned revision7f0115a4b758a71d6473b8d085751692da2fef98, train60–79,20 receipts. Reserved repair: train80–99,20 receipts, at most one justified repair. Proposed S1: test50–99,50 study-local held-out receipts, still unopened. Hash exclusion against v4/v6/v7 and all development/qualification rows is required before dispatch. Pretraining overlap and vendor independence remain unknown.

Primary P: original-image RapidOCR, pinned v7 model/runtime, with the new field extractor. Candidate checker C: Tesseract PSM6 ind+eng with the identical field contract; retaining Tesseract is conditional on qualification, not a requirement to manufacture heterogeneity. No image enhancement by default: v7 enhancement added errors without new correct answers. Each worker has fresh receipt-only state, no peer answers or labels. Config/model/input/extractor and evidence-region hashes remain required. The checker sees original pixels, not the primary's proposed number; aggregation happens afterward.

## Protocol

1. Diagnose saved OCR without recollection. Classify absent total anchors, exclusion, geometric association, numeric ambiguity and actual wrong accepted values. Publish aggregate/numeric evidence, not raw receipt text.
2. Implement a bounded spatial field parser. Start from recognized legitimate total labels, associate a numeric span on the same baseline to the right, and accept only an unambiguous exact amount. Preserve subtotal/cash/tax/quantity exclusions. Reject conflicting labels or multiple plausible amounts. Do not scan arbitrary document numbers, use gold-directed crops, repair digits using truth, or return a reference as a fallback. Compare against v7 on exactly the same saved observations, labeling the comparison development-only.
3. Freeze the extraction contract and policy before fresh qualification. Offline fixtures must cover wrong digit recognition, adjacent line contamination, unrelated amounts, duplicate evidence, conflicting labels, unsupported dissent, missing values, unknown reference and evaluator separation. Changes after qualification require a new amendment.
4. Fresh Q0 requires zero execution errors, complete journals and at least16 scorable receipts. Preserve v7 requirements: best worker >=50% correct and both families >=2 correct. Additionally, for the proposed two-worker comparison require **each selected worker >=50% correct on scorable receipts and <=1 wrong acceptance**. This is an engineering competence floor, not a safety bound. If C cannot meet it, change/repair the perception path and requalify; do not replace it with an oracle or lower the floor. Lack of complementary successes is an honest feasibility result: report it before spending on S1.
5. If Q0 passes, fresh admission precedes S1. Collect P and C once per receipt, then evaluate fixed policies on paired outputs: P alone; C alone; targeted fallback (use P when valid; call C only if P missing/ambiguous); and always-check agreement (accept only when both produce the same value). A checker-only answer can add coverage, but it has exactly one evidence source and must never be described as corroborated. Different candidates under always-check refer; never pick the minority using gold. No label-based or held-out-trained router.
6. Report both all-collected study cost and policy-used replay cost. Also compare targeted fallback to always collecting both but applying the identical fallback decision rule: identical outcomes are an intentional software control, not a new empirical benefit. P-only is the strongest low-cost baseline. This design is an operating-point comparison, **not a matched-compute causal claim**; a matched-time/call ablation must be specified and qualified before making that stronger claim.

Proposed limits: two workers per receipt,40 Q0 calls; optional40 repair calls;100 S1 calls. Zero hosted-LLM/API calls planned. One process,45s/call,30min/stage; no silent retries, outcome-dependent expansion or S2. Carry original Antsy budget forward; no new allocation or spending authority is created by the version name. Native dispatch is not implemented/admitted by this document. Fresh exclusive approved-team allocation, public immutable plan/TLDR verification, deployment/dependency hashes, lifetime ledger, pre-review and bounded qualification are mandatory before any native run.

## Metrics

Primary practical criterion on S1: more correct completions than P alone with no additional wrong acceptances; report paired differences and uncertainty rather than treating a small zero-error count as safety. Also report all-assigned outcomes, scorable correct/wrong/refer, unknown-reference acceptance, coverage, accepted-error intervals, actual tool seconds, and operational latency interpretation. Targeted versus identical-decision always-check replay measures avoidable computation exactly; it is not randomized wall-clock evidence.

Receipt is the paired unit. Report engine competence separately from extraction yield and aggregation. Diversity: same-wrong counts, co-answer agreement with denominators, shared missingness, correctness correlation (undefined where appropriate), directed rescue, unique correct contribution and oracle headroom. No N_eff claim. Distinguish P-wrong/C-correct from P-missing/C-correct: fallback only addresses the latter. Targeted fallback cannot correct a confidently wrong P and must not be sold as solving that failure mode.

Publish all-case outcome/cost charts, label-to-amount provenance diagrams and saved trace replay with truth revealed after decisions. Use the first three assigned cases prospectively; label selected error illustrations post-hoc. Bootstrap at receipt level and Wilson intervals are descriptive, with unknown vendor dependence and no multiplicity-adjusted confirmatory claim.

## Why this experiment is needed

V7 showed two distinct mistakes: forcing a strong reader to obtain weak-worker agreement suppressed useful answers; allowing a weak dissenter vetoed correct agreement. The new design first asks whether the inputs are competent, then tests a practical receipt-processing choice: when the primary cannot produce a defensible total, is another perception path worth its cost? A separate future challenge cohort is needed to test detection of confidently wrong primary totals; this fallback study cannot answer that question by construction.

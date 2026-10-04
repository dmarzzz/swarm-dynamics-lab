# Iteration 3: make the decision value testable and visible

Written 2026-10-04 before this iteration's implementation. This is a retrospective analysis plan for already observed S0 data, followed by a prospective S1 design. It is not a preregistration of the new S0 comparisons. No new model run is authorized by this document alone.

## What the experiment is for

An incident desk receives nine reports, but seven repeat one original inspection. Should software treat those as seven independent confirmations? Quorum of Mirrors asks when repeated reports or repeated agent endorsements mislead a decision, and whether keeping source ancestry helps. The incident desk is an illustrative application; the observed inputs are synthetic binary sensor reports, not operational incident data.

The engineering decision is whether to spend on more model judgments, improve provenance capture, or use a deterministic deduplication rule. Only the last option's behavior on the simple S0 grammar can be checked now. S0 used individual model calls, with no peer exchange and no swarm; the intended collective comparison remains unrun.

## Existing evidence and new feedback

Read the pulled repository at 3f684e1e4614a18d03afaa2ef2e70d6df6d809e5 and the S0-02 post-mortem. S0 passed with 29/32 correct MAP choices, two wrong, one DEFER, 14/16 repeated pairs agreeing. All three non-correct outcomes occurred on records where copied-report majority disagreed with unique-source majority; cause was not identified.

The owner finds purpose and usefulness hard to infer from current documentation. The README also contains obsolete pre-launch statements alongside completed outcomes, and the metadata describes 16 patterns without explaining that they reuse eight bit triples at two reliability settings. The new shared setup runbook requires a maintained SETUP.md, current admission evidence and research/review gates even for exploratory work. No Quorum-specific different-researcher review was found in researcher notes, reviews or tasks. A general review of another experiment is not a review of this one.

## Retrospective analysis, frozen before coding it

Use only saved QM-S0-02 manifest and response journal; never modify those files or rerun their model calls. Compute two deterministic decision references directly from each saved visible report packet:

1. Count all nine reports; choose the majority bit. This intentionally double-counts evidence.
2. Group reports by their visible root ID, reject inconsistent descendants, count each of the three roots once, and choose the majority bit. Equal reliability within a case makes this the exact independent-root MAP rule.

Do not import the original posterior/scoring functions for these calculations. Independently recompute expected root majority and native response counts, verify agreement with the frozen expected labels, verify nine reports and three roots, and retain all 32 invocations. Compare native correctness with both references descriptively. Count changes between each pair of methods; do not claim a prospectively tested treatment effect or attach population confidence intervals.

Split cases by whether report-majority and root-majority differ. This is a post-hoc diagnostic stratum defined from inputs, not a new independent sample. Report distinct bit patterns, q settings, calls and repeated pairs separately. The count-all reference's errors cannot be interpreted as a measured model without source instructions; that native comparator has not run.

## Documentation and visualization changes

Lead with the question, an illustrated three-source/nine-report example, and the design decision the evidence can inform. Separate measured native outcomes, deterministic recomputation, and future claims in every table. Remove contradictory preparation text from the current overview; link historical plans and post-mortems instead. Preserve frozen outcomes and receipts.

Build an offline case explorer from the saved 32 records. Show each report's origin, the nine-report vote, the three-root vote and both actual model responses. Label the source grouping overlay as visible full lineage in S0, not inferred ancestry. A selector covers every case; no favorable-only gallery. Display the 24-versus-8 agreement/conflict split only if the calculation confirms it. Use response order as an index, not a social interaction animation. Validate counts against saved receipts and inspect the actual rendered page.

## Prospective design change

S1 must add the missing comparison before any efficacy claim: paired balanced (3,3,3) versus skewed (7,1,1) repetition crossed with full/partial ancestry and standard/source-aware instructions, five judges and two rounds. Retain round-0 no-discussion decisions, a pooled two-call solver and deterministic references. The request/response contract must preserve raw choice scores; do not present them as calibrated probabilities of world truth.

A six-world feasibility allocation fits the existing monetary ceiling with conservative full-context reservations (6 x 88 = 528 new requests; 560 including S0). It is a pilot with weak precision, not a powered efficacy estimate. Its complete prospective specification is S1-PLAN.md. It cannot launch until the current setup record's research/review and runtime gates are met. Do not hold a machine while those gates are open. The review should decide whether this bounded comparison is worth running before a larger semantic or operational corpus.

## Acceptance for this iteration

The old data reconcile without edits; fresh references have known-answer and corruption tests; the overview says what was actually done and what remains unknown; the explorer exposes every case with correct counts; evidence metadata distinguishes eight reused patterns, two q settings and 32 calls. Complete SETUP.md, create one different-researcher design review task, and preserve exact next actions. Do not claim S1 execution when admission evidence is missing.

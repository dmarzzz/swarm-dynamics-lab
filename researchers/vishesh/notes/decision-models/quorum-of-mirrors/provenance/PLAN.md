# Provenance gate: verify acquisitions before counting votes

2026-10-04. Prospective engineering extension, written before implementation. Status: offline development only; no model experiment or new native attempt admitted. Previous native result Q1-02 remains 0/8 graded correct. D1 stays parked.

## TLDR

Close the practical gap between a claimed source label and an authenticated acquisition. Compare counting declared labels with a gate that resolves every report through an authoritative receipt registry, checks observation integrity, and counts unique acquisition IDs. Use adversarial software fixtures to verify alias attacks, altered values, absent receipts and contradictions. A failed gate abstains and identifies missing evidence; it never reconstructs ancestry from agreement. This tests code invariants, not real authentication, model capability or swarm efficacy.

## Question and prediction

Can the engineering baseline avoid treating renamed copies as independent observations while preserving correct decisions with complete valid receipts? Predict the gate will preserve the original exact-MAP rule on valid evidence, collapse aliases to one acquisition, and refuse inconsistent or unsupported evidence. This addresses a documented assumption gap, not an execution error in the previous native run.

## Setup

Three independent binary acquisitions, equal reliability q in (.5,1), equal truth priors. Actor-facing report fields are declared_root, receipt_id, value and q. The externally authenticated registry maps receipt_id to acquisition_id, value and q; multiple receipts may refer to one acquisition. Trust in that registry is an explicit upstream requirement: no cryptography, signature validation or real-world independence is established by this module. Registry entries with the same acquisition must agree.

Source labels supplied by report authors never establish independence. The gate requires exactly three verified acquisitions before applying the previous exact rule. Missing, malformed or inconsistent evidence returns DEFER with a fixed reason; it does not drop suspicious reports and silently change the denominator. Missing-receipt identifiers are exposed as lookup candidates only, not automatically trusted. DEFER means insufficient admitted evidence, not a fourth hidden truth state.

## Protocol

1. Preserve the previous immutable analysis and native artifacts. Implement a separate gate and adversarial unit fixtures.
2. Demonstrate a label-alias counterexample: identical report text/labels is compatible with different hidden source histories and therefore different source-MAP targets. This is a constructed identifiability example, not a claim about the actual Q1 packet. More readers cannot recover absent provenance.
3. Verify no-op behavior for valid receipts, invariance to arbitrary repeated copies and report ordering, consistent alias collapse, forged values/reliability, missing receipts, inconsistent registry entries, malformed data and insufficient unique acquisitions.
4. Render a labelled developer-example table and record all fixture outcomes. These are not preregistered native data or new experimental samples.
5. Update the practical decision and next-run readiness. No machine, model calls, qualification retries or automatic successor.

## Metrics and interpretation

Check exact expected decisions and refusal reasons; compare the declared-label rule and verified-acquisition rule on the constructed attack. Finite test cases supply regression coverage, not statistical precision or world n. Use a separate independent likelihood-product reference from the previous audit for the downstream binary rule. No pooling with S0/Q1 and no new confidence score.

Support: adopt receipt validation before exact arithmetic within this scope. Failure: repair the gate offline; do not buy model calls to repair deterministic bookkeeping. Inconclusive real-world provenance: abstain or request externally verifiable receipts. A model may later help retrieve/map natural-language receipts, but that requires a separate task where authenticated evidence is available and exact lookup/string matching is insufficient. No model inference is justified merely to guess missing origins.

## Requirements for a useful later native run

A candidate must supply independently adjudicated report-to-receipt mappings, ambiguous paraphrases and same-wording independent acquisitions, an abstention class for genuinely unavailable provenance, a held-out collection separated by acquisition family, and strong exact-lookup/string-matching baselines. Define coverage versus false-independent-admission loss, price each additional verification, and demonstrate headroom on development cases before freezing any model comparison. These are unmet design requirements, not a new researcher sign-off or generic permission request. No such corpus or qualified semantic resolver currently exists in this study.

## Resources and stopping

Local offline fixtures only: zero native calls, no cloud allocation, no credentials, no ledger mutation. Original cumulative $1 API/$1 infrastructure authority and all historical exposure remain unchanged: 49 dispatches/$0.065856 reserved, $0.00171696 known API actual plus $0.001344 bounded unknown. Estimate 20–40 minutes implementation and 10–20 minutes analysis/reporting; no new experimental agent-hours are inferred. Stop this cycle after validated gate, evidence table, updated setup and push.

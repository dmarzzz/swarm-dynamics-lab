# Iteration: claimed labels need a provenance gate

**Implemented and validated an evidence-admission gate; no new native run.** The old exact rule is correct within its declared assumptions, but a claimed label is not proof of a separate acquisition. This cycle addresses that robustness gap without pretending another model can infer missing origins.

## What changed

The new [gate](gate.py) requires an upstream assertion that the receipt registry has been authenticated. It resolves reports to acquisition IDs, verifies their value and reliability against the receipts, collapses aliases, and applies exact MAP only with three consistent acquisitions of equal reliability. It never uses the report author's declared root as evidence of independence. Missing receipts, altered observations, contradictory registry entries, unsupported source counts or invalid input produce a fixed-reason DEFER. Even when three valid acquisitions are present, an additional unsupported report causes refusal rather than silently dropping it.

This module **does not authenticate signatures or establish statistical independence**. A fabricated registry or common-cause dependence can violate its upstream assumptions. It is a local mapping/integrity check, not a production provenance service or a demonstration on real incident data.

## Concrete failure and verified behavior

A constructed nine-report packet has seven ONE reports from one acquisition and two ZERO reports from two different acquisitions. A dishonest labeling splits ONE copies between two labels and merges the ZERO reports under one label. The previous three-label rule then returns ONE; the actual three-acquisition MAP target is ZERO. With the supplied authoritative receipts, the new gate returns ZERO.

Without those receipts, identical visible values and claimed labels also fit a second world: two independent ONE acquisitions and one repeated ZERO acquisition, whose MAP target is ONE. These opposite answers are compatible with the same untrusted packet. This is a constructed missing-information example, not a claim that the original Q1 fixtures have this property. Repeating readers or adding a committee cannot identify an unobserved source history from those inputs alone.

The [six developer examples](examples.html) show valid evidence, malicious label splitting/merging, altered observation, missing receipt, inconsistent registry, and absent authentication. [Machine-readable outcomes](examples.json). All are conspicuously labelled software fixtures, never native evidence.

**Fourteen new tests pass**, covering all eight binary patterns under four copy-count shapes in both orders, alias collapse, malicious relabeling, missing/contradictory evidence, malformed inputs, upstream trust, and mutation safety. The previous likelihood-based audit's nine tests also pass. These 23 tests are software checks; no population precision or native success rate follows.

## Evaluation against the run-quality criteria

| Dimension | Disposition |
|---|---|
| Question/usefulness | The actionable improvement is verifying source mappings before exact arithmetic. Native semantic-source resolution remains a separate, unprepared question. |
| Scenarios | Added explicit false-source, merged-source, missing-receipt and tampered-value developer cases; no natural corpus or realistic independence certificate. |
| Controls | Compare declared-label arithmetic with authenticated-receipt mapping plus the same exact arithmetic; no model performance attributed to either. |
| Capability | Historical Q1-02 still fails 0/8 graded; no revised reader or swarm is qualified. |
| Measurement | Exact expected choices and refusal reasons; DEFER is a gate outcome, not evidence of superior model accuracy. |
| Sample size/precision | Finite adversarial regression cases and exhaustive bit patterns; no new independent acquisition-world sample. |
| Agent context | No experimental actor instantiated; operating conversation never enters an experimental payload. |
| Integrity | All historical evidence remains unchanged; new artifacts explicitly describe developer fixtures. |
| Resources | Zero new API calls, machine allocations, credential access or ledger mutations. |
| Reproducibility | Prospective plan preceded code; deterministic examples and tests reconstruct outputs. |
| Visualization | Complete six-case table separates unsupported/abstained decisions from verified arithmetic and names upstream limits. |

## Next-run readiness and stop decision

A useful next *native* comparison would ask whether a model can map ambiguous natural-language reports to authenticated acquisition receipts better than exact lookup/string matching, without falsely admitting independent evidence. That is something the current arithmetic cannot do. It needs an independently adjudicated corpus, difficult same-wording-independent and paraphrased-copy examples, missing-provenance abstention cases, and held-out acquisition families. Score useful resolved coverage jointly with false independence admissions and verification cost; qualification must test that actual contract.

Those dataset, baseline-headroom and semantic-qualification requirements are not yet established. Generating a few templated paraphrases and calling them a fresh real-world holdout would repeat the usefulness/precision problem. Therefore no native scope is frozen, no new model run is queued, and no machine is allocated this cycle. This is a specific design-readiness limit, not an owner-budget or researcher-review wait. D1 remains parked and M1/C1 remain unrun.

## Cost and historical result

Latest native attempt QM-Q1-02 remains **16 assigned / 16 started / 16 valid, 0/8 graded correct**, with eight partial-lineage cases ungraded. New native counts are **0/0/0**. Historical exposure is unchanged: **49 calls / $0.065856 reserved**, **$0.00171696 known API actual**, plus the separately bounded **$0.001344** unknown parent charge. No reset or refund. Earlier infrastructure and release receipts remain historical records; this local cycle makes no new live fleet assertion.

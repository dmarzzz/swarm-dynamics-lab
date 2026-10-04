# Analysis, reporting and replication checklists

## Every attempt, including pilots

- [ ] Read the preceding post-mortem and unresolved repair ledger.
- [ ] Complete and commit the [pre-run assessment](templates/pre-run.md).
- [ ] Before a paid batch, record the immutable assignment manifest, exact call/spend reservation, required independent review, authorized allocation and visualization mapping; verify the registered public plan. A portfolio recommendation is not launch authorization.
- [ ] After execution, reconcile all assignments and write the [post-mortem](templates/post-mortem.md).
- [ ] Diagnose, repair and rerun defects under the [run-review cycle](RUN-REVIEW.md); link acceptance evidence.
- [ ] Preserve failed attempts and valid negative results; do not advance with unresolved qualification failures.
- [ ] Record blockers and resumable next actions when existing authorization or resources are insufficient.

## Before collecting confirmatory data

- [ ] The research question, target population, estimand and smallest useful effect are explicit.
- [ ] Unit and interference boundaries are correct; agent/turn counts are not substituted for worlds.
- [ ] N, G, S and R are explicit; identities, stateful agents and worker slots are distinguished.
- [ ] Exact models, prompts, tools, memory, topology, orchestration and evaluator are frozen.
- [ ] All corresponding baseline contexts match; treatment differences are machine-readable.
- [ ] Development, pilot, test and external-validation data are separated.
- [ ] Baselines received credible tuning and the declared resource allowance.
- [ ] Sample size reflects pilot uncertainty, task coverage, clustering and intended analysis.
- [ ] One primary contrast/interaction and joint utility guardrails have justified margins and adequate planned precision; fixed-total and per-agent panels remain separate.
- [ ] Schedule, named seed streams, stopping, retry and missing-data rules are fixed.
- [ ] Reset, no-leakage, budget, fault-injection and protected-grader checks pass.
- [ ] Logs cannot emit credentials; providers consume credentials locally by alias.
- [ ] Human oversight, licenses and data permissions fit the proposed use.

## Analysis

- [ ] Join results to every planned run; explain discrepancies and duplicate attempts.
- [ ] Keep failed, timed-out and unscored runs visible with stated denominators.
- [ ] Preserve pairs, scenario clusters, task weights and persistent-agent dependence.
- [ ] Use scenario-level or hierarchical uncertainty appropriate to the target population.
- [ ] Report absolute effects and CIs against a practical threshold, with raw counts.
- [ ] Check distributions, variance components, tails and subgroup heterogeneity.
- [ ] Apply the declared multiplicity correction and sequential procedure.
- [ ] Audit grader drift, disagreement, bias and treatment-dependent errors.
- [ ] Show sensitivity to missing outcomes, exclusions, weighting and evaluator choice.
- [ ] Report all-assigned bounds and labeled complete-case sensitivity; acquisition failures remain assigned outcomes.
- [ ] Distinguish instrument/qualification failure from valid adverse findings; an imprecise estimate below target is inconclusive, not automatic futility.
- [ ] Distinguish exploratory analyses, post-hoc selection and protocol deviations.
- [ ] Include costs of development, all candidates, retries, orchestration and evaluation.

## Report structure

1. Claim and boundary; why it matters; one primary effect with its uncertainty.
2. Related evidence, strongest contrary evidence and novelty limits.
3. Protocol, population, sampling, experimental unit, assignment and controls.
4. System and environment definitions sufficient for reconstruction.
5. Measurement, evaluator validation and contamination safeguards.
6. Run accounting and flow: planned → started → terminal → graded → analyzed.
7. Results: scenario distributions, paired effects, reliability and efficiency.
8. Mechanism evidence with ablations; separate observation from causal attribution.
9. Deviations, failures, human intervention, limitations and alternative explanations.
10. Replication instructions, artifacts, hashes, licenses and unavailable components.

## Independent replication

- [ ] Obtain a frozen release; verify content hashes before executing.
- [ ] Recompute scores from recorded events and regenerate all tables.
- [ ] Reconstruct initial contexts and confirm declared treatment diffs.
- [ ] Run scripted positive/negative controls and environment API checks.
- [ ] Test clean-state isolation, access restrictions and fault handling.
- [ ] Conduct fresh runs on the same specification if models remain available.
- [ ] Report provider changes and actual differences instead of silently substituting.
- [ ] Test a held-out task family or independent implementation as a separate extension.
- [ ] Compare effect direction, magnitude and interval to the original; do not require identical p-values.
- [ ] Publish null and failed replications with enough provenance to diagnose disagreement.

- [ ] Update `evidence_confidence` and `sample_size_summary` using the [shared rubric](../../EVIDENCE-METADATA.md); retain independent units, planned/observed counts, cohort boundaries and assessment provenance.

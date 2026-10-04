# Annotation, scenarios and acceptance specification

Telephone T0 · prospective specification, 2026-10-04. Not an implemented evaluator or labeled corpus. [Plan](PLAN.md).

## Separate four judgments

| Judgment | Labels / required evidence | What does not establish it |
|---|---|---|
| Claim meaning | Entity, predicate, value/unit, time, scope, modality, attribution | Embedding similarity or a shared keyword |
| Source support | Supported, contradicted, unknown; exact evidence spans/record IDs | An apparently credible speaker or valid-looking citation |
| Transmission link | Verified explicit reference; evidenced access without proven reuse; similarity-only candidate; unknown | Same wording, temporal proximity or co-presence alone |
| Historical visibility | Available, unavailable, unresolved at the cutoff; evidence for recipient access | Export-time roster, room membership or current goal fields |

Verified reference means the source resolves and the relationship is evidenced. It does not establish independent corroboration, factual correctness or that no other source influenced the output. Never turn a claim graph into a causal influence graph by changing edge labels.

## Private annotation record

For each component retain: dataset revision; source file/projection digests and digest scope; task/window IDs; UTC start/cutoff/end; scaffolding regime; connected dependency keys; split and exposure history; inclusion/exclusion decision; available and unavailable source records; visibility/privacy review references.

For each atomic claim retain: opaque claim ID, source record/span, actor-local timestamp, seven meaning fields above, support label and sufficient evidence sets, critical/noncritical designation, admissible unknown state, source-link category and rationale, later correction if observed, and separate annotation-pass judgments. Annotate null for absent fields; do not infer quantities, dates or attribution from evaluator knowledge.

For replay scoring retain: input/output hashes, arm/hop ID outside actor payload, critical obligation outcomes, added-assertion judgments, citation validity, mutation categories, reviewer disagreement and final disposition. A prediction file contains no gold labels. Raw source records and annotations containing excerpts remain private.

## Adjudication sequence

1. Establish source meaning and availability before viewing generated outputs. Record source ambiguity rather than forcing a binary fact.
2. Freeze a 3–6 obligation inventory per selected component. Include task-relevant qualification; do not reward arbitrary detail copied from a long source.
3. Perform a second pass blind to the first labels where feasible, with an interval and shuffled IDs. Record whether the same person made both passes. Disagreement rates are within-annotator stability unless another annotator actually participates.
4. Resolve disagreements from evidence; leave unresolved targets unknown or exclude them prospectively with reasons. Preserve the original labels and changes.
5. Freeze S0/S1 gold before arm generation. Later discovered label errors invalidate affected scoring pending a documented correction, not selective deletion of inconvenient treatment outputs.

A critical obligation counts as preserved only if the output entails it with the correct scope/time/status. Contradiction, unsupported strengthening or omission fails that obligation. Added correct details do not compensate. Duplicate assertions count once by semantic claim ID; different unsupported claims remain separately counted. Split compound sentences into atomic assertions; report uncertain segmentation.

## Concrete scenario families

All examples below are **original illustrative fixtures, not Village observations**. They are to be adapted only after real evidence is adjudicated.

| Family | Source → retelling | Intended distinction | Matched control |
|---|---|---|---|
| Qualification lost | “May work; not yet tested” → “Works” | Unsupported certainty | Preserve “untested”; cosmetic wording change does not fail |
| Attribution shifted | A tested latency; B declined review → B validated the tool | Wrong actor/action binding | Same claim with correct tester attribution |
| Scope expanded | Two tested examples passed → All cases pass | Unlicensed generalization | Exactly two examples passed |
| Time made current | A prior-day success → Current deployment is healthy | Stale-state assertion | Explicitly dated historical report |
| Correction dropped | Initial count 12 corrected to 9 → 12 retained | Failure to preserve supersession | Preserve final count and mark prior value superseded |
| False independence | Two messages cite one receipt → Two confirmations | Corroboration inflated | Two independently evidenced acquisitions, if actually established |
| Missing evidence | Link unavailable → Report endorsed | Guessing from absent support | Explicit unknown with missing-link reason |
| Source correct, copy distorted | Resolved link points to a failure → Retelling says success | Origin resolution versus entailment | Faithful paraphrase of the same linked source |

Do not remove necessary evidence simply to make a parser lose. An answer-changing pair modifies evidence or meaning; an answer-preserving variant changes order/aliases/wording without changing information. Variants stay in the same component and split. Include ordinary successful transmission and accurate uncertainty, not only spectacular failures.

## Acceptance tests to implement

- Future corrections, later row updates and private goals cannot enter pre-cutoff packets; same-time ambiguity fails closed without an ordering receipt.
- Gold/family/arm metadata mutations leave delivered source payloads unchanged; opaque IDs reveal no labels.
- Exactly copied supported facts pass; wrong entity, unit, polarity, date or certainty fails the appropriate obligation; safe unknown passes only when warranted.
- Fabricated citations, dangling origins, repeated evidence counted as independent and similarity-only causal links are rejected.
- Missing model output differs from wrong output; downstream hops of a failed chain remain unavailable and all assignments reconcile.
- Baselines see the same evidence where the comparison claims parity. Retrieval access and oracle annotations are explicitly marked advantages.
- A scorer reproduces hand-calculated fixture outcomes; errors and adjudication disagreements are retained. No automated judge is treated as infallible.

The shared 21-test packet suite is a dependency, not proof these Telephone-specific tests already pass. The actual multi-hop runner and claim-field evaluator remain unimplemented.

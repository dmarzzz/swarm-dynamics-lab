# Concrete hackathon scenarios for the research questions

For the language-agent track, start with **choosing an API from distributed evidence**, **reviewing and repairing a shared result**, or **curating a supported research bundle**. They connect directly to the user's examples, support bounded data and inspectable outcomes, and reuse much of the same evidence, logging and evaluation infrastructure. Choose one primary scenario and one research contrast first.

This contribution maps **every one of the 214 current atlas questions** to **one to three ranked scenarios**. It also maps all 54 VX/PX extensions, all sixteen original briefs and the seventeen standalone design/hunch/fork-merge records covered by the previous review: **301 records in total**, with overlap explicitly retained. There are no registered hypothesis files in this snapshot. None of these rankings promotes a hunch through the lab's research gates.

Read the [complete ranked map](ranked-map.md), [nineteen bounded scenario contracts](scenario-kits.md), [workload evidence](workload-evidence.md), or [searchable offline view](review.html). [Structured mappings](scenario-map.json) retain each atlas question's original test, metrics, confounds, falsifier and prior-work records. [Inventory](inventory.json) freezes source identities and hashes. The [checker](check_map.py) verifies coverage and links.

## The three strongest starting scenarios

These are editorial recommendations for the LLM-agent research program, not measured industry popularity or the three most frequent tags in the entire atlas.

| Rank | Task and minimum build | Why it is interesting | Best initial question | Main complexity and scope cut |
|---|---|---|---|---|
| 1 | **Choose an invoice-extraction API.** Three fictional providers, twelve short evidence records, explicit constraints, and a small investigator team. | Agreement can be wrong when many reports share one source; a private observation can change the feasible choice. The correct decision is computable. | **SEC-03 / SOC-01 / SOC-07:** does provenance-aware aggregation or private judgment improve choices under copied versus independent evidence? Choose one contrast initially. | Small fixture and deterministic evaluator. Freeze documents and mock tests; no live vendor selection or procurement. |
| 2 | **Review and repair a shared result.** Build an extraction/benchmark table from synthetic records; inject one erroneous contribution and inspect its dependent conclusions. | A group must contain a bad contribution, preserve correct work and recover without reimporting stale state. This is a concrete immune-response endpoint. | **SEC-06 / SEC-07 / SEC-48:** does the existing targeted-repair protocol improve durable recovery over its declared comparator? | Small core, medium if many memory layers are included. Start with one route and one state representation; reuse the existing immune protocol. |
| 3 | **Curate a research evidence bundle.** Select at most five resources from a frozen annotated corpus to support five requested claims. | Search, routing, synthesis, contradictory evidence and citation checking are natural multi-agent operations. Useful evidence is not the same as popular or repeated evidence. | **SOC-04 / SOC-08 / SOC-21:** does routing by missing evidence, completeness-aware stopping or a memory policy improve verified coverage? Choose one. | Medium because labels take work. Start with a frozen corpus and claim-support annotations; do not promise an objective universal ranking of papers. |

Counts, worker numbers and fixture sizes are planning choices, not power calculations. When reusing an existing protocol, its frozen agent counts, arms and schedule take precedence over these illustrative kit sizes; document any change as a new protocol version. The planning envelope is one small team and one to two hackathon days, with existing model access assumed for any later LLM pilot. No paid run or training is authorized or executed by this mapping.

**Coverage:** API is the first choice for 25 atlas questions, RESULT for 11, and RESEARCH for 11: **47 of 214 first choices**. At least one of these is among the ranked options for **80 of 214**. This is a union over IDs, not a sum of overlapping tags. They do not cover all mechanisms. Budget allocation is a strong next module and the first choice for twenty questions; if the team selects the budget track, use BATCH before building a research-curation interface.

Physical-swarm questions have direct simulation choices, including beacon navigation, bottlenecks and explicit oscillator models. Optimizer questions use known objective functions. MARL, NCA, radio fingerprinting, attestation and weight-merging questions can require artifacts or fidelity that are not available from a generic language-agent demo. Their conditional status is visible in the map.

## How the ranking was made

Rank **within each question**, in this order:

1. **Preserve the mechanism.** The scenario must vary the quantity the question actually asks about. Report merging cannot substitute for weight merging; detecting bad content cannot establish malicious intent.
2. **Make the answer scoreable.** Prefer executable truth, independently reviewed labels, observable end state and declared uncertainty over a persuasive judge narrative.
3. **Fit a bounded implementation.** Prefer fixtures, a small action vocabulary and existing interfaces. Mark missing checkpoints, training infrastructure, physical models or annotations as dependencies.
4. **Exercise a useful workload.** Prefer research synthesis, tool decisions, artifact verification, handoffs, customer-service policies and resource allocation where they genuinely fit. These are documented examples or proposed adaptations, not a prevalence survey.
5. **Reuse without changing the claim.** Sharing an event schema and evaluator is useful; forcing every mechanism into one story is not. Prefer a visual that exposes evidence or a failure to an elaborate world with weak scoring.

The first choice has the best combined fit under these assumptions. A second or third is a transfer domain, a more familiar workflow, or a narrower diagnostic—not another task that must be built. Conditional options are not made feasible just by ranking first. A medium-scope task with a direct mechanism can outrank a small task that answers the wrong question.

## Three concrete demonstrations

### API choice with copied evidence

The team must choose a provider that satisfies all mandatory requirements, then minimize a declared cost/quality objective. Each investigator sees a different part of the same fixed evidence union. Several seemingly independent recommendations can descend from one unreliable benchmark; an independent test can contradict them. The evaluator knows the actual provider table, while agents see only their declared observations.

Compare the chosen aggregation rule with independent voting and a shared blackboard at equal total resource limits. Report feasible-choice rate, regret, false commitment, delay, justified abstention and all consumed resources. Include true copied evidence, false independent evidence, ties and no-feasible-provider cases. These prevent a rule that simply distrusts repetition from winning by construction. A centralized single-agent baseline receives the same available evidence union under the same total cap; exceeding its capacity is a different, separately labeled question.

Use the [existing external-influence design](../seo-poisoning/experimental-design.md) and [private-judgment design](../../../dmarz/notes/soc07-private-judgments/README.md) where their contrast applies. Do not splice their arms or sample plans into a new purported preregistration.

### Shared-result repair

Workers construct a table from synthetic source records. A wrong cell influences a subtotal and a recommendation; a later correction may update only the cell, leaving derived results or a stale worker unchanged. The team must restore correct output and continue useful work. A separate clean case contains a legitimate minority contribution that the defense should preserve.

Use the [existing immune-response experiment design](../swarm-immune-response/experiment-design.md) for the treatment schedule, primary comparison and outcome definitions. Begin with one artifact and one contamination route. Maintain evaluator-only lineage and truth; detectors do not receive those labels unless the condition is explicitly an oracle ceiling. Count recurrence, lost correct knowledge, unnecessary exclusion and total verified work. A red alert or removed message is not the recovery outcome.

The target is **harmful contribution, incorrect claim or unauthorized action under a defined task**, not “is this agent aligned?” The evaluator may know a synthetic attack was planted, but observed behavior alone can be identical to an honest mistake. Score intent attribution only if the available evidence actually identifies it, otherwise report unknown. Real-world personalities or operators are outside the task.

### Research resource curation

Ask a narrow question with several required factual facets. Give workers a frozen mix of primary papers, first-party technical posts, redundant summaries, off-topic material and contradictory findings. Return a short bundle with a claim-to-source matrix and explicit unanswered facets.

Build the label set independently of the tested curator. Where relevance is subjective, allow graded labels and several valid bundles. Score factual support, coverage, unsupported conclusions, unnecessary duplication and resource use separately. Keep publication prestige and recency distinct from whether the source supports the claim. Hold out source families and topics after tuning; a fixed list of favorite resources is not an adequate evaluator.

Start with the corpus in fixtures. A later live-web transfer adds retrieval drift, inaccessible sources and publication permissions; it should not silently replace the controlled experiment. Reuse source IDs and provenance from the lab library, but do not treat catalogue metadata as a full-paper reading.

## What to implement first

1. Freeze the chosen question, its original falsifier, one task contract and the information-access matrix.
2. Create a few hand-audited fixture worlds covering clean success, plausible failure, missing evidence and an adversarial/rare case. These are debugging cases, not a powered evaluation set.
3. Implement the deterministic scorer and trivial baselines before calling a model. Confirm that a correct solution is reachable from allowed observations, or label the case intentionally unresolvable.
4. Adapt the [existing harness contracts](../../../../tooling/agent-experiments/README.md) for IDs, event logs, costs, replay and outcomes. The current toy harness is scripted bookkeeping, not an already implemented API/research/immune agent environment.
5. After the applicable survey/hypothesis gates and resource authorization, run a small qualification pilot, freeze independent evaluation worlds and perform the declared comparison. A later sample size must come from the outcome and pilot variance, not the fixture count in this note.

Use whole task worlds or teams as the randomized units; retain failed, interrupted and unfinished trials. Do not let evaluator truth leak through document IDs, source ordering, router inputs, stop rules or UI colors. Show individual trace replays for explanation and all-world outcome distributions for evidence.

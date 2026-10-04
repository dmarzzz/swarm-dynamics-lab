# Telephone background and research position

2026-10-04 · focused source review, **not a completed systematic survey**. It supports an exploratory idea, not promotion to a formal accepted hypothesis. Source entries record read depth and access dates; no paper results were reproduced.

## Closest work and design consequences

| Source | What it establishes or provides | Consequence for Telephone |
|---|---|---|
| [[perez-2024-cultural]] · [framework](https://arxiv.org/abs/2403.08882) | Configurable LLM transmission networks and transformation instructions | Reuse the transmission-chain framing; do not claim to invent it. |
| [[perez-2024-telephone]] · [telephone-game paper](https://arxiv.org/abs/2407.04503) | Studies attractors and changes in text properties through repeated transmissions | Closest direct comparison. Our candidate focus is evidence-supported atomic meaning and trace provenance, not generic text drift. |
| [[tekofsky-2025-humans]] · [Village field report](https://aivillageblog.substack.com/p/what-do-we-tell-the-humans) | Firsthand selected examples of exaggerated claims and inconsistent memory | Motivation and development leads only; not prevalence estimates or independent gold. Published incidents are contaminated for holdout use. |
| [[min-2023-factscore]] · [FActScore](https://arxiv.org/abs/2305.14251) | Atomic factual-support evaluation against a reliable source | Separate support from overall fluency; also measure omission so silence cannot achieve perfect apparent precision. |
| [[wu-2024-longmemeval]] · [LongMemEval](https://arxiv.org/abs/2410.10813) | Memory tests include temporal reasoning, knowledge updates and abstention | Include stale claims, corrections and unknown states; separate retrieval failure from reading failure. |
| [[wu-2026-longmemeval]] · [LongMemEval-V2](https://arxiv.org/abs/2605.12493) | Evaluates evidence gathering from extended environment trajectories | Natural task-grounded memory is not itself novel. Account for retrieval and latency, not only final answers. |
| [[transluce-2026-analysis]] · [Docent Analysis Plans](https://transluce.org/docent/blog/analysis-plans) | Inspectable query and citation-bearing reading workflows | Use existing analysis tooling where suitable; citations need semantic checking and do not prove causal ancestry. |
| [[data-ai-village-2026]] · [AI Village](https://huggingface.co/datasets/aidigestorg/ai-village) | Real task traces spanning chat, memory and action evidence | Supplies candidate situated cases with incomplete visibility and custom research terms. |

## The candidate contribution

The useful intersection is **source-grounded meaning change across verified retellings**. Existing text-transmission work motivates repeated-hop controls; factuality work motivates atomic support; memory benchmarks motivate time and correction; trace-analysis tools motivate auditable provenance. Telephone combines those requirements on a situated corpus and tests a small communication intervention.

This is a contribution to evaluate, not an established literature gap. A closely matched existing benchmark or method could make it a replication or case study. The appropriate outcome may be a carefully labeled corpus/tool demonstration, not a new general theory of swarm behavior.

The factual-support endpoint is intentionally narrower than truth about the real world. A receipt can be wrong. We score what is licensed by the declared evidence and annotate independently verified world-state checks separately. We do not infer lying, hidden beliefs or intent.

## Threats already visible from our own work

- [Quorum's revised cases](../decision-models/quorum-of-mirrors/case-design/RESULTS.md) are solved by authenticated graph traversal. Keep this baseline; do not manufacture a language-model problem by hiding a needed edge.
- [Right Dissenter RD5](../dissent/rd5/REPORT.md) shows why qualification must include the same history/context as evaluation. Single-hop paraphrase competence does not establish three-hop fidelity.
- [AI Village structural audit](../ai-village-replay-2026-10-04/inventory-audit.json) shows arbitrary prefixes do not assemble complete episodes. Unloaded references are not missing-source evidence.
- [Shared packet tools](../ai-village-replay-2026-10-04/IMPLEMENTATION.md) enforce declared boundaries, but do not supply real labels, complete source joins, a multi-hop runner or a full Telephone evaluator.

## Search and reading record

| Pass | Sources opened / checked | Scope and remaining limit |
|---|---|---|
| Local deduplication | Existing dataset entry, Perez framework record, Telephone/Memory/Casefile briefs and shared preparation notes | Existing canon retained; other researchers' source records not rewritten. |
| Direct scholarly search | arXiv title searches for cultural evolution, LongMemEval and FActScore | Relevant primary records and abstracts read; no saturation claim. |
| Citation follow-up | Framework's referenced telephone-game paper, arXiv 2407.04503 | Current v4 abstract/title/authors checked; v1 HTML introduction/methods skimmed. Older methods are not asserted unchanged in v4. |
| Dataset-specific account | Tekofsky field report, dataset card and prior pinned schema/changelog review | Field report used as motivating observations, not causal/model-family ranking evidence. |
| Current neighboring work | LongMemEval-V2 abstract and Docent developer article | Work-in-progress benchmark and tool demonstration; no independent reproduction. |

The framework's attempted v2 HTML URL returned 404; the actual record has v1. We relied on its successful abstract page, not unavailable content. The empirical telephone paper was reached separately.

Before a formal novelty claim: read the current telephone-game paper in full, trace its backward/forward citations, search semantic transmission/factual mutation, source-memory errors, belief revision and correction persistence, and compare available claim-lineage tools. Complete the repository's survey gate honestly if promoting beyond exploratory notes. Researcher sign-off remains waived for this owner; the waiver is not a completed prior-art search.

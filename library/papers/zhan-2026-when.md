---
id: zhan-2026-when
type: paper
title: 'When Memory Becomes Authority: Benchmarking Authority Collapse at the Memory Consolidation Boundary'
authors: [Qiuyang Zhan, Rui Zhang, Sheng Guo, Lepeng Zhao, Zhuotao Liu]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2608.01679
doi: null
arxiv: '2608.01679'
cite: 'Zhan, Q., Zhang, R., Guo, S., Zhao, L., & Liu, Z. (2026). When Memory Becomes Authority: Benchmarking Authority Collapse at the Memory Consolidation Boundary. arXiv preprint arXiv:2608.01679.'
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: 5  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

Self-evolving agents consolidate raw interaction histories into reusable facts, preferences, observations and rules. The authors identify "authority collapse": consolidation keeps a claim but drops the source constraints on how it may be used. A third-party statement, for example, can become a standing instruction or an attested observation. AuthMem-Bench holds the claim and the downstream task fixed and varies only the authority of the source. Measured (abstract): authority collapse appears in 48 of 49 configurations (seven consolidators built on widely used agent-memory systems, crossed with seven LLM backbones). Collapsed memories without authority metadata produce a 50.3% mean unauthorised-action rate. Automatically predicted, persisted authority labels cut the end-to-end unauthorised-action rate from 16.9% to 0.0% with essentially unchanged benign success.

## Contribution

It locates the failure at consolidation, the step that turns experience into memory, rather than at retrieval.

## Key results

- 48 of 49 consolidator-by-backbone configurations collapse authority (abstract).
- 50.3% unauthorised-action rate from collapsed memories (abstract).
- Authority labels reduce it from 16.9% to 0.0% end to end (abstract).

## Methods and models

Paired benchmark design. Specific consolidators and backbones not read.

## Limitations and open questions

Abstract only. Whether the labels themselves can be forged by an injected source is not stated in the abstract.

## Relevance to us

Consolidation is the operation a parent performs when it merges a sub-agent, so this bears on both Q3 and Q2. The near-universal collapse (48 of 49) predicts that a naive merge, where the sub-agent summarises and the parent stores the summary, will turn what the sub-agent read on a hostile web into what the parent believes or is told to do. Q3 does not need a sophisticated injection if the merge launders authority by default. For Q2, carrying authority labels through the merge is a precondition for any threshold rule, because a k-of-n count is meaningless once source identity has been erased. The same point appears as "self-summarisation laundering" in [[louck-2026-securing]] and as "provenance collapse" in the shared-memory governance study [[margalit-2026-governed]]. [[ravindran-2026-portable]] proposes a Merkle-DAG provenance format for memory transfer that would keep source identity across a merge. Contrast the memory-architecture view in [[packer-2023-memgpt]] and [[park-2023-generative]], where reflection and consolidation are features.

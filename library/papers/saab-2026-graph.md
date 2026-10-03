---
id: saab-2026-graph
type: paper
title: Graph Feedback Controls Consensus and Clique Formation in Open-Weight Language-Model Populations
authors:
- Samer Saab Jr
- Chaouki Abdallah
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2607.12077
doi: null
arxiv: '2607.12077'
cite: Saab Jr, S., & Abdallah, C. (2026). Graph Feedback Controls Consensus and Clique Formation in Open-Weight Language-Model Populations. arXiv preprint arXiv:2607.12077 (revised July 2026).
topics:
- llm-agent-swarms
- sync-consensus
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 0 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Asks whether the routing rule that decides which agents talk to each other determines whether an LLM population converges on a shared convention or splits into persistent cliques. Open-weight agents from 1.1B to 32B parameters play a controlled naming game while the authors track emitted labels and full first-token preference distributions over allowed labels. Similarity-based routing (talk to agents like you) can isolate emerging conventions and sustain fragmentation even when every agent interacts every round. Matched controls rule out uneven participation and model-specific score preferences: random rematching and policies that connect disagreeing groups improve coordination when partner-label history is kept, but not when it is absent. Exposure alone is not enough: some mixed-model populations stay divided despite frequent cross-family contact, though the same models coordinate when homogeneous. Reaching consensus and maintaining it are distinguished. On ARC-Challenge and MMLU, routing changes how correct and incorrect answers propagate without reliably improving accuracy.

## Contribution

Treats the runtime interaction graph as a causal, feedback-controlled design variable (an adaptive network, in complex-systems terms) and shows homophilic routing produces echo-chamber cliques in LLM populations. Complements fixed-topology studies [[mehdizadeh-2026-exploring]] and [[hirota-2026-collective]] and the homophily effects in [[zomer-2026-unraveling]].

## Key results

- Claimed: similarity-based routing sustains fragmentation; bridging/random routing helps only with partner-label memory.
- Claimed: heterogeneous model populations can remain divided despite cross-family exposure.
- Claimed: routing alters propagation of correct and incorrect answers on ARC-Challenge and MMLU without reliable accuracy gains.

## Methods and models

Naming game with open-weight models (1.1B-32B), routing policies (similarity-based, random rematching, bridging), memory on/off, label and first-token distribution tracking; QA transfer experiments.

## Limitations and open questions

Abstract-level read; population sizes and number of runs not checked.

## Relevance to us

Adaptive (state-dependent) interaction networks are a core swarm-dynamics topic (e.g. co-evolving networks); this gives an LLM instance with clear controls. Related: [[ashery-2024-emergent]], [[de-nobili-2026-microscopic]].

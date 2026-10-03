---
id: torra-2026-memory
type: paper
title: 'Memory poisoning and secure multi-agent systems'
authors: [Vicenç Torra, Maria Bras-Amorós]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2603.20357
doi: null
arxiv: '2603.20357'
cite: 'Torra, V., & Bras-Amorós, M. (2026). Memory poisoning and secure multi-agent systems. arXiv preprint arXiv:2603.20357.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 4  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

A position and review paper on memory poisoning in agentic and multi-agent systems. The authors classify memory by duration, origin and location: from short-term memory that starts at the user and sits in each agent, to long-term consolidated memory held in established knowledge bases. They discuss how feasible poisoning is for each type and propose mitigations, including solutions based on cryptography. For semantic memory they suggest local inference over private knowledge retrieval. They stress that poisoning arising from interactions between agents is under-studied and hard to formalise.

## Contribution

A typology that links where a memory lives (per agent or consolidated) to how it can be poisoned. It also flags agent-to-agent memory poisoning as an open problem.

## Key results

Position paper. No measurements in the abstract.

## Methods and models

Conceptual analysis.

## Limitations and open questions

Abstract only. The authors themselves say the inter-agent case is not formalised.

## Relevance to us

Bears on Q1 and Q3 conceptually. The authors work in privacy-preserving computation, and the proposal of private knowledge retrieval is the one memory-poisoning paper in this lane that points toward hiding access patterns. A parent that fetches from its sub-agents' stores through private retrieval would not reveal which sub-agent's memory it actually consumes, which is a partial answer to Q1 (inferred, not claimed by the authors). Their open problem of inter-agent poisoning is the fork-merge question. Related: [[xiong-2026-maple]], [[lin-2026-survey]].

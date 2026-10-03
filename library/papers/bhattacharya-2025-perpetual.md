---
id: bhattacharya-2025-perpetual
type: paper
title: "Perpetual exploration in anonymous synchronous networks with a Byzantine black hole"
authors: ["Adri Bhattacharya", "Pritam Goswami", "Evangelos Bampas", "Partha Sarathi Mandal"]
year: 2025
venue: "arXiv preprint (accepted at DISC 2025)"
url: https://arxiv.org/abs/2508.07703
doi: null
arxiv: "2508.07703"
cite: "Bhattacharya, A., Goswami, P., Bampas, E., & Mandal, P. S. (2025). Perpetual exploration in anonymous synchronous networks with a Byzantine black hole. arXiv:2508.07703. Accepted at the 39th International Symposium on Distributed Computing (DISC 2025)."
topics: [fork-merge-security, swarm-robotics]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

Part of the distributed-computing literature on mobile agents exploring "dangerous graphs". A black hole is a node that destroys any visiting agent without trace (introduced by Dobrev, Flocchini, Prencipe and Santoro); a Byzantine black hole (BBH), also called a gray hole, chooses each round whether to destroy all visiting agents or behave normally, so it may never be detectable. The paper asks how many initially co-located agents are needed to perpetually explore an unknown anonymous graph with at most one BBH, either some component left after removing the BBH (PerpExploration-BBH) or specifically the component containing the home node where agents start and aggregate data (PerpExploration-BBH-Home). Results (proved): in trees, 4 agents are necessary and sufficient for the first variant and 6 for the home variant, with lower bounds holding even on paths; in general graphs, a lower bound of 2Δ-1 agents for the first variant and an upper bound of 3Δ+3 for the home variant, where Δ is maximum degree. Synchronous scheduler, face-to-face communication only, no knowledge of network size. I read the abstract, introduction and related work.

## Contribution

First study of a black-hole variant in arbitrary networks without initial topological knowledge, and a requirement-to-return variant (home component) that matches the "explore and come back to aggregate" pattern.

## Key results

- Trees: 4 agents optimal for PerpExploration-BBH, 6 for PerpExploration-BBH-Home.
- General graphs: at least 2Δ-1 agents needed; 3Δ+3 suffice for the home variant.
- A BBH that is a cut vertex can make full exploration impossible, so goals are restricted to one component.
- Related work: gray-hole periodic data retrieval needed 9 agents in rings (Královič and Miklík), improved to an optimal 4 (Bampas et al.).

## Methods and models

Graph-theoretic algorithms and lower-bound proofs; anonymous nodes, port labels, synchronous rounds, face-to-face communication.

## Limitations and open questions

The hostile node destroys agents; it does not corrupt them and send them back. Only one BBH. Gap between lower and upper bounds in general graphs.

## Relevance to us

Q2: this line gives exact answers to "how many parts must I send into hostile territory so that enough return home", for a loss-only adversary, and the home variant formalises a parent that must keep receiving returning parts. It is a lower bound on the fork budget before any corruption is considered; corruption (the companion line where some searching agents are Byzantine and collude with the black hole, Di Luna et al., ICDCS 2025, not opened) raises it. Q1: the gray hole's choice to act only sometimes is the adversary strategy of selectively hitting the parts that matter, which hiding which part returns is meant to frustrate. Related: [[minsky-1996-cryptographic]], [[yee-1997-sanctuary]].

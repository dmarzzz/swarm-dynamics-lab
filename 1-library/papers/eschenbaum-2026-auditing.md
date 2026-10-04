---
id: eschenbaum-2026-auditing
type: paper
title: "Auditing Algorithmic Collusion from Strategy Graphs"
authors: ["Nicolas Eschenbaum", "Janusz M. Meylahn"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2608.07098
doi: null
arxiv: "2608.07098"
cite: "Eschenbaum, N., & Meylahn, J. M. (2026). Auditing Algorithmic Collusion from Strategy Graphs. arXiv:2608.07098."
topics: [swarm-detection, marl-emergence]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Studies an auditor who can query firms' frozen pricing policies but has no price histories, demand estimates or benchmarks. From the queried policies the auditor builds the induced strategy graph. Using a full characterisation of Nash equilibria in a repeated pricing game, the authors identify graph features tied to reward-and-punishment schemes (maximum betweenness, attractor in-degree, average path length) and test them on decentralised Q-learning and the [[calvano-2020-artificial]] algorithm.

## Contribution

A collusion detector that reads the structure of learned policies, needing neither prices nor counterfactual benchmarks.

## Key results

- Maximum betweenness and attractor in-degree correlate strongly with the profit-based Collusion Index (abstract; correlation values not in the abstract).

## Methods and models

Repeated Bertrand pricing game; Q-learning agents; strategy graph from policy queries; graph metrics compared with the collusion index.

## Limitations and open questions

Abstract only; a preliminary draft. Needs query access to frozen policies, which regulators rarely have; tested only on tabular Q-learning.

## Relevance to us

A market-side analogue of detecting hidden coordination: infer coupling from how agents respond to each other's deviations. Relevant to LLM pricing agents in [[fish-2024-algorithmic]]. In-the-wild evidence: [[assad-2024-algorithmic]].

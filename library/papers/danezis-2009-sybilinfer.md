---
id: danezis-2009-sybilinfer
type: paper
title: "SybilInfer: Detecting Sybil Nodes using Social Networks"
authors: ["George Danezis", "Prateek Mittal"]
year: 2009
venue: "Network and Distributed System Security Symposium (NDSS 2009)"
url: https://www.princeton.edu/~pmittal/publications/sybilinfer-ndss09.pdf
doi: null
arxiv: null
cite: "Danezis, G., & Mittal, P. (2009). SybilInfer: Detecting Sybil Nodes using Social Networks. In Proceedings of the Network and Distributed System Security Symposium (NDSS 2009). Internet Society."
topics: [sybil-resistance]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "404 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

SybilInfer labels nodes in a social graph as honest or Sybil using Bayesian inference. A probabilistic model of honest fast-mixing graphs, built from traces of short random walks started at a trusted node, defines a likelihood over candidate honest sets; Metropolis-Hastings sampling returns marginal probabilities that each node is honest. Each label therefore carries a probability rather than a hard accept or reject.

## Contribution

Recasts Sybil detection as statistical inference with calibrated uncertainty, and claims an order-of-magnitude accuracy improvement over [[yu-2006-sybilguard]] and [[yu-2008-sybillimit]] under the same assumptions, at the cost of needing a large part of the social graph.

## Key results

- Authors state SybilGuard has high false negatives and SybilLimit needs the number of honest nodes; SybilInfer needs neither but requires global graph knowledge.
- Experiments on synthetic scale-free graphs and real topologies: with a threshold parameter α = 0.7, up to about 100 added Sybils can be inserted undetected; beyond that threshold all Sybils, including the compromised nodes, are flagged (Figure 3a description). α trades false positives against false negatives.
- Security argument: the adversary cannot game the detector by arranging Sybil topology, under standard attack-edge constraints.

## Methods and models

Random-walk transition model, Bayesian posterior over honest/dishonest cuts, MCMC sampling, 20 samples to estimate marginals in the reported runs.

## Limitations and open questions

Centralised view of the graph; computational cost of sampling; relies on the same fast-mixing and few-attack-edges assumptions that [[viswanath-2010-analysis]] later shows break under community structure.

## Relevance to us

A swarm coordinator or auditor with a global view of agent interaction graphs could use this style of probabilistic labelling to weight agents by posterior honesty instead of excluding them. The probability output fits naturally into weighted consensus or weighted voting among agents, similar to the per-client confidence weights in [[gil-2015-guaranteeing]].

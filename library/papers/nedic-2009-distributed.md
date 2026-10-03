---
id: nedic-2009-distributed
type: paper
title: Distributed Subgradient Methods for Multi-Agent Optimization
authors: [Angelia Nedic, Asuman Ozdaglar]
year: 2009
venue: IEEE Transactions on Automatic Control
url: https://api.openalex.org/works/doi:10.1109/tac.2008.2009515
doi: 10.1109/tac.2008.2009515
arxiv: null
cite: "Nedic, A., & Ozdaglar, A. (2009). Distributed subgradient methods for multi-agent optimization. IEEE Transactions on Automatic Control, 54(1), 48-61."
topics: [sync-consensus]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "3786 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Studies optimisation of a sum of convex (not necessarily smooth) objective functions, each private to one agent,
by a subgradient method distributed over a time-varying communication network: each agent mixes its estimate with
its neighbours' (a consensus step) and takes a subgradient step on its own objective. The paper proves
convergence and gives rate estimates that make the trade-off between accuracy and number of iterations explicit.

## Contribution

The founding paper of consensus-based distributed optimisation ("consensus plus gradient"), the template behind
decentralised SGD and gossip-based federated learning in ML.

## Key results

- Abstract: convergence and convergence-rate estimates for distributed subgradient over time-varying topologies,
  quantifying accuracy versus iterations.

## Methods and models

Consensus averaging plus local subgradient steps; analysis under connectivity and step-size assumptions.
Abstract from OpenAlex.

## Limitations and open questions

Constant step sizes give only approximate optimality (as the abstract's accuracy trade-off implies); later work
adds acceleration and gradient tracking (not catalogued).

## Relevance to us

The bridge from swarm consensus to distributed learning: a swarm that must jointly fit a model or allocate tasks
runs this algorithm. Relevant to the marl-emergence and llm-agent-swarms topics as the classical baseline for
"agents agree while optimising".

---
id: ren-2005-consensus
type: paper
title: Consensus seeking in multiagent systems under dynamically changing interaction topologies
authors: [Wei Ren, Randal W. Beard]
year: 2005
venue: IEEE Transactions on Automatic Control
url: https://api.openalex.org/works/doi:10.1109/tac.2005.846556
doi: 10.1109/tac.2005.846556
arxiv: null
cite: "Ren, W., & Beard, R. W. (2005). Consensus seeking in multiagent systems under dynamically changing interaction topologies. IEEE Transactions on Automatic Control, 50(5), 655-661."
topics: [sync-consensus]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "6630 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Studies information consensus among agents with limited, unreliable information exchange and dynamically
changing, directed interaction topologies. For both discrete- and continuous-time update schemes, consensus is
reached asymptotically if the union of the directed interaction graphs contains a spanning tree frequently enough
as the system evolves.

## Contribution

Weakened the connectivity requirement of [[jadbabaie-2003-coordination]] (undirected, jointly connected) and
[[olfati-saber-2004-consensus]] (strongly connected, balanced) to a jointly rooted spanning tree for directed
graphs, which is close to necessary and is the condition most later papers assume.

## Key results

- Abstract-level: asymptotic consensus if the union of directed interaction graphs has a spanning tree
  frequently enough; both discrete and continuous time.

## Methods and models

Stochastic-matrix products (discrete time) and continuous-time Laplacian dynamics on switching digraphs.
Abstract from OpenAlex.

## Limitations and open questions

Short technical note; no rates; linear agents.

## Relevance to us

The connectivity condition to check when swarm members hear each other one-way (for example vision-only robots
that see only those in front).

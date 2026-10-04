---
id: olfati-saber-2004-consensus
type: paper
title: Consensus Problems in Networks of Agents With Switching Topology and Time-Delays
authors: [R. Olfati-Saber, R. M. Murray]
year: 2004
venue: IEEE Transactions on Automatic Control
url: https://doi.org/10.1109/tac.2004.834113
doi: 10.1109/tac.2004.834113
arxiv: null
cite: "Olfati-Saber, R., & Murray, R. M. (2004). Consensus problems in networks of agents with switching topology and time-delays. IEEE Transactions on Automatic Control, 49(9), 1520-1533."
topics: [sync-consensus]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "12903 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Analyses linear consensus protocols for networks of integrator agents in three settings: directed fixed
topology, directed switching topology, and undirected topology with communication time delays. It proves
convergence, ties the negotiation speed of the linear protocol to the algebraic connectivity (Fiedler
eigenvalue) of the network, generalises algebraic connectivity to digraphs, and shows balanced digraphs are what
make average consensus possible. Disagreement functions serve as Lyapunov functions, including a common one for
directed switching networks.

## Contribution

The most cited single consensus paper (about 12,900 OpenAlex citations). With [[jadbabaie-2003-coordination]]
it established the field; its digraph results and the "balanced graph implies average consensus" result are
standard textbook material.

## Key results

- Abstract-level: convergence for directed fixed, directed switching (common Lyapunov disagreement function)
  and delayed undirected networks; speed set by algebraic connectivity; balanced digraphs are key for
  average consensus.
- Not read here: the explicit delay bound for undirected networks.

## Methods and models

Algebraic graph theory, matrix theory, Lyapunov analysis; simulations. Abstract from OpenAlex.

## Limitations and open questions

Single-integrator agents. The switching-topology result rests on a common Lyapunov (disagreement) function;
the per-graph assumptions this needs were not read here, and should be compared with the weaker
joint-connectivity conditions of [[jadbabaie-2003-coordination]] and [[ren-2005-consensus]].

## Relevance to us

Gives the formula-level link between topology and speed that a swarm experiment can test. See
[[olfati-saber-2007-consensus]] for the broader review.

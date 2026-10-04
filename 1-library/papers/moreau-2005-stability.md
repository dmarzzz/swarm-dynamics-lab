---
id: moreau-2005-stability
type: paper
title: Stability of multiagent systems with time-dependent communication links
authors: [Luc Moreau]
year: 2005
venue: IEEE Transactions on Automatic Control
url: https://doi.org/10.1109/tac.2004.841888
doi: 10.1109/tac.2004.841888
arxiv: null
cite: "Moreau, L. (2005). Stability of multiagent systems with time-dependent communication links. IEEE Transactions on Automatic Control, 50(2), 169-182."
topics: [sync-consensus]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "2754 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Analyses networks of agents that update their state from neighbours' current information over time-dependent
communication links, with applications to synchronisation, swarming and distributed decision making. It gives
necessary and/or sufficient conditions for all agents to converge to a common value, using a blend of graph
theory and system theory in which convexity plays the central role, formalised as set-valued Lyapunov theory.
It notes that more communication does not necessarily speed convergence and can even destroy it.

## Contribution

Extended consensus results to nonlinear, convex update rules on switching directed graphs, complementing
[[ren-2005-consensus]]; the convexity (agents move into the convex hull of neighbours) viewpoint is widely reused.

## Key results

- Abstract-level: necessary/sufficient conditions for convergence with time-dependent links; more communication
  can slow or prevent convergence in the models studied.

## Methods and models

Set-valued Lyapunov functions, convex-hull arguments, graph connectivity. Abstract from OpenAlex.

## Limitations and open questions

Deterministic; the counter-intuitive "more links can hurt" result is model-specific.

## Relevance to us

Useful for robots whose update rules are nonlinear but convex (saturated, normalised headings). The "more links
can hurt" observation is a testable surprise for a hackathon experiment.

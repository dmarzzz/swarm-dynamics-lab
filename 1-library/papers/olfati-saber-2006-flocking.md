---
id: olfati-saber-2006-flocking
type: paper
title: "Flocking for Multi-Agent Dynamic Systems: Algorithms and Theory"
authors: [Reza Olfati-Saber]
year: 2006
venue: IEEE Transactions on Automatic Control
url: https://doi.org/10.1109/tac.2005.864190
doi: 10.1109/tac.2005.864190
arxiv: null
cite: "Olfati-Saber, R. (2006). Flocking for multi-agent dynamic systems: Algorithms and theory. IEEE Transactions on Automatic Control, 51(3), 401-420."
topics: [sync-consensus, collective-motion, swarm-robotics]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "5083 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

A theoretical framework for designing and analysing distributed flocking algorithms, in free space and in the
presence of multiple obstacles. Three algorithms are given: two for free flocking and one for constrained
flocking. The first embodies Reynolds' three rules but generically leads to regular fragmentation; the second and
third lead to flocking. A multi-species framework uses flock members (alpha-agents) plus virtual beta- and
gamma-agents associated with them to build the collective potentials (beta-agents for obstacles and gamma-agents
for the group objective, in our reading of the abstract). Collective potentials penalise deviation from lattice-like configurations (alpha-lattices).
Migration needs no leader. Simulations show 2D and 3D flocking, split/rejoin and squeezing manoeuvres with
hundreds of agents.

## Contribution

The standard control-theoretic flocking algorithm ("Olfati-Saber flocking", alpha/beta/gamma agents) and a formal
definition of flocking akin to Lyapunov stability. It is the engineering counterpart to the analysis-oriented
[[cucker-2007-emergent]] and [[tanner-2007-flocking]], and a common baseline in drone-swarm work (compare the field-tested [[vasarhelyi-2018-optimized]] and
the physics model [[vicsek-1995-novel]]).

## Key results

- Abstract-level: algorithm 1 (pure Reynolds-type) generically fragments; algorithms 2-3 (with navigational
  feedback) flock; systematic construction of collective potentials; "flocks need no leaders"; simulations with
  hundreds of agents.

## Methods and models

Collective potentials, multi-species (alpha, beta, gamma) agents, Lyapunov-style analysis, 2D and 3D simulations.
Abstract from OpenAlex; full text not read.

## Limitations and open questions

The abstract says only the first algorithm is pure Reynolds and that it fragments; what information the
flocking algorithms need (for example a shared group objective) must be checked in the full text. Simulations
only.

## Relevance to us

The default flocking controller to implement or beat in a hackathon drone/robot demo, and the cleanest place
where consensus (velocity agreement) meets swarming. Seed paper for this topic.

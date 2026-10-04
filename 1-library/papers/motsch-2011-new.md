---
id: motsch-2011-new
type: paper
title: A New Model for Self-organized Dynamics and Its Flocking Behavior
authors: [Sebastien Motsch, Eitan Tadmor]
year: 2011
venue: Journal of Statistical Physics
url: https://arxiv.org/abs/1102.5575
doi: 10.1007/s10955-011-0285-9
arxiv: '1102.5575'
cite: "Motsch, S., & Tadmor, E. (2011). A new model for self-organized dynamics and its flocking behavior. Journal of Statistical Physics, 144(5), 923-947."
topics: [sync-consensus, collective-motion]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "399 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Proposes the Motsch-Tadmor model, a modification of [[cucker-2007-emergent]] in which each agent's velocity
update is normalised by the total influence it receives, so influence depends on relative rather than absolute
distance and the dynamics do not depend explicitly on the number of agents. This breaks the symmetry that earlier
Cucker-Smale proofs relied on, so the authors develop a new framework based on "active sets" that handles
non-symmetric influence matrices, including models with leaders, and carries over to kinetic and hydrodynamic
descriptions; the hydrodynamic version flocks unconditionally for slowly decaying influence functions.

## Contribution

Removes the explicit N-dependence of Cucker-Smale and supplies analysis
tools for asymmetric interactions; widely used in mathematical flocking theory.

## Key results

- Abstract: new normalised model; active-set framework for non-symmetric flocking; unconditional flocking of the
  hydrodynamic model for slowly decaying influence.

## Methods and models

Particle, kinetic and hydrodynamic descriptions; active-set estimates. Abstract read on arXiv.

## Limitations and open questions

Our note, not from the paper: non-symmetric weights give up the momentum-conservation structure of the
symmetric model, which is why new proof tools were needed.

## Relevance to us

Use instead of Cucker-Smale when swarm density varies a lot (clusters plus stragglers). Also an early example of
non-reciprocal interaction, connecting to [[fruchart-2021-non]].

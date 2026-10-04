---
id: hoffmann-2026-consensus
type: paper
title: 'From Consensus-Based Optimization to Particle Swarm Optimization: Convergence Guarantees under Drift-Diffusion Coupling'
authors:
- Franca Hoffmann
- Dohyeon Kim
- Ritvik Teegavarapu
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.17002
doi: null
arxiv: '2609.17002'
cite: 'Hoffmann, F., Kim, D., & Teegavarapu, R. (2026). From consensus-based optimization to particle swarm optimization: Convergence guarantees under drift-diffusion coupling. arXiv preprint arXiv:2609.17002. https://doi.org/10.48550/arXiv.2609.17002'
topics:
- swarm-intelligence
- sync-consensus
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 0 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Notes that CBO convergence guarantees depend on choosing drift and noise strengths independently, whereas in PSO
they are coupled. Shows by explicit construction that the coupling still leaves a non-empty admissible parameter set
for CBO (and CBO with memory) guarantees, but that this set shrinks in the limits used to recover PSO, so CBO
guarantees do not directly extend to classical PSO. Simulations illustrate the trade-offs.

## Contribution

A sobering correction to the "PSO is CBO plus inertia" story of [[grassi-2021-particle]] and [[cipriani-2022-zero]]:
the theory covers PSO-like dynamics, not the classical parameter regime.

## Key results

- Claimed (abstract): non-empty admissible set under coupling; admissible ranges shrink toward the PSO limit.

## Methods and models

Analysis of CBO convergence conditions under PSO-style parameter coupling; numerics (abstract only).

## Limitations and open questions

Abstract-level reading; very recent preprint (September 2026).

## Relevance to us

Important caveat for any claim that swarm optimisers in practice enjoy the mean-field guarantees.

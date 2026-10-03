---
id: kennedy-1995-particle
type: paper
title: Particle swarm optimization
authors:
- James Kennedy
- Russell Eberhart
year: 1995
venue: Proceedings of ICNN'95 - International Conference on Neural Networks (IEEE)
url: https://api.openalex.org/works/W2152195021
doi: 10.1109/ICNN.1995.488968
arxiv: null
cite: Kennedy, J., & Eberhart, R. (1995). Particle swarm optimization. In Proceedings of ICNN'95 - International Conference on Neural Networks (Vol. 4, pp. 1942–1948). IEEE. https://doi.org/10.1109/ICNN.1995.488968
topics:
- swarm-intelligence
- collective-motion
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 48858 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Introduces particle swarm optimisation: a population of candidate solutions ("particles") moves through a continuous
search space, each pulled toward its own best-found position and the best position found by its neighbours, an idea
the authors arrived at by simplifying simulations of bird flocking and social behaviour. The abstract outlines the
evolution of several paradigms, describes one implementation, reports benchmark testing, and proposes applications
to nonlinear function optimisation and neural-network training, relating PSO to artificial life and genetic algorithms.

## Contribution

The founding paper of PSO and, by citation count (about 49k in OpenAlex), the most influential swarm-intelligence
algorithm paper. Its derivation from flocking simulations (Reynolds-style boids) is the historical link between
collective-motion models and swarm optimisation.

## Key results

- Claimed in abstract: a working particle-swarm optimiser with benchmark tests; specific numbers not read (abstract only).
- Context from later work I read: the original update had no inertia weight; velocities required clamping, which
  motivated [[shi-1998-modified]] and [[clerc-2002-particle]]; [[grassi-2021-particle]] shows the classic
  acceleration c = 2 corresponds to lambda = 1, sigma = 1/sqrt(3) in the SDE form and is unstable without bounds.

## Methods and models

Velocity-position update with stochastic cognitive (personal best) and social (global best) attraction; benchmark
function tests and neural-network weight training (details not read beyond the abstract).

## Limitations and open questions

Read at abstract level only. The flocking metaphor was later dropped by the authors themselves in favour of a
dynamical-systems description; early versions had stability problems fixed by inertia and constriction.

## Relevance to us

Must-cite seminal work for any hackathon output that touches swarm optimisation. The bridge to swarm dynamics runs
through [[clerc-2002-particle]], [[grassi-2021-particle]] and [[huang-2023-global]]; the critique side through
[[sorensen-2015-metaheuristics]].

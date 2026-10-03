---
id: berman-2009-optimized
type: paper
title: "Optimized Stochastic Policies for Task Allocation in Swarms of Robots"
authors: ["Spring Berman", "Ádám Halász", "M. Ani Hsieh", "Vijay Kumar"]
year: 2009
venue: "IEEE Transactions on Robotics"
url: https://repository.upenn.edu/bitstreams/15cce1fc-61f4-4f44-b78b-04017c9a504a/download
doi: "10.1109/tro.2009.2024997"
arxiv: null
cite: "Berman, S., Halász, Á., Hsieh, M. A., & Kumar, V. (2009). Optimized Stochastic Policies for Task Allocation in Swarms of Robots. IEEE Transactions on Robotics, 25(4), 927–937."
topics: [swarm-robotics, collective-decision]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "261 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

A decentralised, communication-free way to allocate a swarm of identical robots across parallel tasks in a
desired proportion. The swarm is abstracted as population fractions at each task evolving under a linear
continuous-time Markov chain (rate equations); designing the allocation means choosing transition rates between
tasks. These rates become switching probabilities in each robot's stochastic policy. The authors optimise rates
for fast convergence to the target distribution subject to constraints on how much switching persists at
equilibrium, compare several formulations, and test them with 250 simulated robots redistributing among four
buildings to survey their perimeters.

## Contribution

A foundational example of macroscopic (mean-field) design for robot swarms that synthesises individual
probabilistic policies from a population-level model; a key reference in [[elamvazhuthi-2019-mean]].

## Key results

- Several optimisation formulations (with and without precedence constraints, dependent or independent of
  initial distribution) yield rates that trade convergence speed against equilibrium switching.
- Validated in a 250-robot, four-task simulation (from abstract and introduction).

## Methods and models

Linear rate equations dx/dt = K x with K built from transition rates; optimisation of K's spectrum for speed
under equilibrium-flux constraints; individual robots switch tasks with probabilities derived from K. Read the
abstract and introduction of the author PDF.

## Limitations and open questions

Assumes well-mixed populations and no task-dependent interactions; robots are homogeneous.

## Relevance to us

Template for "design at the density level, execute stochastically at the agent level"; compare with
[[martinoli-2004-modeling]] and division of labour in [[ferrante-2015-evolution]].

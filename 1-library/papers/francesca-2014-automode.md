---
id: francesca-2014-automode
type: paper
title: "AutoMoDe: A novel approach to the automatic design of control software for robot swarms"
authors: ["Gianpiero Francesca", "Manuele Brambilla", "Arne Brutschy", "Vito Trianni", "Mauro Birattari"]
year: 2014
venue: "Swarm Intelligence"
url: https://link.springer.com/article/10.1007/s11721-014-0092-4
doi: "10.1007/s11721-014-0092-4"
arxiv: null
cite: "Francesca, G., Brambilla, M., Brutschy, A., Trianni, V., & Birattari, M. (2014). AutoMoDe: A novel approach to the automatic design of control software for robot swarms. Swarm Intelligence, 8(2), 89–112."
topics: [swarm-robotics, marl-emergence]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "170 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

AutoMoDe treats automatic controller design like the bias-variance trade-off in machine learning: instead of
evolving unconstrained neural networks (low bias, high variance, poor transfer), it injects bias by assembling
pre-existing parametric behaviour modules (random walk, phototaxis, attraction and so on) into a probabilistic
finite-state machine whose topology, transition rules and parameters are optimised in simulation for a
task-specific objective. AutoMoDe-Vanilla, for e-puck robots, designs controllers for aggregation and foraging.

## Contribution

The founding paper of modular automatic design in swarm robotics; a white-box alternative to evolutionary
robotics that crosses the reality gap better. Many follow-ups (Chocolate, stigmergy [[salman-2024-automatic]])
build on it.

## Key results

- Claimed: produced controllers perform well, appear robust to the reality gap, and are human-readable (from
  abstract; numbers not checked).

## Methods and models

Probabilistic finite-state machines assembled from predefined parametric modules, optimised in simulation;
e-puck experiments. Abstract read on the Springer page; module set and optimiser details not checked.

## Limitations and open questions

Module library is hand-designed; tasks are simple benchmark missions.

## Relevance to us

If we want to search for swarm controllers automatically, this is the strongest baseline from the swarm
community. See [[kuckling-2023-recent]], [[valentini-2017-best]].

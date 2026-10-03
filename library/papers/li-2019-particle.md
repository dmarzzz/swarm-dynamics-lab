---
id: li-2019-particle
type: paper
title: "Particle robotics based on statistical mechanics of loosely coupled components"
authors: ["Shuguang Li", "Richa Batra", "David Brown", "Hyun-Dong Chang", "Nikhil Ranganathan", "Chuck Hoberman", "Daniela Rus", "Hod Lipson"]
year: 2019
venue: "Nature"
url: https://www.nature.com/articles/s41586-019-1022-9
doi: "10.1038/s41586-019-1022-9"
arxiv: null
cite: "Li, S., Batra, R., Brown, D., Chang, H. D., Ranganathan, N., Hoberman, C., Rus, D., & Lipson, H. (2019). Particle robotics based on statistical mechanics of loosely coupled components. Nature, 567(7748), 361–365."
topics: [swarm-robotics, active-matter]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "290 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

A "particle robot" is an aggregate of many loosely coupled units that cannot move on their own and have no
individual identity or addressable position. Each particle may only perform uniform volumetric oscillations
(expanding and contracting), with its phase modulated by a global signal. Despite the stochastic motion and the
absence of direct control of any component, the aggregate achieves locomotion, object transport and phototaxis,
which the authors control by exploiting statistical-mechanics phenomena rather than per-unit control.

## Contribution

A clear demonstration that robust locomotion can come from statistical mechanics of many stochastic,
non-addressable components, an alternative to coordinated modular robots. It sits with
[[savoie-2019-robot]] and [[li-2021-programming]] in the "robophysics" line.

## Key results

- Measured: physical robots of up to two dozen particles achieve locomotion, object transport and phototaxis.
- Simulated: robots with up to 100,000 particles.
- Measured robustness: locomotion maintained with 20% of particles malfunctioning.

## Methods and models

Oscillating particles with loose coupling and phase modulation by a global signal; physical prototypes plus
large-scale simulation. Abstract read on the Nature page; particle shape, coupling mechanism and the drift
model not checked.

## Limitations and open questions

Slow; 2D; relies on a global signal for direction. How performance scales with particle number in hardware is
untested.

## Relevance to us

Strong example of collective function without individual control; good conceptual partner for
[[chvykov-2021-low]] and [[ben-zion-2023-morphological]].

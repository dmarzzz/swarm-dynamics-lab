---
id: casert-2024-learning
type: paper
title: "Learning protocols for the fast and efficient control of active matter"
authors: ["Corneel Casert", "Stephen Whitelam"]
year: 2024
venue: "Nature Communications"
url: https://arxiv.org/abs/2402.18823
doi: "10.1038/s41467-024-52878-2"
arxiv: "2402.18823"
cite: "Casert, C., & Whitelam, S. (2024). Learning protocols for the fast and efficient control of active matter. Nature Communications, 15(1), 9128."
topics: ["active-matter", "marl-emergence"]
added_by: dmarz/active-matter
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "21 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Casert and Whitelam encode time-dependent control protocols for active-particle simulation models in neural networks
and optimize them by evolutionary methods to move the system between steady states as fast as possible or with minimal
energy. The learned protocols, which can vary several control parameters and develop sharp features, beat protocols
from recent constrained analytical methods, and the scheme is described as easy to use in experiments. Read from the abstract on the page in `url`; details beyond the abstract are not checked.

## Contribution

Applies neuroevolution to optimal control of active matter, a concrete instance of the agenda in
[[cichos-2020-machine]]; complements the response-theory approach of [[davis-2024-active]].

## Key results

- Learned protocols outperform constrained analytical protocols in speed or energy (abstract).

## Methods and models

Neural-network protocol, evolutionary optimization, active-particle simulations. arXiv:2402.18823; full text not read.

## Limitations and open questions

Simulation-only; controlled parameters are global fields rather than individual agents.

## Relevance to us

Directly usable idea: learn global control inputs (field, light, speed) that steer a swarm between collective states.
Related: [[davis-2024-active]], [[bektas-2025-emergent]].

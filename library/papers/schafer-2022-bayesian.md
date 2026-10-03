---
id: schafer-2022-bayesian
type: paper
title: Bayesian inverse reinforcement learning for collective animal movement
authors:
- Toryn L. J. Schafer
- Christopher K. Wikle
- Mevin B. Hooten
year: 2022
venue: The Annals of Applied Statistics
url: https://arxiv.org/abs/2009.04003
doi: 10.1214/21-AOAS1529
arxiv: '2009.04003'
cite: Schafer, T. L. J., Wikle, C. K., & Hooten, M. B. (2022). Bayesian inverse reinforcement learning for collective animal movement. The Annals of Applied Statistics, 16(2).
topics:
- marl-emergence
- collective-motion
- criticality-measurement
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 7 (Crossref, 2026-10-03)
code: []
---

## Summary

Instead of fixing agent-based rules a priori and fitting parameters, the authors use inverse RL to infer the local rules (decision costs) behind collective movement, using linearly-solvable MDPs for computational efficiency and Bayesian estimation with basis-function smoothing. They recover the true costs from a simulated self-propelled-particle model, and in a captive guppy population find that fish value collective movement more than targeted movement toward shelter.

## Contribution

A statistical-ecology route to rule inference via IRL applied to real animal data, complementing [[sosic-2017-inverse]] (theory) and [[walchli-2025-inverse]] (fluids).

## Key results

- True costs recovered in SPP simulation; guppies weight collective movement above movement to shelter (measured from data, per abstract).

## Methods and models

Linearly-solvable MDP IRL, Bayesian hierarchical estimation, basis-function smoothing. Abstract-level read (arXiv version).

## Limitations and open questions

Discretised state space; one species in captivity.

## Relevance to us

Directly applicable to tracking datasets the team may have; a measurement method for collective behaviour. Related: [[walchli-2025-inverse]], [[sosic-2017-inverse]].

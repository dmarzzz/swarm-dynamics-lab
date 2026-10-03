---
id: borra-2021-optimal
type: paper
title: Optimal collision avoidance in swarms of active Brownian particles
authors:
- Francesco Borra
- Massimo Cencini
- Antonio Celani
year: 2021
venue: Journal of Statistical Mechanics Theory and Experiment
url: https://arxiv.org/abs/2105.10198
doi: 10.1088/1742-5468/ac12c6
arxiv: '2105.10198'
cite: Borra, F., Cencini, M., & Celani, A. (2021). Optimal collision avoidance in swarms of active Brownian particles. Journal of Statistical Mechanics Theory and Experiment, 2021(8), 083401.
topics:
- marl-emergence
- active-matter
- collective-motion
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 9 (Crossref, 2026-10-03); 13 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Active Brownian particles in a finite 2D domain choose controls that trade off avoiding collisions against the energy spent manoeuvring. Posed as optimal stochastic control and solved with a mean-field game approach, the problem has an analytic mean-field solution with a second-order phase transition in the alignment order parameter. A mean-field Vicsek alignment rule performs remarkably close to the optimum.

## Contribution

The analytic, mean-field-game counterpart to the learning results of [[durve-2020-learning]] and [[brambati-2025-learning]]: it shows alignment is near-optimal for collision avoidance and predicts a phase transition, connecting MFG theory ([[lasry-2007-mean]]) to collective motion.

## Key results

- Analytic mean-field optimal control with a continuous (second-order) transition in alignment order (derived, per abstract).
- Mean-field Vicsek control is close to optimal (claimed, compared numerically).

## Methods and models

Optimal stochastic control of active Brownian particles; mean-field game (coupled HJB and Fokker-Planck) solution. Abstract-level read.

## Limitations and open questions

Mean-field (infinite-N) analysis; finite-size and fluctuation effects and true multi-agent learning are not covered.

## Relevance to us

Gives the theoretical prediction (a phase transition of the optimal policy) that a learned-flock experiment could test directly. Related: [[yang-2018-mean]], [[lauriere-2022-learning]], [[brambati-2025-learning]].

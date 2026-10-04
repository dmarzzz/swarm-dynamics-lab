---
id: walchli-2025-inverse
type: paper
title: Inverse reinforcement learning for objective discovery in collective behavior of artificial swimmers
authors:
- Daniel Wälchli
- Pascal Weber
- Michail Chatzimanolakis
- Robert Katzschmann
- Petros Koumoutsakos
year: 2025
venue: Physical Review Fluids
url: https://journals.aps.org/prfluids/abstract/10.1103/646f-dt2k
doi: 10.1103/646f-dt2k
arxiv: null
cite: Wälchli, D., Weber, P., Chatzimanolakis, M., Katzschmann, R., & Koumoutsakos, P. (2025). Inverse reinforcement learning for objective discovery in collective behavior of artificial swimmers. Physical Review Fluids, 10(6), 064901.
topics:
- marl-emergence
- collective-motion
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 0 (Crossref, 2026-10-03)
code: []
---

## Summary

Inverse RL is used to infer what individuals or a group are optimising from their observed states and actions, here for four artificial swimmers in a 2D viscous flow governed by Navier-Stokes. Synthetic trajectories come from a forward-RL policy trained to maximise swimming efficiency; IRL distils reward functions from these efficient patterns, which are interpreted with sensitivity analysis and symbolic regression. The authors argue the method applies to experimental data of natural swimmers.

## Contribution

Turns the Koumoutsakos-group programme ([[gazzola-2016-learning]], [[verma-2018-efficient]]) around: from specifying objectives to discovering them; a fluid-mechanics analogue of [[sosic-2017-inverse]] and [[schafer-2022-bayesian]].

## Key results

- Recovers group and individual objectives from efficient swimming patterns (claimed in abstract, synthetic data).

## Methods and models

Forward RL to generate data, IRL to infer rewards, symbolic regression to interpret. Abstract-level read (APS abstract page).

## Limitations and open questions

Only synthetic data from a known reward; four swimmers.

## Relevance to us

Method for asking "what does a real school optimise?" with tracking data. Related: [[schafer-2022-bayesian]], [[sosic-2017-inverse]].

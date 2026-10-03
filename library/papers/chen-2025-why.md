---
id: chen-2025-why
type: paper
title: 'Why collective behaviours self-organize to criticality: a primer on information-theoretic and thermodynamic utility measures'
authors: ['Qianyang Chen', 'Mikhail Prokopenko']
year: 2025
venue: 'Royal Society Open Science'
url: https://arxiv.org/abs/2409.15668
doi: 10.1098/rsos.241655
arxiv: '2409.15668'
cite: 'Chen, Q., & Prokopenko, M. (2025). Why collective behaviours self-organize to criticality: a primer on information-theoretic and thermodynamic utility measures. Royal Society Open Science, 12(6), 241655.'
topics: [criticality-measurement, collective-motion, marl-emergence]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: '2 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

A primer comparing intrinsic utility functions that might explain why collectives self-organise to
criticality: predictive information, empowerment, variational free energy (active inference) and
thermodynamic efficiency. It recasts the 2D Ising model as a perception-action loop (site = agent; world =
magnetisation; sensor = local energy; action = flip or not) and computes each utility across coupling strength
J under Glauber and Metropolis dynamics. Predictive information peaks at weak or near-critical coupling
depending on dynamics, empowerment and negative free energy peak at strong (supercritical) coupling, and only
thermodynamic efficiency, entropy reduction per unit of generalised work, peaks at the critical coupling. The
authors prove eta(J) ~ |J - J_c|^-1 for the 2D Ising model and propose a "principle of super-efficiency".

## Contribution

Puts several intrinsic-motivation objectives from robotics and active inference on one
benchmark and argues that only a thermodynamic (benefit-per-cost) objective selects criticality. It extends the
thermodynamic-efficiency line of [[crosato-2018-thermodynamics]] with an analytic Ising result.

## Key results

- Predictive information I(S_t; S_t+1): maximal near J_c for Glauber dynamics, maximal as J -> 0 for Metropolis (simulation, 50x50 lattice, 100 runs of 20 million steps per J).
- Average one-step empowerment: maximal at strong coupling, independent of dynamics; channel capacity is 1 bit when neighbour spins are unbalanced and 0 when balanced.
- Negative variational free energy (intrinsic part): maximal at strong coupling.
- Thermodynamic efficiency eta = -(dS/dJ) / integral_J^J* I_F(J') dJ' peaks near J_c ~ 0.4407 for both dynamics; finite-size analysis shows the peak approaches J_c as L grows.
- Analytic: eta(J) = ln(1+sqrt 2)/2 * |J - J_c|^-1 for the 2D Ising model; Curie-Weiss analogue from prior work.
- Cites simulated evidence that eta peaks at criticality in self-propelled particles, urban models and contagion networks.

## Methods and models

2D Ising, 50x50 torus, J in (0,2) step 0.02, beta = 1, ordered initial state, Glauber and Metropolis
single-spin flips. Information quantities from the last 200k steps; configuration entropy via Kikuchi
approximation S = S4 - 2S2 + S1; Fisher information by finite differences of sqrt p. Code:
qianyangchen/isingModelPALoop, Zenodo doi 10.5281/zenodo.13784627.

## Limitations and open questions

Equilibrium Ising only; the authors flag non-equilibrium systems such as real flocks as future work.
The empirical "evidence" section is interpretive (energy savings in formation flight, ant colony metabolic
scaling) and does not measure thermodynamic efficiency directly. The mapping of Ising to perception-action is
a modelling choice that shapes which utilities win.

## Relevance to us

Useful framing for hackathon experiments with learning agents: which objective an agent optimises
determines whether the swarm ends near criticality. Thermodynamic efficiency (Fisher information over entropy
change) is a computable diagnostic for simulated swarms with a tunable coupling. Read with
[[crosato-2018-thermodynamics]], [[hidalgo-2014-information]], [[barnett-2013-information]].

---
id: karamouzas-2014-universal
type: paper
title: Universal Power Law Governing Pedestrian Interactions
authors:
- Ioannis Karamouzas
- Brian Skinner
- Stephen J. Guy
year: 2014
venue: Physical Review Letters
url: https://arxiv.org/abs/1412.1082
doi: 10.1103/physrevlett.113.238701
arxiv: '1412.1082'
cite: Karamouzas, I., Skinner, B., & Guy, S. J. (2014). Universal Power Law Governing Pedestrian Interactions. Physical Review Letters, 113(23), 238701. https://doi.org/10.1103/physrevlett.113.238701
topics:
- crowds-and-traffic
- collective-motion
- criticality-measurement
added_by: dmarz/crowds-and-traffic
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 318 (Crossref, 2026-10-03)
code: []
---

## Summary

Uses the pair distribution function g from statistical mechanics to measure pedestrian interactions directly from trajectory data. Binned by distance, g(r) depends strongly on approach speed, but binned by time-to-collision τ (how long two people could keep walking before colliding) the curves collapse. Inverting a Boltzmann-like relation gives an interaction energy E(τ) ∝ 1/τ^2, truncated beyond a few seconds, in both sparse outdoor data and dense bottleneck data. Simulations with forces derived from this energy reproduce lanes, arching, clogging and the fundamental diagram.

## Contribution

Shows that pedestrian interactions are anticipatory and are governed by a single variable (time-to-collision) with a universal power-law exponent of 2, measured rather than postulated. It provides a model-free inference method (g → E) that can be applied to any tracked collective, and a physically grounded alternative to distance-based social forces ([[helbing-1995-social]]).

## Key results

- Measured: Outdoor dataset 1,146 trajectories (ρ = 0.27 m^-2, mean speed 0.86 m/s); Bottleneck dataset 354 trajectories (ρ = 2.5 m^-2, 0.55 m/s).
- Measured: E(τ) ∝ τ^-2 in both (fits R^2 = 0.94 bottleneck, 0.92 outdoor), saturating for τ below about 0.2 s (attributed to reaction time) and vanishing beyond t0 ≈ 1.4 s (bottleneck) and 2.4 s (outdoor); the shorter cut-off in dense crowds is explained by screening, scaling as ρ^-1/2 / u.
- Inferred: intrinsic interaction horizon τ0 ≈ 3 s, consistent with earlier 2–4 s estimates. Proposed law E(τ) = (k/τ^2) e^{−τ/τ0}.
- Simulated: forces F = −∇_r[(k/τ^2) e^{−τ/τ0}] plus a goal-driving term give lanes, arching, zipping at bottlenecks, the empirical speed–density relation; distance-based forces do not reproduce the E(τ) dependence (figure 4).
- Simulated: walkers with no goal, propelled along their current velocity, relax from a high-energy state to large-scale synchronised motion, which the authors liken to flocking and to non-goal-oriented human crowds such as mosh pits ([[silverberg-2013-collective]]).

## Methods and models

g(x) = observed pair-separation density divided by the density for non-interacting pairs, approximated by pairing pedestrians not present at the same time. Assumes near-equilibrium so g(τ) ∝ exp[−E(τ)/E0] (a maximum-entropy argument for stationary intensive variables, then checked self-consistently by simulations). τ is computed from current positions and velocities treating pedestrians as discs. Code, videos and data links at http://motion.cs.umn.edu/PowerLaw (as stated in the paper, not checked).

## Limitations and open questions

- The Boltzmann inversion is an assumption; crowds are far from equilibrium, and the self-consistency check uses the same model family.
- Datasets are modest and pooled across scenes; dependence on culture, groups or intention is not resolved.
- The authors note the law alone may not capture shock waves and turbulence at extreme densities where contact dominates ([[helbing-2007-dynamics]], [[gu-2025-emergence]]).

## Relevance to us

A reusable recipe for inferring an effective interaction potential from swarm trajectories (robots, animals, simulated agents) via pair statistics in the right variable. The τ^-2 law is a compact, physically interpretable collision-avoidance rule for robot swarms, closely related to velocity-obstacle methods ([[van-den-berg-2011-reciprocal]]). The goal-free simulation linking avoidance to emergent alignment connects crowd dynamics to flocking ([[vicsek-1995-novel]]).

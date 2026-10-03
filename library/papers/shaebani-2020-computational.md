---
id: shaebani-2020-computational
type: paper
title: "Computational models for active matter"
authors: ["M. Reza Shaebani", "Adam Wysocki", "Roland G. Winkler", "Gerhard Gompper", "Heiko Rieger"]
year: 2020
venue: "Nature Reviews Physics"
url: https://arxiv.org/abs/1910.02528
doi: "10.1038/s42254-020-0152-1"
arxiv: "1910.02528"
cite: "Shaebani, M. R., Wysocki, A., Winkler, R. G., Gompper, G., & Rieger, H. (2020). Computational models for active matter. Nature Reviews Physics, 2(4), 181–199."
topics: ["active-matter", "collective-motion", "swarm-robotics", "meta"]
added_by: dmarz/active-matter
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "366 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Review of the computational models and simulation methods used for active matter at every scale, from molecular motors
to animal groups. It goes from dry particle models (active Brownian particles, Vicsek-type alignment models and
variants), to dry continuum theories (Toner–Tu, dry active nematics, Active Model B+), to active particles in fluids
(force dipoles, squirmers, mesoscale hydrodynamics solvers), wet continuum theories (polar and nematic active gels,
generalized Navier–Stokes, Active Model H), and finally cells, tissues and animal groups. It closes with a table of
simulation techniques and open challenges.

## Contribution

A practical map of which model to use at which level of coarse-graining, with the governing equations collected in two
tables. Complements the theory-first reviews [[marchetti-2013-hydrodynamics]] and [[bechinger-2016-active]] with a
methods-first view.

## Key results

- ABP model: dr/dt = (D/k_BT)(−∇U + F_active) + ξ, dθ/dt = rotational noise; repulsive ABPs show MIPS, wall
  accumulation and swim pressure; spherical ABPs have a pressure equation of state but elongated ones do not
  (see [[solon-2015-pressure]]).
- Vicsek-type models: transition properties depend on noise type (intrinsic vs extrinsic), metric vs topological
  neighbours, and step size v₀Δt relative to interaction radius; flocking onset is liquid–gas-like with microphase
  separation (bands), while the active Ising model shows full phase separation.
- Collective motion without explicit alignment is possible through inelastic collisions, nematic collisions, short-range
  interactions, or shape-induced effects (Table I).
- Hydrodynamics: Re ≲ 10⁻³ for microswimmers; far field dominated by force dipole (pushers vs pullers); spherical
  squirmers form small clusters but not MIPS in thin films, while spheroidal squirmers phase separate and swarm.
- Methods table (Table III): MD, Brownian dynamics, kinetic Monte Carlo, lattice Boltzmann, DPD, multiparticle
  collision dynamics, boundary integral, DNS, colored-noise models, cellular Potts, vertex and phase-field models;
  Supplementary Table S1 lists software packages (not read).
- Animal groups: vision-based and non-reciprocal interactions, leadership by informed individuals, and future-option
  maximization are flagged as modelling directions.

## Methods and models

Narrative review with equations; no new simulations. Read the full arXiv version 1910.02528v2.

## Limitations and open questions

The authors list: no comprehensive continuum theory far from equilibrium; activity-dependent noise; complex
environments (viscoelastic, confinement, external flows); mixtures; vision-like information exchange; 3D cell motility;
and the coupling of signalling (biochemistry, food, light cues) to mechanics, which most models ignore. The animal-group
section is short and does not cover robotics in depth.

## Relevance to us

The best single entry point for choosing a simulation method for the hackathon: ABP or Vicsek for dry swarms
(robots, drones on a plane), squirmers or dipoles if fluid coupling matters, continuum PDEs for large-scale patterns.
Follow-ups: [[fily-2012-athermal]] (ABP baseline), [[chate-2008-collective]] (Vicsek bands), [[chate-2019-dry]]
(hydrodynamic derivation), [[gompper-2020-2020]] and [[gompper-2025-2025]] (roadmaps).

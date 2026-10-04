---
id: liebchen-2022-chiral
type: paper
title: "Chiral active matter"
authors: ["Benno Liebchen", "Demian Levis"]
year: 2022
venue: "Europhysics Letters (EPL)"
url: https://arxiv.org/abs/2207.01923
doi: "10.1209/0295-5075/ac8f69"
arxiv: "2207.01923"
cite: "Liebchen, B., & Levis, D. (2022). Chiral active matter. Europhysics Letters, 139(6), 67001."
topics: ["active-matter", "collective-motion", "sync-consensus"]
added_by: dmarz/active-matter-audit
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "127 (OpenAlex, 2026-10-03)"
code: []  # library ids of code that implements this paper
---

## Summary

Short perspective on chiral active particles (CAPs): agents that both self-propel and self-rotate, so that without
noise they move on circles (2D) or helices (3D). Examples are sperm cells, bacteria near walls, L-shaped colloids,
granular ellipsoids and pear-shaped Quincke rollers; "spinners" that rotate without propelling are a third class.
The authors review the single-particle model, then collective behaviour with isotropic repulsion (chirality opposes
MIPS and gives counter-rotating finite clusters), with polar alignment (the chiral Vicsek-like "CAP model": rotating
macro-droplets and micro-flock patterns with a selected size), mixtures of opposite handedness, hydrodynamic
interactions, and spinner fluids with odd viscosity, and close with a list of open questions.

## Contribution

The compact map of chirality in active matter, unifying circle swimmers, aligning chiral flockers and spinners, and
highlighting the generic length scale ℓ ∝ v₀/ω that appears across them. Builds on the authors' own CAP model
([[liebchen-2017-collective]]) and connects to odd transport and to the non-reciprocal physics of [[fruchart-2021-non]]
and to the Kuramoto-like synchronisation of rotating agents.

## Key results

- Single CAP (chiral ABP): ṙ = v₀p + √(2D)ξ, θ̇ = ω + √(2D_R)η. Only two dimensionless numbers matter, Pe and
  Ω = ω/D_R. The mean trajectory is a logarithmic spiral in 2D.
- Isotropic repulsion (simulation and continuum theory, cited): circling shifts the MIPS spinodal to higher v₀, i.e.
  chirality suppresses MIPS, but produces finite dynamical clusters counter-rotating relative to the gas, and a
  short-wavelength instability with onset scale ℓ ∝ v₀ and ℓ ∝ 1/ω at large ω. A chirality-induced absorbing
  transition to a hyperuniform state is also reported.
- CAP model θ̇_i = ω + (K/πR²) Σ sin(θ_j − θ_i) + noise: behaviour is set by gρ₀ and Ω. At Ω = 0 it is Vicsek-like
  (disorder below gρ₀ ≈ 2, bands just above, Toner–Tu-like order far above). Small Ω gives rotating macro-droplets of
  phase-synchronised particles; Ω ≳ 1 gives micro-flock patterns with a size ℓ ∝ v₀/ω independent of system size.
- Mixtures of opposite handedness segregate or form a "mutual flocking" state with global polar order, which is
  predicted to be linearly unstable in large systems.
- Spinner fluids (magnetic colloids in rotating fields): odd (Hall) viscosity, edge flows, and arrested coarsening
  with cluster size ∝ 1/ω.

## Methods and models

Perspective: overdamped Langevin models, mean-field coarse-graining to density and polarisation fields with linear
stability analysis, squirmer and lattice-Boltzmann results for wet CAPs, and spinner models with frictional or
hydrodynamic torques. No new data or code. Read the whole arXiv:2207.01923v1 text.

## Limitations and open questions

Authors' list: nature of the transitions between micro-flocks, macro-droplets and vortex phases; whether micro-flocks
coarsen at long times; effect of chirality on universality classes; conditions for activity-induced synchronisation;
whether ℓ ∝ v₀/ω has a universal explanation; large-scale wet simulations; Hall viscosity in circle swimmers. Most
collective results are from minimal 2D models; experiments are few.

## Relevance to us

Every real robot or drone has some turning bias, and many swarm designs add deliberate circling (loiter patterns).
This review says what that does: circling breaks clustering and flocking into rotating patches with a size set by the
turning radius v₀/ω, and links swarming to synchronisation (swarmalator-like behaviour, see topic sync-consensus).
Related: [[liebchen-2017-collective]], [[caprini-2023-flocking]], [[bandini-2025-xy]], [[lowen-2020-inertial]].

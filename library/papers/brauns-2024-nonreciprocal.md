---
id: brauns-2024-nonreciprocal
type: paper
title: "Nonreciprocal Pattern Formation of Conserved Fields"
authors: ["Fridtjof Brauns", "M. Cristina Marchetti"]
year: 2024
venue: "Physical Review X"
url: https://arxiv.org/abs/2306.08868
doi: "10.1103/physrevx.14.021014"
arxiv: "2306.08868"
cite: "Brauns, F., & Marchetti, M. C. (2024). Nonreciprocal Pattern Formation of Conserved Fields. Physical Review X, 14(2), 021014."
topics: ["active-matter", "collective-motion"]
added_by: dmarz/active-matter-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "70 (OpenAlex, 2026-10-03)"
code: []  # library ids of code that implements this paper
---

## Summary

Brauns and Marchetti study the minimal nonreciprocal Cahn–Hilliard (NRCH) model: a phase-separating conserved field ϕ
coupled through cross-diffusion to a second, purely diffusive conserved field ψ, with D₁₂ ≠ D₂₁. With reciprocal
coupling the system phase separates and coarsens as usual; with strong enough anti-reciprocal coupling ("A chases B,
B runs from A") the two branches of the linear dispersion relation coalesce and acquire an imaginary part, and the
phase-separated domains turn into travelling waves or travelling droplets. They argue NRCH is the mass-conserving
analogue of the FitzHugh–Nagumo model and a common normal form for active–passive mixtures, mass-conserving
reaction–diffusion systems (e.g. Min proteins) and active gels, and show that the wave speed is predicted by a local
dispersion relation evaluated at the interfaces, far from the homogeneous state.

## Contribution

Extends the non-reciprocal phase transition picture of [[fruchart-2021-non]] (global Goldstone-mode coalescence in
flocks) to conserved scalar fields, where the exceptional point is localised at domain interfaces. Gives a minimal,
easy-to-simulate model for "chase-and-run" pattern formation between two agent types.

## Key results

- Model: ∂ₜϕ = ∇²(D₁₁ϕ + D₁₂ψ + ϕ³ − κ∇²ϕ), ∂ₜψ = ∇²(D₂₁ϕ + D₂₂ψ), D₂₂ > 0, spinodal when D₁₁ < 0.
- Example (1D simulations, ϕ̄ = 0, D₂₂ = 0.1, L = 20): reciprocal D₁₂ = D₂₁ = 0.07 gives coarsening phase separation;
  anti-reciprocal D₁₂ = −D₂₁ = 0.14 gives travelling waves.
- Transition from static to travelling patterns is a drift-pitchfork bifurcation heralded by an exceptional point of
  the local (interfacial) dispersion relation; for strong enough nonreciprocity it occurs for all parameters.
- Coarsening of travelling droplets is interrupted without wavelength selection: stable wavelengths range from the
  interface width to the system size, depending on initial conditions.
- In 2D, travelling fronts develop transverse undulations that propagate along the interface (breaking chiral as well
  as polar symmetry), up to spatiotemporal chaos. No-flux boundaries give standing waves in 1D and sloshing in 2D.

## Methods and models

Linear stability analysis, phase-portrait analysis of the FitzHugh–Nagumo analogy, local (regional) stability analysis
at interfaces, and numerical simulations (Mathematica NDSolve in 1D, COMSOL finite elements in 2D). Mappings to
active–passive particle mixtures, mass-conserving reaction–diffusion and active gel models. No code repository given.
Read abstract, introduction with the summary of results, and conclusion of arXiv:2306.08868v4; derivation sections and
appendices only glanced at.

## Limitations and open questions

Deterministic analysis: the role of noise in wavelength selection is open (the authors suggest it may matter as in
flocking). The mechanism of the 2D interface undulations is hypothesised (a nonreciprocal Mullins–Sekerka instability)
but not established. Coarse-grained continuum model; the mapping to specific microscopic agent rules is only shown for
a few cases.

## Relevance to us

Two-species swarms with asymmetric rules (pursuers and evaders, leaders and followers, robots attracted to a group that
avoids them) are generically predicted to form travelling bands or droplets instead of static clusters, with a speed
set at the interfaces. A cheap PDE testbed for such heterogeneous swarms. Related: [[fruchart-2021-non]],
[[zhao-2023-chemotactic]], [[cates-2015-motility]], [[chate-2019-dry]].

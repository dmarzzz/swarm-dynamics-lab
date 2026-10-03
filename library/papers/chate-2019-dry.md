---
id: chate-2019-dry
type: paper
title: "Dry, aligning, dilute, active matter: A synthetic and self-contained overview"
authors: ["Hugues Chaté", "Benoît Mahault"]
year: 2019
venue: "arXiv preprint (cond-mat.stat-mech), lecture notes"
url: https://arxiv.org/abs/1906.05542
doi: null
arxiv: "1906.05542"
cite: "Chaté, H., & Mahault, B. (2019). Dry, aligning, dilute, active matter: A synthetic and self-contained overview. arXiv preprint arXiv:1906.05542 (lecture notes, 47 pages)."
topics: ["active-matter", "collective-motion"]
added_by: dmarz/active-matter
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "4 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Lecture notes giving a self-contained account of "DADAM": point particles that move, align and feel noise, with no
fluid and no excluded volume. They define three classes by Vicsek-style models (polar/Vicsek with ferromagnetic
alignment; active nematics with nematic alignment and fast velocity reversals; self-propelled rods with nematic
alignment and no reversals), describe their phase diagrams from large simulations, derive hydrodynamic equations for
each class with the Boltzmann–Ginzburg–Landau (BGL) method, and analyse the inhomogeneous band solutions of those
equations. The central message: the onset of orientational order is not an order–disorder critical point but a
liquid–gas-like phase separation, with a coexistence phase of bands between a disordered gas and an ordered liquid.

## Contribution

The clearest synthesis of 15 years of work from the Chaté–Tailleur–Bertin groups ([[gregoire-2004-onset]],
[[chate-2008-collective]], [[bertin-2006-boltzmann]], [[solon-2015-phase]]). It makes explicit the agreements and
disagreements between particle simulations and Toner–Tu theory ([[toner-1995-long]]). The companion published review is
[[chate-2020-dry]].

## Key results

- Phase diagram (all three classes): gas, coexistence and liquid separated by two binodals that meet at the origin and
  converge at infinite density (no critical point at finite density).
- Polar class (measured): true long-range order in the liquid, Π − Π∞ ~ L^(−0.64) with Π∞ = 0.8685 at ρ₀ = 2,
  η = 0.2; giant number fluctuations ΔN² ~ ⟨N⟩^φ with φ ≈ 1.6 (Toner–Tu predicts 8/5); transverse superdiffusion
  roughly consistent with Toner–Tu. Coexistence phase is a smectic train of identical traveling bands whose number
  scales with system length (microphase separation), with constant gas density.
- Nematic classes (measured): quasi-long-range nematic order for active nematics (decay exponent ∝ η²); apparently
  true long-range order for rods without reversals (possibly a finite-size effect); GNF exponent also 1.6–1.7, in
  disagreement with the predicted φ = 2. Nematic bands are unstable, giving spatiotemporal "band chaos".
- Hydrodynamics (derived): polar class ∂ₜρ = −∇·w, ∂ₜw = −½∇ρ + (μ₁[ρ] − ξ|w|²)w + ν∆w − κ₁... with all
  coefficients expressed through noise Fourier modes and density; instability of the homogeneous ordered state comes
  from μ₁ increasing with ρ (density–order feedback). Spurious instabilities appear deep in the ordered phase, removed by
  adding positional diffusion.
- Deterministic Toner–Tu-like equations admit a large family of stable band solutions (periodic, solitonic,
  phase-separated, organized around a unique heteroclinic orbit); adding noise selects a unique band number, as in the
  microscopic model.
- Nematic band solution found in closed form; always unstable to long-wavelength undulations.

## Methods and models

Canonical Vicsek model θⱼ(t+1) = arg⟨exp(iθₖ)⟩ + ηξ with v₀ = 0.5, r₀ = 1, periodic boxes up to L = 2048 and ~10⁷
time steps for GNF; Boltzmann equation with binary collisions and molecular chaos, angular Fourier expansion,
ε-scaling ansatz truncation; ODE phase-portrait analysis of traveling waves; numerical PDE integration. Full read of
arXiv:1906.05542v1.

## Limitations and open questions

- Molecular chaos is a strong assumption for aligning particles, so hydrodynamic agreement is qualitative only.
- Deterministic PDEs cannot capture GNF or the QLRO vs LRO distinction; a proper fluctuating theory (RG with
  multiplicative noise) is missing.
- 2D, periodic boundaries, point particles; walls, dense regimes, wet systems, cohesion, memory, quenched disorder and
  chirality are listed as extensions.

## Relevance to us

This is the reference for anyone simulating Vicsek-type swarms: it tells you that bands near onset are expected, that
finite-size order-parameter curves mislead (the transition looks continuous in small systems but is discontinuous),
and which observables (GNF exponent, band count, gas density) are robust. Use with [[vicsek-1995-novel]],
[[chate-2008-collective]], [[mahault-2019-quantitative]] and [[chate-2024-dynamic]].

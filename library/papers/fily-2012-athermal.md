---
id: fily-2012-athermal
type: paper
title: "Athermal Phase Separation of Self-Propelled Particles with No Alignment"
authors: ["Yaouen Fily", "M. Cristina Marchetti"]
year: 2012
venue: "Physical Review Letters"
url: https://arxiv.org/abs/1201.4847
doi: "10.1103/physrevlett.108.235702"
arxiv: "1201.4847"
cite: "Fily, Y., & Marchetti, M. C. (2012). Athermal Phase Separation of Self-Propelled Particles with No Alignment. Physical Review Letters, 108(23), 235702."
topics: ["active-matter", "collective-motion"]
added_by: dmarz/active-matter
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "1153 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Fily and Marchetti simulate self-propelled soft repulsive disks in 2D with rotational noise but no alignment rule and
no translational noise. Above a packing fraction φ_c ≈ 0.4, well below close packing, the system phase separates into
a dense, solid-like cluster and a gas, with giant number fluctuations (ΔN ~ N^0.95) despite no broken orientational
symmetry. Fitting the mean-square displacement shows the effective swim speed decreases linearly with density,
v_e(φ) = v₀(1 − λφ) with λ ≈ 0.9, and a continuum model with this v_e predicts an instability at φ* = 1/(2λ) ≈ 0.45,
close to the simulated onset.

## Contribution

With [[redner-2013-structure]], the minimal active Brownian particle demonstration that motility-induced phase separation
([[cates-2015-motility]]) happens from steric slowing alone, linking the run-and-tumble theory of
[[tailleur-2008-statistical]] to particle simulations, and showing that the giant fluctuations seen in flocks
([[narayan-2007-long]]) can also arise without alignment.

## Key results

- Measured: phase separation for φ > φ_c ≈ 0.4 at v₀ = 1, ν_r = 5 × 10⁻³ (N up to 10⁴).
- Measured: giant number fluctuations ΔN ~ N^a with a = 0.95 ± 0.05 above φ_c (consistent with a = 1 for 2D phase
  separation); normal fluctuations below.
- Measured: effective speed v_e(φ) = v₀(1 − λφ), λ ≈ 0.9 independent of v₀ ∈ {0.5, 1, 2}; effective diffusivity
  D_e ∝ (1 − λφ)²; rotational relaxation nearly density independent.
- Measured: no effective temperature reproduces the active clustering; a thermal system with matched overlap
  (k_BT = 0.1) shows far less clustering.
- Theory: linearized continuum model gives D = D_ρ + v_e w/ν_r with w = v_e + ρ v_e'; instability when w < 0, i.e.
  φ > 1/(2λ) ≈ 0.45 for D_ρ = 0. Static structure factor S(0) diverges at the instability, correlation length
  ξ ~ (φ − φ_c)^(−1/2) (mean field). Simulated S(q) ~ q⁻² above φ_c, Lorentzian below.

## Methods and models

Overdamped Langevin dynamics ∂ₜrᵢ = v₀ν̂ᵢ + μΣFᵢⱼ + ηᵢ, ∂ₜθᵢ = ηᵢ with harmonic repulsion F = −k(2a − r)r̂ for r < 2a;
T = 0; periodic box; N = 100–10,000; lengths in units of particle radius. Continuum equations for density ρ and
polarization p (Eqs. 4a–b) with v_e(ρ) inserted, linear stability and structure factor computed analytically.
No code released.

## Limitations and open questions

- Short PRL; the transition region and critical exponents are not studied ("a detailed study ... is needed").
- Only one rotational noise value; Péclet-number dependence of the phase boundary not mapped (done later by
  [[digregorio-2018-full]] and Stenhammar et al.).
- No hydrodynamics; mean-field continuum model neglects nonlinear noise.

## Relevance to us

A ten-line simulation that any team member can reproduce as a baseline swarm model: constant-speed agents, repulsion,
rotational noise. It shows that collision-induced slowing alone produces clustering and jamming, which matters for
dense robot swarms ([[deblais-2018-boundaries]], [[scholz-2018-rotating]]) and for interpreting "clumps" in agent
simulations as phase separation rather than coordination. Compare with flocking that needs alignment
([[vicsek-1995-novel]], [[chate-2008-collective]]) and with turn-away flocking ([[das-2024-flocking]]).

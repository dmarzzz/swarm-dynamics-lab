---
id: cates-2015-motility
type: paper
title: "Motility-Induced Phase Separation"
authors: ["Michael E. Cates", "Julien Tailleur"]
year: 2015
venue: "Annual Review of Condensed Matter Physics"
url: https://arxiv.org/abs/1406.3533
doi: "10.1146/annurev-conmatphys-031214-014710"
arxiv: "1406.3533"
cite: "Cates, M. E., & Tailleur, J. (2015). Motility-Induced Phase Separation. Annual Review of Condensed Matter Physics, 6(1), 219–244."
topics: ["active-matter", "collective-motion", "criticality-measurement"]
added_by: dmarz/active-matter
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "1721 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Review of motility-induced phase separation (MIPS): self-propelled particles with purely repulsive (or no direct)
interactions can split into a dense, slow liquid and a dilute, fast gas. The mechanism is a positive feedback:
active particles accumulate where they move slowly (steady state P ∝ 1/v(r)), and if speed falls with local density,
accumulation causes slowing and slowing causes accumulation. The authors show that, to leading order in gradients,
active particles with density-dependent speed v(ρ) map exactly onto passive Brownian particles with attractions and
an effective free energy, so the binodals follow from a common-tangent construction. They then show where the
mapping breaks: gradient terms that violate detailed balance (Active Model B) shift the coexisting densities, and
experiments show arrested cluster phases that no theory yet explains.

## Contribution

The standard reference that unified run-and-tumble (Tailleur and Cates 2008, [[tailleur-2008-statistical]]) and active
Brownian particle (ABP) work ([[fily-2012-athermal]], [[redner-2013-structure]]) into one picture of MIPS and introduced
the "equilibrium mapping plus non-integrable corrections" framing that later field theories (Active Model B/B+,
[[wittkowski-2014-scalar]]) build on.

## Key results

- Single-particle result (exact for isotropic tumbling or rotational diffusion): steady state P_stat(r) ∝ 1/v(r).
  Large-scale diffusivity D = v²τ/d + D_t with τ⁻¹ = α + (d−1)D_r (Eqs. 4–5).
- Linear (spinodal) instability criterion: v'(ρ)/v(ρ) < −1/ρ (Eq. 3). With thermal diffusion D_t the condition becomes
  v²τ(1 + ρv'/v) < −dD_t, so MIPS needs a minimum ratio of active to thermal diffusivity.
- Effective free energy in the local approximation: βf(ρ) = ρ(ln ρ − 1) + ∫₀^ρ ln v(s) ds (Eq. 27); coexistence by
  common tangent.
- For linear slowing v(ρ) = v₀(1 − ρ/ρ*) (measured in ABP simulations, Eq. 39), spinodals are
  ρ± = ρ*(3 ± √(1 − 8ε))/4 with ε = dD_t/(v₀²τ); MIPS exists only for ε < 1/8.
- Measured in simulations (cited): ABPs show no MIPS below a critical Péclet number Pe_c ≈ 55 in 2D and ≈ 125 in 3D;
  the simple theory under-predicts Pe_c by a factor of 50 or more, so translational noise is not the main cause.
- Coarsening: domain size L(t) ~ t^α with α ≈ 0.25–0.28 in 2D ABP simulations (up to 40 million particles) versus 1/3
  for passive Model B; lattice run-and-tumble models give 1/3. The authors say the difference may be a slow transient.
- Active Model B: μ = −φ + φ³ − ∇²φ + λ(∇φ)²; the λ term replaces the common tangent with an "uncommon tangent"
  (equal μ, unequal pseudo-pressure) and explains shifted binodals seen in ABP simulations.
- Experimental status (2015): clusters in synthetic swimmers ([[buttinoni-2013-dynamical]], [[palacci-2013-living]])
  often arrest at finite size; decisive experimental evidence for bulk MIPS is lacking ("the dog that did not bark").

## Methods and models

Analytical coarse-graining of run-and-tumble and active Brownian particle dynamics to fluctuating hydrodynamics
(Itō multiplicative noise, Eqs. 16–17), Fokker–Planck functional analysis for the integrability condition
k_BT ln v([ρ], r) = δF_ex/δρ, mean-field thermodynamics, lattice-gas simulations of run-and-tumble particles with
partial exclusion, and comparison with off-lattice ABP simulations and the Cahn–Hilliard–Cook / Model B continuum
equations. Read from arXiv:1406.3533 (HTML), which is the preprint of the published review.

## Limitations and open questions

- No complete theory of the critical Péclet number or of the MIPS critical point (later work suggests Ising class).
- Hydrodynamic interactions can suppress MIPS in 2D (torques at collisions); their 3D effect was unknown.
- No framework (as of 2015) combining MIPS with passive attractions, alignment, or mixtures; cluster arrest unexplained.
- Applies to "active simple fluids" only; orientational interactions are discussed as an open frontier where Vicsek
  physics and MIPS overlap.

## Relevance to us

The cleanest mechanism for density instabilities in any swarm whose agents slow down when crowded: robots that stall
on contact, drones that throttle near neighbours, or agents with density-dependent speed rules (quorum sensing,
[[bauerle-2018-self]]). The criterion v'/v < −1/ρ is a design rule: a swarm controller with speed decreasing faster
than 1/ρ will clump. Pairs with [[fily-2012-athermal]] (minimal simulation), [[redner-2013-structure]],
[[digregorio-2018-full]] (full ABP phase diagram), [[solon-2015-pressure]] (no equation of state), and
[[wittkowski-2014-scalar]] (Active Model B). Contrasts with alignment-driven phase separation in Vicsek-type flocks
([[chate-2019-dry]], [[solon-2015-phase]]).

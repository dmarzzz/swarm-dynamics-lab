---
id: chate-2024-dynamic
type: paper
title: Dynamic Scaling of Two-Dimensional Polar Flocks
authors: [Hugues Chaté, Alexandre Solon]
year: 2024
venue: Physical Review Letters
url: https://arxiv.org/abs/2403.03804
doi: 10.1103/PhysRevLett.132.268302
arxiv: '2403.03804'
cite: Chaté, H., & Solon, A. (2024). Dynamic scaling of two-dimensional polar flocks. Physical Review Letters, 132(26), 268302.
topics: [collective-motion, active-matter]
added_by: dmarz/collective-motion
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "20 (Crossref is-referenced-by-count, 2026-10-03); 26 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Rather than expanding the isotropic Toner-Tu equations around the ordered state, the authors write the most
general symmetry-allowed equation for the Goldstone mode (the local direction of order) of a polar flock,
then specialise to d = 2 for two universality classes: "Malthusian" flocks (density is a fast variable, as
with birth and death) and "Vicsek" flocks (Goldstone mode coupled to a conserved density). Assuming the
nonlinear convective terms receive no graphical corrections (a generalized Galilean invariance) and the noise
none either, they obtain scaling relations that fix the exponents exactly. Numerical integration of their
reduced equations and earlier large Vicsek-model simulations agree with the predictions. Read in full from
the arXiv version (3 pages plus supplement not read).

## Contribution

Proposes a resolution of the 30-year question of the scaling exponents of the 2D ordered flocking phase:
the 1995 Toner-Tu values ([[toner-1995-long]]) are wrong for Vicsek flocks (already shown numerically by
[[mahault-2019-quantitative]]), and here exact values are argued. The result competes with the
functional-RG universality class of [[jentsch-2024-new]], and the claims were disputed in 2025 (Chen et al.,
"The inconvenient truth about flocks"; authors' reply arXiv 2504.13683, not catalogued separately).

## Key results

- Malthusian flocks, d = 2 (roughness chi, anisotropy zeta, dynamic z): this work chi = -1/4, zeta = 3/4,
  z = 5/4; Toner 2012 prediction -1/5, 3/5, 6/5; their numerics -0.25(1), 0.75(2), 1.27(3).
- Vicsek flocks, d = 2: this work chi = -1/3, zeta = 1, z = 4/3; Toner-Tu 1995 -1/5, 3/5, 6/5;
  Mahault et al. 2019 Vicsek-model simulations -0.31(2), 0.95(2), 1.33(2); their hydrodynamic numerics
  -0.34(3), 1.01(4), 1.30(6).
- chi < 0 confirms true long-range order in 2D and that higher-order nonlinearities are irrelevant.
- Practical point: integrating the Goldstone-mode equation with the zero mode of the noise removed avoids the
  slow diffusion of the global order direction that plagues simulations of the isotropic equations.
- Notes that the Goldstone mode is not the velocity phase phi itself but phi - alpha d_par phi.

## Methods and models

Goldstone equation d_t n = R x n with R_alpha = d_beta R_alphabeta + noise, R built from all first-order
gradient terms allowed by O(d) symmetry (Levi-Civita structure). In 2D with theta the angle:
d_t theta + lambda d_par theta = D lap theta + noise; expanded at order theta^3 around order along x:
d_t theta + lambda_y d_y theta^2 + lambda_x d_x theta^3 = D_x d_x^2 theta + D_y d_y^2 theta + noise
(the lambda_x term was previously neglected). For Vicsek flocks a density equation (their Eqs. 13, 15, 16) is
coupled in. One-loop RG flow plus non-renormalization assumptions give 2chi + z - zeta = chi + z - 1 =
z - 2chi - 1 - zeta = 0. Simulations of the reduced equations at L = 2400-4800.

## Limitations and open questions

- Exactness rests on an assumed non-renormalization of the convective terms, argued from a generalized
  Galilean invariance rather than proven.
- Anisotropic diffusion terms were dropped "for simplicity".
- Disagreement with [[jentsch-2024-new]] and the 2025 Chen et al. critique mean the universality class of the
  2D Vicsek ordered phase should be treated as contested.

## Relevance to us

Background theory rather than something we would build on in a hackathon, but it tells us which fluctuation
exponents to expect if we measure density or orientation correlations in large simulated flocks and gives a
fast way to simulate the ordered phase. Context: [[toner-1998-flocks]], [[chate-2020-dry]],
[[ginelli-2016-physics]].

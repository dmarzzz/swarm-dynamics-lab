---
id: mahault-2019-quantitative
type: paper
title: Quantitative Assessment of the Toner and Tu Theory of Polar Flocks
authors: [Benoît Mahault, Francesco Ginelli, Hugues Chaté]
year: 2019
venue: Physical Review Letters
url: https://arxiv.org/abs/1908.03794
doi: 10.1103/PhysRevLett.123.218001
arxiv: '1908.03794'
cite: 'Mahault, B., Ginelli, F., & Chaté, H. (2019). Quantitative assessment of the Toner and Tu theory of polar flocks. Physical Review Letters, 123(21), 218001.'
topics: [collective-motion, active-matter]
added_by: dmarz/collective-motion
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "63 (OpenAlex, 2026-10-03); 66 (Crossref is-referenced-by-count, 2026-10-03); 50 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Very large simulations of the Vicsek model in 2D and 3D test Toner-Tu theory of the ordered phase. The
overall phenomenology and algebraic scaling are confirmed, but density correlations show qualitative
discrepancies and the scaling exponents differ significantly from the 1995 conjecture; beyond a large
crossover scale flocks are only weakly anisotropic. Read at abstract level from arXiv; the 2D exponents
quoted in [[chate-2024-dynamic]] are chi = -0.31(2), zeta = 0.95(2), z = 1.33(2).

## Contribution

The numerical benchmark that later theories ([[chate-2024-dynamic]], [[jentsch-2024-new]]) are judged
against.

## Key results

- Measured: exponents differ from TT95 (TT95 2D: chi = -1/5, zeta = 3/5, z = 6/5).
- Measured: large crossover scale to weak anisotropy.

## Methods and models

Large-scale Vicsek-model simulations, 2D and 3D, correlation functions of orientation and density.

## Limitations and open questions

Abstract-level read.

## Relevance to us

Benchmark numbers if we ever measure fluctuation scaling in large swarms.

## Notes from dmarz/active-matter

Full read of arXiv:1908.03794 (main text; Supplementary not read). Numbers from Table I and the figures:

- Measured exponents, 2D: χ = −0.31(2), ξ = 0.95(2), ζ = z = 1.33(2), GNF exponent 1.67(2). Toner–Tu 1995 conjecture: χ = −0.20, ξ = 0.60, ζ = z = 1.20, GNF 1.60.
- 3D: χ ≈ −0.62, ξ ≈ 1, ζ = 1.77(3), z ≈ 1.77, GNF 1.59(3) (TT95: −0.60, 0.80, 1.60, 1.60, 1.53).
- Longitudinal transverse-velocity correlations in 2D cross over from exponent ≈ −1.65 to ≈ −1.4 at ℓ_c ≈ 100 interaction ranges, close to the transverse −1.33, so anisotropy is weak or vanishing at large scales; isotropic in 3D beyond ℓ_c ≈ 30. ℓ_c is about the size of most earlier simulations, which explains why it was missed.
- Sound speeds agree exactly with linear theory; peak widths give z ≈ 1.33 (2D), ≈ 1.77 (3D). Hyperscaling z = d − 1 + 2χ + ξ appears satisfied, which the authors read as: the noise variance does not renormalize, and the relevant corrections come from vertices not coupling density and order.
- Longitudinal density correlations do not follow TT (collapse with q⊥^(−μ), μ ≈ 1 in 2D and 0.5 in 3D, instead of 2), and an extra slow regime (exponent ≈ −0.7) appears in 2D.
- Why GNF studies never caught this: ζ/d, which sets the GNF exponent, barely changes across scales.
- Setup: discrete-time Vicsek, vectorial noise, v₀ = 1, ρ₀ = 2, η = 0.5 (2D) / 0.45 (3D), L up to 8000 (2D) and 960 (3D), N from millions to billions; order pinned with reflecting channel walls (checked against two other protocols).

Use these exponents, not the 1995 ones, as the reference when testing flocking simulations. Related: [[toner-1995-long]], [[chate-2019-dry]], [[chate-2024-dynamic]].

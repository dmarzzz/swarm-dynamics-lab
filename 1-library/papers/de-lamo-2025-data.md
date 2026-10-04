---
id: de-lamo-2025-data
type: paper
title: "Data-Driven Stochastic Modeling of Schooling Fish: From Collective Dynamics to Individual Fluctuations"
authors: ["Elena G. de Lamo", "M. Carmen Miguel", "Romualdo Pastor-Satorras"]
year: 2025
venue: "arXiv preprint (cond-mat.other)"
url: https://arxiv.org/html/2509.08630
doi: null
arxiv: "2509.08630"
cite: "de Lamo, E. G., Miguel, M. C., & Pastor-Satorras, R. (2025). Data-Driven Stochastic Modeling of Schooling Fish: From Collective Dynamics to Individual Fluctuations. arXiv preprint arXiv:2509.08630 (v2, 14 January 2026)."
topics: [collective-motion, active-matter]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "0 (OpenAlex W4417070642, 2026-10-03)"
code: []
---
## Summary

Trajectories of black neon tetra schools (group sizes N = 40, 50 and 60, three independent 60-minute recordings per size at 50 fps, idtracker.ai, quasi-2D tank) are decomposed into centre-of-mass (CM) motion and motion relative to the CM. The CM is modelled as a finite-size active Brownian particle with Schienbein-Gruler active friction and a non-potential hard-wall force that favours wall following; parameters fit by minimising Kullback-Leibler divergence between simulated and empirical position and velocity distributions. In the CM frame each fish is treated as independent in a mean-field radial confining potential inferred from the radial density (flat inside, exponential decay outside, so an almost constant restoring force once outside), plus drift and multiplicative (state-dependent) diffusion for speed and turning rate estimated by kernel-based Kramers-Moyal regression. Synthetic schools reproduce CM position and velocity distributions (crater-shaped velocity PDF), radial density, exponential-tailed velocity components, burst-and-coast speed oscillations with partial synchrony, MSD with confinement plateau and oscillations, residence and peripheral times, and the bimodal polarisation distribution.

## Contribution

Shows that a two-level, mean-field stochastic model with data-inferred drift and multiplicative noise can reproduce many school observables without explicit pairwise rules; complements pairwise force-map approaches such as [[puy-2024-selective]].

## Key results

- Measured: radial density in the CM frame collapses across group sizes when scaled by radius of gyration and mean density.
- Measured: weak cross-correlation of speed and turning rate between different fish compared with strong autocorrelation, which motivates the independent-in-CM-frame approximation.
- Analytic (N -> infinity limit): stationary speed and turning-rate PDFs with power-law tails; turning-rate tail exponent essentially independent of group size.
- Model vs data: good agreement for most observables; the model underestimates long excursions away from the CM (heavy tails missed).

## Methods and models

SDEs: Eq. (2) CM active Brownian pseudo-particle; Eq. (4) polar-coordinate SDEs for speed, heading and turning rate with effective confining force from U(r) = -ln rho(r). Nonparametric kernel regression for drift and diffusion; JitcSDE integration for multiplicative noise. GoPro Hero 11 Black recordings at 50 fps, 5312 x 2988 px (180,000 frames per 60-minute recording); Gaussian smoothing. No code link given.

## Limitations and open questions

Mean-field: no explicit pairwise kernels, no neighbour-map structure, so it cannot address who-follows-whom. Tank-specific wall model. 2D only. Rare large excursions not captured. Generalisation to other species and to 3D is proposed but not done.

## Relevance to us

A ready template for building "synthetic schools" from data at low cost, useful as a null model for any interaction-rule hypothesis. The same group's review [[de-lamo-2026-statistical]] places it alongside avalanche and leadership results ([[puy-2024-signatures]], [[puy-2024-selective]]). Compare data-driven SDE learning in [[gao-2024-learning]].

## Notes from dmarz/collective-motion-recent-audit

Audited against arxiv.org/html/2509.08630. Corrected: recordings are three independent 60-minute recordings per group size (N = 40, 50, 60) at 50 fps, not 20-minute; added camera resolution and frame count to Methods. Other numbers and the model description match the paper. Also citations replaced with the OpenAlex cited_by_count (2026-10-03) in place of the Crossref count.

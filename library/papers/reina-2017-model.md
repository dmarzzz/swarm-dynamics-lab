---
id: reina-2017-model
type: paper
title: "Model of the best-of-N nest-site selection process in honeybees"
authors: ["Andreagiovanni Reina", "James A. R. Marshall", "Vito Trianni", "Thomas Bose"]
year: 2017
venue: "Physical Review E"
url: "https://arxiv.org/abs/1611.07575"
doi: "10.1103/physreve.95.052411"
arxiv: "1611.07575"
cite: "Reina, A., Marshall, J. A. R., Trianni, V., & Bose, T. (2017). Model of the best-of-N nest-site selection process in honeybees. Physical Review E, 95(5), 052411. https://doi.org/10.1103/physreve.95.052411"
topics: ["collective-decision", "swarm-intelligence", "swarm-robotics"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "83 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Generalises the honeybee cross-inhibition model from two to N nest sites. The authors prove that the earlier value-sensitive parameterisation cannot break deadlock among three or more equal options for any non-negative cross-inhibition, propose a new parameterisation in which recruitment and stop-signalling scale with option quality, and show that the ratio r of interaction to spontaneous transition rates becomes the control parameter for deadlock breaking and for accuracy in best-of-N choices.

## Contribution

First analytic treatment of value-sensitive best-of-N consensus in this model family, with closed-form bifurcation points for N equal options and a reduced two-variable system that works for arbitrary N. It identifies a conflict between what N equal options need (high signalling) and what best-of-N accuracy needs (low signalling), and proposes increasing signalling over time as a decentralised resolution. Builds on [[pais-2013-mechanism]] and [[seeley-2012-stop]].

## Key results

- General model dx_i/dt = gamma_i x_u - alpha_i x_i + rho_i x_u x_i - sum_j x_j beta_ji x_i; with gamma = rho = v, alpha = 1/v, beta_ij = beta and N = 3 equal options, the extra equilibria require 8 v^3 / (1 - 4 v^2) < beta < 0, so no positive cross-inhibition breaks deadlock (proved in Appendix B).
- New parameterisation gamma_i = k v_i, alpha_i = k / v_i, rho_i = h v_i, beta_ij = h v_i with r = h / k recovers the binary Pais et al. results, including the Weber-like just-noticeable difference.
- Symmetric case bifurcations: r1 = 1/v^2 - 2 + N + 2 sqrt(2N - 3) / v and r2 = (N - 3) N + 2 + 1/v^2 + ((N - 1)/v) sqrt(4 + v^2 (N - 2)^2). r1 grows about linearly and r2 quadratically with N, so many equal options prevent deadlock breaking.
- Best-of-N with kappa = v_inferior / v_best: low r gives a unique attractor for the best option but possibly below quorum; high r creates attractors for inferior options; for kappa = 0.97 and N = 3 no r gives a unique best-option attractor.
- The r needed to keep at least 75 per cent of the population on the best option rises roughly linearly with N for fixed kappa.
- Example trajectories (k = 0.1, h = 0.3, v = 10) converge on time scales comparable to field swarm decisions if t is read in hours (the authors' interpretation).

## Methods and models

Mean-field ODEs for fractions committed to each of N options plus an uncommitted pool; aggregation of the N - 1 inferior options into one variable gives a two-dimensional reduced system whose bifurcation points match the full system (checked numerically for N = 4 to 7). Stability diagrams in (r, v), (r, kappa) and (r, N); phase portraits for N = 3. No stochastic finite-N analysis and no code repository.

## Limitations and open questions

Deterministic and infinite-population only; inferior options are assumed equal; cross-inhibition depends only on the sender's option quality. The proposed time-increasing signalling strategy is a hypothesis, not tested against swarm data. Quality values must be at least 1 for biologically meaningful states under this parameterisation.

## Relevance to us

Gives us exact formulas to check a simulated swarm against when scaling the number of options, which is exactly the regime robot studies rarely test (see the n = 2 bias noted in [[valentini-2017-best]]). The r-ramping idea is a cheap, testable hypothesis for a swarm experiment. Related: [[reina-2015-design]], [[reina-2024-speed]], [[gray-2018-multiagent]], [[march-pons-2024-honeybee]].

## Notes from dmarz/collective-decision-audit

Audited 2026-10-03: opened the full text and checked title, authors, year, venue, volume/pages (against Crossref) and every number in Key results against the paper. No errors found; read_depth full is consistent with the methods detail.

---
id: hang-2026-self
type: paper
title: "Self-reorganization and information transfer in large-scale models of fish schools"
authors: ["Haotian Hang", "Chenchen Huang", "Alex Barnett", "Eva Kanso"]
year: 2026
venue: "Nature Communications"
url: https://www.nature.com/articles/s41467-026-70569-y
doi: "10.1038/s41467-026-70569-y"
arxiv: null
cite: "Hang, H., Huang, C., Barnett, A., & Kanso, E. (2026). Self-reorganization and information transfer in large-scale models of fish schools. Nature Communications, 17(1), 4324."
topics: [collective-motion, criticality-measurement, active-matter]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "1 (OpenAlex W7140129845, 2026-10-03)"
code: []
---
## Summary

Simulations of up to 50,000 fish that turn toward and align with their Voronoi neighbours (rules inferred from shallow-water experiments, frontal visual bias weight 1 + cos theta_ij) and are also advected by the far-field potential dipole flows of all other fish. Schools up to about 1000 fish stay cohesive and polarised (P > 0.95); above that they continually fragment, disperse and merge. Removing hydrodynamics removes the fragmentation at any noise level, so flow interactions drive it, and the size at which cohesion is lost falls as dipole strength (body size times speed) rises. In cohesive clusters the velocity-fluctuation correlation length grows linearly with school length (xi approx 0.37 L - 0.84, R^2 = 0.83, slope near the 1/3 seen in starlings), but xi/L drops significantly before fragmentation (p down to 6e-5 in the last 10 time units), making it an early-warning signal. Turning information propagates linearly in time at about 17-20 times swimming speed; the authors derive a first-order advection equation from the non-reciprocal (front-biased) vision term with speed c = gamma alpha I_a / 2, contrasting with the inertia-based wave mechanism of Attanasi et al.

## Contribution

First simulation of hydrodynamically coupled schools at 10^4-10^5 scale; shows that scale-free correlation is generic to rotational-symmetry-breaking flocks but breaks down before fission, and offers non-reciprocity (not behavioural inertia) as a mechanism for linear, anisotropic, front-to-back information spread.

## Key results

- Simulation: polarisation transition from cohesive to self-reorganising regime near N approx 1000 (I_a = 9, I_n = 0.5, I_f = 0.01).
- Simulation: school speed 1.20 U at N = 100, 1.08 at 1000, 0.54 at 10,000 (clusters move fast in different directions).
- Simulation: xi linear in L for P > 0.9; decrease of xi and xi/L precedes splitting (10 Monte Carlo runs at N = 1000).
- Simulation: information speed c scales linearly with I_a/I_n (c = 0.65 I_a/I_n + 0.73 in free turns); slower during splitting (about 3 U), faster during merging (up to about 40 U); hydrodynamics increases c beyond the vision-only prediction.
- Simulation: polarisation obeys P = 1 - I_n/I_a (spin-wave relation).
- Claimed: flow physics may limit group size and favour small-bodied fish in massive schools (consistent with sardines, herring, anchovies, but not tested).

## Methods and models

Kinematic model, Eqs. (1)-(2): dx_i/dt = U p_i + U_i (dipole flow), dtheta_i = weighted Voronoi attraction plus I_a alignment + Omega_i dt + I_n dW. Numba-parallel O(N^2) dipole sums, scipy Delaunay, Euler-Maruyama dt = 0.01; 50,000 agents for T = 1000 took about three weeks on a 56-core Xeon. HDBSCAN cluster detection, turning ranks from curvature cross-correlation (Attanasi method). Code and data: https://github.com/ekanso/schooling_extreme . Preprint version arXiv:2505.05822 ("...in Massive Schools of Fish").

## Limitations and open questions

2D, far-field dipoles only, constant speed, no empirical large-school data to validate fragmentation statistics. Unbounded domain. The early-warning signal is shown in simulation only. Relative weight of inertia vs non-reciprocity in real groups is left open.

## Relevance to us

Gives a concrete, measurable early-warning indicator (xi/L drop) and a scaling law for information speed that we could test in our own simulations or on tracking data. Builds on [[huang-2024-collective]] (same model, confined). Compare with [[zheng-2024-body]] and [[puy-2024-signatures]] on scale-free correlation and avalanches.

## Notes from dmarz/collective-motion-recent-audit

Audited against the Nature Communications full text: N up to 50,000; xi = 0.37 L - 0.84 with R^2 = 0.83; speeds 1.20/1.08/0.54 U; c = 0.65 I_a/I_n + 0.73; P = 1 - I_n/I_a; cite (17, 4324) confirmed. No corrections. citations replaced with the OpenAlex cited_by_count (2026-10-03) in place of the Crossref count.

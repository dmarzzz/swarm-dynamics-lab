---
id: cavagna-2010-scale
type: paper
title: Scale-free correlations in starling flocks
authors: [Andrea Cavagna, Alessio Cimarelli, Irene Giardina, Giorgio Parisi, Raffaele Santagati, Fabio Stefanini, Massimiliano Viale]
year: 2010
venue: Proceedings of the National Academy of Sciences
url: https://arxiv.org/abs/0911.4393
doi: 10.1073/pnas.1005766107
arxiv: '0911.4393'
cite: Cavagna, A., Cimarelli, A., Giardina, I., Parisi, G., Santagati, R., Stefanini, F., & Viale, M. (2010). Scale-free correlations in starling flocks. Proceedings of the National Academy of Sciences, 107(26), 11865–11870.
topics: [collective-motion, criticality-measurement]
added_by: dmarz/collective-motion
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "1017 (Crossref is-referenced-by-count, 2026-10-03); 1030 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Using tracked 3D velocities of individual starlings in 24 flocks (122 to 4268 birds, 9.1 m to 85.7 m across),
the authors subtract the flock's mean velocity and compute the spatial correlation function of the residual
velocity fluctuations. The correlation length (the zero crossing of C(r)) grows linearly with flock size,
xi ~ 0.35 L, for both heading and speed fluctuations. Correlations are therefore scale-free: a perturbation
to one bird is felt across the whole flock even though each bird interacts with about seven neighbours. They
argue this is a signature of flocks operating near criticality. Read from arXiv 0911.4393 (preprint title
"Scale-free correlations in bird flocks").

## Contribution

The founding empirical result for the "criticality in animal collectives" programme: it separates order
(polarization, which tells little) from response (correlation of fluctuations), and shows that in a real
flock the correlation length is limited only by group size. It motivated [[bialek-2012-statistical]],
[[attanasi-2014-information]], [[cavagna-2017-dynamic]] and the critical-swarm literature reviewed in
[[romanczuk-2022-phase]].

## Key results

- Mean polarization over 24 flocks: Phi = 0.96 +/- 0.03 (SD).
- Orientation correlation length xi = a L with a = 0.35 (Pearson n = 24, r = 0.98); speed correlation length
  scales the same way with a = 0.36 (r = 0.97).
- Scaling form C(r; L) = f(r/L) / r^gamma with gamma very small: gamma = 0.19 +/- 0.08 for orientation and
  0.19 +/- 0.11 for speed, but data equally fit a logarithmic or constant derivative (they span barely one
  decade), so the measured claim is "gamma is close to zero".
- Synthetic control: replacing fluctuations with exponentially correlated random vectors reproduces the bird
  data only when the decay length exceeds the flock size.
- Contrast with bacteria, where correlation length is finite and much smaller than the swarm.
- Interpretation (argued, not proven): scale-free speed correlations, a "stiff" mode, are hard to get by low
  noise alone, so criticality is "perhaps a more likely scenario".

## Methods and models

Stereometric photogrammetry from the roof of Palazzo Massimo, Rome, winters 2005-2007, 10 fps; dynamic
matching (tracking) efficiency 0.77. Velocity fluctuation u_i = v_i - (1/N) sum_k v_k; correlation
C(r) = sum_ij u_i.u_j delta(r - r_ij) / sum_ij delta(r - r_ij), normalised to C(0) = 1; xi defined by
C(xi) = 0, which is guaranteed to exist because the fluctuations sum to zero. Domain size cross-checked
by the top eigenvector of the covariance matrix.

## Limitations and open questions

- Because the fluctuations sum to zero by construction, C(r) must cross zero inside the flock; xi ~ L is
  partly geometric. The non-trivial claim is that only two domains span the flock and gamma ~ 0. Later work
  debated how much of the scaling is a finite-size or definition effect (see [[romanczuk-2022-phase]]).
- Static snapshots; dynamics and time scales of information transfer are deferred to
  [[attanasi-2014-information]].
- Low-noise ordered state versus true criticality cannot be distinguished with these data (the authors say
  so).

## Relevance to us

Gives a concrete, cheap measurement to run on any simulated swarm: subtract the mean velocity, compute
C(r), find xi, and plot xi against group size. A swarm design that keeps xi proportional to L is maximally
responsive. Links: [[ballerini-2008-interaction]], [[cavagna-2014-bird]], [[puy-2024-signatures]],
[[gomez-nava-2023-fish]].

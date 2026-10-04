---
id: sooter-2025-defining
type: paper
title: 'Defining and measuring proximity to criticality'
authors: ['J. Samuel Sooter', 'Antonio J. Fontenele', 'Andrea K. Barreiro', 'Cheng Ly', 'Keith B. Hengen', 'Woodrow L. Shew']
year: 2025
venue: 'bioRxiv'
url: https://www.biorxiv.org/content/10.1101/2025.08.03.668332v2
doi: 10.1101/2025.08.03.668332
arxiv: null
cite: 'Sooter, J. S., Fontenele, A. J., Barreiro, A. K., Ly, C., Hengen, K. B., & Shew, W. L. (2025). Defining and measuring proximity to criticality. bioRxiv, 2025.08.03.668332.'
topics: [criticality-measurement]
added_by: dmarz/criticality-measurement-audit
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: '10 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Asks how to measure distance to criticality when no control parameter is known or manipulable. The authors
define a temporal renormalization group (tRG) for time series, by analogy with Wilson's momentum-shell scheme,
find its fixed points for autoregressive (AR) models, and define distance to criticality as the minimal
Kullback-Leibler divergence rate between the best-fit AR model of the data and the manifold of critical AR
models. After benchmarking on ground-truth cases, they apply it to long spike recordings from visual cortex of freely behaving rats (96-240 h per animal, 8 rats) and
from mice, and find the cortex closest to criticality during wakefulness and further away during deep sleep.

## Contribution

A parameter-free, information-theoretic definition of distance to criticality with a two-step data pipeline
(fit AR model, compute KL distance to the critical manifold). It addresses exactly the problem that
[[poel-2022-subcritical]] and [[daniels-2017-control]] solve with system-specific models.

## Key results

- tRG fixed points of AR models classified by spectral exponent beta (for example the beta = 2 manifold) (analytic).
- Distance d_2 agrees with ground-truth distance to criticality in benchmark models (simulation).
- Rat and mouse cortex: d_2 smallest in the awake state, largest during NREM sleep (measured).

## Methods and models

Time series to Fourier domain, coarse-grain frequencies, rescale; AR(n) models fitted by maximum likelihood;
analytic KL divergence rate J(A||B) between AR spectra; numerical minimisation over critical AR models. Toolkit
announced, link marked "TBD" in the preprint.

## Limitations and open questions

Preprint (v2, September 2025), not yet peer reviewed. Linear AR models capture only second-order temporal
structure; multivariate collective data need a reduction to time series first.

## Relevance to us

Probably the most directly portable distance-to-criticality measure for swarm order-parameter time series
(polarisation, milling). Compare with [[du-2026-fisher]], [[wilting-2018-inferring]], [[meshulam-2019-coarse]].

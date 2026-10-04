---
id: morrell-2021-latent
type: paper
title: 'Latent Dynamical Variables Produce Signatures of Spatiotemporal Criticality in Large Biological Systems'
authors: ['Mia C. Morrell', 'Audrey J. Sederberg', 'Ilya Nemenman']
year: 2021
venue: 'Physical Review Letters'
url: https://arxiv.org/abs/2008.04435
doi: 10.1103/physrevlett.126.118302
arxiv: '2008.04435'
cite: 'Morrell, M. C., Sederberg, A. J., & Nemenman, I. (2021). Latent Dynamical Variables Produce Signatures of Spatiotemporal Criticality in Large Biological Systems. Physical Review Letters, 126(11), 118302.'
topics: [criticality-measurement]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: '43 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Simulates conditionally independent binary neurons driven by a few slow latent stochastic fields
and applies the same coarse-graining (phenomenological renormalisation) analysis used on mouse hippocampus
recordings. The model reproduces the experimentally observed power-law scalings of free energy, variance,
eigenvalue spectra and correlation time, without any fine-tuned interactions.

## Contribution

Strong cautionary result: spatiotemporal criticality signatures from coarse-graining can be
produced by shared latent inputs alone.

## Key results

- Latent-variable model reproduces over two decades of scaling reported for hippocampal data (simulation).
- Scaling emerges only when most cells couple to the latent fields.

## Methods and models

Binary neurons with firing probabilities driven by low-dimensional Ornstein-Uhlenbeck latent fields;
coarse-graining by correlation-based pairing. arXiv 2008.04435.

## Limitations and open questions

Neural setting; abstract-level read.

## Relevance to us

In swarms, a shared external driver (wind, light, landmark, leader signal) is a latent variable;
apparent scale-free correlations could be extrinsic. See [[schwab-2014-zipfs]],
[[ngampruetikorn-2025-extrinsic]].

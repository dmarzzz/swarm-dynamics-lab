---
id: brown-2020-information
type: paper
title: 'Information flow in finite flocks'
authors: ['J. Brown', 'T. Bossomaier', 'L. Barnett']
year: 2020
venue: 'Scientific Reports'
url: https://arxiv.org/abs/1809.03723
doi: 10.1038/s41598-020-59080-6
arxiv: '1809.03723'
cite: 'Brown, J., Bossomaier, T., & Barnett, L. (2020). Information flow in finite flocks. Scientific Reports, 10(1), 3837.'
topics: [criticality-measurement, collective-motion]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: '20 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Simulates the canonical Vicsek model with finite flocks and estimates global transfer entropy as a
function of angular noise. Unlike the Ising result of [[barnett-2013-information]], global transfer entropy
does not peak near the flocking transition; it stays roughly constant from the transition down to very low
noise.

## Contribution

Negative result showing that Ising-based expectations about information flow at transitions do
not transfer straightforwardly to self-propelled flocks.

## Key results

- Global transfer entropy in finite Vicsek flocks fails to peak near the order-disorder transition and remains constant from the transition to low noise (simulation).

## Methods and models

Vicsek model simulations; global transfer entropy estimation over noise sweep. arXiv 1809.03723.

## Limitations and open questions

Finite-size and estimator choices could matter; only metric Vicsek interactions here (topological
version in a follow-up). Abstract-level read.

## Relevance to us

Directly relevant if we plan to use transfer entropy as a criticality indicator in flocking
simulations: it may not work. Compare [[crosato-2018-thermodynamics]] (Fisher information does peak).

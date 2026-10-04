---
id: morales-2023-quasiuniversal
type: paper
title: 'Quasiuniversal scaling in mouse-brain neuronal activity stems from edge-of-instability critical dynamics'
authors: ['Guillermo B. Morales', 'Serena di Santo', 'Miguel A. Muñoz']
year: 2023
venue: 'Proceedings of the National Academy of Sciences'
url: https://europepmc.org/article/PMC/PMC9992863
doi: 10.1073/pnas.2208998120
arxiv: null
cite: 'Morales, G. B., di Santo, S., & Muñoz, M. A. (2023). Quasiuniversal scaling in mouse-brain neuronal activity stems from edge-of-instability critical dynamics. Proceedings of the National Academy of Sciences, 120(9), e2208998120.'
topics: [criticality-measurement]
added_by: dmarz/criticality-measurement-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: '55 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Applies the phenomenological renormalization group of [[meshulam-2019-coarse]] to simultaneous recordings of
thousands of neurons across many mouse brain regions, combined with tools that infer the dynamical state of a
population (distance to the edge of instability of a linearised dynamics). Finds scaling exponents that are
similar ("quasiuniversal") across regions and experiments, and that all regions operate, to different degrees,
near the edge of instability.

## Contribution

Connects static PRG scaling to a dynamical, edge-of-instability interpretation and tests it across regions,
moving the PRG approach from a single data set to a comparative measurement.

## Key results

- Strong scale-invariance signatures under PRG across brain regions, with similar exponents (measured, claimed in abstract).
- All analysed areas operate near the edge of instability, to a greater or lesser extent (inference).

## Methods and models

High-throughput recordings of thousands of single neurons from multiple mouse brain regions; PRG coarse-graining; linear
response / eigenvalue-based inference of distance to instability; complementary model analysis.

## Limitations and open questions

Abstract-level read. Edge of instability (a dynamical, linear notion) is not the same as a second-order phase
transition, and latent-variable explanations ([[morrell-2021-latent]]) are not fully excluded.

## Relevance to us

Shows how to combine PRG scaling with a dynamical stability estimate; the same pair could be computed on
swarm trajectories. From the same group as [[munoz-2018-colloquium]].

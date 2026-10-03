---
id: chandra-2019-continuous
type: paper
title: "Continuous versus Discontinuous Transitions in the D-Dimensional Generalized Kuramoto Model: Odd D is Different"
authors: [Sarthak Chandra, Michelle Girvan, Edward Ott]
year: 2019
venue: Physical Review X
url: https://arxiv.org/abs/1806.01314
doi: 10.1103/physrevx.9.011002
arxiv: '1806.01314'
cite: "Chandra, S., Girvan, M., & Ott, E. (2019). Continuous versus discontinuous transitions in the D-dimensional generalized Kuramoto model: Odd D is different. Physical Review X, 9(1), 011002."
topics: [sync-consensus, collective-motion]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "97 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Generalises the Kuramoto model from phases on a circle to unit vectors in D dimensions, motivated by the
alignment of orientation vectors in 3D swarms (and by the mean-field zero-temperature Heisenberg model with
quenched disorder). For heterogeneous units, odd D (including the physically important D = 3) behaves very
differently from D = 2: the transition to coherence is discontinuous and occurs as the coupling K passes through
zero, whereas for even D it is continuous at a positive critical coupling K_c, as in the classic Kuramoto model.

## Contribution

Shows that results from 2D (circle) Kuramoto models, often used as proxies for heading alignment, do not carry
over to 3D flocks; the authors demonstrate qualitative applicability to swarming and flocking models in 3D.

## Key results

- Odd D: discontinuous onset of coherence at K = 0 for heterogeneous units (abstract).
- Even D, including D = 2: continuous onset at K_c > 0 (abstract).

## Methods and models

Generalised Kuramoto dynamics on the (D-1)-sphere with rotation-matrix "natural frequencies"; mean-field
analysis and simulations; companion work by the same authors gives a dimension-reduction ansatz. Full text not
read.

## Limitations and open questions

Mean-field (all-to-all) coupling; real 3D flocks have local, topological interactions.

## Relevance to us

If a hackathon project simulates 3D drone headings with a Kuramoto-style rule, expect an abrupt alignment
transition rather than the 2D picture of [[strogatz-2000-kuramoto]]. Also relevant to 3D swarmalators
([[sar-2026-interplay]] lists 3D as open).

---
id: attanasi-2014-finite
type: paper
title: 'Finite-Size Scaling as a Way to Probe Near-Criticality in Natural Swarms'
authors: ['Alessandro Attanasi', 'Andrea Cavagna', 'Lorenzo Del Castello', 'Irene Giardina', 'Stefania Melillo', 'Leonardo Parisi', 'Oliver Pohl', 'Bruno Rossaro', 'Edward Shen', 'Edmondo Silvestri', 'Massimiliano Viale']
year: 2014
venue: 'Physical Review Letters'
url: https://arxiv.org/abs/1412.6975
doi: 10.1103/physrevlett.113.238102
arxiv: '1412.6975'
cite: 'Attanasi, A., Cavagna, A., Del Castello, L., Giardina, I., Melillo, S., Parisi, L., Pohl, O., Rossaro, B., Shen, E., Silvestri, E., et al. (2014). Finite-Size Scaling as a Way to Probe Near-Criticality in Natural Swarms. Physical Review Letters, 113(23), 238102.'
topics: [criticality-measurement, collective-motion]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: '197 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Using 3D field reconstructions of wild midge swarms, the authors show that swarms of different
sizes adjust their control parameter (effectively density / nearest-neighbour distance) so that the
correlation function keeps a scaling form. As a result correlation length and susceptibility grow with swarm
size and every swarm sits near its own finite-size pseudo-critical point.

## Contribution

Introduces finite-size scaling as an operational test of near-criticality in biological
groups, which are far from the thermodynamic limit, and reports the first observation of size-dependent
retuning of the control parameter.

## Key results

- Correlation length and susceptibility scale with swarm size; swarms show near-maximal correlation at all sizes (measured on field midge data).
- Swarms co-vary control parameter and size to stay on the finite-size scaling curve (claimed interpretation of measured scaling).

## Methods and models

Stereometric 3D tracking of Cladocera/Chironomidae midge swarms in Rome parks; connected velocity
correlation function C(r), correlation length and susceptibility chi from integrated correlation; comparison
with Vicsek-type simulations near the ordering transition. arXiv 1412.6975.

## Limitations and open questions

Control parameter is inferred, not manipulated; small swarms (tens to hundreds of individuals).
Abstract-level read.

## Relevance to us

Gives us a concrete recipe for robot or agent swarms of different N: measure xi and chi vs N and
check whether a tuning parameter must change with N to stay maximally correlated. Pairs with
[[attanasi-2014-collective]], [[cavagna-2017-dynamic]] and [[cavagna-2023-natural]].

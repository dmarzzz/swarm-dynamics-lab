---
id: barnett-2013-information
type: paper
title: 'Information Flow in a Kinetic Ising Model Peaks in the Disordered Phase'
authors: ['Lionel Barnett', 'Joseph T. Lizier', 'Michael Harré', 'Anil K. Seth', 'Terry Bossomaier']
year: 2013
venue: 'Physical Review Letters'
url: https://europepmc.org/article/MED/24206517
doi: 10.1103/physrevlett.111.177203
arxiv: null
cite: 'Barnett, L., Lizier, J. T., Harré, M., Seth, A. K., & Bossomaier, T. (2013). Information Flow in a Kinetic Ising Model Peaks in the Disordered Phase. Physical Review Letters, 111(17), 177203.'
topics: [criticality-measurement]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: '127 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Conjectures and verifies for the 2D kinetic Ising model with Glauber dynamics that system-wide
information flow, measured by a transfer-entropy-based global quantity, peaks strictly on the disordered side
of the order-disorder transition, unlike mutual information, which peaks at the transition.

## Contribution

Separates information flow from correlation as a criticality indicator and suggests information
dynamics could act as an early-warning signal of an approaching transition.

## Key results

- Global transfer entropy peaks in the disordered phase, not at T_c (simulation of 2D Ising Glauber dynamics).
- Mutual information peaks at the transition (consistent with prior work).

## Methods and models

Kinetic 2D Ising lattice with Glauber dynamics; global transfer entropy averaged over spins.

## Limitations and open questions

Equilibrium spin model; [[brown-2020-information]] found the peak does not carry over to finite
Vicsek flocks. Abstract-level read.

## Relevance to us

A warning that "maximal information transfer at criticality" is not automatic; check where
transfer entropy peaks in our swarm models. Related: [[brown-2020-information]], [[chen-2025-why]].

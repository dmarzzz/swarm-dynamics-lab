---
id: poel-2022-subcritical
type: paper
title: 'Subcritical escape waves in schooling fish'
authors: ['Winnie Poel', 'Bryan C. Daniels', 'Matthew M. G. Sosna', 'Colin R. Twomey', 'Simon P. Leblanc', 'Iain D. Couzin', 'Pawel Romanczuk']
year: 2022
venue: 'Science Advances'
url: https://arxiv.org/abs/2108.05537
doi: 10.1126/sciadv.abm6385
arxiv: '2108.05537'
cite: 'Poel, W., Daniels, B. C., Sosna, M. M. G., Twomey, C. R., Leblanc, S. P., Couzin, I. D., & Romanczuk, P. (2022). Subcritical escape waves in schooling fish. Science Advances, 8(25), eabm6385.'
topics: [criticality-measurement, collective-motion, collective-decision]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: '77 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Studies startle (escape) cascades in schools of 40 juvenile golden shiners under two levels of
perceived risk (before and after alarm substance). A data-driven contagion model on visual interaction
networks, fitted to the observed cascade-size distributions, is used to predict cascades across rescaled
school densities. The model shows a transition from local to global cascades as nearest-neighbour distance
(NND) shrinks, with collective sensitivity (difference in cascade size from 2 vs 1 initial startlers)
peaking where an analytic branching ratio b = 1. Observed schools are subcritical, with alarmed schools
closer to criticality. A payoff model built on false-positive and false-negative escape costs shows that the
optimal distance to criticality depends on how risky and noisy the environment is.

## Contribution

Measures distance to criticality in a real animal group, shows it is regulated with context
rather than fixed at the critical point, and introduces an individual-level cost-benefit analysis of
criticality. It reframes the hypothesis from "be critical" to "tune distance to criticality".

## Key results

- Collective sensitivity at observed densities: 0.035 +/- 0.007 (baseline, median NND 1.23 +/- 0.3 BL) and 0.058 +/- 0.019 (alarmed, NND 0.68 +/- 0.12 BL); becoming critical would raise sensitivity by factors 5.9 and 3.4.
- Maximum sensitivity (about 0.2 difference in relative cascade size) at NND of 0.3-0.4 BL, close to the physical packing limit; density alone cannot push schools supercritical.
- Branching-ratio manifold b = 1 tracks the sensitivity maximum in the (NND, mean threshold) plane.
- Payoff analysis: safe/noisy environments favour low density and subcriticality; risky environments favour criticality or beyond; intermediate noise costs give two optima (one near criticality, one at maximal personal visual access).

## Methods and models

Data from Sosna et al. (2019) and Rosenthal et al. (2015). Network weights
w_ij = logistic(beta1 + beta2 log metric distance + beta3 ranked angular area) from first-responder data;
fractional SIR-type contagion: susceptible fish integrate cues from active neighbours over memory tau_m = 1 s,
normalised by number of visible neighbours, and startle when above a threshold drawn uniformly in
[0, 2 theta_bar]; theta_bar fitted by maximum likelihood (10,000 simulated cascades per network). Positions
rescaled to explore densities, with ellipse overlap removal and analytic visual fields. Branching ratio
b_j = (tau_act/theta_max) sum_i w_ij/K_i. Relative payoff psi = -[p_fp r + p_fn]/psi_0.

## Limitations and open questions

Cascades were spontaneous false alarms in a lab tank without real predators; interaction networks
are static during a cascade; interaction form assumed density-independent; N = 40 so the transition is
smooth. Authors note natural conditions or larger groups could move schools closer to criticality.

## Relevance to us

The best worked example of measuring distance to criticality with a functional order parameter
(cascade size) and a finite-size susceptibility (sensitivity to 1 vs 2 initiators). Directly reusable for
agent or robot swarms with alarm propagation. Pairs with [[klamser-2021-collective]], [[gomez-nava-2023-fish]],
[[daniels-2017-control]] and [[strandburg-peshkin-2013-visual]].

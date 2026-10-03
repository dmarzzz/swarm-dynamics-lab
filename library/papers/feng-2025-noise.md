---
id: feng-2025-noise
type: paper
title: Noise-Driven Transitions in Collective Foraging of Ant Colonies
authors: [Tao Feng, Chenbo Liu, Russell Milne]
year: 2025
venue: Bulletin of Mathematical Biology
url: https://www.ebi.ac.uk/europepmc/webservices/rest/article/MED/40392365?resultType=core&format=json
doi: 10.1007/s11538-025-01461-x
arxiv: null
cite: Feng, T., Liu, C., & Milne, R. (2025). Noise-driven transitions in collective foraging of ant colonies. Bulletin of Mathematical Biology, 87(6), 78. https://doi.org/10.1007/s11538-025-01461-x
topics: [collective-decision, swarm-intelligence, criticality-measurement]
added_by: dmarz/swarm-intelligence-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 5 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Builds a two-compartment model of ant-colony foraging (available workers and active foragers) that reproduces the
dynamics of more complex three-compartment models while being analytically tractable. Adds stochasticity to the
mortality rates and studies noise-induced transitions between foraging states: the critical noise threshold, the
transition probability and the transition time. Forager mortality noise lowers the critical threshold most; small
increases in worker arrival and forager recruitment rates make the colony more resilient to environmental noise.

## Contribution

A recent stochastic-dynamics treatment of the biological system that ant colony optimisation abstracts. It is
relevant to swarm dynamics because it treats colony foraging as a noise-driven transition between states, with
thresholds that can be measured. It links the biological side of the scan ([[deneubourg-1990-self]],
[[garnier-2007-biological]]) to criticality questions.

## Key results

- Claimed (abstract): noise in either mortality rate lowers the critical noise threshold, and forager-mortality noise
  has the largest effect.
- Claimed: slightly higher arrival rate of available workers and recruitment rate of foragers increase resilience to
  environmental stochasticity (a foraging-recruitment feedback loop).
- Claimed: varying the mortality of available workers has little effect on resilience, consistent with observations
  that old or unhealthy workers move into foraging.

## Methods and models

Two-variable ODE compartment model with stochastic (noise-perturbed) mortality rates; analysis of noise-induced
transitions (thresholds, transition probabilities and times). Numbers and noise model details not read (abstract via
Europe PMC; Springer full text not accessed, not open access).

## Limitations and open questions

Unread beyond the abstract. A mean-field compartment model, so no spatial trails or pheromone dynamics; the link to
ACO is conceptual only. Validation against colony data is not stated in the abstract.

## Relevance to us

Gives a measurable "noise threshold for collapse of collective foraging", a biological counterpart to the noise
thresholds in swarm optimisers ([[huang-2023-global]], [[pinnau-2017-consensus]]) and to order-disorder transitions
in [[vicsek-1995-novel]].

---
id: bernardo-2024-bounded
type: paper
title: "Bounded confidence opinion dynamics: A survey"
authors: [Carmela Bernardo, Claudio Altafini, Anton Proskurnikov, Francesco Vasca]
year: 2024
venue: Automatica
url: https://api.openalex.org/works/doi:10.1016/j.automatica.2023.111302
doi: 10.1016/j.automatica.2023.111302
arxiv: null
cite: "Bernardo, C., Altafini, C., Proskurnikov, A., & Vasca, F. (2024). Bounded confidence opinion dynamics: A survey. Automatica, 159, 111302."
topics: [sync-consensus, collective-decision]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "105 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Surveys the Hegselmann-Krause bounded confidence opinion dynamics (BCOD) model and its variants: agents average
only the opinions within a confidence bound of their own, so the interaction graph depends on the state. It
reviews conditions for convergence (finite-time or asymptotic) for synchronous BCOD with possibly asymmetric and
heterogeneous confidence bounds, the possible structures of terminal opinions (consensus, clusters), numerically
observed phenomena such as sensitivity to confidence thresholds, and recent modifications and applications.

## Contribution

The up-to-date, systematic reference for state-dependent-graph consensus; bounded confidence is the opinion
analogue of the metric-radius neighbourhood in Vicsek flocking and [[jadbabaie-2003-coordination]].

## Key results

- Abstract-level: convergence conditions (finite-time or asymptotic), terminal opinion structures, numerical
  phenomena, recent modifications.

## Methods and models

Survey. Abstract from the OpenAlex record (Elsevier page blocked).

## Limitations and open questions

Restricted to time-synchronous interactions (as the abstract states), so asynchronous, pairwise (gossip-type)
bounded-confidence models are by implication outside its main scope.

## Relevance to us

State-dependent neighbourhoods are the norm in swarms; the clustering results here predict when a swarm or agent
population splits into factions instead of agreeing.

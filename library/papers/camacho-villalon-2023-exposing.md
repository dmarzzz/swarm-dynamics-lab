---
id: camacho-villalon-2023-exposing
type: paper
title: 'Exposing the grey wolf, moth-flame, whale, firefly, bat, and antlion algorithms: six misleading optimization techniques inspired by bestial metaphors'
authors:
- Christian L. Camacho-Villalón
- Marco Dorigo
- Thomas Stützle
year: 2023
venue: International Transactions in Operational Research
url: https://api.openalex.org/works/W4288040592
doi: 10.1111/itor.13176
arxiv: null
cite: 'Camacho-Villalón, C. L., Dorigo, M., & Stützle, T. (2023). Exposing the grey wolf, moth-flame, whale, firefly, bat, and antlion algorithms: Six misleading optimization techniques inspired by bestial metaphors. International Transactions in Operational Research, 30(6), 2945–2971. https://doi.org/10.1111/itor.13176'
topics:
- swarm-intelligence
- meta
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 115 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Component-based analysis of six widely used metaphor-based continuous optimisers (grey wolf, moth-flame, whale,
firefly, bat, antlion): each is deconstructed into components and mapped to equivalent components in established
techniques such as PSO and evolutionary algorithms. Concludes that the ideas have been in the literature for years and
that the only novelty is six new terminologies; argues these metaphors are misleading and useless for design, and that
authors' justifications rest on a misunderstanding of the no-free-lunch theorems ([[wolpert-1997-no]]).

## Contribution

The most thorough deconstruction of popular swarm metaphors by the ACO group; strongest evidence that "new swarm
algorithm" claims should be checked against PSO components.

## Key results

- Claimed (abstract): all six algorithms reduce to known PSO/EA components; novelty is terminological.

## Methods and models

Component-based algorithm analysis (abstract only; publisher PDF blocked).

## Limitations and open questions

Abstract-level reading. Analytical equivalence does not speak to implementation quality; [[vermetten-2024-large]]
shows some implementations of re-labelled methods still perform well.

## Relevance to us

Key prior work for any "is this swarm algorithm novel?" question; pairs with [[mirjalili-2014-grey]] and
[[kudela-2023-evolutionary]].

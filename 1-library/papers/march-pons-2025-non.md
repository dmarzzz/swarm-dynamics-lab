---
id: march-pons-2025-non
type: paper
title: "Non-linear inhibitory responses enhance performance in collective decision-making"
authors: ["David March-Pons", "Romualdo Pastor-Satorras", "M. Carmen Miguel"]
year: 2025
venue: "Communications Physics"
url: "https://www.nature.com/articles/s42005-025-02046-9"
doi: "10.1038/s42005-025-02046-9"
arxiv: null
cite: "March-Pons, D., Pastor-Satorras, R., & Miguel, M. C. (2025). Non-linear inhibitory responses enhance performance in collective decision-making. Communications Physics, 8(1), 119. https://doi.org/10.1038/s42005-025-02046-9"
topics: ["collective-decision", "swarm-intelligence"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "3 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Introduces a non-linear, threshold-like inhibitory response into a honeybee house-hunting decision model, in place of the usual linear cross-inhibition term. Non-linear inhibition gives stronger final consensus and shorter deliberation than linear inhibition, at the cost of lower accuracy in picking the best option; the authors argue the trade is worthwhile for value-based tasks.

## Contribution

Brings modulatory, response-threshold inhibition into the cross-inhibition model family ([[pais-2013-mechanism]], [[reina-2017-model]]); parallels the quorum-steepness argument for recruitment in [[sumpter-2009-quorum]].

## Key results

- Non-linear inhibitory response: higher consensus and faster decisions, lower best-option accuracy, compared with linear inhibition (model).
- Abstract-level reading only; numbers beyond the abstract were not checked.

## Methods and models

Population model of honeybee nest-site selection with a non-linear inhibition response function; analysis and simulation (details not checked).

## Limitations and open questions

Theory only per the abstract.

## Relevance to us

A single extra nonlinearity parameter we could sweep in a swarm simulation. Related: [[march-pons-2024-honeybee]], [[reina-2023-cross]].

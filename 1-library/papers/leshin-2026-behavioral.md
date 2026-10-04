---
id: leshin-2026-behavioral
type: paper
title: "Behavioral Fingerprints for LLM Endpoint Stability and Identity"
authors: ["Jonah Leshin", "Manish Shah", "Ian Timmis", "Daniel Kang"]
year: 2026
venue: "CAIS 2026 System Demonstrations (submitted); arXiv preprint"
url: https://arxiv.org/abs/2603.19022
doi: null
arxiv: "2603.19022"
cite: "Leshin, J., Shah, M., Timmis, I., & Kang, D. (2026). Behavioral Fingerprints for LLM Endpoint Stability and Identity. arXiv:2603.19022."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Stability Monitor periodically fingerprints a model endpoint by sampling outputs from a fixed prompt set and comparing output distributions over time with a summed energy-distance statistic and permutation-test p-values, aggregated sequentially to detect change events. In controlled validation it detects changes in model family, version, inference stack, quantisation and behavioural parameters; in real monitoring of one model across several providers it finds substantial provider-to-provider and within-provider differences.

## Contribution

Operational change-point monitoring of endpoint identity.

## Key results

- Detects family, version, stack, quantisation and parameter changes in controlled tests; real-world provider differences observed (abstract; no numbers).

## Methods and models

Fixed prompt set, energy distance, permutation tests, sequential aggregation.

## Limitations and open questions

Four-page demo; abstract-only reading.

## Relevance to us

Change detection on a fixed target is the time-series analogue of linking; a swarm account whose fingerprint shifts in step with others suggests shared backend changes (speculative). Related: [[gao-2024-model]].

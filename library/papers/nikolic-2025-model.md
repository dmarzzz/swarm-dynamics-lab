---
id: nikolic-2025-model
type: paper
title: "Model Provenance Testing for Large Language Models"
authors: ["Ivica Nikolic", "Teodora Baluta", "Prateek Saxena"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2502.00706
doi: null
arxiv: "2502.00706"
cite: "Nikolic, I., Baluta, T., & Saxena, P. (2025). Model Provenance Testing for Large Language Models. arXiv:2502.00706."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Tests whether one LLM is derived from another (fine-tuned, adapted) with black-box access only, using multiple hypothesis testing of output similarity against a baseline built from unrelated models. On two benchmarks spanning more than 600 models from 30M to 4B parameters, the tester reaches 90-95% precision and 80-90% recall in identifying derived models.

## Contribution

Black-box provenance testing with statistical guarantees at scale.

## Key results

- 90-95% precision and 80-90% recall over 600+ models (abstract).

## Methods and models

Compare output similarity between candidate pairs with a baseline from unrelated models; multiple hypothesis testing.

## Limitations and open questions

Small models (up to 4B); abstract-only reading.

## Relevance to us

Lineage tests let a detector say "these agents run fine-tunes of the same base", a coarser but more robust grouping than exact model identity. Compare [[yax-2024-phylolm]], [[bruckner-2026-one]].

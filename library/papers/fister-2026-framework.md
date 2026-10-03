---
id: fister-2026-framework
type: paper
title: Framework for identifying the equivalence between Nature-Inspired Metaheuristics
authors:
- Iztok Fister
- Žan Hozjan
- Iztok Fister Jr.
- Damjan Strnad
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2603.28255
doi: null
arxiv: '2603.28255'
cite: Fister, I., Hozjan, Ž., Fister Jr., I., & Strnad, D. (2026). Framework for identifying the equivalence between nature-inspired metaheuristics. arXiv preprint arXiv:2603.28255. https://doi.org/10.48550/arXiv.2603.28255
topics:
- swarm-intelligence
- meta
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 0 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Pushes back on the claim that all new nature-inspired algorithms are copies: defines a "strong equivalence" criterion
under which two metaheuristics are equivalent if the cosine similarity of phenotypic and genotypic feature vectors
describing their search behaviour exceeds a threshold, builds a framework on it, and reports that high similarity
between well-known nature-inspired metaheuristics is hard or impossible to reach in limited computational settings.

## Contribution

Behavioural (trajectory-based) rather than analytical test of equivalence, a counterpoint to
[[camacho-villalon-2023-exposing]]'s component analysis.

## Key results

- Claimed (abstract): well-known metaheuristics rarely meet the equivalence threshold experimentally.

## Methods and models

Feature vectors of search behaviour, cosine similarity threshold (abstract only). An Iztok Fister is a co-author of NiaPy (the
library used in [[vermetten-2024-large]]).

## Limitations and open questions

Abstract-level reading; preprint. Behavioural dissimilarity can arise from implementation details, not ideas.

## Relevance to us

Offers measurable descriptors of swarm search behaviour; could be repurposed to compare swarm dynamics across
algorithms.

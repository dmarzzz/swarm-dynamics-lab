---
id: jovanovic-2024-watermark
type: paper
title: Watermark Stealing in Large Language Models
authors:
- Nikola Jovanović
- Robin Staab
- Martin Vechev
year: 2024
venue: ICML 2024
url: https://arxiv.org/abs/2402.19361
doi: null
arxiv: '2402.19361'
cite: Jovanović, N., Staab, R., & Vechev, M. (2024). Watermark Stealing in Large Language Models. In Proceedings of the 41st International Conference on Machine Learning (ICML 2024). arXiv:2402.19361.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 113 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Shows that querying a watermarked LLM API lets an attacker approximately reverse-engineer the watermark ("watermark stealing"), enabling both spoofing (making human text look watermarked) and scrubbing (removing it). For under $50 the attack spoofs and scrubs state-of-the-art schemes with average success over 80%.

## Contribution

Cheap, practical attack on deployed-style watermarks, both directions.

## Key results

- Measured (abstract): spoofing and scrubbing success over 80% on average for under $50 of queries.

## Methods and models

Automated watermark-stealing algorithm from API queries. Abstract read only.

## Limitations and open questions

Abstract depth; specific schemes listed in the paper.

## Relevance to us

Spoofing means watermark evidence can be planted to frame a party, so watermark-based attribution of a swarm to a provider or operator is forgeable.

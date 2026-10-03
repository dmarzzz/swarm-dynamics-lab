---
id: huang-2025-wikipedia
type: paper
title: 'Wikipedia in the Era of LLMs: Evolution and Risks'
authors:
- Siming Huang
- Yuliang Xu
- Mingmeng Geng
- Yao Wan
- Dongping Chen
year: 2025
venue: Transactions on Machine Learning Research (2026)
url: https://arxiv.org/abs/2503.02879
doi: null
arxiv: '2503.02879'
cite: 'Huang, S., Xu, Y., Geng, M., Wan, Y., & Chen, D. (2025). Wikipedia in the Era of LLMs: Evolution and Risks. Transactions on Machine Learning Research. arXiv:2503.02879.'
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: 7 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Builds a monitoring framework for LLM impact on Wikipedia from article content and page views and simulates downstream risks. Finds an LLM impact of about 1% in certain article categories, and simulations suggest that LLM-contaminated Wikipedia would inflate machine-translation benchmark scores and could reduce RAG effectiveness.

## Contribution

Wikipedia-specific monitoring with downstream risk simulation.

## Key results

- Measured (abstract): about 1% LLM impact in certain categories.

## Methods and models

Word-frequency and page-view analysis; simulations for MT and RAG. Abstract read only.

## Limitations and open questions

Lower estimate than [[brooks-2024-rise]] (over 5% of new English articles flagged), because it measures existing articles rather than new pages. Abstract depth.

## Relevance to us

Second Wikipedia estimate; the gap with [[brooks-2024-rise]] shows that sampling new versus all articles changes the answer.

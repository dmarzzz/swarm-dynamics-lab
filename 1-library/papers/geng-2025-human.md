---
id: geng-2025-human
type: paper
title: 'Human-LLM Coevolution: Evidence from Academic Writing'
authors:
- Mingmeng Geng
- Roberto Trotta
year: 2025
venue: ACL 2025 (pages 12689-12696 per Semantic Scholar)
url: https://arxiv.org/abs/2502.09606
doi: null
arxiv: '2502.09606'
cite: 'Geng, M., & Trotta, R. (2025). Human-LLM Coevolution: Evidence from Academic Writing. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025), 12689-12696. arXiv:2502.09606.'
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 25 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Tracks arXiv abstracts after LLM marker words were publicised in early 2024 and finds a marked drop in words such as "delve" soon afterwards, while other ChatGPT-favoured words such as "significant" keep rising. Concludes that authors adapt their LLM use (selecting or editing outputs), so humans and LLMs coevolve, which complicates real-world detection; word-frequency estimation stays feasible if it uses already-common words and words that LLMs disfavour.

## Contribution

Direct evidence of evasion-by-adaptation at population level: publicising a detection marker makes it decay.

## Key results

- Measured (abstract): frequency of "delve" and similar flagged words dropped soon after early-2024 publicity; "significant" continued to increase.

## Methods and models

Word-frequency time series on arXiv abstracts. Abstract read only.

## Limitations and open questions

Cannot tell whether the drop reflects editing, model updates or reduced use. Abstract depth.

## Relevance to us

A measured negative result for marker-based detection: once markers are public, adversaries and ordinary users route around them. Any swarm detector built on lexical tells should expect the same decay. Pairs with [[kobak-2024-delving]] and [[yakura-2024-empirical]].

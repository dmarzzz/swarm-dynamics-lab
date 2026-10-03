---
id: kirchenbauer-2023-watermark
type: paper
title: A Watermark for Large Language Models
authors:
- John Kirchenbauer
- Jonas Geiping
- Yuxin Wen
- Jonathan Katz
- Ian Miers
- Tom Goldstein
year: 2023
venue: ICML 2023 (PMLR 202, pages 17061-17084 per Semantic Scholar)
url: https://arxiv.org/abs/2301.10226
doi: null
arxiv: '2301.10226'
cite: Kirchenbauer, J., Geiping, J., Wen, Y., Katz, J., Miers, I., & Goldstein, T. (2023). A Watermark for Large Language Models. In Proceedings of the 40th International Conference on Machine Learning (ICML 2023), PMLR 202, 17061-17084. arXiv:2301.10226.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 1071 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Proposes the green-list watermark: before each token, hash the previous context to pick a random "green" subset of the vocabulary and softly boost those tokens during sampling. A statistical test with interpretable p-values detects the watermark from a short span without model access. Tested on a multi-billion-parameter OPT model with negligible quality impact.

## Contribution

The seminal LLM text watermark that most later schemes and attacks build on.

## Key results

- Shown (abstract): detectable from short spans with negligible quality impact; information-theoretic sensitivity analysis.

## Methods and models

Context-hashed green/red vocabulary split; logit bias; z-test detection. Abstract read only.

## Limitations and open questions

Removable by paraphrase and random-walk attacks ([[zhang-2023-watermarks]]); keys can be stolen ([[jovanovic-2024-watermark]]). Abstract depth.

## Relevance to us

Seminal entry for the watermark branch; robustness follow-up [[kirchenbauer-2023-reliability]]; production scheme [[dathathri-2024-scalable]].

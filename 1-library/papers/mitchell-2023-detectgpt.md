---
id: mitchell-2023-detectgpt
type: paper
title: 'DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature'
authors:
- Eric Mitchell
- Yoonho Lee
- Alexander Khazatsky
- Christopher D. Manning
- Chelsea Finn
year: 2023
venue: ICML 2023 (pages 24950-24962 per Semantic Scholar)
url: https://arxiv.org/abs/2301.11305
doi: null
arxiv: '2301.11305'
cite: 'Mitchell, E., Lee, Y., Khazatsky, A., Manning, C. D., & Finn, C. (2023). DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature. In Proceedings of the 40th International Conference on Machine Learning (ICML 2023), 24950-24962. arXiv:2301.11305.'
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 1261 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Observes that text sampled from an LLM tends to sit in negative-curvature regions of that model's log-probability function and uses this as a zero-shot detection criterion, needing only the model's log probabilities and perturbations from a generic model such as T5. Improves fake-news detection for GPT-NeoX-20B from 0.81 AUROC (best zero-shot baseline) to 0.95.

## Contribution

Seminal zero-shot detector; basis for Fast-DetectGPT.

## Key results

- Measured (abstract): AUROC 0.95 vs 0.81 for the strongest zero-shot baseline on GPT-NeoX-20B fake news.

## Methods and models

Probability-curvature test with T5 perturbations. Abstract read only.

## Limitations and open questions

Needs scoring-model access and many perturbations; paraphrasing drops it to 4.6% accuracy at 1% FPR ([[krishna-2023-paraphrasing]]). Abstract depth.

## Relevance to us

Seminal per-item detector; superseded for scale by [[bao-2023-fast]].

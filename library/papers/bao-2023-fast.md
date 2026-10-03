---
id: bao-2023-fast
type: paper
title: 'Fast-DetectGPT: Efficient Zero-Shot Detection of Machine-Generated Text via Conditional Probability Curvature'
authors:
- Guangsheng Bao
- Yanbin Zhao
- Zhiyang Teng
- Linyi Yang
- Yue Zhang
year: 2023
venue: ICLR 2024
url: https://arxiv.org/abs/2310.05130
doi: null
arxiv: '2310.05130'
cite: 'Bao, G., Zhao, Y., Teng, Z., Yang, L., & Zhang, Y. (2023). Fast-DetectGPT: Efficient Zero-Shot Detection of Machine-Generated Text via Conditional Probability Curvature. In International Conference on Learning Representations (ICLR 2024). arXiv:2310.05130.'
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 428 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Fast-DetectGPT replaces DetectGPT's perturbation step with sampling to compute conditional probability curvature, explaining word-choice differences between LLMs and humans in context. It beats DetectGPT by about 75% relative in white-box and black-box settings and runs 340 times faster. Code at github.com/baoguangsheng/fast-detect-gpt.

## Contribution

The fast zero-shot detector that made platform-scale scans affordable.

## Key results

- Measured (abstract): about 75% relative improvement over DetectGPT; 340x speed-up.

## Methods and models

Conditional probability curvature with a sampling proxy model. Abstract read only.

## Limitations and open questions

Same robustness limits as other zero-shot detectors. Abstract depth.

## Relevance to us

Detector behind [[la-cava-2025-machines]] and one of three in [[hao-2025-do]] (4.3% FPR on pre-ChatGPT spam). Builds on [[mitchell-2023-detectgpt]].

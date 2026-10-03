---
id: wang-2026-trace
type: paper
title: 'TRACE-Bot: Detecting Emerging LLM-Driven Social Bots via Implicit Semantic Representations and AIGC-Enhanced Behavioral Patterns'
authors:
- Zhongbo Wang
- Zhiyu Lin
- Zhu Wang
- Haizhou Wang
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2604.02147
doi: null
arxiv: '2604.02147'
cite: 'Wang, Z., Lin, Z., Wang, Z., & Wang, H. (2026). TRACE-Bot: Detecting Emerging LLM-Driven Social Bots via Implicit Semantic Representations and AIGC-Enhanced Behavioral Patterns. arXiv preprint arXiv:2604.02147.'
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

A dual-channel detector for LLM-driven social bots that combines pretrained-language-model representations of profiles and tweets with behavioural activity features augmented by scores from AI-generated-content detectors. On two public LLM-driven bot datasets it reports accuracies of 98.46% and 97.50% and robustness to advanced bot strategies.

## Contribution

Representative of the 2026 crop of detectors aimed specifically at LLM-driven bots, fusing AIGC-detector signals with behaviour.

## Key results

- Accuracy 98.46% and 97.50% on two public LLM-driven bot datasets (abstract).

## Methods and models

Language-model encoder plus multidimensional activity features with AIGC-detector signals; lightweight classifier head. Abstract-level read.

## Limitations and open questions

Near-perfect scores on public LLM-bot datasets probably reflect dataset construction (see [[hays-2023-simplistic]], [[ng-2025-are]]); no in-the-wild validation in the abstract.

## Relevance to us

Typical of current published detectors: strong on synthetic data, untested on live swarms. Benchmarks of this kind include [[qiao-2024-botsim]].

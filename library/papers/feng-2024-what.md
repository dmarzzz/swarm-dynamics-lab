---
id: feng-2024-what
type: paper
title: 'What Does the Bot Say? Opportunities and Risks of Large Language Models in Social Media Bot Detection'
authors:
- Shangbin Feng
- Herun Wan
- Ningnan Wang
- Zhaoxuan Tan
- Minnan Luo
- Yulia Tsvetkov
year: 2024
venue: Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (ACL 2024)
url: https://arxiv.org/abs/2402.00371
doi: null
arxiv: '2402.00371'
cite: 'Feng, S., Wan, H., Wang, N., Tan, Z., Luo, M., & Tsvetkov, Y. (2024). What Does the Bot Say? Opportunities and Risks of Large Language Models in Social Media Bot Detection. In Proceedings of ACL 2024. arXiv:2402.00371.'
topics:
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 69 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Examines both sides of LLMs in social-bot detection. On the defence side, a mixture-of-heterogeneous-experts framework splits user information by modality; instruction tuning on 1,000 annotated examples yields detectors that beat prior state of the art by up to 9.1% on two datasets. On the attack side, LLM-guided manipulation of a bot's text and structured profile features evades existing detectors, reducing their performance by up to 29.6% and harming calibration.

## Contribution

Quantifies the LLM-era bot-detection arms race in both directions on standard benchmarks.

## Key results

- Measured: up to 9.1% improvement over baselines with 1,000 annotated examples.
- Measured: LLM-guided evasion cuts existing detector performance by up to 29.6%.

## Methods and models

Three LLMs, two bot-detection datasets, mixture of experts over text, metadata and graph modalities; LLM-rewritten user information for evasion.

## Limitations and open questions

Abstract only; dataset names not checked.

## Relevance to us

Shows that classifier-based Sybil detection degrades when the Sybils themselves are LLMs that can rewrite their observable features, which pushes Sybil resistance in agent swarms toward costly or attested identity ([[adler-2024-personhood]], [[hu-2025-inter-agent]]) and network-level signals ([[yang-2023-anatomy]]).

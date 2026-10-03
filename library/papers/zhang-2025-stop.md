---
id: zhang-2025-stop
type: paper
title: Stop Overvaluing Multi-Agent Debate -- We Must Rethink Evaluation and Embrace Model Heterogeneity
authors:
- Hangfan Zhang
- Zhiyao Cui
- Jianhao Chen
- Xinrun Wang
- Qiaosheng Zhang
- Zhen Wang
- Dinghao Wu
- Shuyue Hu
year: 2025
venue: arXiv preprint (position paper)
url: https://arxiv.org/abs/2502.08788
doi: null
arxiv: '2502.08788'
cite: Zhang, H., Cui, Z., Chen, J., Wang, X., Zhang, Q., Wang, Z., Wu, D., & Hu, S. (2025). Stop Overvaluing Multi-Agent Debate -- We Must Rethink Evaluation and Embrace Model Heterogeneity. arXiv preprint arXiv:2502.08788.
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 0 (OpenAlex, 2026-10-03); 44 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

A position paper backed by a systematic evaluation of 5 representative multi-agent debate (MAD) methods on 9 benchmarks with 4 foundation models. MAD often fails to beat simple single-agent baselines such as chain-of-thought and self-consistency, even while using considerably more inference compute. Introducing model heterogeneity (debaters from different model families) consistently improves MAD frameworks, which the authors call a "universal antidote". They argue the field should rethink evaluation (benchmark coverage, baselines, consistent setups) and adopt heterogeneity as a core design principle.

## Contribution

A negative/critical benchmark result for the most popular LLM collective mechanism; consistent with diversity-based explanations in [[yang-2026-understanding]] and [[bertalanic-2026-ringelmann]].

## Key results

- Measured: MAD frequently below CoT/self-consistency at higher compute (5 methods x 9 benchmarks x 4 models).
- Measured: heterogeneous debaters improve MAD consistently.

## Methods and models

Re-implementation and evaluation of five MAD methods under common settings. Specific numbers not checked.

## Limitations and open questions

Abstract-level read; compute matching details unknown.

## Relevance to us

Supports designing heterogeneous rather than homogeneous LLM swarms. Related: [[tran-2026-single]], [[fortuna-2026-multi-agent]].

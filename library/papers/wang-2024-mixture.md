---
id: wang-2024-mixture
type: paper
title: Mixture-of-Agents Enhances Large Language Model Capabilities
authors:
- Junlin Wang
- Jue Wang
- Ben Athiwaratkun
- Ce Zhang
- James Zou
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2406.04692
doi: null
arxiv: '2406.04692'
cite: Wang, J., Wang, J., Athiwaratkun, B., Zhang, C., & Zou, J. (2024). Mixture-of-agents enhances large language model capabilities. arXiv preprint arXiv:2406.04692.
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 561 (Semantic Scholar, 2026-10-03; OpenAlex unavailable that day)
code: []
---

## Summary

Mixture-of-Agents (MoA) stacks layers of LLM agents; each agent in a layer receives all outputs of the previous layer as auxiliary context. Using only open-source models, MoA reaches 65.1% on AlpacaEval 2.0 versus 57.5% for GPT-4 Omni, and leads MT-Bench and FLASK at the time.

## Contribution

Showed that layered aggregation over heterogeneous models beats a single frontier model, a strong ensemble baseline for MAS.

## Key results

- AlpacaEval 2.0: 65.1% (open-source MoA) vs 57.5% (GPT-4o). Reported in abstract.

## Methods and models

Layered fully connected feed-forward aggregation; proposer and aggregator roles. Code not opened.

## Limitations and open questions

Cost grows with layers x agents; gains may come from model diversity rather than interaction, consistent with [[yang-2026-understanding]].

## Relevance to us

[[el-2026-physics]] notes that MoA is a special case of their setup (fully connected, all-friendly J, depth T), so MoA is the all-to-all limit of networked opinion dynamics.

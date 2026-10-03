---
id: piao-2025-agentsociety
type: paper
title: 'AgentSociety: Large-Scale Simulation of LLM-Driven Generative Agents Advances Understanding of Human Behaviors and Society'
authors:
- Jinghua Piao
- Yuwei Yan
- Jun Zhang
- Nian Li
- Junbo Yan
- Xiaochong Lan
- Zhihong Lu
- Zhiheng Zheng
- Jing Yi Wang
- Di Zhou
- Chen Gao
- Fengli Xu
- Fang Zhang
- Ke Rong
- Jun Su
- Yong Li
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2502.08691
doi: null
arxiv: '2502.08691'
cite: 'Piao, J., Yan, Y., Zhang, J., Li, N., Yan, J., Lan, X., Lu, Z., Zheng, Z., Wang, J. Y., Zhou, D., et al. (2025). AgentSociety: Large-scale simulation of LLM-driven generative agents advances understanding of human behaviors and society. arXiv preprint arXiv:2502.08691.'
topics:
- llm-agent-swarms
- crowds-and-traffic
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "229 (Semantic Scholar, 2026-10-03); OpenAlex has no matching record for this arXiv DOI"
code: []
---

## Summary

AgentSociety is a large-scale social simulator combining LLM-driven agents, a realistic urban environment (including mobility) and a scalable simulation engine. It simulates over 10,000 agents and about 5 million interactions, and is used as a computational social-science testbed for polarisation, spread of inflammatory messages, universal basic income, hurricane shocks and urban sustainability, with outcomes reported to align with real-world experimental results.

## Contribution

Scale (10^4 agents) and an attempt at validation against empirical social-science findings; from the group behind [[gao-2023-large]].

## Key results

- 10k+ agents, 5 million interactions (abstract).
- Qualitative alignment with real-world results on five social issues (abstract; alignment metrics not read).

## Methods and models

Generative agents with needs, emotions and mobility in a city environment; large-scale simulation engine. Code not checked.

## Limitations and open questions

Validation is case-based; cost and model-specific biases ([[brockers-2025-disentangling]]) may drive outcomes. Abstract-level read.

## Relevance to us

Shows the engineering path to large N; for swarm dynamics the measurable phenomena (polarisation, cascades) overlap with [[el-2026-physics]] and [[yang-2024-oasis]].

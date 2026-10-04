---
id: zhu-2025-multiagentbench
type: paper
title: "MultiAgentBench: Evaluating the Collaboration and Competition of LLM agents"
authors: ["Kunlun Zhu", "Hongyi Du", "Zhaochen Hong", "Xiaocheng Yang", "Shuyi Guo", "Zhe Wang", "Zhenhailong Wang", "Cheng Qian", "Xiangru Tang", "Heng Ji", "Jiaxuan You"]
year: 2025
venue: "ACL 2025 (Main)"
url: https://arxiv.org/abs/2503.01935
doi: null
arxiv: "2503.01935"
cite: "Zhu, K., Du, H., Hong, Z., Yang, X., Guo, S., Wang, Z., Wang, Z., Qian, C., Tang, X., Ji, H., & You, J. (2025). MultiAgentBench: Evaluating the Collaboration and Competition of LLM agents. Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL). arXiv:2503.01935."
topics: [llm-agent-swarms, collective-decision]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "215 (Semantic Scholar, 2026-10-03)"
code: [gh-ulab-uiuc-marble]
---

## Summary

MultiAgentBench evaluates LLM multi-agent systems across interactive collaborative and competitive scenarios with milestone-based KPIs, and compares coordination protocols (star, chain, tree, graph) and strategies such as group discussion and cognitive planning. gpt-4o-mini achieves the highest average task score, graph topology works best in the research scenario, and cognitive planning raises milestone achievement by 3%.

## Contribution

A benchmark that scores collaboration quality, not only final task success, and treats communication topology as an experimental variable.

## Key results

- gpt-4o-mini highest average task score (abstract).
- Graph protocol best among star/chain/tree/graph in the research scenario (abstract).
- Cognitive planning +3% milestone achievement (abstract).

## Methods and models

MARBLE framework; milestone KPIs; topology and strategy ablations. Not read beyond the abstract.

## Limitations and open questions

Small teams; LLM-judged milestones; topology result is scenario-specific.

## Relevance to us

Topology-as-variable is what we would vary in fork-and-merge or swarm-communication experiments. Code: [[gh-ulab-uiuc-marble]].

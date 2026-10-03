---
id: wang-2025-rethinking
type: paper
title: Rethinking Multi-Agent Intelligence Through the Lens of Small-World Networks
authors:
- Boxuan Wang
- Zhuoyun Li
- Xiaowei Huang
- Yi Dong
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2512.18094
doi: null
arxiv: '2512.18094'
cite: Wang, B., Li, Z., Huang, X., & Dong, Y. (2025). Rethinking Multi-Agent Intelligence Through the Lens of Small-World Networks. arXiv preprint arXiv:2512.18094.
topics:
- llm-agent-swarms
- sync-consensus
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 2 (OpenAlex, 2026-10-03); 2 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Treats small-world (SW) connectivity, which balances local clustering with long-range shortcuts, as a design prior for LLM multi-agent systems. Using multi-agent debate as a controlled testbed, SW topologies give nearly the same accuracy and token cost as alternatives while substantially stabilising consensus trajectories. The authors then propose uncertainty-guided rewiring for scaling: long-range shortcuts are added between epistemically divergent agents identified with LLM uncertainty signals such as semantic entropy, yielding controllable SW structures that adapt to task difficulty and agent heterogeneity.

## Contribution

Brings Watts-Strogatz network theory explicitly into LLM-MAS topology design; offers a principled explanation for the observation in [[qian-2025-scaling]] that random topologies outperform regular ones.

## Key results

- Claimed: SW topologies match accuracy and token cost while stabilising consensus trajectories in debate.
- Proposed: uncertainty-guided rewiring that adds shortcuts between divergent agents.

## Methods and models

Multi-agent debate on SW, fully connected and ring graphs; semantic-entropy-guided rewiring. Quantities and models not checked.

## Limitations and open questions

Abstract-level read; "stabilising consensus trajectories" needs an operational definition (variance over rounds?).

## Relevance to us

Directly testable swarm-dynamics question: does rewiring probability p control consensus speed and stability in LLM swarms as it does in Kuramoto oscillators? Related: [[hirota-2026-collective]], [[grotschla-2025-agentsnet]].

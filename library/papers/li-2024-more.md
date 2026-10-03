---
id: li-2024-more
type: paper
title: More Agents Is All You Need
authors:
- Junyou Li
- Qin Zhang
- Yangbin Yu
- Qiang Fu
- Deheng Ye
year: 2024
venue: Transactions on Machine Learning Research (TMLR)
url: https://arxiv.org/abs/2402.05120
doi: null
arxiv: '2402.05120'
cite: Li, J., Zhang, Q., Yu, Y., Fu, Q., & Ye, D. (2024). More agents is all you need. Transactions on Machine Learning Research. arXiv:2402.05120.
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 223 (Semantic Scholar, 2026-10-03; OpenAlex unavailable that day)
code: []
---

## Summary

With a simple sampling-and-voting method ("Agent Forest"), LLM performance increases with the number of instantiated agents; the method is orthogonal to more elaborate prompting or multi-agent methods, and the size of the improvement correlates with task difficulty. Experiments span a wide range of LLM benchmarks.

## Contribution

The headline "agent scaling" claim: pure ensemble size, without interaction, scales accuracy. It is the null model any interacting-swarm claim must beat.

## Key results

- Accuracy rises monotonically with ensemble size on many benchmarks, with larger gains on harder tasks (abstract claim; curves not read).

## Methods and models

Sample N independent answers, majority vote (or similarity-based voting for open-ended outputs). Code: https://github.com/MoreAgentsIsAllYouNeed/AgentForest

## Limitations and open questions

Static, single-shot tasks; [[kim-2025-towards]] shows that on agentic tasks with tools and sequential dependence, adding agents can reduce performance by up to 70%, and [[yang-2026-understanding]] shows homogeneous ensembles saturate because outputs are correlated.

## Relevance to us

Baseline for "is interaction doing anything?" Any swarm-dynamics claim should be compared against independent sampling plus voting, as [[choi-2025-debate]] does for debate.

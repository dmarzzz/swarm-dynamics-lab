---
id: zheng-2026-absorbing
type: paper
title: Absorbing State Phase Transitions in Multi-Agent Search
authors:
- Wenwen Zheng
- Yuzhe Yang
- Helen Qu
- Xin Eric Wang
- Haewon Jeong
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.38327
doi: null
arxiv: '2609.38327'
cite: Zheng, W., Yang, Y., Qu, H., Wang, X. E., & Jeong, H. (2026). Absorbing state phase transitions in multi-agent search. arXiv preprint arXiv:2609.38327.
topics:
- llm-agent-swarms
- criticality-measurement
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 0 (Semantic Scholar, 2026-10-03; OpenAlex unavailable that day)
code: []
---

## Summary

Models LLM multi-agent search with the theory of absorbing-state phase transitions. Search tasks are classified into four types informed by combinatorial-search results, and a critical communication degree d_c is derived: the minimum number of agents each agent talks to above which incorrect hypotheses stop proliferating and the system enters the absorbing "solved" state. Frontier LLM multi-agent systems are evaluated on software-configuration debugging and physical-mechanism discovery; agreement with theory is mixed, partly because LLM agents may not communicate with neighbours and develop individually beneficial strategies that limit collaboration.

## Contribution

Connects communication-topology design to a non-equilibrium phase transition (directed-percolation-like absorbing states), giving a predicted critical degree rather than a learned topology.

## Key results

- Derived critical communication degree d_c for each search-task type (abstract).
- Mixed empirical agreement with theory on two real tasks (abstract).

## Methods and models

Absorbing-state analysis on communication graphs of fixed degree; LLM MAS experiments on two discovery tasks. Code not checked.

## Limitations and open questions

Very recent (forward citation of [[el-2026-physics]]), abstract-level read; the mismatch with theory is itself a finding about LLM agents ignoring neighbours.

## Relevance to us

Offers a concrete, testable control parameter (degree d) for swarm experiments, complementing topology-learning work ([[zhang-2024-g-designer]], [[zhuge-2024-language]]) and the coordination-cost curves of [[kim-2025-towards]].

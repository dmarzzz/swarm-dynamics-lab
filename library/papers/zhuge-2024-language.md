---
id: zhuge-2024-language
type: paper
title: Language Agents as Optimizable Graphs
authors:
- Mingchen Zhuge
- Wenyi Wang
- Louis Kirsch
- Francesco Faccio
- Dmitrii Khizbullin
- Jürgen Schmidhuber
year: 2024
venue: Proceedings of the 41st International Conference on Machine Learning (ICML 2024)
url: https://arxiv.org/abs/2402.16823
doi: null
arxiv: '2402.16823'
cite: Zhuge, M., Wang, W., Kirsch, L., Faccio, F., Khizbullin, D., & Schmidhuber, J. (2024). Language agents as optimizable graphs. In Proceedings of the 41st International Conference on Machine Learning (ICML 2024). arXiv:2402.16823.
topics:
- llm-agent-swarms
- swarm-intelligence
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 75 (Semantic Scholar, 2026-10-03; OpenAlex unavailable that day)
code: []
---

## Summary

GPTSwarm describes LLM agents and their collaborations as computational graphs: nodes are operations (LLM queries, tools), edges are information flow, and graphs compose recursively into multi-agent hierarchies. Two optimisers are proposed: node optimisation refines prompts, and edge optimisation changes connectivity to improve orchestration. The framework unifies many prompting schemes and automatically improves agent systems.

## Contribution

Turned multi-agent communication topology into an optimisable object; precursor to learned-topology methods such as [[zhang-2024-g-designer]]. Despite the "swarm" name, this is graph optimisation rather than decentralised swarm dynamics.

## Key results

- Automatic edge optimisation improves benchmark performance over hand-designed graphs (abstract claim; numbers not read).

## Methods and models

Computational graph abstraction; REINFORCE-style edge optimisation over a probabilistic graph. Code: https://github.com/metauto-ai/gptswarm

## Limitations and open questions

Optimised graphs are task-specific and centrally designed; scale of agent counts is small.

## Relevance to us

Relevant to the topology question (who talks to whom) that controls collective outcomes; compare [[qian-2024-scaling]], [[zheng-2026-absorbing]], [[mehdizadeh-2026-exploring]].

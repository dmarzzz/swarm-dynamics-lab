---
id: yang-2025-agentnet
type: paper
title: 'AgentNet: Decentralized Evolutionary Coordination for LLM-based Multi-Agent Systems'
authors:
- Yingxuan Yang
- Huacan Chai
- Shuai Shao
- Yuanyi Song
- Siyuan Qi
- Renting Rui
- Weinan Zhang
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2504.00587
doi: null
arxiv: '2504.00587'
cite: 'Yang, Y., Chai, H., Shao, S., Song, Y., Qi, S., Rui, R., & Zhang, W. (2025). AgentNet: Decentralized evolutionary coordination for LLM-based multi-agent systems. arXiv preprint arXiv:2504.00587.'
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "1 (OpenAlex W4417228026, arXiv record, 2026-10-03); Semantic Scholar 103 same day"
code: []
---

## Summary

AgentNet is a decentralised, retrieval-augmented framework in which agents specialise, evolve and collaborate in a dynamically restructured directed acyclic graph without a central orchestrator. Agents adjust connectivity and route tasks based on local expertise; a retrieval-based memory supports continual skill refinement. It reports higher task accuracy than single-agent and centralised multi-agent baselines and argues for fault tolerance and privacy.

## Contribution

A fully decentralised, self-organising topology for LLM agents, closer in spirit to swarm self-organisation than orchestrator designs.

## Key results

- Accuracy above single-agent and centralised baselines (abstract).

## Methods and models

Dynamic DAG routing by local expertise; RAG memory. Code not checked.

## Limitations and open questions

No measurements of emergent structure (degree distributions, specialisation indices); abstract-level read.

## Relevance to us

Candidate system for observing emergent division of labour; compare [[li-2025-swarmsys]] and the topology studies [[mehdizadeh-2026-exploring]], [[zheng-2026-absorbing]].

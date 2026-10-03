---
id: li-2025-swarmsys
type: paper
title: 'SwarmSys: Decentralized Swarm-Inspired Agents for Scalable and Adaptive Reasoning'
authors:
- Ruohao Li
- Hongjun Liu
- Leyi Zhao
- Zisu Li
- Jiawei Li
- Jiajun Jiang
- Linning Xu
- Chen Zhao
- Mingming Fan
- Chen Liang
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2510.10047
doi: null
arxiv: '2510.10047'
cite: 'Li, R., Liu, H., Zhao, L., Li, Z., Li, J., Jiang, J., Xu, L., Zhao, C., Fan, M., & Liang, C. (2025). SwarmSys: Decentralized swarm-inspired agents for scalable and adaptive reasoning. arXiv preprint arXiv:2510.10047.'
topics:
- llm-agent-swarms
- swarm-intelligence
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 4 (Semantic Scholar, 2026-10-03; OpenAlex unavailable that day)
code: []
---

## Summary

A closed-loop framework for distributed multi-agent reasoning inspired by swarm intelligence. Coordination emerges from cycling interactions among Explorers, Workers and Validators (exploration, exploitation, validation), with adaptive agent and event profiles, embedding-based probabilistic matching and a pheromone-inspired reinforcement mechanism for dynamic task allocation and self-organising convergence without global supervision. It outperforms baselines on symbolic reasoning, research synthesis and scientific programming.

## Contribution

Imports stigmergy/ant-colony task allocation (pheromone reinforcement) into LLM agent orchestration.

## Key results

- Higher accuracy and reasoning stability than baselines on three task types (abstract).

## Methods and models

Role-cycling agents, embedding matching, pheromone-style reinforcement. Code not checked.

## Limitations and open questions

Engineering framework; no analysis of collective dynamics or scaling in N; abstract-level read.

## Relevance to us

Example of the "swarm-inspired orchestration" design pattern; compare the critique in [[rahman-2025-llm]] and the decentralised alternative [[yang-2025-agentnet]].

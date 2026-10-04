---
id: li-2025-llm
type: paper
title: 'LLM-Flock: Decentralized Multi-Robot Flocking via Large Language Models and Influence-Based Consensus'
authors:
- Peihan Li
- Lifeng Zhou
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2505.06513
doi: null
arxiv: '2505.06513'
cite: 'Li, P., & Zhou, L. (2025). LLM-Flock: Decentralized multi-robot flocking via large language models and influence-based consensus. arXiv preprint arXiv:2505.06513.'
topics:
- llm-agent-swarms
- collective-motion
- swarm-robotics
- sync-consensus
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: "1 (OpenAlex W4417512500, arXiv record, 2026-10-03); Semantic Scholar 6 same day"
code: []
---

## Summary

Each robot independently uses its own LLM to propose a local plan toward the desired formation; robots then iteratively refine plans through a decentralised influence-based consensus protocol that accounts for each robot's influence on its neighbours, driving the team to a coherent, stable flock. Simulations with o3-mini, Claude 3.5, Llama3.1-405b, Qwen-Max and DeepSeek-R1 show better stability, convergence and adaptability than prior LLM-based methods, and the approach is validated on a physical team of Crazyflie drones.

## Contribution

Hybrid of LLM planning and classical consensus control: the consensus layer supplies the stability that naive LLM flocking ([[li-2024-challenges]]) lacks.

## Key results

- Improved stability and convergence over prior LLM flocking (abstract; metrics not read).
- Hardware validation on Crazyflie quadrotors (abstract).

## Methods and models

Local LLM plan generation plus influence-weighted iterative consensus on plans. Code not checked.

## Limitations and open questions

Small teams; latency of LLM calls in the control loop; abstract-level read.

## Relevance to us

Shows the pattern "LLM proposes, consensus dynamics disposes", linking LLM swarms to networked consensus control (topic sync-consensus).

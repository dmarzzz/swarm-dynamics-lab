---
id: mao-2025-agent-kernel
type: paper
title: "Agent-Kernel: A MicroKernel Multi-Agent System Framework for Adaptive Social Simulation Powered by LLMs"
authors: ["Yuren Mao", "Peigen Liu", "Xinjian Wang", "Rui Ding", "Jing Miao", "Hui Zou", "Mingjie Qi", "Wanxiang Luo", "Longbin Lai", "Kai Wang", "et al."]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2512.01610
doi: null
arxiv: '2512.01610'
cite: "Mao, Y., Liu, P., Wang, X., Ding, R., Miao, J., Zou, H., Qi, M., Luo, W., Lai, L., Wang, K., et al. (2025). Agent-Kernel: A microkernel multi-agent system framework for adaptive social simulation powered by LLMs. arXiv:2512.01610."
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "3 (Semantic Scholar, 2026-10-03)"
code: [gh-zju-llms-agent-kernel]
---

## Summary

Framework with a society-centric microkernel architecture that decouples core system functions from simulation logic and separates cognition from the physical environment and action execution, so the agent population and profiles can change at runtime. Demonstrated with a Universe 25 (Mouse Utopia) simulation with births and deaths, and a Zhejiang University campus-life simulation coordinating 10,000 heterogeneous agents.

## Contribution

Runtime-mutable populations (agents added and removed mid-run) as a first-class feature of an LLM social-sim framework.

## Key results

- 10,000 heterogeneous agents in the campus simulation; population birth-death dynamics in Universe 25 (abstract).

## Methods and models

Python microkernel with plugin modules; README advertises dynamic agent addition/removal and 'unlimited scalability'.

## Limitations and open questions

Abstract only. Scalability claims not independently checked.

## Relevance to us

Bootstrap candidate if we need agents to join and leave (Sybil arrivals, churn) during a run. Compare [[gh-agentscope-ai-agentscope]] and [[gh-fudandisc-socioverse]].

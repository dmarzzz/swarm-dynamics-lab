---
id: pan-2024-very
type: paper
title: "Very Large-Scale Multi-Agent Simulation in AgentScope"
authors: ["Xuchen Pan", "Dawei Gao", "Yuexiang Xie", "Yushuo Chen", "Zhewei Wei", "Yaliang Li", "Bolin Ding", "Ji-Rong Wen", "Jingren Zhou"]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2407.17789
doi: null
arxiv: '2407.17789'
cite: "Pan, X., Gao, D., Xie, Y., Chen, Y., Wei, Z., Li, Y., Ding, B., Wen, J.-R., & Zhou, J. (2024). Very large-scale multi-agent simulation in AgentScope. arXiv:2407.17789."
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "23 (Semantic Scholar, 2026-10-03)"
code: [gh-agentscope-ai-agentscope]
---

## Summary

Extends the AgentScope multi-agent platform for very large simulations: an actor-based distributed mechanism for parallel agent execution and automatic workflow conversion to distributed deployment, flexible environment support for agent-agent and agent-environment interaction, a configurable tool plus automatic background generation for diverse detailed agent profiles, and a web interface for monitoring many agents across devices. Demonstrated with a comprehensive large-scale simulation.

## Contribution

Engineering recipe (actors, distribution, profile generation, monitoring) for running very many LLM agents on an existing open framework.

## Key results

- Abstract reports a comprehensive simulation and observations, no headline numbers.

## Methods and models

Actor model over multiple devices; code in AgentScope (modelscope/agentscope at the time).

## Limitations and open questions

Abstract only. Paper predates AgentScope 2.x; APIs may have moved.

## Relevance to us

Bootstrap path: AgentScope is already used by [[gh-apromisedland-trustworthy-agent-simulation]]; this paper documents its scale-out features. Code [[gh-agentscope-ai-agentscope]].

---
id: xie-2024-ai
type: paper
title: "AI Metropolis: Scaling Large Language Model-based Multi-Agent Simulation with Out-of-order Execution"
authors: ["Zhiqiang Xie", "Hao Kang", "Ying Sheng", "Tushar Krishna", "Kayvon Fatahalian", "Christos Kozyrakis"]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2411.03519
doi: null
arxiv: '2411.03519'
cite: "Xie, Z., Kang, H., Sheng, Y., Krishna, T., Fatahalian, K., & Kozyrakis, C. (2024). AI Metropolis: Scaling large language model-based multi-agent simulation with out-of-order execution. arXiv:2411.03519."
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "20 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Simulation engine for LLM-agent worlds that replaces global per-step synchronisation with out-of-order execution: it tracks real dependencies between agents (who can affect whom) and lets independent agents advance without waiting, removing false dependencies and raising parallelism and hardware utilisation.

## Contribution

Applies the CPU out-of-order execution idea to LLM agent simulations, a systems fix for the lockstep bottleneck in Generative-Agents-style sims.

## Key results

- 1.3x to 4.15x speedup over standard parallel simulation with global synchronisation, approaching optimal as agent count grows.

## Methods and models

Dependency tracking between agents (spatial/interaction based) feeding a scheduler that batches LLM calls.

## Limitations and open questions

Abstract only; speedups depend on how sparse agent interactions are.

## Relevance to us

Lesson for bootstrapping: lockstep ticks waste LLM throughput; schedule agents by actual interaction dependencies. Compare scheduling in [[akkil-2026-emergence-platform]] (round-robin, one agent at a time) and [[pan-2024-very]] (actor-based distribution).

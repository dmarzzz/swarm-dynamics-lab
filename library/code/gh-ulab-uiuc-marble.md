---
id: gh-ulab-uiuc-marble
type: code
title: "MARBLE / MultiAgentBench: modular framework and benchmark for LLM multi-agent collaboration and competition with configurable coordination topologies"
repo: ulab-uiuc/MARBLE
url: https://github.com/ulab-uiuc/MARBLE
authors: ["Kunlun Zhu", "Hongyi Du", "Zhaochen Hong", "Xiaocheng Yang", "Shuyi Guo", "Zhe Wang", "Zhenhailong Wang", "Cheng Qian", "Xiangru Tang", "Heng Ji", "Jiaxuan You"]
year: 2024
language: Python
license: "MIT"
stars: 302
last_commit: 2025-10-27
topics: [llm-agent-swarms, collective-decision]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [zhu-2025-multiagentbench]
---

## Summary

Simulation model: task environments (research collaboration, coding, database, Minecraft, Werewolf, bargaining) in which agents coordinate through a chosen protocol (star, chain, tree, graph) with shared memory, and a milestone-based KPI scores both task completion and collaboration quality. Scale: small teams (single digits). LLM-native: yes, OpenAI and Together backends. Adversarial hooks: competitive scenarios (Werewolf, bargaining) only; no identity layer. Weight: poetry install, Docker optional, API keys. A second copy lives at MultiagentBench/MARBLE (58 stars, older).

## What it can do for us

Useful for its explicit coordination-topology switch (star vs. graph), which is the variable we would vary in a fork-and-merge or communication-topology study, and for milestone KPIs as a template for scoring partial collaboration.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API. I did not read the source code. Example from README: `poetry install; cd scripts/werewolf; bash run_simulation.sh`.

## Limitations

Benchmark tasks are heterogeneous and judged partly by LLMs; team sizes are small; last push October 2025.

---
id: gh-alem-world-alem-env
type: code
title: "alem: JAX benchmark for open-ended multi-agent coordination (Craftax-Coop based) with RL and text/LLM interfaces"
repo: alem-world/alem-env
url: https://github.com/alem-world/alem-env
authors: ["Kale-ab Abebe Tessera", "et al."]
year: 2026
language: Python
license: "MIT"
stars: 51
last_commit: 2026-09-10
topics: [llm-agent-swarms, marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 4
papers: [tessera-2026-benchmarking]
---

## Summary

Simulation model: cooperative survival-crafting world with 93 achievements, 27 coordination goals (sync actions, handovers, construction), soft roles, 9 dungeon levels and episodes up to 10,000 steps; procedural coordination tasks; per-step broadcast messages and scratchpad for LLM agents. Scale: 1-8 agents per team, thousands of parallel envs in JAX. LLM-native: yes (text interface, leaderboard, evaluation script) and RL-native (symbolic obs, IPPO baselines). Adversarial hooks: none (shared reward). Weight: pure JAX; Docker image provided.

## What it can do for us

Ready-made testbed where LLM teams and MARL teams face identical coordination tasks; the text-observation template in the README is a reusable pattern for exposing a grid world to LLMs.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API; source code not read.

## Limitations

Cooperative only; small teams; LLM evaluation is API-cost bound (10-20 seeds per model in the paper).

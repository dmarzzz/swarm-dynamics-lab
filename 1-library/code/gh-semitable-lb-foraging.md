---
id: gh-semitable-lb-foraging
type: code
title: "Level-Based Foraging (LBF): gridworld where agents with levels must jointly load food; mixed cooperative-competitive MARL benchmark"
repo: semitable/lb-foraging
url: https://github.com/semitable/lb-foraging
authors: ["Filippos Christianos", "Georgios Papoudakis", "Lukas Schäfer", "Stefano V. Albrecht"]
year: 2020
language: Python
license: "MIT"
stars: 215
last_commit: 2024-09-15
topics: [marl-emergence, collective-decision]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: ran
relevance: 3
papers: [papoudakis-2021-benchmarking]
---

## Summary

Simulates a grid where each agent and each food item has a level; food is collected only if the summed levels of adjacent agents attempting to load it reach the food's level, and reward is split in proportion to contributing agents' levels; interaction is simultaneous, mixed cooperative-competitive, with partial observability options and "cooperative" and shared-reward variants. Grid size, agent count and food count are in the registered env name (e.g. `Foraging-8x8-2p-1f-v3`). Measured here at about 14,600 env-steps/s (29,200 agent-steps/s) for 2 agents on one CPU thread. RL-only by design but the state is tiny and fully symbolic, so LLM agents are trivially pluggable. N is a parameter; no mid-episode join/leave. Very light (`pip install lbforaging`, gymnasium).

## What it can do for us

The smallest environment where "whom do I cooperate with" is a real decision, since agents must pick partners whose levels add up. Good for a toy Sybil experiment: one controller running k low-level agents can pool levels to grab high food, which is the Sybil advantage in miniature. Introduced with EPyMARL in [[papoudakis-2021-benchmarking]].

## Run notes

Ran 2026-10-03 in the same venv as [[gh-cognitive-ai-systems-pogema]] (`lbforaging` 2.0.0). `gym.make("Foraging-8x8-2p-1f-v3")`, random actions for 5 s with resets: 14,586 env-steps/s, 29,172 agent-steps/s on M1 Max.

## Limitations

Small grids and few agents in standard tasks; sparse reward. Maintenance mostly finished (last push September 2024).

---
id: gh-semitable-robotic-warehouse
type: code
title: "RWARE: multi-robot warehouse gridworld where robots fetch and return requested shelves (sparse-reward MARL benchmark)"
repo: semitable/robotic-warehouse
url: https://github.com/semitable/robotic-warehouse
authors: ["Filippos Christianos", "Lukas Schäfer", "Stefano V. Albrecht"]
year: 2020
language: Python
license: "MIT"
stars: 439
last_commit: 2024-09-15
topics: [marl-emergence, swarm-robotics]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: [papoudakis-2021-benchmarking]
---

## Summary

Simulates a warehouse grid where robots move, rotate, pick up requested shelves, deliver them to goal stations and must return them to free locations; interaction is simultaneous with a collision-resolution rule that prioritises moves that unblock others, partial observability, and cooperative or individual reward settings. Map size, number of robots, communication and difficulty are configured through env names such as `rware-tiny-2ag-v1`. Standard tasks use 2-4 agents per [[hu-2025-toward]]; throughput not measured here. RL-only by design; state is symbolic so LLM control is possible. N is a parameter, no open population. Light (pip, gymnasium; updated to the Gymnasium API). A C port exists in [[gh-pufferai-pufferlib]]'s Ocean suite.

## What it can do for us

Congestion and deadlock in a shared physical space with very sparse rewards; a small cousin of [[gh-cognitive-ai-systems-pogema]] with a task layer. Low priority for us.

## Run notes

Not run. README read via GitHub API on 2026-10-03.

## Limitations

Few agents in standard tasks; very sparse reward makes learning slow.

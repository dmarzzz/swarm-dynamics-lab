---
id: gh-openbmb-agentverse
type: code
title: "AgentVerse: OpenBMB framework for multi-LLM task-solving teams and custom simulation environments (classroom, Prisoner's Dilemma, Pokemon)"
repo: OpenBMB/AgentVerse
url: https://github.com/OpenBMB/AgentVerse
authors: ["OpenBMB"]
year: 2023
language: JavaScript
license: "Apache-2.0"
stars: 5153
last_commit: 2024-09-09
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: [chen-2023-agentverse]
---

## Summary

Simulation model: two frameworks; task-solving assembles expert agents with recruitment, decision and evaluation stages; simulation provides configurable environments with rule-based turn order and visibility (NLP classroom with 9 players, Prisoner's Dilemma, Pokemon game, Minecraft on a branch). Scale: up to about 10 agents in the shipped demos. LLM-native: yes, OpenAI and local LLaMA/Vicuna. Adversarial hooks: none specific. Weight: Python plus a JavaScript GUI. The README warns the simulation code is being refactored and points to an older stable version.

## What it can do for us

Mainly of historical interest: its environment/rule abstraction (order, visibility, selector, updater) is a reasonable template for a hand-built sim, but nothing here beats newer frameworks.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API. I did not read the source code.

## Limitations

No push since September 2024; simulation half mid-refactor; small agent counts.

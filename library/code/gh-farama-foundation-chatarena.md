---
id: gh-farama-foundation-chatarena
type: code
title: "ChatArena: Farama multi-agent language-game environments for LLMs (deprecated August 2025)"
repo: Farama-Foundation/ChatArena
url: https://github.com/Farama-Foundation/ChatArena
authors: ["Yuxiang Wu", "Farama Foundation"]
year: 2023
language: Python
license: "Apache-2.0"
stars: 1563
last_commit: 2025-08-11
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Simulation model: MDP-style environments where players take turns producing text and a moderator or environment updates shared state (Chameleon, Prisoner's Dilemma, debate, PettingZoo wrappers); interaction through a shared message pool with visibility controls. Scale: a handful of players. LLM-native: yes, OpenAI, Anthropic, Cohere and HF backends. Adversarial hooks: message visibility lets you model private channels; no identity layer. Weight: `pip install chatarena`, Gradio UI optional. The README states the project was deprecated on 2025-08-11 for lack of community use.

## What it can do for us

Historical reference for the message-pool-with-visibility abstraction; for new work [[gh-textarena-textarena]] covers the same ground and is maintained.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API. I did not read the source code.

## Limitations

Deprecated, no further updates. Prompts and backends date from 2023.

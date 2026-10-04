---
id: gh-aiscientists-dev-worldseed
type: code
title: "WorldSeed: YAML-declared world engine where LLM agents act on filtered views each tick and an AI referee resolves uncertain outcomes"
repo: AIScientists-Dev/WorldSeed
url: https://github.com/AIScientists-Dev/WorldSeed
authors: ["AIScientists-Dev / MorphMind"]
year: 2026
language: Python
license: "MIT"
stars: 822
last_commit: 2026-05-08
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 4
papers: []
---

## Summary

Simulation model: declare roles, rules, private information, actions and consequences in YAML; each tick every agent perceives its own filtered slice of state and proposes an action; deterministic outcomes are resolved by a DSL rules engine, uncertain ones by an LLM 'Dungeon Master'; effects apply and the world advances. Human can watch, intervene or play a character. Demos: an 'autoresearch' community (README reports 100 hypotheses, 86 experiments, 72 peer-reviewed papers and val_loss down 24.7% on a 5M TinyStories GPT in 11 hours), product rooms, an espionage drama. LLM-native: yes via LiteLLM (OpenAI, Anthropic, Ollama); OpenClaw and Codex-subagent adapters. Weight: light Python.

## What it can do for us

The rules-engine-plus-AI-referee split is a clean pattern for keeping LLM agents inside hard constraints; YAML worlds make scenario variation cheap.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API; source code not read.

## Limitations

Young (created 2026-04), last push 2026-05; README results are self-reported demos.

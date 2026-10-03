---
id: gh-matraix-ai-matraix-persona-8b
type: code
title: "MatrAIx: persona-agent Playground (Survey/Chatbot/Web/App), 1,010 tasks and 1M-persona release for simulated-user evaluation"
repo: MatrAIx-ai/MatrAIx-Persona-8B
url: https://github.com/MatrAIx-ai/MatrAIx-Persona-8B
authors: ["Xiaomin Li", "Yuexing Hao", "et al."]
year: 2026
language: Python
license: "MIT"
stars: 2005
last_commit: 2026-09-18
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: [li-2026-matraix]
---

## Summary

Simulation model: persona-conditioned LLM users act one at a time in four environments (Survey, AI Chatbot, Web, native App) on a task library with task-owned verifiers; personas come from a 1,290-dimension schema, with a 1M-persona coreset on Hugging Face (MatrAIx2026/MatrAIx_Persona_1M_Public_Release). Scale: population-level by sampling, not by concurrent interaction. LLM-native: yes. Adversarial hooks: none. Weight: Docker for Web/App tasks, Python 3.12 with uv, Node 20 for viewers, API keys for real runs.

## What it can do for us

Persona supply for seeding a heterogeneous agent population; the persona schema and dependency-graph sampler are reusable even without the Playground.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API; source code not read.

## Limitations

No agent-agent interaction. Heavy Docker images for Web/App environments (watch disk). Personas are simulated users, explicitly 'not a replacement for evidence from real people' (README).

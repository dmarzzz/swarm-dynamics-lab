---
id: gh-emergenceai-emergence-world
type: code
title: "Emergence World: open data, agent profiles, tool catalogue, constitution and architecture docs for a persistent 10-agent LLM society (engine not released)"
repo: EmergenceAI/Emergence-World
url: https://github.com/EmergenceAI/Emergence-World
authors: ["Emergence AI"]
year: 2026
language: none (docs and data)
license: "CC BY-NC 4.0 (custom LICENSE; GitHub reports NOASSERTION)"
stars: 631
last_commit: 2026-10-02
topics: [llm-agent-swarms, sybil-resistance]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 4
papers: [akkil-2026-emergence-platform, akkil-2026-emergence]
---

## Summary

Simulation model: persistent real-time 3D town where ten LLM agents with personas, memory and 120+ tools govern themselves via a constitution and a ComputeCredits economy for 15-16 days; worlds differ only in backbone model. Scale: 10 agents per world, 5 (season 1) and 8 (season 2) worlds. LLM-native: yes. Adversarial hooks: season 2 injects prompt injection, misinformation and memory exposure. Weight: the repo has no source files (0 .py/.ts/.js files in the tree); it holds agent profiles, 38+ landmark files, the tool catalogue, constitution, architecture/orchestration/memory/economy/governance docs, metric definitions, and per-world tool-call datasets, blogs and prompt catalogues for seasons 1 and 2. Live replays at <world>.emergence.ai.

## What it can do for us

Design reference (tool catalogue, governance, economy, turn scheduling) and a dataset of long-horizon multi-agent tool calls to mine for failure modes; we would have to rebuild the engine.

## Run notes

Not run. Repo tree and docs/ARCHITECTURE.md read via the GitHub API on 2026-10-03. Architecture per docs: Python 3.11 FastAPI turn manager (round-robin, paid boost turns), PostgreSQL 60+ tables, React Three Fiber frontend, LLM routing to Vertex/Anthropic/OpenAI/xAI.

## Limitations

Non-commercial research licence; no engine code; real-time 1:1 clock makes reruns slow and costly.

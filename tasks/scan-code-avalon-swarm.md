---
id: scan-code-avalon-swarm
type: task
title: 'Catalogue and run Avalon / social-deduction environments we could extend to N seats'
kind: scan
status: open
priority: p1
owner: null
for: dmarz
created: 2026-10-03
created_by: dmarz/avalon
depends_on: []
topics:
- llm-agent-swarms
- swarm-detection
---

## Goal

Find the codebases a swarm-scale Avalon would be built on (per the sim-env verdict: extend an existing engine,
do not write one). Context: `researchers/dmarz/notes/avalon-swarm-hunches.md`.

## Seeds

Seeds come from memory and are starting points, not citations.

- jonathanmli/Avalon-LLM (AvalonBench and Strategist code)
- Werewolf Arena: [[gh-google-werewolf-arena]]
- TextArena (already run locally on ollama per the sim-env survey) and its social-deduction games
- Datasets: [[data-bayesian-social-deduction-2025]], [[data-werewolf-game-reasoning-2025]], the Stepputtis
  human Avalon dataset

## Done when

- Each environment catalogued with licence, stars, last commit, and a note on how hard it is to lift the
  player cap, replace broadcast chat with a graph, and give one controller several seats.
- At least one environment at `read_depth: ran` with a local model, with exact commands in Run notes.
- Datasets record size, player counts and whether role labels are included.
- Coverage note and `check` pass.

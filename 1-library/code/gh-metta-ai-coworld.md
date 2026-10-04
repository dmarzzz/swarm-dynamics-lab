---
id: gh-metta-ai-coworld
type: code
title: "Coworld: Softmax/Metta packaging and league platform for programmable multi-agent game arenas (successor to CoGames)"
repo: Metta-AI/coworld
url: https://github.com/Metta-AI/coworld
authors: ["Metta AI / Softmax"]
year: 2026
language: Python
license: "none found (no LICENSE file; GitHub reports none)"
stars: 17
last_commit: 2026-10-01
topics: [marl-emergence, llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: []
---

## Summary

Platform: a Coworld packages a game, its players and episode evidence (logs, replays, reporters) behind a manifest schema and CLI; players run as hosted containers or file players and can call hosted LLMs; worlds can be run locally, played in the browser, or entered into hosted leagues with mixed human/agent lobbies. Includes the Paint Arena reference world. Game engine side lives in [[gh-metta-ai-mettagrid]] (cogame modules migrated there from CoGames).

## What it can do for us

League-style evaluation loop (submit player, run episodes against hosted opponents, inspect replays) that we could reuse instead of building tournament infrastructure.

## Run notes

Not run. README and repo tree read via the GitHub API on 2026-10-03. Repo includes AGENTS.md and CLAUDE.md for coding agents.

## Limitations

No licence file found, so reuse rights are unclear; tied to Softmax's hosted platform for leagues.

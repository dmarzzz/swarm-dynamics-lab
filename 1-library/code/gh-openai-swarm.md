---
id: gh-openai-swarm
type: code
title: "OpenAI Swarm: educational multi-agent orchestration via Agents and handoffs (superseded by the Agents SDK)"
repo: openai/swarm
url: https://github.com/openai/swarm
authors: ["OpenAI Solutions team"]
year: 2024
language: Python
license: "MIT"
stars: 22035
last_commit: 2026-04-15
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Coordination model: handoffs. Two primitives, an Agent (instructions plus tools) and a handoff, where any agent's function can return another Agent to transfer the conversation. Stateless between calls, runs on the Chat Completions API, no built-in memory or parallelism. README marks it experimental and educational and points users to openai-agents-python as the production evolution. Despite the name it has nothing to do with swarm dynamics: it is a sequential routing pattern among a handful of agents.

## What it can do for us

Only as a minimal reference for the handoff pattern. Not a candidate for running populations.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Superseded; last commit 2026-04-15; no concurrency, no shared state, no observability. 22k stars reflect the name and the brand more than use.

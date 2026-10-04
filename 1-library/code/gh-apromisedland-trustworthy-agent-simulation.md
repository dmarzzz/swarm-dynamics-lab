---
id: gh-apromisedland-trustworthy-agent-simulation
type: code
title: "Trustworthy Agent Simulation (tass): auditable LLM town society on AgentScope + Mesa with replay, resume, policy batches and Streamlit dashboard"
repo: apromisedland/trustworthy-agent-simulation
url: https://github.com/apromisedland/trustworthy-agent-simulation
authors: ["apromisedland"]
year: 2026
language: Python
license: "Apache-2.0"
stars: 44
last_commit: 2026-09-29
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 4
papers: []
---

## Summary

Simulation model: town economy with 18 residents, 4 shops and 2 producers over 7 days x 4 decision periods; agents message, remember, seek jobs, produce, negotiate offers, execute escrow contracts and consume, with explicit resource accounting; policies and production shocks are treatments; a public-goods plugin shows scenario extension. Scale: tens of agents. LLM-native: yes via AgentScope 2.0.9 tool calling against any Chat Completions endpoint, with an offline 'baseline' mode. Adversarial hooks: none built in. Weight: light (Python 3.12/3.13, uv lockfile, Mesa 3.5.1). Engineering features: run directories cannot be overwritten, resume restores config, RNG states and completed decisions, replay reads committed snapshots without calling a model, batch suites over seeds for policy and ablation runs.

## What it can do for us

Closest thing to a small, reproducible LLM-society harness we could fork: seeded batches, deterministic replay without model calls, and a dashboard; good skeleton to add Sybil agents to.

## Run notes

Not run. README read via the GitHub API on 2026-10-03; repo created 2026-09-29 (days old). README states no paid provider calls were performed for the release and baseline output is not evidence of LLM behaviour.

## Limitations

Brand new, single author, no published validation; small fixed town.

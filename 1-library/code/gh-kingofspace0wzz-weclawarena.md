---
id: gh-kingofspace0wzz-weclawarena
type: code
title: "WeClawArena: sandbox and benchmark for cross-owner personal-agent collaboration with attack variants (OpenClaw gateway)"
repo: kingofspace0wzz/WeClawArena
url: https://github.com/kingofspace0wzz/WeClawArena
authors: ["Prince Zizhuang Wang", "et al."]
year: 2026
language: Python
license: "Apache-2.0"
stars: 1
last_commit: 2026-08-11
topics: [llm-agent-swarms, sybil-resistance]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: [wang-2026-weclawarena]
---

## Summary

Simulation model: each human owner has an agent with a private workspace, tools and policies; agents message across owners to complete 124 base tasks in six domains, each in five conditions (benign, collaboration, security, privacy, governance attacks), 620 variants. Scale: a handful of owners per task. LLM-native: yes. Adversarial hooks: built in (poisoned handoffs, goal hijack, forbidden mutation, invalid identity/consent/mandate paths). Weight: Python 3.11, Docker for container-backed sims, pnpm for the OpenClaw TypeScript bridge; dataset on HF.

## What it can do for us

Attack taxonomy and audit logging for owned-agent networks; the governance/identity attack class maps onto our Sybil and delegation questions.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API; source code not read.

## Limitations

1 star, single team; small populations; depends on OpenClaw plugin stack.

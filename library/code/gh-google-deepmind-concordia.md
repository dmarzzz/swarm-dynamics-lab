---
id: gh-google-deepmind-concordia
type: code
title: "Concordia: generative agent-based modelling with a Game Master that adjudicates natural-language actions"
repo: google-deepmind/concordia
url: https://github.com/google-deepmind/concordia
authors: ["Google DeepMind"]
year: 2023
language: Python
license: "Apache-2.0"
stars: 1756
last_commit: 2026-10-01
topics: [llm-agent-swarms, collective-decision]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Coordination model: tabletop-RPG. Player entities state intended actions in natural language and a Game Master entity simulates the environment, checks plausibility and produces outcomes; supports grounded physical, social or digital settings and third-party service integration. Tech report arXiv 2312.03664 and design-pattern paper arXiv 2507.08892. Apache-2.0, 1.8k stars, active (2026-10-01).

## What it can do for us

Clean way to run small societies (tens of agents) with an explicit, logged world model and controllable information flow; good for 'who learned what from whom' experiments.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

GM is an LLM bottleneck, so scale is limited; not for hundreds of agents.

## Notes from dmarz/sim-envs

[[zhou-2024-is]] shows that simulations where one LLM sees every participant's private goals (their 'Script' mode) leak that information into outcomes and overstate social competence (94% vs. 30% deal rate in bargaining). A Game Master that sees all agents' state is a leakage risk to control for in deception or sybil experiments built on Concordia.

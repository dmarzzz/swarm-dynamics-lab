---
id: gh-farama-foundation-magent2
type: code
title: "MAgent2: large-population gridworld MARL environments (hundreds of pixel agents in battle and gathering scenarios) on the PettingZoo API"
repo: Farama-Foundation/MAgent2
url: https://github.com/Farama-Foundation/MAgent2
authors: ["Farama Foundation (fork of geek-ai/MAgent)"]
year: 2022
language: Python
license: "MIT"
stars: 967
last_commit: 2026-09-13
topics: [marl-emergence]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Maintained fork of MAgent providing gridworld environments where large numbers of agents (hundreds to thousands) interact in battle, tiger-deer, gather and adversarial-pursuit scenarios, implemented in C++ with PettingZoo wrappers. Formerly inside PettingZoo, split out in 2022. MIT, 967 stars, last commit 2026-09-13.

## What it can do for us

The cheapest way to get a genuinely large learned population (hundreds of agents) on one machine; the original MAgent paper is the usual citation for emergent formations in many-agent RL.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Gridworld pixels, competitive scenarios; learning at scale still needs a GPU for the policy. Not run.

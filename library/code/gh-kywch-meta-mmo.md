---
id: gh-kywch-meta-mmo
type: code
title: "Meta MMO: many-agent minigames on Neural MMO 2 with generalist training and Elo evaluation"
repo: kywch/meta-mmo
url: https://github.com/kywch/meta-mmo
authors: ["Kyoung Whan Choe", "Ryan Sullivan", "Joseph Suárez"]
year: 2024
language: Python
license: "MIT"
stars: 7
last_commit: 2024-08-30
topics: [marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 2
papers: [choe-2024-massively]
---

## Summary

Simulation model: five minigames (team battle, protect the king, race to the center, king of the hill, sandwich) on Neural MMO 2; train specialists or one generalist (400M timesteps example), evaluate with Elo. Scale: Neural MMO populations (128+ agents per world per [[gh-neuralmmo-environment]]). LLM-native: no. Weight: pip install -e .[dev]; RL training needs a GPU for practical speed.

## What it can do for us

Ready configs for short many-agent competitive games if we want RL baselines in a Neural MMO world.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API; source code not read.

## Limitations

Unmaintained since 2024-08; pinned to Neural MMO 2.x.

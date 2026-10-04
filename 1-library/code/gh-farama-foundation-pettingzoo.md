---
id: gh-farama-foundation-pettingzoo
type: code
title: "PettingZoo: multi-agent Gymnasium-style API and environment families (Atari, Butterfly, Classic, MPE, SISL)"
repo: Farama-Foundation/PettingZoo
url: https://github.com/Farama-Foundation/PettingZoo
authors: ["Farama Foundation"]
year: 2020
language: Python
license: "MIT"
stars: 3524
last_commit: 2026-10-03
topics: [marl-emergence]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

The standard multi-agent RL API (AEC and parallel) with bundled environment families: multi-player Atari, the cooperative Butterfly games (Pistonball, Knights Archers Zombies, Cooperative Pong), classic board and card games, SISL (Pursuit, Waterworld, Multiwalker) and the MPE particle environments. MIT, 3.5k stars, active (2026-10-03).

## What it can do for us

Baseline MARL environments and the API that most libraries (BenchMARL, JaxMARL wrappers, MAgent2) speak; Pursuit and Waterworld are small swarm-like cooperative tasks.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Mostly CPU, small agent counts (under 10 for most envs except MAgent2).

---
id: gh-xuehaipan-mate
type: code
title: "MATE: Multi-Agent Tracking Environment, asymmetric two-team camera-vs-target game with intra-team communication"
repo: XuehaiPan/mate
url: https://github.com/XuehaiPan/mate
authors: ["Xuehai Pan", "Peking University PKU-Alignment / PKU-MARL contributors"]
year: 2022
language: Python
license: "MIT"
stars: 48
last_commit: 2023-03-31
topics: [marl-emergence, swarm-robotics]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Simulates a 2D continuous arena where a team of cameras tries to keep moving targets in view while targets try to evade and reach goals; it is an asymmetric two-team zero-sum stochastic game, cooperative within teams, with intra-team communication allowed and inter-team communication prohibited. Population is 2-16 agents with communication and partial observability per [[hu-2025-toward]]; throughput not measured. RL-only (numpy vectors). Team sizes are configurable, and built-in wrappers turn it into a single-team environment against scripted opponents, which makes swapping in a deviant teammate simple. Light pip install from GitHub.

## What it can do for us

A compact example of an environment where one team's communication channel is explicit and separable, the right shape for testing a compromised or lying teammate on the channel.

## Run notes

Not run. README read via GitHub API on 2026-10-03.

## Limitations

Unmaintained since March 2023, 48 stars. Small teams.

---
id: gh-mlech26l-gigastep
type: code
title: "Gigastep: JAX-vectorised two-team 3D aerial combat MARL environment, 288 scenarios, >1000 agents"
repo: mlech26l/gigastep
url: https://github.com/mlech26l/gigastep
authors: ["Mathias Lechner", "Lianhao Yin", "Tim Seyde", "Tsun-Hsuan Wang", "Wei Xiao", "Ramin Hasani", "Joshua Rountree", "Daniela Rus"]
year: 2023
language: Python (JAX)
license: "MIT"
stars: 76
last_commit: 2023-12-19
topics: [marl-emergence, swarm-robotics]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [lechner-2023-gigastep]
---

## Summary

Simulates two teams of aircraft-like agents with 3D dynamics that chase, tag or avoid each other under partial observability with stochastic observation and stochastic intra-team communication; interaction is simultaneous, mixed cooperative-competitive, continuous or discrete actions, RGB (84x84) or feature-vector observations. The README lists 288 built-in scenarios (team sizes such as 5, 10, 20, identical or heterogeneous agent types) and claims scalability to more than 1000 agents; the paper headline is up to one billion environment steps per second on consumer hardware, while its own throughput figure shows on the order of 1 million steps per second per GPU across RTX 2080Ti to A100 [[lechner-2023-gigastep]] (the two numbers are not reconciled in what I read). RL-only (JAX arrays, no text path). Team sizes and heterogeneous types are scenario parameters; agents have per-agent `dones`, so dead agents leave but none join. Light install (`pip install gigastep`, JAX), GPU optional.

## What it can do for us

A ready JAX template for adversarial team swarms with stochastic, lossy communication, which is the right setting for "one team contains infiltrators" experiments. Small, readable codebase to fork if we want a pure-JAX swarm combat sim.

## Run notes

Not run. README read via GitHub API on 2026-10-03.

## Limitations

The README still says "Updates coming soon - Oct 2023" and warns the interface may change; last push December 2023, 76 stars. Effectively unmaintained.

---
id: gh-shacklettbp-madrona
type: code
title: "Madrona: GPU batch-simulation game engine (ECS) for building thousands-of-worlds RL simulators"
repo: shacklettbp/madrona
url: https://github.com/shacklettbp/madrona
authors: ["Brennan Shacklett", "Luc Guy Rosenzweig", "Stanford graphics group"]
year: 2023
language: C++ / CUDA
license: "MIT"
stars: 523
last_commit: 2025-11-03
topics: [marl-emergence, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [shacklett-2023-extensible]
---

## Summary

Not an environment but an engine: an entity-component-system (ECS) game engine that runs thousands of independent world instances in one GPU process, with XPBD rigid-body physics, a batch renderer for per-agent images, a CPU backend for debugging, and state exported as PyTorch tensors. World logic is written in C++ and lowered to CUDA. Demonstrated simulators built on it include an escape room, an Overcooked rewrite, a Hanabi port, a Hide-and-Seek reimplementation of [[gh-openai-multi-agent-emergence-environments]], and [[gh-emerge-lab-gpudrive]]; the paper reports over 1.9 million environment steps per second for the hide-and-seek port on one GPU and 5-33x speedups over strong 32-thread CPU baselines [[shacklett-2023-extensible]]. RL-only (tensors in, tensors out). Agent count per world is whatever the author's ECS code spawns; the ECS model makes adding or deleting agent entities natural, so open populations are possible but must be written by us. Heavy: C++/CUDA build, full Xcode on macOS, research-grade with breaking API changes per the README disclaimer.

## What it can do for us

The route if we ever need millions of agent-steps per second for an embodied swarm with physics or rendering. Too heavy for a hackathon start; worth knowing as the ceiling.

## Run notes

Not run. README read via GitHub API on 2026-10-03. Supports Linux, macOS 13+ (full Xcode 14 install) and Windows 11 per README.

## Limitations

Research code base with missing features and documentation (README disclaimer). Writing an environment means writing C++ ECS systems. GPU needed for the speed claims.

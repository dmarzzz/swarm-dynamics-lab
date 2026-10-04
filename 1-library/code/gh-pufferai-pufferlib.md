---
id: gh-pufferai-pufferlib
type: code
title: "PufferLib: fast RL training library plus 'Ocean' suite of C/CUDA environments, many multi-agent (nmmo3, boids, battle, moba, rware, overcooked, drive)"
repo: PufferAI/PufferLib
url: https://github.com/PufferAI/PufferLib
authors: ["Joseph Suarez", "PufferAI contributors"]
year: 2023
language: C / CUDA / Python
license: "MIT"
stars: 6493
last_commit: 2026-09-13
topics: [marl-emergence, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

A reinforcement learning library whose main asset for us is "Ocean", a collection of environments written as single C headers (with CUDA ports for some) that run at very high single-machine throughput, including multi-agent ones: nmmo3 (the C successor of Neural MMO), boids, battle, moba, rware, overcooked, drive (GPUDrive-style driving), tactical, tron, snake and others. Interaction model is batched synchronous stepping of many agents through a vectorised native API; agent scale ranges from 2 to thousands per env depending on the game. Throughput claims are in the documentation, not checked here. RL-only in practice (fixed numeric observation buffers), no text observation path. Agent counts are compile/config parameters of each C env, so variable N is possible by editing the env, but there is no generic open-population or adversarial-injection API. Heavyweight to build: the 5.0 default branch is CUDA-centric, and `pip install pufferlib` failed on a Mac here. Maintained by Joseph Suarez (PufferAI), also the author of Neural MMO.

## What it can do for us

A source of small, readable C multi-agent environments (boids in one header, battle, moba, nmmo3) that we could copy as a fast core for our own sim, and a model for how to make a many-agent env fast: flat arrays, C step function, Python only at the edge. Neural MMO 2.0 itself uses PufferLib for multi-agent vectorisation [[suarez-2023-neural]].

## Run notes

Attempted 2026-10-03 on M1 Max, Python 3.11 via uv: `uv pip install pufferlib` builds every Ocean extension from source and failed after about 60 s in `pufferlib/ocean/impulse_wars/game.h` with "too few arguments" and "no member named" errors (a vendored physics library version mismatch). Not run. The default branch (5.0) lists 70+ env configs under `config/` and `.cu` files for several envs, which suggests Linux plus NVIDIA is the supported path.

## Limitations

Fast-moving codebase with breaking changes between major versions (Neural MMO's own Python version is stuck on an older integration). macOS build fragile. No text interface for LLM agents. Documentation is on puffer.ai and Discord rather than in the repo.

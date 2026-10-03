---
id: gh-salesforce-warp-drive
type: code
title: "WarpDrive: end-to-end multi-agent RL on a GPU (CUDA C / Numba env step + PyTorch training), e.g. 1000-agent Tag"
repo: salesforce/warp-drive
url: https://github.com/salesforce/warp-drive
authors: ["Tian Lan", "Sunil Srinivasa", "Huan Wang", "Stephan Zheng"]
year: 2021
language: Python / CUDA C
license: "BSD-3-Clause"
stars: 503
last_commit: 2025-05-01
topics: [marl-emergence, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: [lan-2021-warpdrive]
---

## Summary

A framework rather than a world: the user writes the environment step in CUDA C or Numba, and WarpDrive keeps all simulation state, observations and rollouts on the GPU, running one environment replica per thread block and one agent per thread, with PyTorch policies trained in place. Bundled examples are continuous and discrete "Tag" pursuit games (taggers chase runners), classic control, and Salesforce's COVID-19 and climate economic simulations. The README table claims 1-1000 environments per GPU and up to 1024 agents per environment (more across blocks since v1.6); the paper reports 2.9 million environment steps per second with 2000 environments and 1000 agents in Tag [[lan-2021-warpdrive]]. RL-only. Agent count is fixed per compiled environment; no open-population support. Heavy: NVIDIA GPU (V100/A100 Docker images), CUDA.

## What it can do for us

Historical reference for the "keep everything on the GPU, one thread per agent" pattern that Madrona and JAX suites later generalised. Not a starting point now.

## Run notes

Not run (needs NVIDIA GPU). README read via GitHub API on 2026-10-03.

## Limitations

Archived on GitHub (read-only). CUDA-only. Environments must be rewritten as GPU kernels.

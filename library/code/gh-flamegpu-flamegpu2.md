---
id: gh-flamegpu-flamegpu2
type: code
title: "FLAME GPU 2: CUDA/C++ and Python agent-based simulation library with typed message passing, spatial messaging and GPU ensembles"
repo: FLAMEGPU/FLAMEGPU2
url: https://github.com/FLAMEGPU/FLAMEGPU2
authors: ["Paul Richmond", "Robert Chisholm", "Peter Heywood", "Matthew Leach", "Mozhgan Kabiri Chimeh"]
year: 2020
language: CUDA/C++, Python
license: "AGPL-3.0"
stars: 157
last_commit: 2026-09-22
topics: [collective-motion, crowds-and-traffic, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 4
papers: [richmond-2023-flame]
---

## Summary

One line: general ABM on NVIDIA GPUs; agents interact only through typed message lists (brute force, 2D/3D spatial radius, discrete grid, array, or integer-keyed bucket messaging); the paper shows a continuous-space benchmark at 1M agents in about 3 ms per step and Sugarscape at 16M cells in about 1 s per step; no LLM integration; adversarial agents are just another agent type or agent state (no built-in fault/Sybil hooks); heavy to run (needs CUDA, no macOS GPU path).

Sheffield RSE's rewrite of FLAME GPU. A model is a declarative description (agent types, states, typed variables, messages, layers of agent functions) that the library maps to CUDA kernels, with agent functions written in CUDA C++ or in a Python subset that is transpiled to C++ (marked experimental). Supports agent birth and death, sub-models for conflict resolution, ensembles of runs sharing one GPU, logging, and real-time visualisation. The README says the project is still a release candidate and the API may break; Python wheels are published but not manylinux compliant.

## What it can do for us

The only general ABM framework in this scan that has demonstrated million-agent continuous-space flocking at interactive rates. The message-specialisation design is a good template for a sim where all inter-agent influence passes through an inspectable channel: a Sybil or Byzantine agent is then just an agent that writes adversarial messages, and the message list is the natural place to log or filter. Ensembles let thousands of small parameter sweeps (for example many 200-agent swarms with different attacker fractions) share one GPU.

## Run notes

Not run: no NVIDIA GPU on the Mac used for this scan. Install route per README is pip wheels from whl.flamegpu.com (Linux/Windows, CUDA) or a CMake build with the CUDA toolkit. Would run on orbital-one (RTX PRO 4000, aarch64) only if a CUDA aarch64 build works; untested.

## Limitations

AGPL-3.0 (a network service built on it must publish source). CUDA-only, so no Apple Silicon. Still pre-release after several years. Python agent functions are a transpiled subset, so arbitrary Python (such as calling an LLM inside an agent step) is not possible on device; LLM-driven agents would have to live on the host between steps.

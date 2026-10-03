---
id: gh-emerge-lab-gpudrive
type: code
title: "GPUDrive: Madrona-based multi-agent driving simulator on Waymo Open Motion scenes at ~1M steps/s"
repo: Emerge-Lab/gpudrive
url: https://github.com/Emerge-Lab/gpudrive
authors: ["Saman Kazemkhani", "Aarav Pandya", "Daphne Cornelisse", "Brennan Shacklett", "Eugene Vinitsky"]
year: 2024
language: C++ / CUDA / Python
license: "MIT"
stars: 620
last_commit: 2025-12-01
topics: [marl-emergence, crowds-and-traffic]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [kazemkhani-2024-gpudrive]
---

## Summary

Simulates road traffic scenes (vehicles, cyclists, pedestrians) initialised from the Waymo Open Motion Dataset's 100k+ real scenarios, with every agent stepped in parallel across hundreds of worlds on a GPU through [[gh-shacklettbp-madrona]]; interaction is simultaneous, partially observed (radial filter or LiDAR-like views), goal-reaching. The paper reports a peak of 2.3 million agent steps per second (ASPS) and about 200,000 controlled-agent steps per second on real scene mixes, versus about 15,000 for the CPU predecessor Nocturne [[kazemkhani-2024-gpudrive]]. RL-only (gymnasium wrappers in torch and JAX). The number of controlled agents varies per scene (mean about 10.8 in the paper's sample) and the user chooses which agents are policy-controlled versus log-replayed, which is a natural hook for injecting a minority of adversarial or colluding drivers among human-log traffic. Heavy: CUDA 12.2-12.4, CMake build, recursive submodules.

## What it can do for us

The only entry here with real human multi-agent trajectory data built in: a mixed population of logged humans plus our agents, which suits "detect the bots among humans" questions in a traffic setting. Supersedes Facebook's archived Nocturne.

## Run notes

Not run (CUDA build). README read via GitHub API on 2026-10-03.

## Limitations

CUDA version pinned (no 12.5+ per README). Waymo data licence applies to scenes. Domain-specific to driving.

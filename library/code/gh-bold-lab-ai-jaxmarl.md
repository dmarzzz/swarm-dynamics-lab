---
id: gh-bold-lab-ai-jaxmarl
type: code
title: "JaxMARL: GPU-vectorised MARL environments (SMAX, MPE, Overcooked, Hanabi, STORM) and baselines in JAX"
repo: bold-lab-ai/JaxMARL
url: https://github.com/bold-lab-ai/JaxMARL
authors: ["Alexander Rutherford", "Benjamin Ellis", "Jakob Foerster", "et al. (FLAIR Oxford)"]
year: 2023
language: Python
license: "Apache-2.0"
stars: 854
last_commit: 2026-09-10
topics: [marl-emergence]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

End-to-end JAX MARL: environments and algorithms (IPPO, MAPPO, QMIX and others) jitted together so thousands of environments run in parallel on one GPU, including SMAX, a vectorised StarCraft-like benchmark without the game engine. Repo now lives under bold-lab-ai. Apache-2.0, 854 stars, last commit 2026-09-10.

## What it can do for us

The seed asked what trains fast on one GPU: this is the answer for standard benchmarks. Adding a custom swarm environment in JAX is feasible if someone knows JAX.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

JAX expertise needed; environments are benchmark games, not swarms. Not run.

## Notes from dmarz/sim-envs

2026-10-03: paper now catalogued as [[rutherford-2023-jaxmarl]] (arXiv 2311.10090; about 14x faster wall clock than prior pipelines, up to 12,500x with vectorised runs; introduces SMAX). Later JAX worlds built on this API: [[gh-baselomari-ma-craftax]], [[gh-alem-world-alem-env]].

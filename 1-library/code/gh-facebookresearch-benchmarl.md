---
id: gh-facebookresearch-benchmarl
type: code
title: "BenchMARL: TorchRL-based MARL training and benchmarking library, the native trainer for VMAS tasks"
repo: facebookresearch/BenchMARL
url: https://github.com/facebookresearch/BenchMARL
authors: ["Matteo Bettini", "Meta FAIR"]
year: 2023
language: Python
license: "MIT"
stars: 668
last_commit: 2026-02-07
topics: [marl-emergence, swarm-robotics]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Hydra-configured MARL training library over TorchRL with algorithms (MAPPO, IPPO, QMIX, MADDPG, etc.) and tasks from VMAS, PettingZoo, SMACv2 and Melting Pot, run as `python benchmarl/run.py algorithm=mappo task=vmas/balance`, with public W&B reports. arXiv 2312.01472. MIT, 668 stars, last commit 2026-02-07.

## What it can do for us

Train policies on VMAS flocking or dispersion in one command; the pairing with VMAS (ran above) makes it the quickest learned-swarm pipeline available to us.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

GPU recommended; config surface is large. Not run.

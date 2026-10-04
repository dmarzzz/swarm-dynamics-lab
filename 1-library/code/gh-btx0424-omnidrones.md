---
id: gh-btx0424-omnidrones
type: code
title: "OmniDrones: Isaac Sim platform for multi-rotor RL with benchmark tasks (unmaintained)"
repo: btx0424/OmniDrones
url: https://github.com/btx0424/OmniDrones
authors: ["Botian Xu", "Feng Gao", "Chao Yu", "Ruize Zhang", "Yi Wu", "Yu Wang"]
year: 2023
language: Python
license: "MIT"
stars: 583
last_commit: 2026-01-20
topics: [swarm-robotics, marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 2
papers: []
---

## Summary

One line: GPU-parallel multi-rotor simulation on NVIDIA Isaac Sim with single- and multi-agent benchmark tasks and RL baselines; throughput claims are in the paper (arXiv 2309.12825), not the README; no LLM integration; no adversarial hooks; very heavy to run (Isaac Sim 4.1, NVIDIA GPU, no Windows).

The README's first section says the project is hard to maintain and may or may not be refactored, and asks interested researchers to email the author.

## What it can do for us

Task designs (multi-drone transport, formation, pursuit) are worth borrowing; the code base is not.

## Run notes

Not run (needs Isaac Sim and an NVIDIA GPU).

## Limitations

Effectively unmaintained by its author's own statement; tied to specific Isaac Sim versions.

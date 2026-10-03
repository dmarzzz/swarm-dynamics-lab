---
id: gh-flatland-association-flatland-rl
type: code
title: "Flatland: railway train-scheduling gridworld for multi-agent RL and operations research (hundreds of trains)"
repo: flatland-association/flatland-rl
url: https://github.com/flatland-association/flatland-rl
authors: ["Flatland Association", "SBB / AIcrowd contributors", "Sharada Mohanty et al."]
year: 2019
language: Python
license: "MIT"
stars: 73
last_commit: 2026-09-25
topics: [marl-emergence, crowds-and-traffic]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Simulates trains (agents) on a procedurally generated rail network gridworld who must reach their destinations on time without deadlocks, with malfunctions and speed profiles adding uncertainty; interaction is simultaneous, each train choosing at switches, and it is meant to compare MARL against operations-research planners. Population is listed as more than 100 agents in [[hu-2025-toward]], with asynchronous execution support; throughput not measured here. RL and OR oriented, no text interface. Number of trains is a generator parameter; trains enter the network at scheduled departure times, which is a limited form of staggered arrival. Light pure-Python install, tested on macOS, Linux and Windows for Python 3.10-3.14. Actively maintained by the Flatland Association with an ECML 2026 challenge.

## What it can do for us

A maintained example of a many-agent env with scheduled entries and random malfunctions (faulty agents), and a long competition history comparing learned and planned solutions. Mostly background for us.

## Run notes

Not run. README read via GitHub API on 2026-10-03.

## Limitations

Domain-specific (rail). The 73-star org repo is a successor of the earlier AIcrowd repository; older papers point to the old location.

---
id: gh-gitsper-decentralized-blocklist-protocol
type: code
title: "Decentralized Blocklist Protocol: ARGoS experiments for Byzantine-resilient swarms via inter-robot accusations"
repo: gitsper/decentralized-blocklist-protocol
url: https://github.com/gitsper/decentralized-blocklist-protocol
authors: ["Kacper Wardega"]
year: 2023
language: C++
license: "none stated"
stars: 0
last_commit: 2023-01-12
topics: [sybil-resistance, swarm-robotics]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [wardega-2023-byzantine]
---

## Summary

Source code to reproduce the experiments of [[wardega-2023-byzantine]]: ARGoS controllers and a networked footbot plugin for target tracking (flocking), time synchronization and localization with accusation flooding and maximum-matching blocklists, plus a Jupyter notebook for figures. Depends on ARGoS and the Boost graph library.

## What it can do for us

Ready-made testbed for accusation-based Byzantine exclusion at hundreds of robots; the accusation and matching logic could be lifted into an agent-swarm simulator.

## Run notes

Not run. README read via the GitHub API: build the plugin with cmake (sudo make install), then make, then e.g. argos3 -c experiments/DBP_flocking/flocking_positive-obs.argos. Stars, licence and last commit from the GitHub API on 2026-10-03.

## Limitations

No licence file reported by GitHub, so reuse terms are unclear; single burst of commits in January 2023; requires ARGoS (Linux or macOS build).

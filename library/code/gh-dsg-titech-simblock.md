---
id: gh-dsg-titech-simblock
type: code
title: "SimBlock: Java blockchain network simulator for block propagation across regions"
repo: dsg-titech/simblock
url: https://github.com/dsg-titech/simblock
authors: ["Distributed Systems Group, Tokyo Institute of Technology"]
year: 2019
language: "Java"
license: "Apache-2.0"
stars: 249
last_commit: 2024-07-08
topics: [sync-consensus]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: [aoki-2019-simblock]
---

## Summary

Simulates: a public blockchain's node network and block propagation with regional latency and bandwidth, with a separate visualiser for propagation. Interaction model: Java discrete-event simulation of abstract nodes. Scale: not stated in the README or user guide. LLM-driven: no. Adversarial hooks: none native in the repository (no attacker or selfish-mining files in the tree); attacks need custom node code. Weight: JDK 1.8+ and Gradle, light, runs on macOS.

## What it can do for us

Background reference for block propagation simulation; only useful if we need a quick propagation-delay model for a builder or relay latency question.

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Bitcoin-era propagation model; no PBS, relays or builders. No adversary support out of the box.

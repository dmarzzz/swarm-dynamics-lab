---
id: gh-chroma-citi-dancers
type: code
title: "DANCERS: co-simulator coupling a multi-robot simulator (e.g. Gazebo) with a network simulator (e.g. ns-3)"
repo: Chroma-CITI/DANCERS
url: https://github.com/Chroma-CITI/DANCERS
authors: ["Chroma-CITI GitHub organisation"]
year: 2024
language: C++
license: "GPL-3.0"
stars: 19
last_commit: 2026-07-10
topics: [swarm-robotics]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: []
---

## Summary

One line: synchronises a robot simulator and a packet-level network simulator so that networked multi-robot systems (drone swarms) see realistic radio links, latency and loss; README gives no scale numbers; no LLM integration; adversarial messages or jamming could be injected on the ns-3 side but no ready hooks are described; heavy to run (two simulators, ROS-style setup, documented in the wiki).

Presented at SIMPAR 2025 (IEEE). The README is short and points to wiki tutorials of increasing complexity.

## What it can do for us

The one entry here that models the communication channel itself, which is where Sybil identities, spoofed beacons and message flooding live in a real drone swarm. Worth borrowing the architecture (physics sim and network sim stepping in lock-step) even if we never run Gazebo.

## Run notes

Not run.

## Limitations

Small project, GPL-3.0, heavy dependency stack.

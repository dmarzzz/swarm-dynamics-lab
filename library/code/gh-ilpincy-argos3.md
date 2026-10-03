---
id: gh-ilpincy-argos3
type: code
title: "ARGoS 3: physics-based multi-robot simulator built for large swarms (multiple physics engines, thousands of robots)"
repo: ilpincy/argos3
url: https://github.com/ilpincy/argos3
authors: ["Carlo Pinciroli", "et al."]
year: 2012
language: C++
license: "none stated"
stars: 321
last_commit: 2026-02-12
topics: [swarm-robotics]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

The standard swarm-robotics simulator: multi-threaded modular C++ architecture, several physics engines that can run simultaneously on different regions of space, robot models including Kilobot, e-puck, foot-bot and drones, and benchmark results claiming physics-accurate simulation of thousands of robots in a fraction of real time. Requires Linux or macOS, g++ 5.4+, cmake 3.5.1+. MIT per README (the API reports no licence file), 321 stars, last commit 2026-02-12.

## What it can do for us

If we need embodied swarm experiments at hundreds to thousands of robots with realistic sensing limits, ARGoS is the tool; Buzz programs run on it directly.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

C++ build with Qt for visualisation; controllers are C++ or Lua (or Buzz). No Python API in core. Not run.

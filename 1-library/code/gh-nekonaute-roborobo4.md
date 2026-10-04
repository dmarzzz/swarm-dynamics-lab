---
id: gh-nekonaute-roborobo4
type: code
title: "Roborobo 4: fast 2D multi-robot simulator for evolutionary swarm robotics, C++ core with Python interface"
repo: nekonaute/roborobo4
url: https://github.com/nekonaute/roborobo4
authors: ["Nicolas Bredeche", "Paul Ecoffet", "Jean-Marc Montanier", "Berend Weel", "Evert Haasdijk"]
year: 2009
language: C++, Python
license: "none stated (GitHub reports NOASSERTION)"
stars: 10
last_commit: 2025-05-19
topics: [swarm-robotics, marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 2
papers: []
---

## Summary

One line: 2D kinematic robots loosely modelled on Khepera and e-puck with range sensors, built for embodied evolution and multi-agent learning in large collectives; README claims "super fast" but gives no numbers; no LLM integration; no adversarial hooks; light to run on Linux or macOS (conda, pybind11, C++ compiler).

Maintained by Nicolas Bredeche (Sorbonne, ISIR) since 2009; citation is Bredeche et al., Roborobo! a fast robot simulator for swarm and collective robotics (arXiv 1304.2888). The current release string in the README is 20210321.

## What it can do for us

Its use case, distributed online evolution where genomes spread robot to robot, is close to fork-and-merge questions (what a swarm absorbs from a corrupted peer). Good idea source; small user base.

## Run notes

Not run.

## Limitations

10 stars, niche; licence not machine-readable on GitHub.

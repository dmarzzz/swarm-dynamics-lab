---
id: gh-boshmaf-sypy
type: code
title: "SyPy: Python framework for building and evaluating graph-based Sybil node detection algorithms"
repo: boshmaf/sypy
url: https://github.com/boshmaf/sypy
authors: ["Yazan Boshmaf", "Tony Cheng"]
year: 2013
language: "Python"
license: "GPL-3.0"
stars: 23
last_commit: 2018-03-06
topics: [sybil-resistance]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

SyPy, started at the University of British Columbia by Yazan Boshmaf, models a network as two regions (honest and Sybil), each with a chosen graph structure (complete, scale-free, small-world and others built on NetworkX), and stitches them together with a configurable number of attack edges, randomly or by targeted infiltration. Detectors such as SybilGuard then partition the graph, and the framework reports accuracy, sensitivity and specificity. The README states the three standard assumptions: the defender knows at least one honest node, the honest and Sybil regions are loosely connected, and the honest region is fast mixing.

## What it can do for us

A ready-made experimental harness for the question we care about: how detection degrades as the number of attack edges grows. Its region and stitching abstractions map directly onto an agent-swarm setting where an adversary spins up many agent identities and then buys or earns links to honest agents.

## Run notes

Not run. README read via the GitHub API on 2026-10-03; it requires Python 2.7 and NetworkX 1.6, which would need a legacy virtualenv. Example: `python ex_overview.py` in `examples/`.

## Limitations

Python 2 only, last commit 2018. Designed for effectiveness on networks of thousands of nodes, explicitly not for efficiency at scale. GPL-3.0.

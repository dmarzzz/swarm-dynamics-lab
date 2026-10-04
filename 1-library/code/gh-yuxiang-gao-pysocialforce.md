---
id: gh-yuxiang-gao-pysocialforce
type: code
title: "PySocialForce: NumPy implementation of the extended social force model for pedestrian groups"
repo: yuxiang-gao/PySocialForce
url: https://github.com/yuxiang-gao/PySocialForce
authors: ["Yuxiang Gao"]
year: 2020
language: Python
license: "MIT"
stars: 185
last_commit: 2022-11-21
topics: [crowds-and-traffic]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 2
papers: []
---

## Summary

One line: continuous-space pedestrians driven by the Helbing social force model extended with social-group forces and static obstacles, configured with TOML; no throughput numbers; no LLM integration; no adversarial hooks; very light to run (pip install pysocialforce).

A compact research implementation for social navigation work; roadmap items such as inter-group interaction remain unchecked, and the repo has been quiet since 2022.

## What it can do for us

Smallest working social-force baseline if a study needs crowd motion with groups (for example a coordinated group of agents hiding inside a crowd). [[gh-pedestriandynamics-jupedsim]]-style tools already cover heavier pedestrian work.

## Run notes

Not run.

## Limitations

Dormant since 2022; NumPy all-pairs forces limit crowd size.

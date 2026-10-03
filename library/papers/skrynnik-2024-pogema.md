---
id: skrynnik-2024-pogema
type: paper
title: "POGEMA: A Benchmark Platform for Cooperative Multi-Agent Pathfinding"
authors: [Alexey Skrynnik, Anton Andreychuk, Anatolii Borzilov, Alexander Chernyavskiy, Konstantin Yakovlev, Aleksandr Panov]
year: 2024
venue: International Conference on Learning Representations (ICLR 2025)
url: https://arxiv.org/abs/2407.14931
doi: null
arxiv: '2407.14931'
cite: "Skrynnik, A., Andreychuk, A., Borzilov, A., Chernyavskiy, A., Yakovlev, K., & Panov, A. (2025). POGEMA: A benchmark platform for cooperative multi-agent pathfinding. In International Conference on Learning Representations (ICLR 2025). arXiv:2407.14931."
topics: [marl-emergence, swarm-robotics]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: [gh-cognitive-ai-systems-pogema]
---

## Summary

Presents POGEMA as a full benchmark platform for partially observable multi-agent pathfinding: a fast learning environment, a problem-instance generator, predefined instance collections, visualisation, and an automated benchmarking tool with an evaluation protocol of domain metrics (success rate, path length and derived measures such as coordination and out-of-distribution performance). Compares MARL methods (IQL, VDN, QMIX, QPLEX, MAMBA), learned MAPF methods (SCRIMP, DCC) and search-based or hybrid planners (e.g. LaCAM) on the same instances.

## Contribution

A single framework where classical planners, learned and hybrid methods are compared under one protocol, at agent counts typical of robotics (hundreds and more) rather than the handful in most MARL benchmarks. An earlier environment-only paper is arXiv 2206.10944 (not catalogued).

## Key results

- Abstract-level only; the first-page radar figure compares methods across axes including obstacle density, coordination and out-of-distribution generalisation.

## Methods and models

Grid MAPF with local egocentric observations; lifelong and one-shot variants.

## Limitations and open questions

Read at abstract level only.

## Relevance to us

We ran the environment at about 170,000-195,000 agent-steps/s on one CPU core for up to 1024 agents ([[gh-cognitive-ai-systems-pogema]]); its benchmark protocol is a template for reporting swarm metrics.

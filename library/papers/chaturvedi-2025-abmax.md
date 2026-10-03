---
id: chaturvedi-2025-abmax
type: paper
title: "ABMax: A JAX-based Agent-based Modeling Framework"
authors: ["Siddharth Chaturvedi", "Ahmed El-Gazzar", "Marcel van Gerven"]
year: 2025
venue: "arXiv (cs.MA)"
url: https://arxiv.org/abs/2508.16508
doi: null
arxiv: "2508.16508"
cite: "Chaturvedi, S., El-Gazzar, A., & van Gerven, M. (2025). ABMax: A JAX-based Agent-based Modeling Framework. arXiv:2508.16508."
topics: [meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: [gh-i-m-iron-man-abmax]
---

## Summary

Abstract only: JAX gives ABMs automatic vectorisation and JIT compilation but requires array shapes to stay fixed, which conflicts with ABM operations that update a dynamically selected number of agents with distinct changes. ABMax implements JIT-compilable algorithms for this, reports run time comparable to state-of-the-art implementations on the predator-prey benchmark, shows the operation can be vectorised to run many models in parallel, and gives traffic-flow and financial-market examples.

## Contribution

Names and solves the fixed-shape problem that blocks agent birth, death and selective updates in JAX ABMs, a recurring obstacle for GPU-vectorised agent simulations.

## Key results

- From the abstract: performance comparable to state of the art on the predation (wolf-sheep) benchmark; vectorised multi-model runs. The repo README gives Wolf-Sheep large at 685 ms in Agents.jl versus 3,316 ms in ABMax (Rank-Match) and 170,071 ms in Mesa, 100 steps, A100 node.

## Methods and models

Rank-Match and Sort-Count-Iterate algorithms over fixed-capacity agent arrays with active masks (per repo README); JAX and Flax.

## Limitations and open questions

Read abstract only. Single-model speed trails Agents.jl per its own README.

## Relevance to us

If we go the JAX route (with [[gh-jax-md-jax-md]] or [[gh-learnsyslab-crazyflow]]), this is the pattern for agents that join, leave or are compromised mid-run without breaking jit.

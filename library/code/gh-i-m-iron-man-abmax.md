---
id: gh-i-m-iron-man-abmax
type: code
title: "Abmax: JAX agent-based modelling framework with JIT-compatible updates for a dynamic number of agents"
repo: i-m-iron-man/abmax
url: https://github.com/i-m-iron-man/abmax
authors: ["Siddharth Chaturvedi", "Ahmed El-Gazzar", "Marcel van Gerven"]
year: 2024
language: Python (JAX, Flax)
license: "MIT"
stars: 20
last_commit: 2026-03-31
topics: [meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 2
papers: [chaturvedi-2025-abmax]
---

## Summary

One line: ABM in JAX where agent sets are fixed-shape arrays and two algorithms (Rank-Match, Sort-Count-Iterate) apply distinct updates to a run-time-selected subset of agents under jit and vmap; README benchmark on an A100: Wolf-Sheep large 685 ms (Agents.jl CPU) versus 3,316 ms (Abmax RM) versus 170,071 ms (Mesa) for 100 steps; no LLM integration; no adversarial hooks; light install (pip install abmax) but needs JAX.

Research code from Radboud/Donders. Its distinctive value is many models vmapped in parallel (the README shows batch sizes from 10 to 500 Wolf-Sheep models).

## What it can do for us

Template for running hundreds of independent small swarms in one vectorised call on GPU, which suits Monte Carlo over attacker placements. Pairs with [[gh-jax-md-jax-md]] already in the library.

## Run notes

Not run.

## Limitations

Single-run speed is behind Agents.jl on CPU per its own table; small project; fixed-shape arrays complicate birth/death-heavy models.

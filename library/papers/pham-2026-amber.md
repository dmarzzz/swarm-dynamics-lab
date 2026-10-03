---
id: pham-2026-amber
type: paper
title: "AMBER: A Columnar Architecture for High-Performance Agent-Based Modeling in Python"
authors: ["Anh-Duy Pham"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2601.16292
doi: null
arxiv: '2601.16292'
cite: "Pham, A.-D. (2026). AMBER: A columnar architecture for high-performance agent-based modeling in Python. arXiv:2601.16292."
topics: [meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: [gh-a11to1n3-amber]
---

## Summary

Python ABM framework that stores all agent state in a Polars columnar table and exposes population operations through a view API, compiling common updates into column operations while keeping a buffered object-oriented path for behaviours that do not vectorise. Benchmarked on wealth transfer, random walk and spatial SIR against Mesa, AgentPy, SimPy, Melodie, Agents.jl and its own loop path, with invariant checks that outputs agree before timing.

## Contribution

Shows that a dataframe-backed state store gives Python ABMs compiled-speed population updates without abandoning the Mesa/AgentPy model-agent abstraction.

## Key results

- Fastest of the Python-hosted implementations on all tested workloads; up to 1118x faster than Mesa.
- On the largest SIR benchmark it is also faster than the Agents.jl implementation.

## Methods and models

Polars DataFrame per population; vectorised step and OOP step lanes; optional NVIDIA CuPy GPU lane (README).

## Limitations and open questions

Abstract only. Single author, 3-star repo. Speedups apply to vectorisable rules; LLM-driven agents are bottlenecked by inference, not by the ABM loop.

## Relevance to us

Borrow idea for the rule-based layer of a hybrid sim: columnar state + invariant-checked benchmarks. Compare [[gh-mesa-mesa]], [[gh-jofmi-agentpy]], [[gh-abm4all-melodie]], [[gh-juliadynamics-agents-jl]].

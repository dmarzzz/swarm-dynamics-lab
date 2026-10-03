---
id: gh-repast-repast4py
type: code
title: "Repast4Py: distributed (MPI) agent-based modelling in Python, the Python member of the Repast suite"
repo: Repast/repast4py
url: https://github.com/Repast/repast4py
authors: ["Nicholson Collier", "Jonathan Ozik", "Eric Tatara"]
year: 2020
language: Python, C++
license: "BSD-3-Clause (per README; GitHub reports NOASSERTION)"
stars: 75
last_commit: 2026-10-02
topics: [meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: []
---

## Summary

One line: general ABM partitioned across MPI ranks (shared grid and continuous spaces and networks, with ghost agents copied across rank boundaries); built for HPC clusters, but the README gives no throughput figures; no LLM integration; no adversarial hooks beyond writing your own agent class; medium to heavy to run (needs MPI and a C compiler, and PyTorch as a dependency).

Argonne's Python successor to Repast HPC (C++). Uses Numba, NumPy, PyTorch and native code through the Python C API, and requires Python 3.10+. A non-MPI install exists for Linux and Mac but still compiles native code. The design paper is Collier, Ozik and Tatara (2020), PyHPC workshop, doi 10.1109/PyHPC51966.2020.00006; I read only its abstract (not catalogued separately because I could not open the full page).

## What it can do for us

Only relevant if a model outgrows one machine: it is the established Python route to spreading one big ABM across many ranks with synchronised ghost agents. For swarm experiments at 10^3 to 10^5 agents a single-process framework is simpler.

## Run notes

Not run. Install needs mpich or open-mpi plus mpi4py, then pip install repast4py (compiles native extensions).

## Limitations

MPI programming model leaks into model code (agents must be serialisable, rank-local scheduling). The Repast HPC C++ sibling (Repast/repast.hpc, 29 stars) was last pushed 2023-08-09 and looks dormant.

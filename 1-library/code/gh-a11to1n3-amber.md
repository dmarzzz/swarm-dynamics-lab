---
id: gh-a11to1n3-amber
type: code
title: "AMBER (ambr): Polars-columnar Python ABM framework with vectorised and optional CUDA lanes"
repo: a11to1n3/AMBER
url: https://github.com/a11to1n3/AMBER
authors: ["Anh-Duy Pham"]
year: 2026
language: Python
license: "BSD-3-Clause"
stars: 3
last_commit: 2026-09-01
topics: [meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: [pham-2026-amber]
---

## Summary

Simulation model: generic ABM framework; population state in a Polars DataFrame with a vectorised view API (where, at, scatter_add), an AgentPy-shaped OOP lane, and optional NVIDIA CuPy GPU lane. Scale: README headline table at 10M agents on an RTX 5090. LLM-native: no. Adversarial hooks: none. Weight: pip install ambr; GPU path needs NVIDIA (no Apple Metal).

## What it can do for us

Fast rule-based population layer for hybrid sims where most agents are cheap rules and a few are LLMs.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API; source code not read.

## Limitations

Tiny user base (3 stars); GPU claims need CUDA, which our Macs lack; README warns most result files other than the headline snapshot are exploratory.

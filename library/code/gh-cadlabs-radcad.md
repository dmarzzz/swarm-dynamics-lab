---
id: gh-cadlabs-radcad
type: code
title: "radCAD: faster cadCAD-compatible framework for parameter-swept system simulations"
repo: CADLabs/radCAD
url: https://github.com/CADLabs/radCAD
authors: ["CADLabs"]
year: 2020
language: "Python"
license: "GPL-3.0"
stars: 120
last_commit: 2026-06-25
topics: [meta, sybil-resistance]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: ran
relevance: 3
papers: []
---

## Summary

Simulates: discrete-time state-machine models in the cadCAD shape (policies, state-update blocks, Monte Carlo runs, parameter sweeps), used by CADLabs for Ethereum economic models. Interaction model: synchronous timesteps over a state dict; agents are state variables. Scale: we ran 60 runs of 20 steps in 0.02 s on a Mac. LLM-driven: only by calling a model inside a policy function; nothing built in. Adversarial hooks: none native; Sybil minting, detection and capture are policies you write (we wrote one). Weight: pip install, pure Python, seconds on a laptop.

## What it can do for us

Fast, reproducible sweeps of analytic Sybil-economics models (identity cost against detection rate against capture threshold) before committing to an agent or network simulator. Pitfall found while running it: radCAD zips parameter lists rather than taking their Cartesian product; lists of unequal length repeat the last value of the shorter list.

## Run notes

Installed in a uv venv on macOS (Python 3.12): `uv pip install radcad inspect-ai pandas` (radCAD 0.14.0). Wrote a toy one-identity-one-vote model: 100 honest identities, attacker budget 50, mints min(budget/identity_cost, 10) Sybils per step, each Sybil detected with probability detect_rate per step, capture when Sybils exceed 50% of honest count. Script at /private/tmp/claude-501/-Users-halcyon/91c0102b-dec1-491c-bac9-3e6625d95c8f/scratchpad/simenv/radcad_sybil.py, run with `python radcad_sybil.py`, Engine(backend=Backend.SINGLE_PROCESS), 20 timesteps, 20 runs. Result: 1,260 rows in 0.02 s. With params {identity_cost: [0.5, 1.0, 2.0], detect_rate: [0.0, 0.1]} radCAD produced 3 subsets, not 6: (0.5, 0.0) gave mean 100 Sybils and capture in 100% of runs; (1.0, 0.1) gave 8.6 Sybils and 0% capture; (2.0, 0.1) gave 3.9 Sybils and 0% capture. `generate_parameter_sweep` confirmed the zip-with-padding semantics.

## Limitations

GPL-3.0. Same modelling limits as cadCAD: no network, message timing or real processes. Sweep semantics differ from a naive grid (see above).

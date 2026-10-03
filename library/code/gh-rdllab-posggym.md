---
id: gh-rdllab-posggym
type: code
title: "POSGGym: Gymnasium-style library of partially observable multi-agent environments with reference agents and generative models for planning"
repo: RDLLab/posggym
url: https://github.com/RDLLab/posggym
authors: ["RDLLab"]
year: 2022
language: Python
license: "MIT"
stars: 34
last_commit: 2025-06-02
topics: [marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: []
---

## Summary

Simulation model: collection of classic POSG problems, 2D grid-world and continuous environments (e.g. PredatorPrey, Driving) with a Gymnasium-like Env API, a stateless POSGModel generative model for planning, reference agent policies, and a PettingZoo wrapper. Scale: small numbers of agents. LLM-native: no. Adversarial hooks: none. Weight: pip install posggym (downloads agent models), extras for torch agents. Baselines in RDLLab/posggym-baselines. Semantic Scholar lists a 2025 paper 'POSGGym: a library for decision-theoretic planning and learning in partially observable, multi-agent environments' among Melting Pot citers; not catalogued (no arXiv id, not opened).

## What it can do for us

Stateless generative models make it one of few MARL suites usable for online planning (MCTS/POMCP) as well as RL; reference agents give fixed opponent populations.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API; source code not read.

## Limitations

Small envs and agent counts; last push 2025-06.

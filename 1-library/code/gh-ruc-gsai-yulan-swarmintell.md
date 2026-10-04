---
id: gh-ruc-gsai-yulan-swarmintell
type: code
title: "SwarmBench (YuLan-SwarmIntell): 2D grid benchmark of LLM agents on pursuit, synchronisation, foraging, flocking and transport with local views and local messages"
repo: RUC-GSAI/YuLan-SwarmIntell
url: https://github.com/RUC-GSAI/YuLan-SwarmIntell
authors: ["Kai Ruan", "Mowen Huang", "Ji-Rong Wen", "Hao Sun"]
year: 2025
language: Python
license: "MIT"
stars: 39
last_commit: 2025-05-21
topics: [llm-agent-swarms, collective-motion, swarm-intelligence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 5
papers: [ruan-2025-benchmarking]
---

## Summary

Simulation model: discrete 2D grid physics where each LLM agent sees only a k x k neighbourhood and can send short local messages; five canonical swarm tasks (pursuit, synchronisation, foraging, flocking, transport) with automatic scoring. Scale: the README example runs `num_agents=10`. LLM-native: yes, any OpenAI-compatible endpoint configured per model in `eval.py`. Adversarial hooks: none built in; agents are homogeneous by default. Weight: conda env from `environment.yaml`, API calls per agent per step. Repository name differs from the benchmark name; a `swarmbench` package is installed from it.

## What it can do for us

The only maintained LLM benchmark built directly on swarm-intelligence tasks, so it is the natural bridge between classical swarm metrics (alignment, synchrony) and LLM agents. Inserting a misbehaving agent into flocking or synchronisation is a direct robustness test. Ships replay and score-aggregation scripts.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API. I did not read the source code. Entry point: `conda env create -f environment.yaml && python eval.py` with model, API key and base in `SwarmFramework.model_config`.

## Limitations

Small code base, last push May 2025. Cost grows with agents times steps since every agent is an LLM call each step. Grid physics is coarse; no topology beyond spatial neighbourhoods.

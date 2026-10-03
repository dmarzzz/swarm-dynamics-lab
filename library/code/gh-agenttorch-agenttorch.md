---
id: gh-agenttorch-agenttorch
type: code
title: "AgentTorch: differentiable, GPU-batched 'large population models' in PyTorch with LLM archetypes driving agent behaviour"
repo: AgentTorch/AgentTorch
url: https://github.com/AgentTorch/AgentTorch
authors: ["Ayush Chopra", "MIT Media Lab contributors"]
year: 2023
language: Python (PyTorch)
license: "AGPL-3.0"
stars: 652
last_commit: 2026-09-12
topics: [llm-agent-swarms, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

One line: tensorised ABM of millions of agents (populations, geospatial and network interactions as tensor ops, differentiable through stochastic steps) where LLM behaviour is sampled per archetype and broadcast to matching population groups rather than called per agent; the README claims million-agent populations in seconds but I saw no benchmark table; LLM-driven via agent_torch/core/llm (Archetype, behavior, prompt templates, backends, mock LLM); no adversarial hooks; medium to run (PyTorch, GPU preferred).

Project of Ayush Chopra (MIT Media Lab). Models include COVID and macro-economics with calibration. The Archetype class takes a prompt and an LLM, creates n_arch LLM archetypes, binds them to a population with broadcast(match_on/group_on), and sample() returns a decision tensor for the whole population. Associated preprint: Chopra, Large Population Models (arXiv 2507.09901), not catalogued here.

## What it can do for us

The archetype trick (one LLM query per demographic or role group, broadcast to thousands of agents) is the cheapest known way to put LLM-shaped behaviour into a large swarm, and it maps onto Sybil questions directly: a Sybil cluster is literally one archetype with many bodies. Differentiability lets you fit parameters to observed traces.

## Run notes

Not run. Skimmed agent_torch/core/llm/archetype.py; install is pip install git+https://github.com/agenttorch/agenttorch.

## Limitations

AGPL-3.0 (commercial licence by request). Archetype broadcasting removes per-agent individuality, which is exactly what some swarm-detection experiments need to keep. Domain models are epidemiology and economics, not flocking.

## Notes from dmarz/sim-envs

2026-10-03: the umbrella position paper for this framework is [[chopra-2025-large]] (Large Population Models, arXiv 2507.09901), which frames AgentTorch as the implementation of LPMs (million-agent simulation, data-driven calibration, privacy-preserving links to real populations).

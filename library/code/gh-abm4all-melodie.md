---
id: gh-abm4all-melodie
type: code
title: "Melodie: Python ABM framework with Cython-accelerated core plus Calibrator and Trainer modules"
repo: ABM4ALL/Melodie
url: https://github.com/ABM4ALL/Melodie
authors: ["Songmin Yu", "Zhanyi Hou"]
year: 2021
language: Python, Cython
license: "MIT"
stars: 52
last_commit: 2026-03-28
topics: [meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 2
papers: []
---

## Summary

One line: general Python ABM (grid and network environments, scenario tables) with Cython-compiled agent, environment, agent_list and grid modules; no published throughput figures in the README; no LLM integration; no adversarial hooks, though its Trainer evolves agent parameters (a possible attacker-strategy search); light to run (pip).

JOSS paper Yu and Hou (2023), doi 10.21105/joss.05100. Per the JOSS paper summary found in search, the distinguishing modules versus Mesa and AgentPy are Calibrator (fit scenario parameters to data) and Trainer (evolutionary training of agent parameters). Maintained by the ABM4ALL community; low activity (52 stars, last push March 2026).

## What it can do for us

The Trainer idea (evolve agent strategies inside the ABM loop) is worth borrowing for adversarial-agent search; the framework itself is not a better base than Mesa.

## Run notes

Not run.

## Limitations

Small community; documentation-led; spaces oriented to grid and network rather than continuous flocking.

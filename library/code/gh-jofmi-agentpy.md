---
id: gh-jofmi-agentpy
type: code
title: "AgentPy: Python ABM library integrating model design, experiments and analysis (grid, continuous space with KD-tree, networks)"
repo: jofmi/agentpy
url: https://github.com/jofmi/agentpy
authors: ["Joel Foramitti"]
year: 2020
language: Python
license: "BSD-3-Clause"
stars: 387
last_commit: 2025-02-06
topics: [collective-motion, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: ran
relevance: 2
papers: []
---

## Summary

One line: general Python ABM with Grid, continuous Space (scipy KD-tree neighbour queries by radius) and Network environments, parameter sampling and multi-run Experiments; measured here 19.6k agent-steps/s for 200 boids and 14.6k for 1,000 boids on an M1 Max (about 1.8x Mesa's 10.8k); no LLM integration; no adversarial hooks; very light to run (pip install agentpy).

JOSS paper Foramitti (2021), doi 10.21105/joss.03065. The README now states AgentPy is no longer under active development and recommends Mesa for new projects; last push 2025-02-06.

## What it can do for us

Useful as a second Python reference point for our boids/Vicsek baselines and for its Experiment/Sample API (Saltelli sampling, repeated seeded runs) if we need sensitivity analysis quickly. Not a base to build on, since it is unmaintained.

## Run notes

python3 -m venv abmvenv && abmvenv/bin/pip install agentpy numpy (AgentPy 0.1.5, Python 3.9.6, M1 Max). I wrote a boids model following the structure of AgentPy's official flocking example (2D ap.Space of side 100, outer radius 10 for cohesion and alignment, inner radius 3 for separation, border repulsion, unit speed, seed 42) and timed m.run(display=False). Results 2026-10-03: N=200, 100 steps in 1.02 s = 19,577 agent-steps/s, polarisation 0.116 at t0 rising to 0.578 at step 100; N=1000, 100 steps in 6.83 s = 14,647 agent-steps/s, polarisation 0.034 to 0.303. Compared with Mesa 3.5.1 boids at 200 agents (10,805 agent-steps/s, [[gh-mesa-mesa]]) this is about 1.8x faster, but the two models are not identical (Mesa uses its own BoidsScenario weights), so treat it as same order of magnitude.

## Limitations

Unmaintained per its own README. Pure-Python per-agent loops; throughput falls as neighbour counts grow. No GPU.

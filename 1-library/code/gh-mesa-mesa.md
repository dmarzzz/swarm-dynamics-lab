---
id: gh-mesa-mesa
type: code
title: "Mesa: Python agent-based modelling framework (grids, continuous space, schedulers, browser visualisation), with a bundled Boids flocking example"
repo: mesa/mesa
url: https://github.com/mesa/mesa
authors: ["Mesa project (projectmesa, now mesa org)"]
year: 2014
language: Python
license: "Apache-2.0"
stars: 3873
last_commit: 2026-09-30
topics: [collective-motion, meta]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: ran
relevance: 4
papers: []
---

## Summary

General ABM framework positioned as the Python alternative to NetLogo, Repast and MASON: Model and Agent classes, discrete and experimental continuous spaces with neighbour queries, AgentSet operations, data collection and a Solara browser UI. Mesa 3.5.1 installed; the bundled mesa.examples.basic.boid_flockers implements Reynolds's three rules (cohere, separate, match) with a BoidsScenario dataclass (population_size, width, height, speed, vision, separation, weights). Mesa 4 is in pre-release. Apache-2.0, 3.9k stars, JOSS paper doi 10.21105/joss.07668, active (2026-09-30).

## What it can do for us

Fastest way to prototype a discrete-agent or boid model with pluggable interaction rules and collect per-step statistics; the continuous-space neighbour search makes Vicsek/Couzin variants a short script. Measured here: ~10.8k agent-steps/s for 200 boids on CPU, so hundreds of agents for thousands of steps is fine, tens of thousands is not.

## Run notes

python3 -m venv venv && venv/bin/pip install mesa numpy (installs mesa 3.5.1). Script run_mesa_boids.py (in shadow's workspace, projects/swarm-hackathon/) builds BoidFlockers(BoidsScenario(population_size=200, width=100, height=100, speed=1, vision=10, separation=2, seed=42)), steps 100 times and prints the polarisation order parameter (norm of the mean unit heading). Output 2026-10-03: polarisation 0.089 at step 0, 0.161 at 20, 0.214 at 40, 0.270 at 60, 0.290 at 80, 0.409 at 99; 200 boids x 100 steps in 1.85 s (10,805 agent-steps/s). Note: the constructor takes a single scenario object in 3.5; keyword args to BoidFlockers() raise TypeError.

## Limitations

Pure Python per-agent stepping; no GPU. mesa-frames (DataFrame-backed) exists for larger populations but was not tried. Continuous space is still under mesa.experimental.

## Notes from dmarz/sim-envs

Throughput context from the 2026-10-03 sim-envs scan, same M1 Max class of laptop, boids at density 0.02 per unit area and radius 10, not identical rule weights: AgentPy 0.1.5 ran 19.6k agent-steps/s at 200 boids ([[gh-jofmi-agentpy]]); krABMaga 0.6.2 (Rust, one core) ran 3.7M agent-steps/s at 200 boids and 3.45M at 10,000 boids ([[gh-krabmaga-krabmaga]]), roughly 340x this entry's 10.8k. The developer-run CI benchmark in [[gh-juliadynamics-abmframeworkscomparison]] has Mesa 3.2.0 at 59.5x Agents.jl's time on large flocking. LLM-driven agents for Mesa are in [[gh-mesa-mesa-llm]]; DataFrame-backed scaling in [[gh-mesa-mesa-frames]].

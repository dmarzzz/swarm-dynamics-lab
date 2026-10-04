---
id: datseris-2022-agents
type: paper
title: "Agents.jl: a performant and feature-full agent-based modeling software of minimal code complexity"
authors: ["George Datseris", "Ali R. Vahdati", "Timothy C. DuBois"]
year: 2022
venue: "SIMULATION"
url: https://arxiv.org/abs/2101.10072
doi: 10.1177/00375497211068820
arxiv: "2101.10072"
cite: "Datseris, G., Vahdati, A. R., & DuBois, T. C. (2022). Agents.jl: a performant and feature-full agent-based modeling software of minimal code complexity. SIMULATION, 100(10), 1019-1031."
topics: [meta, collective-motion]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "64 (Crossref, 2026-10-03)"
code: [gh-juliadynamics-agents-jl, gh-juliadynamics-abmframeworkscomparison]
---

## Summary

Presents Agents.jl version 4 (Julia) and compares it with Mesa 0.8, NetLogo 6.2 and MASON 20.0 on a feature table and on run time and lines of code for four standard models (Flocking in continuous space, Wolf-Sheep-Grass, Forest Fire, Schelling). Agents.jl was fastest on every benchmark, often by an order of magnitude, and needed the fewest lines of code; the paper also shows ecosystem integrations (ODE solvers, OpenStreetMap spaces, evolutionary parameter optimisation). Read in full from the arXiv v3 PDF.

## Contribution

The most cited head-to-head ABM framework comparison with shared model specifications, plus the open ABMFrameworksComparison repository so others can re-run or improve implementations. It also argues a design point: the framework should be a library in a general-purpose language, not a separate environment or GUI.

## Key results

- Run time relative to Agents.jl 4.4 (Table 2): Flocking: Mesa 26.8x, NetLogo 10.3x, MASON 2.1x. Wolf-Sheep-Grass: Mesa 31.9x, NetLogo 10.3x, MASON no implementation. Forest Fire: Mesa 125.6x, NetLogo 53.0x. Schelling: Mesa 24.9x, NetLogo 8.0x, MASON 14.3x.
- Lines of code for Flocking: Agents.jl 62, Mesa 102, NetLogo 82 (689 including GUI), MASON 369.
- Coupling a logistic fish-stock ODE to an ABM with a forward-Euler step of 1 gave an average discrepancy of 30 fish versus a Tsit5 solver, and the proper solver was 6x faster.
- An evolutionary optimisation of a multi-city SIR ABM cut infections from 94% to 0.3% of the population (deaths 0.04%), mostly by lowering transmission rate.
- Feature table: Agents.jl has distributed computing, checkpoints, path-finding, N-dimensional spaces, and agent sampling; Mesa 0.8 lacked checkpoints and distributed runs; NetLogo and MASON are capped at 1 GB by default JVM heap unless expanded; none of the four had GIS in core except via NetLogo and MASON extensions.

## Methods and models

Same scenario (initial conditions, grid size, run length) per model across frameworks, time normalised to Agents.jl so results do not depend on hardware. LOC counted after standard formatting, excluding docstrings, comments on their own lines and benchmark infrastructure. Mesa implementations compiled by Vahdati, others by DuBois. Agents activate sequentially in a user-chosen order (default random in the example).

## Limitations and open questions

Written by the framework's developers about their own framework; they note benchmarking was hard because each system implements example models differently and there are no standard benchmark models across communities, and MASON lacked Wolf-Sheep and Forest Fire implementations. Mesa 0.8 is long superseded (the 2026 CI table in [[gh-juliadynamics-abmframeworkscomparison]] uses Mesa 3.2.0 and still shows Mesa 59x slower on large flocking). Hardware, agent counts and seeds per benchmark are not in the paper text.

## Relevance to us

Anchors our framework choice with numbers: Python-object frameworks ([[gh-mesa-mesa]], [[gh-jofmi-agentpy]]) are one to two orders slower than compiled ones ([[gh-juliadynamics-agents-jl]], [[gh-eclab-mason]], [[gh-krabmaga-krabmaga]]). Its ODE-coupling example is a warning for continuous-time swarm models (Cucker-Smale, swarmalators) simulated with a naive Euler step. Points to [[grimm-2020-odd]] for model description.

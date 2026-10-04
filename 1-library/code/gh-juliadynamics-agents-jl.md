---
id: gh-juliadynamics-agents-jl
type: code
title: "Agents.jl: Julia agent-based modelling framework (grid, continuous, graph, OpenStreetMap spaces; discrete-time and event-queue models)"
repo: JuliaDynamics/Agents.jl
url: https://github.com/JuliaDynamics/Agents.jl
authors: ["George Datseris", "Ali R. Vahdati", "Timothy C. DuBois", "JuliaDynamics contributors"]
year: 2018
language: Julia
license: "MIT"
stars: 918
last_commit: 2026-09-15
topics: [collective-motion, crowds-and-traffic, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 4
papers: [datseris-2022-agents]
---

## Summary

One line: general ABM with any-dimensional grid, continuous, graph and OpenStreetMap spaces, neighbour queries by radius, and either discrete-time stepping or continuous-time event-queue scheduling; the CI benchmark puts it about 59x faster than Mesa on large flocking and 2 to 19x faster than NetLogo; no LLM integration in core; no adversarial hooks beyond custom agent types; light to run once Julia is installed (no Julia on this Mac, so not run).

Maintained by JuliaDynamics. README highlights: short learning curve, thousands of built-in agent actions, OpenStreetMap simulations, event-queue ABMs, and native integration with reinforcement learning. Benchmark and feature claims come from the developers' own comparison repository ([[gh-juliadynamics-abmframeworkscomparison]]) and paper ([[datseris-2022-agents]]).

## What it can do for us

Best performance-per-line of the CPU frameworks in the published comparison, with a continuous space and ODE coupling (DifferentialEquations.jl) that suits Vicsek/Cucker-Smale style models where discretisation error matters. Event-queue scheduling is a ready answer to synchronous-update artefacts ([[huberman-1993-evolutionary]]).

## Run notes

Not run: julia is not installed on this machine (which julia returned nothing). Install would be juliaup plus ] add Agents.

## Limitations

Julia toolchain is a new dependency for a Python-centric lab; LLM calls from Julia agents would need an HTTP client or PythonCall. Performance numbers are self-reported by the developers.

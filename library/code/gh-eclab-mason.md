---
id: gh-eclab-mason
type: code
title: "MASON: Java multi-agent simulation toolkit (GMU ECLab) with discrete-event schedule, 2D/3D fields and GUI"
repo: eclab/mason
url: https://github.com/eclab/mason
authors: ["Sean Luke", "Claudio Cioffi-Revilla", "Liviu Panait", "Keith Sullivan", "Gabriel Balan"]
year: 2003
language: Java
license: "Academic Free License (per Datseris et al. 2022; GitHub reports NOASSERTION)"
stars: 191
last_commit: 2026-07-10
topics: [collective-motion, swarm-robotics, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: []
---

## Summary

One line: general ABM with a discrete-event schedule, grid and continuous 2D/3D fields and network fields, model separate from visualisation; in the JuliaDynamics benchmark it is about 1.4x slower than Agents.jl on small flocking and 1.6x faster on large flocking ([[gh-juliadynamics-abmframeworkscomparison]]); no LLM integration; no adversarial hooks beyond custom Steppable agents; light to run (JVM), but 3D needs Java3D/JOGL, which the README calls hard to install on macOS.

The repository holds core MASON (Maven build) plus contrib extensions such as GeoMason. The README is only build instructions; documentation lives on the GMU site. MASON is the architectural ancestor of [[gh-krabmaga-krabmaga]].

## What it can do for us

A mature, fast JVM option with deterministic checkpointing (Datseris et al. list whole-model checkpoints). Its schedule-plus-Steppable design is the reference for event-ordered simulation, which matters for the update-order artefacts in [[radax-2010-timing]].

## Run notes

Not run. Build: cd mason/mason && mvn clean install.

## Limitations

Datseris et al. ([[datseris-2022-agents]]) rate its API complex (369 lines for flocking versus 62 in Agents.jl in their 2022 table) and its docs hard to navigate. Java-only, so LLM calls or Python analysis tools need a bridge.

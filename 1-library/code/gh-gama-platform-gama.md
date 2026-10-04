---
id: gh-gama-platform-gama
type: code
title: "GAMA: GAML-language platform for spatially explicit (GIS) agent-based simulation with an Eclipse IDE and headless mode"
repo: gama-platform/gama
url: https://github.com/gama-platform/gama
authors: ["GAMA platform team (IRD, UMMISCO and partners)"]
year: 2007
language: Java (models in GAML)
license: "GPL-3.0"
stars: 118
last_commit: 2026-10-03
topics: [crowds-and-traffic, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 2
papers: []
---

## Summary

One line: spatially explicit ABM written in its own modelling language (GAML) with GIS data as first-class environment, grids, graphs and continuous space, an IDE and a headless runner; README gives no throughput numbers; no LLM integration mentioned in the README; no adversarial hooks; heavy to run (Java 21 desktop app, Maven multi-module build from source).

The 2025+ development repository of GAMA. Releases are bundled with a JDK. Strong in urban, traffic, epidemiology and land-use models built on shapefiles.

## What it can do for us

Mainly an idea source for GIS-anchored scenarios (agents on real street networks or terrain). For swarm and LLM-agent work the custom language is a cost with no clear payoff.

## Run notes

Not run. Release download, or build gama.annotations, gama.processor, gama.parent with mvn clean install in order.

## Limitations

GPL-3.0. Separate DSL, Eclipse-based tooling, Java 21 required. Not aimed at large-N flocking.

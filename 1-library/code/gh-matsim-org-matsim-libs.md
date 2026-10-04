---
id: gh-matsim-org-matsim-libs
type: code
title: "MATSim: large-scale agent-based transport simulation toolbox (demand modelling, mobsim, iterative replanning)"
repo: matsim-org/matsim-libs
url: https://github.com/matsim-org/matsim-libs
authors: ["MATSim community"]
year: 2015
language: Java
license: "not stated by GitHub API (no top-level LICENSE detected); check repo"
stars: 647
last_commit: 2026-10-02
topics: [crowds-and-traffic]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: []
---

## Summary

Simulation model: agents with daily activity plans travel on a network; a queue-based mobility simulation executes plans, a scoring function evaluates them, and agents iteratively replan (co-evolutionary) until a relaxed state. Modular contribs for many extensions. Scale: city- to country-scale populations (website claims; not checked here). LLM-native: no. Adversarial hooks: none. Weight: Java/Maven build (mvn package). GitHub repo created 2015; the project is older.

## What it can do for us

Mature, actively maintained large-population ABM with an iterate-score-replan loop; a reference design if our sim needs agents that adapt plans across repeated days.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API; source code not read.

## Limitations

Transport-specific; JVM toolchain; licence not confirmed via API.

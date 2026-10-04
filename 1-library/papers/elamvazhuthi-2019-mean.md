---
id: elamvazhuthi-2019-mean
type: paper
title: "Mean-field models in swarm robotics: a survey"
authors: ["Karthik Elamvazhuthi", "Spring Berman"]
year: 2019
venue: "Bioinspiration & Biomimetics"
url: https://doi.org/10.1088/1748-3190/ab49a4
doi: "10.1088/1748-3190/ab49a4"
arxiv: null
cite: "Elamvazhuthi, K., & Berman, S. (2019). Mean-field models in swarm robotics: a survey. Bioinspiration & Biomimetics, 15(1), 015001."
topics: [swarm-robotics, sync-consensus, active-matter]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "124 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

A survey of fluid (mean-field) approximations used to design and analyse controllers for robot swarms. Mean-field
models in the form of ODEs, PDEs or difference equations, chosen according to whether agent states and time
are discrete or continuous, describe the swarm by densities rather than individuals. They are independent of
the number of agents, so controllers synthesised on them scale, and they are open to dynamical-systems,
control, stochastic-process and PDE analysis with provable guarantees. The survey covers applications to
coverage, task allocation, self-assembly, consensus and environmental mapping.

## Contribution

The best entry point to the micro-macro (agent to density) toolkit in swarm robotics, which connects swarm
engineering to the continuum theories of active matter and to mean-field games and control.

## Key results

- Organises the literature by model class (ODE, PDE, difference equations) and task.
- Claims (review): macroscopic models enable scalable synthesis and provable guarantees that microscopic models
  do not.

## Methods and models

Survey; abstract read. Related primary work: stochastic task allocation via rate equations
([[berman-2009-optimized]]) and microscopic-macroscopic modelling ([[martinoli-2004-modeling]]).

## Limitations and open questions

Mean-field validity at small N and with strong spatial correlations is the standing caveat (not checked in
detail).

## Relevance to us

Core for any hackathon project that wants to analyse or control a swarm at the density level, or to compare
agent-based simulations with continuum predictions. Links to [[yang-2018-mean]] (mean-field RL) and
[[jin-2026-physics]] (density-field control).

---
id: radax-2010-timing
type: paper
title: "Timing matters: Lessons From The CA Literature On Updating"
authors: ["Wolfgang Radax", "Bernhard Rengs"]
year: 2010
venue: "arXiv (cs.MA)"
url: https://arxiv.org/abs/1008.0941
doi: null
arxiv: "1008.0941"
cite: "Radax, W., & Rengs, B. (2010). Timing matters: Lessons From The CA Literature On Updating. arXiv:1008.0941."
topics: [meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "10 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Surveys how cellular-automata research learned that synchronous updating creates artefacts, maps the CA updating regimes (synchronous; ordered asynchronous such as line-by-line sweeps or a fixed random order; random asynchronous with or without replacement; time-driven with exponential waiting times; incentive-based) onto agent activation in ABMs, and tests the effect by re-running Schelling's segregation model and Epstein's Demographic Prisoner's Dilemma under different activation regimes and modes.

## Contribution

Introduces a vocabulary for the problem (activation regime: uniform versus random activation, sync versus async; activation mode: agent-guided, where each agent fires all its rules, versus rule-guided, where all agents fire rule 1, then rule 2) and shows that results become sensitive to these choices as soon as interactions are strong. Notes that platform defaults, not modelling reasons, often decide the regime.

## Key results

- Schelling (100 runs per tolerance value, sampled at t=1000, two movement rules): uniform versus random activation give qualitatively the same results, with small differences only at high tolerance under the Edmonds-Hales local movement rule.
- Demographic Prisoner's Dilemma (Epstein's five settings, 100 runs, sampled after 1000 periods): setting 1 is insensitive; setting 2 differs when run by agent; setting 3 is highly sensitive to activation regime in both modes; in setting 4 any change of regime or mode leads to population extinction in almost all runs. Setting 5 (50% mutation) is noise-dominated.
- Cites Axtell's emergence-of-firms model, where switching from random to uniform activation reversed the dependence between firm growth rate and size, turning a good empirical fit into a bad one.
- NetLogo's ask primitive defaults to uniform activation (random order without replacement each step); Repast did not shuffle by default at the time.

## Methods and models

Literature survey of CA updating plus re-implementations of two classic ABMs run under the four combinations {uniform, random activation} x {by rule, by agent}.

## Limitations and open questions

Short workshop-style paper; only two abstract models; figures carry the quantitative results without statistics; platform survey limited to NetLogo, Repast and Repast Simphony circa 2010. Does not address continuous-space flocking, where synchronous updates are the norm.

## Relevance to us

Any swarm sim we build must make the schedule a declared, switchable parameter and report sensitivity to it. Vectorised frameworks ([[gh-mesa-mesa-frames]], [[gh-flamegpu-flamegpu2]], [[gh-i-m-iron-man-abmax]], JAX) are synchronous by construction while Mesa, AgentPy and Agents.jl default to sequential random activation, so the same model can behave differently across frameworks for this reason alone. For LLM-agent swarms the analogue is whether agents see each other's messages within a round or only the next round. Builds on [[huberman-1993-evolutionary]].

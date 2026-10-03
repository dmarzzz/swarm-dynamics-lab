---
id: sanders-2018-prevalence
type: paper
title: The prevalence of chaotic dynamics in games with many players
authors: [James B. T. Sanders, J. Doyne Farmer, Tobias Galla]
year: 2018
venue: Scientific Reports
url: https://www.nature.com/articles/s41598-018-22013-5
doi: 10.1038/s41598-018-22013-5
arxiv: null
cite: Sanders, J. B. T., Farmer, J. D., & Galla, T. (2018). The prevalence of chaotic dynamics in games with many players. Scientific Reports, 8(1), 4902.
topics: [marl-emergence]
added_by: dmarz/marl-emergence-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "41 (Crossref is-referenced-by-count, 2026-10-03)"
code: []
---

## Summary

Extends [[galla-2013-complex]] from two players to p players. Payoffs of a p-player game with many actions are drawn
at random and fixed; players adapt by experience-weighted attraction learning. Trajectories show unique fixed
points, multiple fixed points, limit cycles and chaos. A generating-functional calculation in the limit of many
actions gives the parameter region where learning converges to a stable fixed point, and that region shrinks to
zero as the number of players goes to infinity.

## Contribution

The key "many agents" result in the statistical physics of learning: with many players, non-convergent (often
chaotic) learning dynamics are the norm, not the exception. It frames convergence of MARL as a property of the
game's parameters, like a Reynolds number for turbulence.

## Key results

- Analytical stability boundary of the unique fixed point from a generating-functional (dynamical mean-field)
  calculation, confirmed by simulation (derived and measured).
- The fixed-point-stable region vanishes as p -> infinity, so complex non-equilibrium behaviour dominates for
  complicated games with many players (derived).

## Methods and models

Random p-player normal-form games with N actions per player and tunable payoff correlations; EWA learning with memory
and intensity-of-choice parameters; dynamical mean-field (generating functional) analysis in the large-N limit,
checked against numerical integration of the learning dynamics. Abstract and introduction read on the
publisher page; analysis sections skimmed.

## Limitations and open questions

Random, unstructured games without space or local interaction, and one learning rule. It is open whether
structured swarm tasks (local, cooperative, homogeneous agents) escape this regime, or whether learned swarms
are typically non-stationary.

## Relevance to us

Directly relevant to any claim that a MARL swarm "converges": with many learners, convergence is not guaranteed and
chaotic learning dynamics are plausible. A measurable question for the hackathon. Related:
[[galla-2013-complex]], [[barfuss-2019-deterministic]], [[yang-2018-mean]].

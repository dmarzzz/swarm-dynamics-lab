---
id: arbel-2024-mechanical
type: paper
title: "A Mechanical Route for Cooperative Transport in Autonomous Robotic Swarms"
authors: ["Eden Arbel", "Luco L. K. M. Buise", "Charlotte C. R. M. M. van Waes", "Naomi Oppenheimer", "Yoav Lahini", "Matan Yah Ben Zion"]
year: 2024
venue: "Nature Communications"
url: https://arxiv.org/abs/2402.05659
doi: "10.1038/s41467-025-61896-7"
arxiv: "2402.05659"
cite: "Arbel, E., Buise, L., van Waes, C., Oppenheimer, N., Lahini, Y., & Ben Zion, M. Y. (2025). A mechanical route for cooperative transport in autonomous robotic swarms. Nature Communications, 16(1), 7519. (Preprint arXiv:2402.05659, 2024.)"
topics: [swarm-robotics, active-matter]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "6 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

Cooperative transport, which ants achieve routinely, is hard for artificial swarms because it needs
synchronisation in a noisy many-body system. Here robots with no sensing or communication are placed
isotropically around a passive circular payload, and the payload nonetheless moves directionally. A small
change in each robot's mechanical design (friction and mass distribution) flips its alignment response to an
external force, and robots with a negative "active charge" spontaneously cooperate. A coarse-grained mechanical
description shows the force-alignment is intrinsic and captured by a signed parameter with units of curvature.

## Contribution

Derives from mechanics the force-alignment parameter that [[ben-zion-2023-morphological]] measured empirically,
and gives an analytic criterion for emergent cooperative transport.

## Key results

- Measured: transport increases with payload size; its persistence exceeds the robots' own persistence by more
  than an order of magnitude.
- Analytic: geometric criterion for cooperative transport from a bifurcation of a nonlinear dynamical system;
  simulations with negative active charge reproduce experiments.

## Methods and models

Self-propelled robots with tunable friction and mass distribution; coarse-grained mechanics; active-particle
simulations. Abstract read on arXiv (preprint; peer-reviewed version not checked).

## Limitations and open questions

Preprint; only circular payloads; no sensing.

## Relevance to us

A sharp, testable mechanism (sign of a single parameter decides cooperation); ideal for a simulation study.

## Notes from dmarz/swarm-robotics-audit

The preprint was published as Arbel et al. (2025), Nature Communications 16, 7519, DOI 10.1038/s41467-025-61896-7 (Crossref, checked). Updated venue, doi, cite and citations. The id keeps the preprint year 2024 so existing [[arbel-2024-mechanical]] links do not break. Content is still abstract-level.

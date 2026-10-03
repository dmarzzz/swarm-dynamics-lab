---
id: sar-2026-interplay
type: paper
title: "Interplay of sync and swarm: Theory and application of swarmalators"
authors: [Gourab Kumar Sar, Kevin O'Keeffe, Joao U. F. Lizarraga, Marcus A. M. de Aguiar, Christian Bettstetter, Dibakar Ghosh]
year: 2026
venue: Physics Reports
url: https://arxiv.org/abs/2510.09819
doi: 10.1016/j.physrep.2026.01.002
arxiv: '2510.09819'
cite: "Sar, G. K., O'Keeffe, K., Lizárraga, J. U. F., de Aguiar, M. A. M., Bettstetter, C., & Ghosh, D. (2026). Interplay of sync and swarm: Theory and application of swarmalators. Physics Reports, 1167, 1-52."
topics: [sync-consensus, active-matter, swarm-robotics, collective-motion]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: "11 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

The comprehensive review of swarmalators (agents that both swarm in space and synchronise an internal phase),
written by the field's main groups. It covers foundations (Kuramoto, pulse-coupled oscillators, Vicsek,
Cucker-Smale, Couzin), early mobile-oscillator models, the 2D swarmalator model and its phenomenology (coupling
functions, forcing, delays, higher harmonics, distributed frequencies, non-Kuramoto internal dynamics, 3D and
higher dimensions), theory (the solvable 1D ring and 2D periodic models, the unsolved "melting point" K_m of the
2D model), predator-swarmalator models, and applications in biology, physics, chemistry and robotics.

## Contribution

The current entry point and reference map for the swarmalator subfield (about 245 references), superseding the
short [[sar-2022-dynamics]]. Its robotics section, written with Bettstetter (who built the first robot
swarmalators, [[barcis-2020-sandsbots]]), lists the engineering changes needed to move the model onto hardware.

## Key results

- Section 4.2 explains why the 2D async-to-active-phase-wave "melting point" K_m is still unsolved: linearising
  around the compactly supported async density gives non-standard eigenvalue equations with Heaviside and delta
  prefactors that nobody has solved; Kuramoto's self-consistency trick is also blocked. Stated as one of the
  field's big open problems.
- Robotics (Section 6.4), as reported by the review: the original model must change from time-continuous global
  coupling to discrete, range-limited coupling; with an Euler step of 0.1 and one state exchange per step, pattern
  formation tolerated more than 90 percent message loss without lowering convergence probability (citing
  Schilcher et al., ACSOS 2021), which motivates sparse "stochastic coupling"; limited interaction range deforms
  or replaces the five canonical states; localisation errors are tolerated within bounds. Robot platforms listed:
  wheeled robots and Crazyflie drones ([[barcis-2020-sandsbots]]), Sphero BOLT robots
  ([[beattie-2025-realizing]]), Crazyflies ([[quinn-2025-decentralised]]), bristle-bots.
- Future directions named: topological (metric-free, k-nearest) neighbourhoods, theory for 3D, non-reciprocal
  swarmalators with topological states, and ML-assisted discovery or RL control of interaction rules that yield
  user-specified space-phase formations.

## Methods and models

Review. Central model is the 2D swarmalator of [[okeeffe-2017-oscillators]]; theoretical tools are linear
stability, Kuramoto self-consistency and Ott-Antonsen-type ansatzes ([[ott-2008-low]], [[yoon-2022-sync]]).
Read: table of contents, Section 4.2 and Sections 6.4 and 7 in full; the phenomenology chapters were skimmed.

## Limitations and open questions

A review by the model's proponents; experimental validation of swarmalator states in natural systems is
qualitative throughout. The robotics numbers are second-hand (from the cited conference papers), not
re-measured here. The authors disclose using ChatGPT for grammar.

## Relevance to us

Start here for any swarmalator-based hackathon project. The robotics section is effectively a checklist for
running swarmalators on drones (discrete messages, range limits, collision margins, localisation). The open
problems (K_m, topological neighbourhoods, learned interaction rules) are candidate hackathon questions, to be
checked against [[ceron-2024-reciprocal]] and [[anwar-2024-collective]] first.

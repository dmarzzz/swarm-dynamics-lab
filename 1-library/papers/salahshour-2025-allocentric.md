---
id: salahshour-2025-allocentric
type: paper
title: "Allocentric flocking"
authors: ["Mohammad Salahshour", "Iain D. Couzin"]
year: 2025
venue: "Nature Communications"
url: https://www.nature.com/articles/s41467-025-64676-5
doi: "10.1038/s41467-025-64676-5"
arxiv: null
cite: "Salahshour, M., & Couzin, I. D. (2025). Allocentric flocking. Nature Communications, 16(1), 9051."
topics: [collective-motion, collective-decision]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "6 (OpenAlex W4415101862, 2026-10-03)"
code: []
---
## Summary

Each agent's movement is set by a ring-attractor network (the neural motif that encodes head direction and goal direction in flies, fish and mammals). Neighbours act as sensory inputs: each excites the neurons whose receptive field points toward it, and the network settles on a bump of activity that becomes the goal direction. Two implementations are studied, a Hopfield-style spin system with Glauber dynamics and an Amari neural field. The key variable is the reference frame: if bearings are encoded egocentrically (relative to current heading), social attraction only produces stationary aggregates; if encoded allocentrically (relative to a world-anchored compass), the population shows a disordered phase, a collective-motion phase with high global and local order, and an aggregation phase as social attraction h_t^s increases. Allocentric flocks show swirling, fission-fusion, flash-expansion-like events and sudden turns without parameter changes. Random fast switching between frames (probability omega of egocentric per step) can increase global order further.

## Contribution

Proposes that alignment need not be an explicit rule: it can emerge from consensus dynamics on navigational circuits if bearings are allocentric. Provides a neurobiologically grounded alternative to SPP models and a mechanistic explanation for the locust result in [[sayin-2025-behavioral]].

## Key results

- Simulation: no collective motion with egocentric encoding in either model (only aggregation; spin model gives local but not global order).
- Simulation: three phases with allocentric encoding; small groups (N = 10) show bistable, discontinuous transitions; larger groups (N = 320) show more continuous transitions with strong fission-fusion.
- Simulation: no density-dependent order transition (unlike Vicsek), matching the locust data claim.
- Simulation (individual): egocentric agents are better at reaching and staying at static targets; allocentric agents track fast-moving targets better; performance peaks in the ordered phase near criticality.
- Simulation: removing recurrent connections (J_ij = 0) collapses agents into a static aggregate.

## Methods and models

Spin model: N_s = 100 spins on a ring, J_ij = cos(pi (|alpha_i - alpha_j|/pi)^nu), Hamiltonian with Gaussian receptive-field inputs h_i, Glauber updates at inverse temperature beta, velocity v = v0/N_s sum over active spins of goal vectors. Neural field: du_i/dt = -u_i + (1/N_s) sum_j J_ij tanh(beta u_j) - h_b + h_i. Periodic arena L = 1000, typically N = 80, beta = 400 (spin) or 1000 (field). Order parameters: global angular order and local topological (k = 5) order. MATLAB code on Code Ocean; data on figshare 10.6084/m9.figshare.28925888.

## Limitations and open questions

No direct fit to animal trajectories in this paper (empirical anchor is the locust study). Assumes agents can steer to the goal and maintain an allocentric compass; how real animals schedule frame switches is unknown. 2D, no explicit collision physics in the base model (repulsion added in SI).

## Relevance to us

A strong, very recent alternative model class for the hackathon: agents with an internal ring attractor instead of alignment rules. Testable prediction: removing allocentric cues (landmarks, sky) should impair flocking. Compare [[heins-2024-collective]], [[sayin-2025-behavioral]], [[li-2025-reverse]] (zebrafish pursuit uses egocentric positional information), and [[couzin-2025-collective]].

## Notes from dmarz/collective-motion-recent-audit

Audited against the Nature Communications full text: N = 10 bistable versus N = 320 continuous transitions confirmed; cite (16, 9051) confirmed. No corrections. citations replaced with the OpenAlex cited_by_count (2026-10-03) in place of the Crossref count.

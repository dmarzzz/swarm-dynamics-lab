---
id: filella-2018-model
type: paper
title: Model of Collective Fish Behavior with Hydrodynamic Interactions
authors: [Audrey Filella, François Nadal, Clément Sire, Eva Kanso, Christophe Eloy]
year: 2018
venue: Physical Review Letters
url: https://arxiv.org/pdf/1705.07821
doi: 10.1103/PhysRevLett.120.198101
arxiv: '1705.07821'
cite: 'Filella, A., Nadal, F., Sire, C., Kanso, E., & Eloy, C. (2018). Model of collective fish behavior with hydrodynamic interactions. Physical Review Letters, 120(19), 198101.'
topics: [collective-motion, active-matter]
added_by: dmarz/collective-motion-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "159 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Adds far-field hydrodynamic interactions to a data-driven 2D fish-school model. Each fish is a
self-propelled point that is attracted to and aligns with its Voronoi neighbours, weighted by
(1 + cos theta) to mimic a rear blind angle, with rotational noise, following attraction-alignment rules inferred from
shallow-water fish tracking (their refs. 19-21; compare [[gautrais-2012-deciphering]],
[[calovi-2014-swarming]]). On top, every fish creates a
potential-flow dipole, which advects and rotates its neighbours. Without flow the model gives the known
swarming, schooling and milling phases; with flow a new "turning" phase appears, fish swim faster on average,
and the flow acts as extra behavioural noise. Read: abstract, full main text and figure captions of the
arXiv v4 (posted 3 May 2018, after acceptance); supplement not read.

## Contribution

One of the first collective-motion models to couple behavioural rules with fluid-mediated physical
interactions at fish scale (high Reynolds number), in contrast to low-Reynolds active-matter models. It
argues that "dry" behavioural models such as [[couzin-2002-collective]] miss a qualitative phase.

## Key results

- Dimensionless parameters: alignment I_k = k_v sqrt(v/k_p), noise I_n = sigma (v k_p)^(-1/4), dipole
  I_f = S k_p / v. For 10 cm fish (r_0 = 5 cm), v about 0.2 m/s and k_p = 0.41 m^-1 s^-1, I_f is about
  0.016; simulations use I_f = 10^-2.
- Phases classified by polarization P and milling M (thresholds P = 0.5, M = 0.4): schooling for
  I_k >~ 2; milling for I_k <~ 2 and I_n <~ 0.5; swarming otherwise (no-flow case reproduces the earlier
  data-driven phase diagram).
- Flow drift alone (U_i, no induced rotation) leaves the phase diagram practically unchanged but raises the
  mean speed V slightly above 1.
- Full model (drift plus rotation): new turning phase (P > 0.5 and M > 0.4) for I_n <~ 0.25 and
  3 <~ I_k <~ 5, where the polarized group follows a large quasi-circular path; some individuals reach
  |dr/dt| = 2.5.
- Flow-induced rotations act like additional noise (claimed from the phase-boundary shifts).

## Methods and models

dr_i/dt = e_i + U_i; dtheta_i/dt = <rho_ij sin(theta_ij) + I_k sin(phi_ij)> + I_n eta + Omega_i, average
over Voronoi neighbours with weight (1 + cos theta_ij); U_i is the sum of dipole velocities
u_ji = (I_f / pi rho_ij^2)(e_theta_j sin theta_ji + e_j cos theta_ji); Omega_i from velocity gradients along
the body. N = 100, explicit scheme with dt = 10^-2, 100 time units transient, averages over 100 time
units and 100 realizations. Wake vorticity is neglected (potential flow).

## Limitations and open questions

- Far-field dipoles only: no wake vortices, no near-field effects, which matter for energy saving in
  formations (see [[ko-2023-role]]).
- 2D, point-like swimmers, constant speed relative to the flow; fish do not respond behaviourally to flow.
- Not compared with experimental trajectories beyond inheriting the behavioural rules.

## Relevance to us

A template for adding a physical medium to an agent-based swarm: the same behavioural rules can give new
collective states once agents are coupled through an environment. Relevant to underwater or aerial robot
swarms where wakes couple agents. Related: [[ko-2023-role]], [[wang-2025-collective]],
[[huang-2024-collective]], [[lopez-2012-behavioural]].

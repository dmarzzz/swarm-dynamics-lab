---
id: verma-2018-efficient
type: paper
title: Efficient collective swimming by harnessing vortices through deep reinforcement learning
authors: [Siddhartha Verma, Guido Novati, Petros Koumoutsakos]
year: 2018
venue: Proceedings of the National Academy of Sciences
url: https://arxiv.org/abs/1802.02674
doi: 10.1073/pnas.1800923115
arxiv: '1802.02674'
cite: Verma, S., Novati, G., & Koumoutsakos, P. (2018). Efficient collective swimming by harnessing vortices through deep reinforcement learning. Proceedings of the National Academy of Sciences, 115(23), 5849–5854.
topics: [marl-emergence, collective-motion, swarm-robotics]
added_by: dmarz/marl-emergence
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "439 (Crossref is-referenced-by-count, 2026-10-03); 414 (OpenCitations, 2026-10-03)"
code: []
---

## Summary

Whether schooling saves fish energy through hydrodynamics has been argued since Weihs (1973) without a
mechanism. The authors couple deep RL (a recurrent DQN) to direct numerical simulation of the Navier-Stokes
equations for self-propelled zebrafish-shaped swimmers at Re about 5000. A follower behind a steadily swimming
leader learns to modulate its body curvature. When rewarded for swimming efficiency alone, it learns to sit in
the centre of the leader's wake at about 2.2 or 1.5 body lengths behind and to synchronise its head motion with
the wake's lateral velocity, intercepting shed vortices; this raises its efficiency by 32% over an identical
solitary swimmer at no cost to the leader. A 3D extension with a PI controller places two followers on the
diverging wake branches and yields a 7.4% group efficiency gain.

## Contribution

First combination of deep RL with high-fidelity flow simulation for collective locomotion, and a mechanistic
answer (vortex interception plus "lifted vortex" interactions along the midsection) to the fish-schooling
energetics question. It sits between the classic theoretical channelling and drag-reduction arguments and
experimental trout-in-vortex-street work (Liao et al. 2003); it extends Gazzola et al. (2016) "Learning to school
in the presence of hydrodynamic interactions".

## Key results

- Efficiency-rewarded follower (IS_eta) versus solitary swimmer with identical actions (SS_eta), over 10
  tail-beat periods: +11% mean speed, +32% mean swimming efficiency, -36% cost of transport, -29% deformation
  power, +53% thrust power (measured in simulation).
- Without any positional reward, IS_eta settles at Delta y ~ 0 and Delta x ~ 2.2 L, with a second stable point at
  1.5 L; the 0.7 L difference equals the wake's vortex spacing (measured).
- A follower rewarded only for staying on the leader's line (R = 1 - |Delta y|/L) holds position but spends more
  energy through aggressive turns.
- The policy, trained with a steady leader, still extracts benefit behind an erratic leader without retraining.
- 3D, three swimmers, PI-controlled followers at positions chosen using the 2D insight: +11% efficiency and -5%
  cost of transport per follower; +7.4% group efficiency versus three isolated swimmers.
- Mechanism: the main energy gain is from reduced deformation power near the midsection (0.4 to 0.7 L), in areas
  of high relative velocity, contrary to earlier drag-reduction explanations.

## Methods and models

2D: wavelet-adapted remeshed vortex methods; 3D: finite differences with pressure projection. Swimmer midline
curvature k(s,t) = A(s) sin(2 pi t / Tp - 2 pi s / L) with A rising linearly 0.82 to 5.7; actions superimpose a
spline perturbation with amplitude in {0, +-0.25, +-0.5}, chosen every half tail-beat. Observed state: Delta x,
Delta y, orientation theta, last two actions, tail-beat phase. Episodes end with reward -1 if the follower leaves
1 <= Delta x/L <= 3, |Delta y| <= L, |theta| <= pi/2. Q approximated by a 3-layer, 24-cell LSTM; asynchronous
recurrent DQN with target network (soft update 1e-4), Adam, epsilon annealed 1 to 0.1, gamma = 0.9; many
simulations run in parallel feeding a central learner. Single learning agent with a scripted leader: this is
single-agent RL in a multi-body environment, not concurrent MARL.

## Limitations and open questions

Two swimmers in 2D, one learner; the 3D result uses a hand-designed controller, not RL. The leader never adapts,
so this is not a test of mutual adaptation or of school-level emergence. Computational cost is extreme (supercomputer
allocations), so the approach does not scale to large schools. Real fish sense flow through the lateral line,
whereas the agent is given exact relative position.

## Relevance to us

The flagship physics example that RL can discover physically grounded coordination that hand-written rules
missed. For a hackathon, its flow solver is too expensive, but the framing (reward energy, observe what formation
emerges) transfers to cheap surrogate hydrodynamics or to drone downwash. Related: [[durve-2020-learning]]
(cohesion reward yields alignment), [[huttenrauch-2019-deep]], and the active-matter RL review [[cai-2025-reinforcement]].

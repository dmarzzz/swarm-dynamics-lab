---
id: viragh-2014-flocking
type: paper
title: "Flocking algorithm for autonomous flying robots"
authors: ["Csaba Virágh", "Gábor Vásárhelyi", "Norbert Tarcai", "Tamás Szörényi", "Gergő Somorjai", "Tamás Nepusz", "Tamás Vicsek"]
year: 2014
venue: "Bioinspiration & Biomimetics"
url: https://arxiv.org/abs/1310.3601
doi: "10.1088/1748-3182/9/2/025012"
arxiv: "1310.3601"
cite: "Virágh, C., Vásárhelyi, G., Tarcai, N., Szörényi, T., Somorjai, G., Nepusz, T., & Vicsek, T. (2014). Flocking algorithm for autonomous flying robots. Bioinspiration & Biomimetics, 9(2), 025012."
topics: [swarm-robotics, collective-motion]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "208 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Before the 30-drone flock of [[vasarhelyi-2018-optimized]], this paper built the realistic robot model and
first decentralised algorithms. It defines a generic flying-robot model with six deficiencies: inertia
(exponential relaxation to the desired velocity with time tau_CTRL and bounded acceleration a_max), sensor noise
(a Langevin process for GPS error), finite sensor refresh rate, finite communication range r_c, communication
delay t_del, and outer acceleration noise. It then shows that Reynolds-type flocking (repulsion plus alignment
inside a bounded arena) and a collective target-tracking algorithm become unstable under delay and noise unless
a viscous-friction-like alignment term damps the oscillations, and tests both on a small group of quadcopters.

## Contribution

It made delays and robot imperfections first-class parts of a flocking model and identified velocity damping
(alignment as friction) as the stabilising ingredient, which later became the braking-curve alignment of
[[vasarhelyi-2018-optimized]].

## Key results

- Simulated: the friction-like alignment term substantially reduces delay- and noise-induced oscillations;
  without it flocks oscillate and collide (qualitative, from the stability plots).
- Fixed model values representative of their quadcopters: t_s = 0.2 s, tau_CTRL = 1 s, a_max = 6 m/s^2.
- Real flights with a small group of quadcopters demonstrate both algorithms (details in the paper; I skimmed).

## Methods and models

Desired velocity as a function of delayed, noisy neighbour positions and velocities, integrated with
Euler-Maruyama; pairwise local terms gated by a Heaviside function of distance versus r_c. Quadcopters with
onboard computers, GPS and radio modules. The later simulation framework is at
https://github.com/csviragh/robotsim.

## Limitations and open questions

Small flight experiments; parameters hand-tuned; no formal stability analysis. Velocity scalability was
limited (later fixed by the braking-curve alignment).

## Relevance to us

The robot-imperfection model here is a compact, reusable recipe for making a simulated swarm realistic
(delay, refresh, range, noise, inertia). See [[vasarhelyi-2014-outdoor]] and [[vasarhelyi-2018-optimized]].

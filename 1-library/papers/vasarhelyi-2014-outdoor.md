---
id: vasarhelyi-2014-outdoor
type: paper
title: "Outdoor flocking and formation flight with autonomous aerial robots"
authors: ["Gábor Vásárhelyi", "Csaba Virágh", "Gergő Somorjai", "Norbert Tarcai", "Tamás Szörényi", "Tamás Nepusz", "Tamás Vicsek"]
year: 2014
venue: "2014 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)"
url: https://arxiv.org/abs/1402.3588
doi: "10.1109/iros.2014.6943105"
arxiv: "1402.3588"
cite: "Vásárhelyi, G., Virágh, C., Somorjai, G., Tarcai, N., Szörényi, T., Nepusz, T., & Vicsek, T. (2014). Outdoor flocking and formation flight with autonomous aerial robots. 2014 IEEE/RSJ International Conference on Intelligent Robots and Systems, 3866–3873."
topics: [swarm-robotics, collective-motion]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "292 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

The first decentralised multicopter flock flying stable autonomous outdoor flights with up to 10 drones. Each
drone computes its own control on board from GPS positions broadcast locally by neighbours; there is no central
processing. Using the bio-inspired, statistical-physics-derived control framework of [[viragh-2014-flocking]],
optimised for noise, wind and delay, they demonstrate self-propelled flocking in a bounded area with
self-organised obstacle avoidance and collective target tracking with formations (grid, rotating ring, line).
Realistic simulations suggest the local broadcast scheme scales to larger flocks.

## Contribution

Experimental milestone: moved flocking models from indoor motion-capture setups to real outdoor decentralised
flight, the stepping stone to [[vasarhelyi-2018-optimized]].

## Key results

- Measured: stable outdoor flights with up to 10 autonomous quadcopters; flocking with obstacle avoidance and
  three formation types.
- Claimed from simulation: scalability to much larger flocks.
- Per the 2018 follow-up, this system was oscillatory and limited to about 4 m/s because acceleration limits
  were not treated properly.

## Methods and models

GPS-based positioning, local radio broadcast, onboard computation; repulsion, friction-like alignment and
virtual walls; formation via target tracking. I read only the abstract on arXiv.

## Limitations and open questions

Small N, low speed, parameters hand-tuned; relies on GNSS and radio, so not sensor-local.

## Relevance to us

Historical baseline for outdoor flocking and a useful reference point for how much the 2018 braking-curve
alignment improved things.

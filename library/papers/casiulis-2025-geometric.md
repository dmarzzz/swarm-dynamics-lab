---
id: casiulis-2025-geometric
type: paper
title: "A geometric condition for robot-swarm cohesion and cluster–flock transition"
authors: ["Mathias Casiulis", "Eden Arbel", "Charlotte van Waes", "Yoav Lahini", "Stefano Martiniani", "Naomi Oppenheimer", "Matan Yah Ben Zion"]
year: 2025
venue: "Proceedings of the National Academy of Sciences"
url: https://arxiv.org/html/2409.04618
doi: "10.1073/pnas.2502211122"
arxiv: "2409.04618"
cite: "Casiulis, M., Arbel, E., van Waes, C., Lahini, Y., Martiniani, S., Oppenheimer, N., & Ben Zion, M. Y. (2025). A geometric condition for robot-swarm cohesion and cluster–flock transition. Proceedings of the National Academy of Sciences, 122(37), e2502211122."
topics: [collective-motion, swarm-robotics, active-matter]
added_by: dmarz/collective-motion-recent-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "10 (OpenAlex W4414052664, 2026-10-03)"
code: []
---

## Summary

Self-propelled particles that rotate under an external force have a signed, intrinsic parameter with units of curvature, the curvity kappa, which sets whether the body turns toward or away from an applied force. Using vibration-driven robots and simulations, the authors show that a pair of particles of radius b sticks together when kappa + 1/b < 0, a purely geometric criterion independent of speeds and force magnitudes. In many-body Langevin simulations (N = 8192) varying curvity and packing fraction produces three steady states: flocks (positive curvity, collision-induced alignment), an active fluid with motility-induced phase separation, and self-limiting clusters of controlled size for sufficiently negative curvity.

## Contribution

Shows that the collective state of a robot swarm (flock versus cohesive clusters) can be programmed purely through body geometry and mechanics, without sensing, communication or computation, and gives a first-principles design rule for it.

## Key results

- Analytic and experimental: pair cohesion when kappa + 1/b < 0 (Eq. 1), independent of kinematics and force magnitude.
- Simulation: phase diagram over 1,500 combinations of curvity (-1 < kappa b < 0.5) and filling fraction at zero noise, with flock, MIPS fluid and cluster phases; cluster size controlled by curvity.
- Experiment: curvity measured for individual robots from their reorientation under force; pair cohesion matches the criterion.

## Methods and models

Vibration-driven robots with two soft front legs and a stiff back leg, displaced centre of mass; overhead imaging, position and orientation tracking; curvity measured from response to known forces. Overdamped Langevin simulations of N = 8192 active discs with harmonic repulsion (k = 100, mu F0/v0 = 1), Péclet number as noise control.

## Limitations and open questions

Read at skim depth (abstract, introduction, main result and simulation setup). Experiments are with small numbers of robots in a confined arena; the flocking phase relies on collision-induced alignment and is only shown at high density.

## Relevance to us

Embodied alignment: flocking that emerges from contact mechanics rather than any rule, a strong baseline for our 'is alignment necessary' theme along with [[das-2024-flocking]] (flocking by turning away) and the active-matter review [[gompper-2025-motile]]. Directly usable for a cheap physical swarm demo.

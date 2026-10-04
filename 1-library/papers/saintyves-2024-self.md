---
id: saintyves-2024-self
type: paper
title: "A self-organizing robotic aggregate using solid and liquid-like collective states"
authors: ["Baudouin Saintyves", "Matthew Spenko", "Heinrich M. Jaeger"]
year: 2024
venue: "Science Robotics"
url: https://arxiv.org/abs/2304.03125
doi: "10.1126/scirobotics.adh4130"
arxiv: "2304.03125"
cite: "Saintyves, B., Spenko, M., & Jaeger, H. M. (2024). A self-organizing robotic aggregate using solid and liquid-like collective states. Science Robotics, 9(86), eadh4130."
topics: ["swarm-robotics", "active-matter"]
added_by: dmarz/swarm-robotics-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "57 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

The Granulobot is a gear-like, two-wheeled robotic unit (62 mm wide, 48 mm wheels) with one geared DC motor
driving a rotor magnet and a second, freely rotating magnet. Units can roll alone, dock magnetically into
aggregates, and split off again. Magnetic contacts give gear-like, no-slip coupling, while non-magnetic
contacts can slide. Because each unit's speed responds to load like a yield-stress material, an aggregate can
sit in a jammed, solid-like state or, with suitable voltage biases, flow like a liquid. Coupled through
inertia and contact, closed and open chains self-oscillate into limit-cycle gaits that move the aggregate and
let it climb obstacles, with no sensors, coordinates or electronic communication between units.

## Contribution

Blurs modular, soft and swarm robotics: collective states (solid versus liquid) are the control variable,
in the same robophysics line as [[li-2019-particle]], [[savoie-2019-robot]], [[li-2021-programming]] and the
later [[devlin-2025-material]].

## Key results

- Measured: single-unit speed-torque curves are linear above a yield threshold, so units act as
  Bingham-like elements; aggregates show a rate-dependent effective viscosity.
- Measured: closed-chain (N = 6) and open-chain (N = 8) aggregates reach self-oscillating limit cycles after one
  unit is switched off, giving steady gaits; N = 10 aggregates characterised by power spectra versus voltage.
- Demonstrated: an N = 8 liquid-like gait (phase-shifted voltage biases) moves over an obstacle.

## Methods and models

3D-printed units, N20 Pololu geared DC motor, neodymium magnets, battery-powered custom electronics. Torque
balance model per unit: rotor speed set by applied voltage u, load torque and motor constant; aggregate
dynamics from magnetic gear coupling. Tensile tests at 1 mm/s. Code repository not found in the text read.

## Limitations and open questions

Small aggregates (N up to about 10); gaits partly come from hand-chosen voltage patterns rather than full
self-organisation; no large-N statistics. Read: arXiv v2, results and methods skimmed.

## Relevance to us

A physical example of switching a collective between solid and fluid states as a control strategy. A
hackathon simulation could explore jamming versus flow transitions in coupled rotor chains. Compare with
[[baconnier-2022-selective]] (active solids) and [[veenstra-2025-adaptive]].

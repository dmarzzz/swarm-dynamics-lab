---
id: turgut-2008-self
type: paper
title: "Self-organized flocking in mobile robot swarms"
authors: ["Ali E. Turgut", "Hande Çelikkanat", "Fatih Gökçe", "Erol Şahin"]
year: 2008
venue: "Swarm Intelligence"
url: https://doi.org/10.1007/s11721-008-0016-2
doi: "10.1007/s11721-008-0016-2"
arxiv: null
cite: "Turgut, A. E., Çelikkanat, H., Gökçe, F., & Şahin, E. (2008). Self-organized flocking in mobile robot swarms. Swarm Intelligence, 2(2-4), 97–120."
topics: [swarm-robotics, collective-motion]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "280 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

Introduces the Kobot platform and a "virtual heading system" (digital compass plus wireless messages) so each
robot can sense neighbours' headings, then implements Vicsek-like flocking with heading alignment plus proximal
control (short-range attraction/repulsion from infrared sensing). The behaviour produces coherent group motion
with obstacle avoidance in a small group of physical robots and in 1000 simulated robots. They propose flocking
quality metrics and run sensitivity analyses on heading noise, number of neighbours used and communication
range.

## Contribution

One of the first demonstrations of self-organised flocking on ground robots grounded explicitly in
statistical-physics flocking models, with systematic parameter analysis.

## Key results

- Measured/simulated: communication range is the main factor setting the maximum number of robots that can
  flock together; the behaviour is robust to heading noise and the number of neighbours.
- Flocking in a small physical group (closed arena) and 1000 simulated robots (open space).

## Methods and models

Kobot robots, IR proximity, compass-based heading broadcast; alignment plus proximal control; metrics of order
and cohesion. Abstract read.

## Limitations and open questions

Relies on a compass and radio to obtain headings (not purely local sensing). Results are discussed in light of
statistical physics, but no phase diagram is measured.

## Relevance to us

A ground-robot counterpart to [[vasarhelyi-2018-optimized]]; its "range limits group size" finding is a simple
testable scaling claim. Successor: [[ferrante-2012-self]].

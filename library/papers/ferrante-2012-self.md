---
id: ferrante-2012-self
type: paper
title: "Self-organized flocking with a mobile robot swarm: a novel motion control method"
authors: ["Eliseo Ferrante", "Ali Emre Turgut", "Cristián Huepe", "Alessandro Stranieri", "Carlo Pinciroli", "Marco Dorigo"]
year: 2012
venue: "Adaptive Behavior"
url: https://api.crossref.org/works/10.1177/1059712312462248
doi: "10.1177/1059712312462248"
arxiv: null
cite: "Ferrante, E., Turgut, A. E., Huepe, C., Stranieri, A., Pinciroli, C., & Dorigo, M. (2012). Self-organized flocking with a mobile robot swarm: a novel motion control method. Adaptive Behavior, 20(6), 460–477."
topics: [swarm-robotics, collective-motion]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "171 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

Robot flocking is usually built from proximal control (stay at a preferred distance) plus explicit alignment
(match neighbours' headings). This paper proposes a different motion control method that maps the combined
proximal and alignment vector to the robot's forward and angular velocities in a way that can produce flocking
without explicit heading alignment, relying on the robots' own motion and proximal interactions, and tests it on
foot-bot robots and in simulation.

## Contribution

Shows that the motion-control mapping (how a desired vector becomes wheel commands) is itself a design lever
for collective motion, an early hint of the "morphology/embodiment matters" theme later made precise in
self-aligning active matter ([[ben-zion-2023-morphological]]).

## Key results

- Flocking achieved with the new motion control on real robots and in simulation (from abstract; numbers not
  checked).

## Methods and models

Foot-bots, ARGoS simulator. Abstract read via Crossref.

## Limitations and open questions

Not checked beyond abstract.

## Relevance to us

Relevant to experiments on minimal flocking rules; compare [[turgut-2008-self]] and [[mezey-2025-purely]].

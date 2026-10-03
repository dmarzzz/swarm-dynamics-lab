---
id: karaguzel-2023-collective
type: paper
title: "Collective gradient perception with a flying robot swarm"
authors: ["Tugay Alperen Karagüzel", "Ali Emre Turgut", "A. E. Eiben", "Eliseo Ferrante"]
year: 2023
venue: "Swarm Intelligence"
url: https://doi.org/10.1007/s11721-022-00220-1
doi: "10.1007/s11721-022-00220-1"
arxiv: null
cite: "Karagüzel, T. A., Turgut, A. E., Eiben, A. E., & Ferrante, E. (2023). Collective gradient perception with a flying robot swarm. Swarm Intelligence, 17(1-2), 117–146."
topics: ["swarm-robotics", "collective-motion", "collective-decision"]
added_by: dmarz/swarm-robotics-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "18 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

How can a swarm follow the gradient of a scalar field (light, temperature, pollutant) when no individual can
sense the gradient? The authors propose two social mechanisms: each drone modulates either its desired
distance to neighbours or its own speed according to the local scalar value, with or without velocity
alignment. They test these in a kinematic simulator, a physics-based simulator and on real nano-drones,
across field shapes, swarm sizes and densities. Both mechanisms let the swarm climb the gradient; distance
modulation works without alignment (alignment still helps), while speed modulation needs alignment to keep
collective motion. Published online 2022, in the 2023 volume.

## Contribution

A robotic realisation of emergent collective sensing (the group perceives a gradient that no individual
can), carried through to real flying robots. It links the collective-decision and collective-motion topics.

## Key results

- Both proposed methods achieve gradient following without individual gradient sensing (from abstract).
- Alignment is unnecessary for distance modulation but necessary for speed modulation (from abstract).
- Real nano-drone experiments confirm feasibility (sizes and numbers not checked).

## Methods and models

Self-propelled flocking agents with modulated pairwise desired distance or speed; two metrics of gradient
following; three test environments including a real nano-drone swarm (platform and numbers not checked).

## Limitations and open questions

Abstract-level entry: the full text (Springer open access) was blocked to automated download in this session.
Quantitative performance and swarm sizes still need to be read.

## Relevance to us

A clean, simulable hackathon task: a swarm of "blind" agents finding a gradient through interactions alone.
It extends the delay-aware flocking of [[vasarhelyi-2018-optimized]] and the self-organised flocking of
[[ferrante-2012-self]] toward collective perception, and connects to the best-of-n framing in
[[valentini-2017-best]].

---
id: berlinger-2021-implicit
type: paper
title: "Implicit coordination for 3D underwater collective behaviors in a fish-inspired robot swarm"
authors: ["Florian Berlinger", "Melvin Gauci", "Radhika Nagpal"]
year: 2021
venue: "Science Robotics"
url: https://doi.org/10.1126/scirobotics.abd8668
doi: "10.1126/scirobotics.abd8668"
arxiv: null
cite: "Berlinger, F., Gauci, M., & Nagpal, R. (2021). Implicit coordination for 3D underwater collective behaviors in a fish-inspired robot swarm. Science Robotics, 6(50), eabd8668."
topics: [swarm-robotics, collective-motion, sync-consensus]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "341 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

Blueswarm is a swarm of fish-inspired miniature underwater robots that coordinate in 3D using only implicit,
vision-based cues: each robot emits blue LED light and senses neighbours' light with cameras, without radio or
central control. Building on evidence that fish school from visual observation of neighbours, the robots show
synchrony (firefly-like flash synchronisation), dispersion and aggregation, dynamic circle formation (milling)
and a search-and-capture task, from minimal, noisy impressions of neighbours.

## Contribution

The first demonstration of complex 3D collective behaviours in an underwater robot swarm with implicit, local
visual coordination only, closing the gap between fish-school models and robot collectives.

## Key results

- Demonstrated behaviours: synchrony, dispersion/aggregation, dynamic circle formation, search-capture (from
  abstract; numbers not checked).

## Methods and models

Fish-inspired miniature underwater robots that produce and sense blue light; behaviours are local rules on
perceived neighbour impressions. Abstract read; hardware details not checked.

## Limitations and open questions

Small swarm in a tank; perception limited by occlusion and water turbidity.

## Relevance to us

A key example of vision-only, communication-free coordination; pair with [[mezey-2025-purely]] (ground robots)
and the synchronisation topic ([[mirollo-1990-synchronization]] for pulse-coupled sync).

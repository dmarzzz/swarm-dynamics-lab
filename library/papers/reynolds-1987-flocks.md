---
id: reynolds-1987-flocks
type: paper
title: 'Flocks, herds and schools: A distributed behavioral model'
authors: [Craig W. Reynolds]
year: 1987
venue: 'ACM SIGGRAPH Computer Graphics (SIGGRAPH ''87 Proceedings)'
url: https://www.red3d.com/cwr/papers/1987/boids.html
doi: 10.1145/37402.37406
arxiv: null
cite: 'Reynolds, C. W. (1987). Flocks, herds and schools: A distributed behavioral model. ACM SIGGRAPH Computer Graphics, 21(4), 25–34.'
topics: [collective-motion, swarm-robotics]
added_by: dmarz/collective-motion
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "4663 (Crossref is-referenced-by-count, 2026-10-03)"
code: []
---

## Summary

The "boids" paper. For computer animation, a flock is simulated as a particle system in which each bird is
an independent actor steering by local perception of its neighbours and environment, simulated flight
physics and a small set of programmed behaviours; flock-level motion emerges from these local interactions
instead of scripted paths. The three behaviours that became standard are collision avoidance (separation),
velocity matching (alignment) and flock centering (cohesion). Read: the author's abstract page (abstract,
keywords and citation).

## Contribution

Origin of the separation/alignment/cohesion rule set used in computer graphics, robotics and most later
zonal models ([[aoki-1982-simulation]] is an earlier, independent fish-schooling version;
[[couzin-2002-collective]] formalises the zones).

## Key results

- Qualitative demonstration (animation), no quantitative analysis; the abstract states aggregate motion
  results from dense interaction of simple individual behaviours.

## Methods and models

Agent-based steering simulation in 3D with local perception; each boid combines prioritised steering
behaviours.

## Limitations and open questions

Abstract-level read. Rules were designed for visual plausibility, not fitted to animal data.

## Relevance to us

The most familiar baseline for any agent swarm demo; boids variants are the easiest way to show emergent
flocking in a hackathon UI. Compare with [[vicsek-1995-novel]] (alignment only).

---
id: van-den-berg-2011-reciprocal
type: paper
title: Reciprocal n-Body Collision Avoidance
authors:
- Jur van den Berg
- Stephen J. Guy
- Ming Lin
- Dinesh Manocha
year: 2011
venue: Springer Tracts in Advanced Robotics (Robotics Research)
url: https://gamma.cs.unc.edu/ORCA/publications/ORCA.pdf
doi: 10.1007/978-3-642-19457-3_1
arxiv: null
cite: van den Berg, J., Guy, S. J., Lin, M., & Manocha, D. (2011). Reciprocal n-body collision avoidance. In Robotics Research (Springer Tracts in Advanced Robotics), 3–19. Springer. https://doi.org/10.1007/978-3-642-19457-3_1
topics:
- crowds-and-traffic
- swarm-robotics
added_by: dmarz/crowds-and-traffic
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 1313 (Crossref, 2026-10-03)
code: []
---

## Summary

Introduces optimal reciprocal collision avoidance (ORCA) for many agents: each agent computes, for every neighbour, a half-plane of velocities that guarantees collision-free motion for a time horizon if both agents take half the responsibility, and then picks the velocity closest to its preferred one inside the intersection of half-planes by solving a low-dimensional linear program. It is decentralised, needs no communication, and scales to thousands of agents in real time.

## Contribution

The robotics and graphics standard for multi-agent collision avoidance and crowd simulation (RVO2 library), an anticipatory, velocity-space alternative to force-based crowd models.

## Key results

- Claimed (abstract and intro): sufficient conditions for collision-free motion under reciprocity; efficient linear-programming solution; real-time simulation of thousands of agents.

## Methods and models

Velocity obstacles, reciprocal half-planes, 2D linear programming. Book chapter in Springer Tracts in Advanced Robotics. PDF opened from the authors' site; the RVO2 library is distributed from the UNC GAMMA group (not checked in this session).

## Limitations and open questions

Assumes all agents run ORCA; holonomic agents; can produce oscillations or deadlocks in dense, symmetric scenes. Abstract-level read.

## Relevance to us

The default collision-avoidance layer for robot swarms and a strong baseline when comparing to human-derived rules ([[karamouzas-2014-universal]] shares an author lineage, S. J. Guy). Candidate code entry for the code scan task.

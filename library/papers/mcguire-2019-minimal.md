---
id: mcguire-2019-minimal
type: paper
title: "Minimal navigation solution for a swarm of tiny flying robots to explore an unknown environment"
authors: ["K. N. McGuire", "C. De Wagter", "K. Tuyls", "H. J. Kappen", "G. C. H. E. de Croon"]
year: 2019
venue: "Science Robotics"
url: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1126/scirobotics.aaw9710?fields=title,abstract
doi: "10.1126/scirobotics.aaw9710"
arxiv: null
cite: "McGuire, K. N., De Wagter, C., Tuyls, K., Kappen, H. J., & de Croon, G. C. H. E. (2019). Minimal navigation solution for a swarm of tiny flying robots to explore an unknown environment. Science Robotics, 4(35), eaaw9710."
topics: [swarm-robotics, swarm-intelligence]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "273 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

Introduces the swarm gradient bug algorithm (SGBA), a minimal navigation strategy that lets a swarm of 33 g
off-the-shelf nano-quadrotors explore an unknown, GPS-denied indoor environment and return home without SLAM.
Robots fly off in different directions to maximise coverage, handle obstacles by wall-following with visual
odometry, communicate with each other to avoid collisions and spread out, and return by gradient search on the
signal strength of a home beacon. A proof-of-concept search-and-rescue mission finds "victims" in an office.

## Contribution

Shows that a bug-algorithm-level navigation stack, coordinated by minimal inter-robot communication, suffices for
useful swarm exploration on extremely resource-limited robots.

## Key results

- Demonstrated with real 33 g quadrotors in an office environment (abstract); coverage numbers not checked.

## Methods and models

33 g commercial quadrotors; visual odometry, wall-following, inter-robot communication, gradient search to a
home beacon. Abstract read.

## Limitations and open questions

Exploration efficiency versus SLAM-based methods not quantified here.

## Relevance to us

Example of minimal-sensing collective behaviour in flying robots; see [[zhou-2022-swarm]] for the
compute-heavy alternative.

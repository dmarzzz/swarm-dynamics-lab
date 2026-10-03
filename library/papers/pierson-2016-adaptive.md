---
id: pierson-2016-adaptive
type: paper
title: "Adaptive Inter-Robot Trust for Robust Multi-Robot Sensor Coverage"
authors: ["Alyssa Pierson", "Mac Schwager"]
year: 2016
venue: "Robotics Research (ISRR 2013), Springer Tracts in Advanced Robotics, vol. 114"
url: https://sites.bu.edu/msl/files/2013/12/PiersonISRR13AdaptiveTrust.pdf
doi: "10.1007/978-3-319-28872-7_10"
arxiv: null
cite: "Pierson, A., & Schwager, M. (2016). Adaptive Inter-Robot Trust for Robust Multi-Robot Sensor Coverage. In M. Inaba & P. Corke (Eds.), Robotics Research, Springer Tracts in Advanced Robotics, vol. 114, 167-183. Springer, Cham."
topics: [sybil-resistance, swarm-robotics]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "23 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Robots doing Voronoi coverage adapt a trust weighting for each teammate online by comparing their own sensor readings with neighbours'. Trust weights set the power-diagram (weighted Voronoi) cells, so robots with better sensors take larger regions and degraded robots shrink. A Lyapunov argument shows convergence to locally optimal positions that are as good as if sensor qualities were known in advance; demonstrated in Matlab simulations.

## Contribution

Early robotics formulation of trust as a continuous, learned weight folded into the controller rather than a binary accept/reject decision.

## Key results

- Lyapunov-type proof of convergence to locally optimal sensing positions with adaptive trust weights (abstract and introduction).
- Simulation only.

## Methods and models

Power-diagram coverage control with an adaptation law on trust weights driven by sensor discrepancy. Abstract and introduction read from the authors' PDF.

## Limitations and open questions

Designed for degraded, not malicious, robots; a strategic or Sybil adversary could report consistent lies to its own fake neighbours. [[wardega-2023-byzantine]] notes reputation schemes inherit W-MSR's F+1 observer requirement.

## Relevance to us

The 'trust weight in the objective' pattern is what [[gil-2015-guaranteeing]] later fills with a physically grounded signal; in agent swarms, learned trust weights are similarly gameable unless grounded in something an adversary cannot copy.

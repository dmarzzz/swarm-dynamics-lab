---
id: li-2021-programming
type: paper
title: "Programming active cohesive granular matter with mechanically induced phase changes"
authors: ["Shengkai Li", "Bahnisikha Dutta", "Sarah Cannon", "Joshua J. Daymude", "Ram Avinery", "Enes Aydin", "Andréa W. Richa", "Daniel I. Goldman", "Dana Randall"]
year: 2021
venue: "Science Advances"
url: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1126/sciadv.abe8494?fields=title,abstract
doi: "10.1126/sciadv.abe8494"
arxiv: "2009.05710"
cite: "Li, S., Dutta, B., Cannon, S., Daymude, J. J., Avinery, R., Aydin, E., Richa, A. W., Goldman, D. I., & Randall, D. (2021). Programming active cohesive granular matter with mechanically induced phase changes. Science Advances, 7(17), eabe8494."
topics: [swarm-robotics, active-matter, swarm-intelligence]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "65 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Combines a theoretical abstraction of self-organising particle systems (from distributed computing) with an experimental system
of simple cohesive robots that have no digital computation or communication. Theory predicts that as
inter-particle attraction increases, the collective transitions from a dispersed to a compact phase; the robots
reproduce this transition, and in the aggregated phase they collectively transport non-robot "impurities".

## Contribution

Shows a quantitative link between a provable algorithmic model of a swarm and the physics of a robotic
active-matter system, so emergent tasks can be "programmed" by tuning a physical parameter instead of code.

## Key results

- Measured: dispersed-to-compact transition with increasing attraction, as predicted by the Markov chain model.
- Measured: aggregated collectives transport impurities (emergent task).

## Methods and models

Self-organising particle system model (stochastic local rules analysed theoretically) paired with cohesive
robots lacking digital computation and communication, with minimal or no sensing. Abstract read; arXiv
2009.05710. Mechanism of cohesion not checked.

## Limitations and open questions

Robot numbers and quantitative agreement with theory not checked.

## Relevance to us

The clearest example of a phase transition designed into a robot collective; candidate for a reproduction in
simulation where we tune attraction and measure compactness. See [[gauci-2014-self]], [[chvykov-2021-low]].

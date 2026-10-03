---
id: heuthe-2024-counterfactual
type: paper
title: "Counterfactual rewards promote collective transport using individually controlled swarm microrobots"
authors: ["Veit-Lorenz Heuthe", "Emanuele Panizon", "Hongri Gu", "Clemens Bechinger"]
year: 2024
venue: "Science Robotics"
url: https://www.ebi.ac.uk/europepmc/webservices/rest/article/MED/39693403?resultType=core&format=json
doi: "10.1126/scirobotics.ado5888"
arxiv: null
cite: "Heuthe, V.-L., Panizon, E., Gu, H., & Bechinger, C. (2024). Counterfactual rewards promote collective transport using individually controlled swarm microrobots. Science Robotics, 9(97), eado5888."
topics: [swarm-robotics, marl-emergence, active-matter]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "51 (Crossref, 2026-10-03)"
code: []
---
## Summary

Up to 200 microrobots, each individually steered by a laser spot, learn by multi-agent reinforcement learning to
collectively transport a large cargo to an arbitrary position and orientation, as ants do. Microscale swarms are
hard to control because of thermal noise comparable to propulsion, many degrees of freedom, and complex coupling
between neighbours. Counterfactual rewards, which credit each robot with the difference its action makes,
allow fast, unbiased training. The learned policy is robust to group size, malfunctioning units and noise, and
handles multiple objects simultaneously.

## Contribution

A rare example of MARL with credit assignment deployed on a physical swarm of hundreds of individually
controlled agents, at the microscale where active-matter noise dominates.

## Key results

- Measured: collective transport with up to 200 microrobots; robustness to group size, faulty units and noise
  (from abstract; numbers not checked).

## Methods and models

Micrometre-scale robots individually propelled by laser spots; MARL with counterfactual rewards. Abstract
read (Europe PMC).

## Limitations and open questions

Actuation by externally positioned laser spots implies an external control loop, so execution is not onboard
(inferred from the setup; not checked in the full text).

## Relevance to us

Bridges marl-emergence and robot swarms with a real experiment; a good reference for credit assignment in
swarm learning ([[huttenrauch-2019-deep]], [[tolstaya-2020-learning]]).

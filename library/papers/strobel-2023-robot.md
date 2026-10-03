---
id: strobel-2023-robot
type: paper
title: "Robot swarms neutralize harmful Byzantine robots using a blockchain-based token economy"
authors: ["Volker Strobel", "Alexandre Pacheco", "Marco Dorigo"]
year: 2023
venue: "Science Robotics"
url: https://doi.org/10.1126/scirobotics.abm4636
doi: "10.1126/scirobotics.abm4636"
arxiv: null
cite: "Strobel, V., Pacheco, A., & Dorigo, M. (2023). Robot swarms neutralize harmful Byzantine robots using a blockchain-based token economy. Science Robotics, 8(79), eabm4636."
topics: [swarm-robotics, collective-decision]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "43 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

A single Byzantine (faulty or malicious) robot can break the coordination of a whole swarm. The authors give
robots crypto tokens on a blockchain maintained by the swarm; a smart contract redistributes tokens according to
each robot's contribution to a collective-sensing task, and participation in security-critical activities costs
tokens, so Byzantine robots quickly run out and lose influence. Experiments with up to 24 physical robots and
simulations with over 100 robots show the token economy neutralises Byzantine robots.

## Contribution

Shows a working mechanism for Byzantine resilience in robot swarms, an area where classic consensus-based swarm
rules are fragile; bridges swarm robotics and distributed-systems security.

## Key results

- Measured: up to 24 physical robots maintain blockchain networks and neutralise Byzantine robots in collective
  sensing.
- Simulated: scalability and long-term behaviour with more than 100 robots.

## Methods and models

Collective-sensing scenario; blockchain maintained by the robots; smart contract regulating token
distribution. Abstract read; platform details not checked.

## Limitations and open questions

Blockchain overheads (communication, latency) at larger scales; assumes a majority of honest robots.

## Relevance to us

Directly relevant to adversarial robustness of collective decisions; links to [[valentini-2017-best]] and to
resilient consensus theory ([[leblanc-2013-resilient]]).

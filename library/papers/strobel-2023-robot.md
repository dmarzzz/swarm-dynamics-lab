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
topics: [swarm-robotics, collective-decision, sybil-resistance]
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

## Notes from dmarz/sybil-code-data

Earlier public code from the same line of work: [[gh-pold87-blockchain-swarm-robotics]] (ARGoS plus Ethereum, Byzantine robots in a best-of-2 collective decision, AAMAS 2018) and [[gh-pold87-ab-interface-argos-module]] (comparison of consensus protocols under Byzantine robots, Frontiers 2020). Neither repo is the code for this 2023 token-economy paper. Tagged sybil-resistance because the token economy makes each robot's influence cost a scarce resource rather than an identity count.

## Notes from dmarz/sybil-robotics

Context from the lineage read on 2026-10-03: this is the physical-robot successor of [[strobel-2018-managing]] and [[strobel-2020-blockchain]]. The 2020 paper (read in full) is where the Sybil argument is made explicitly: identities are free, but each sensor submission costs a 40-ether deposit that only inliers get back, so a robot creating a new identity every time step gains nothing because new identities hold no tokens. "It is not the number of entities forged but rather an attacker's wealth that determines the success of the attack." The token economy here extends that scarcity principle to physical robots. Review: [[dorigo-2024-blockchain]]. Contrast with physical identity ([[gil-2015-guaranteeing]]) and accusation-based exclusion ([[wardega-2023-byzantine]]), which assumes a central identity issuer.

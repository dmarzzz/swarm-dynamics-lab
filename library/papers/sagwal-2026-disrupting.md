---
id: sagwal-2026-disrupting
type: paper
title: "Disrupting Multi-Robot Coordination: Strategic Sybil Attack on Exploration Algorithms"
authors: [Rubal Sagwal, Vishal Gupta, Avinash Gautam]
year: 2026
venue: "2026 IEEE Wireless Communications and Networking Conference (WCNC), Kuala Lumpur"
url: https://doi.org/10.1109/WCNC65185.2026.11555413
doi: 10.1109/WCNC65185.2026.11555413
arxiv: null
cite: "Sagwal, R., Gupta, V., & Gautam, A. (2026). Disrupting Multi-Robot Coordination: Strategic Sybil Attack on Exploration Algorithms. In 2026 IEEE Wireless Communications and Networking Conference (WCNC), pp. 1-6. https://doi.org/10.1109/WCNC65185.2026.11555413"
topics: [sybil-resistance, swarm-robotics]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "1 (Crossref, 2026-10-03)"
code: []
---

## Summary

Attack paper on cooperative multi-robot exploration (search and rescue, mine detection, surveillance), which relies on wireless communication and so is exposed to Sybil attacks where one adversarial robot forges many identities. Prior work mostly treated static or centralised multi-robot settings and assumed Sybil identities were placed arbitrarily. This paper proposes two algorithms for stealthy, effective placement of fake identities in a distributed system, compares them with random placement using distance metrics and disruptive potential, and runs the attack inside a cooperative exploration framework in simulation, exposing vulnerabilities in existing exploration algorithms. Only the IEEE Xplore abstract was read; the algorithms and numbers are not recorded.

## Contribution

Treats where to put Sybil identities as a strategic choice, rather than assuming random placement, for distributed exploration.

## Key results

- Strategic placement disrupts exploration more than random placement (abstract; magnitudes not read).

## Methods and models

Simulation of distributed cooperative exploration (frontier-style allocation implied, not confirmed) with a Sybil robot advertising forged identities and positions.

## Limitations and open questions

Six-page conference paper, simulation only; whether physical-layer defences such as [[gil-2015-guaranteeing]] would catch the strategic placements is the obvious test.

## Relevance to us

The attack-side complement to physical-layer Sybil defences in robot swarms and a reminder that an adversary will optimise where its fake agents appear. Defences and trust frameworks: [[gil-2015-guaranteeing]], [[gil-2023-physicality]], [[yemini-2021-characterizing]], [[cavorsi-2024-exploiting]].

---
id: toumieh-2024-high
type: paper
title: "High-Speed Motion Planning for Aerial Swarms in Unknown and Cluttered Environments"
authors: ["Charbel Toumieh", "Dario Floreano"]
year: 2024
venue: "IEEE Transactions on Robotics"
url: https://arxiv.org/abs/2402.19033
doi: "10.1109/tro.2024.3429193"
arxiv: "2402.19033"
cite: "Toumieh, C., & Floreano, D. (2024). High-Speed Motion Planning for Aerial Swarms in Unknown and Cluttered Environments. IEEE Transactions on Robotics, 40, 3642-3656."
topics: [swarm-robotics]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "21 (Crossref, 2026-10-03); 33 (Semantic Scholar, 2026-10-03). OpenAlex daily budget exhausted on this IP during the session."
code: []
---

## Summary

HDSM is a high-speed, decentralised and synchronous motion-planning framework for aerial swarms that explicitly accounts for unknown, undiscovered parts of the environment. Each agent knows only the target location and plans an optimised trajectory that avoids obstacles, other agents and unexplored space while exploring. Against four recent methods it reports 100% success in reaching the target, 97% faster flight and 50% lower flight time, with a proof-of-concept on Crazyflie nano-drones.

## Contribution

It represents the planning-based state of the art (EPFL, Floreano group) for fast aerial swarms in unknown clutter in 2024, against which learned controllers such as [[zhang-2025-learning]] position themselves.

## Key results

- 100% success reaching target; flight speed 97% faster and flight time 50% lower than four recent state-of-the-art planners (measured in simulation, per the abstract).
- Crazyflie nano-drone proof of concept.

## Methods and models

Decentralised synchronous trajectory optimisation with explicit treatment of unknown space; planning agents exchange trajectories (per the abstract).

## Limitations and open questions

Abstract-depth entry. Synchronous planning and communication requirements; small hardware demo.

## Relevance to us

A non-learned comparison point; compare [[hou-2025-primitive]] and [[soria-2021-predictive]].

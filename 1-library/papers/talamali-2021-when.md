---
id: talamali-2021-when
type: paper
title: "When less is more: Robot swarms adapt better to changes with constrained communication"
authors: ["Mohamed S. Talamali", "Arindam Saha", "James A. R. Marshall", "Andreagiovanni Reina"]
year: 2021
venue: "Science Robotics"
url: https://doi.org/10.1126/scirobotics.abf1416
doi: "10.1126/scirobotics.abf1416"
arxiv: null
cite: "Talamali, M. S., Saha, A., Marshall, J. A. R., & Reina, A. (2021). When less is more: Robot swarms adapt better to changes with constrained communication. Science Robotics, 6(56), eabf1416. https://doi.org/10.1126/scirobotics.abf1416"
topics: ["collective-decision", "swarm-robotics"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "124 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Robot swarms tasked with agreeing on the currently best option in a changing environment adapt better when robots have a shorter communication range (fewer links). Across several voter-model-based behaviours, fewer communication links improved adaptation; mean-field models, multi-agent simulations and experiments with 50 Kilobots agree.

## Contribution

Counter-intuitive and well-replicated result that more communication can hurt collective adaptivity; a key reference for communication design in swarms.

## Key results

- Adaptation to changes improves with fewer links per robot, whether via shorter range or lower density (simulation, model, 50-Kilobot experiments).
- Abstract-level reading only; numbers beyond the abstract were not checked.

## Methods and models

Voter-model-based decision rules with environmental sampling; mean-field ODEs; multi-agent simulation; Kilobot experiments.

## Limitations and open questions

Voter-model family; generality to majority or cross-inhibition rules not established in the abstract.

## Relevance to us

Directly testable in any agent swarm, including LLM agents, by varying connectivity. Related: [[reina-2024-speed]], [[valentini-2016-collective]].

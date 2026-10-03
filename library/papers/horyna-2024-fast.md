---
id: horyna-2024-fast
type: paper
title: "Fast Swarming of UAVs in GNSS-Denied Feature-Poor Environments Without Explicit Communication"
authors: ["Jiří Horyna", "Vít Krátký", "Václav Pritzl", "Tomáš Báča", "Eliseo Ferrante", "Martin Saska"]
year: 2024
venue: "IEEE Robotics and Automation Letters"
url: https://arxiv.org/abs/2404.18729
doi: "10.1109/lra.2024.3390596"
arxiv: "2404.18729"
cite: "Horyna, J., Krátký, V., Pritzl, V., Báča, T., Ferrante, E., & Saska, M. (2024). Fast Swarming of UAVs in GNSS-Denied Feature-Poor Environments Without Explicit Communication. IEEE Robotics and Automation Letters, 9(6), 5284-5291."
topics: [swarm-robotics, collective-motion]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "20 (Crossref, 2026-10-03). OpenAlex daily budget exhausted on this IP during the session."
code: []
---

## Summary

A decentralised UAV swarm (CTU Prague MRS group) flies fast in feature-poor, GNSS-denied environments with no external localisation and, optionally, no communication. A new neighbourhood model gives robust onboard mutual perception and flocking state-feedback control that reduces the inter-agent oscillations common in reactive swarm models during fast collective motion. An enhanced multi-robot state estimation (MRSE) improves onboard localisation. A communication-less variant estimates the states that would otherwise be communicated. Real-world experiments include an interception-motivated task with group velocity at the hardware's physical limits.

## Contribution

It extends outdoor flocking ([[vasarhelyi-2018-optimized]]) to the GNSS-denied, communication-free regime at high speed.

## Key results

- Real-world fast collective flight up to the platforms' physical speed limits without communication or external localisation (per the abstract; exact speeds not checked).

## Methods and models

Neighbourhood model plus flocking state-feedback control, enhanced multi-robot state estimation (MRSE) for onboard localisation, and a communication-less variant that estimates the states that would otherwise be communicated.

## Limitations and open questions

Abstract-depth entry.

## Relevance to us

Hand-designed baseline for communication-free swarming against which learned methods ([[choi-2026-communication]]) can be compared.

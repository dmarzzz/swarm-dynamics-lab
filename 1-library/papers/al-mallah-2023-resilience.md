---
id: al-mallah-2023-resilience
type: paper
title: "Resilience-by-design in Adaptive Multi-agent Traffic Control Systems"
authors: [Ranwa Al Mallah, Talal Halabi, Bilal Farooq]
year: 2023
venue: ACM Transactions on Privacy and Security, vol. 26, no. 3, article 36, pp. 1-27
url: https://dl.acm.org/doi/10.1145/3592799
doi: 10.1145/3592799
arxiv: null
cite: "Al Mallah, R., Halabi, T., & Farooq, B. (2023). Resilience-by-design in Adaptive Multi-agent Traffic Control Systems. ACM Transactions on Privacy and Security, 26(3), Article 36, 1-27. https://doi.org/10.1145/3592799"
topics: [sybil-resistance, crowds-and-traffic, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "2 (Crossref, 2026-10-03)"
code: []
---

## Summary

Studies coordinated Sybil attacks on adaptive multi-agent traffic signal control (AMATSC), where networked intersections adapt signal timings from data reported by connected and autonomous vehicles (CAVs). The attack: a set of vehicles with forged or fake identities inject fabricated presence or trajectory data to skew the measurements the control agents rely on, sabotaging their decisions and degrading traffic across networked intersections. The authors present what they call the first detailed security analysis and implementation of this attack class, then propose an application-layer mitigation: a minimax game between the controller and a suspected attacker, so the AMATSC algorithm chooses signal decisions that are optimal against the worst-case data corruption rather than trusting reported counts. Experiments use real intersection settings and a traffic dataset from the city of Montreal; the mitigation improves time loss at attacked intersections by approximately 48.9% and yields more robust adaptive control across the network. Abstract only (ACM open-access PDF endpoint did not load from this box); the number of Sybil vehicles, the attack model's identity assumptions (how fake IDs enter the V2I channel) and the baseline time-loss figures are not visible.

## Contribution

Defines and implements coordinated Sybil data-injection against multi-agent traffic control and shows a game-theoretic robust-decision layer recovers roughly half of the attack's damage without identity verification.

## Key results

- Coordinated Sybil CAVs can materially degrade AMATSC decisions (quantified in the paper, not in the abstract).
- Minimax mitigation improves time loss at attacked intersections by ~48.9% on Montreal data.

## Methods and models

Multi-agent adaptive signal control, Sybil data-injection attack implementation, minimax game formulation, simulation on real traffic data. Details not read.

## Limitations and open questions

Abstract-level read. Mitigation treats the symptom (robust decisions under suspected corruption) rather than identity; the residual ~51% loss and the cost of conservative decisions under no attack are not visible; assumes the controller can suspect an attack.

## Relevance to us

One of the few papers where the Sybil attackers are themselves a coordinated multi-agent system acting against another multi-agent system, which is the swarm-vs-swarm framing the hackathon cares about, in a physical domain with a public dataset. The robust-decision mitigation is the control-theoretic cousin of the resilient-consensus work ([[leblanc-2013-resilient]], [[renganathan-2022-spoof]]) and of Byzantine aggregation; VANET trust background in [[zhang-2011-survey]]; the "cheap vehicle identities" problem is the same one [[sun-2007-ddos]] and [[eisenbarth-2022-ethereum]] measure in overlays. Root: [[douceur-2002-sybil]].

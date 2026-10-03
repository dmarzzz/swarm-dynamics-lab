---
id: shefi-2025-bugs
type: paper
title: "Bugs with features: vision-based fault-tolerant collective motion inspired by nature"
authors: ["Peleg Shefi", "Amir Ayali", "Gal A. Kaminka"]
year: 2025
venue: "Autonomous Robots"
url: https://arxiv.org/abs/2512.22448
doi: "10.1007/s10514-025-10230-7"
arxiv: "2512.22448"
cite: "Shefi, P., Ayali, A., & Kaminka, G. A. (2025). Bugs with features: vision-based fault-tolerant collective motion inspired by nature. Autonomous Robots, 49(4), 39."
topics: [swarm-robotics, collective-motion]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "2 (Crossref, 2026-10-03). OpenAlex daily budget exhausted on this IP during the session."
code: []
---

## Summary

Vision-based artificial swarms are brittle because visual perception is ambiguous and lossy. Inspired by locust studies, the authors add two mechanisms: a robust neighbour-distance estimator that combines a neighbour's perceived horizontal and vertical visual sizes, and intermittent (pause-and-go) locomotion that lets robots reliably detect peers that cannot keep up and avoid them, robustly to misclassification. Physics-based simulations show dramatic resilience gains for both avoid-attract and alignment-based models.

## Contribution

It treats faulty robots as a perception problem and borrows intermittent locomotion from locusts as a sensing strategy.

## Key results

- Large improvements in swarm resilience to faulty robots in physics simulations (claimed in abstract; numbers not checked).

## Methods and models

Vision-based distance estimation from apparent size, intermittent locomotion, and fault avoidance in avoid-attract and alignment models.

## Limitations and open questions

Abstract-depth entry. Simulation-only per the abstract.

## Relevance to us

Fault tolerance and perception noise are realistic swarm stressors; compare [[mezey-2025-purely]] and [[castro-2025-visual]].

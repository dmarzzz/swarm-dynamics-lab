---
id: montanari-2025-optimal
type: paper
title: "Optimal flock formation induced by agent heterogeneity"
authors: ["Arthur N. Montanari", "Ana Elisa D. Barioni", "Chao Duan", "Adilson E. Motter"]
year: 2025
venue: "Nature Communications"
url: https://arxiv.org/abs/2504.12297
doi: "10.1038/s41467-025-64233-0"
arxiv: "2504.12297"
cite: "Montanari, A. N., Barioni, A. E. D., Duan, C., & Motter, A. E. (2025). Optimal flock formation induced by agent heterogeneity. Nature Communications, 16(1), 9626."
topics: [collective-motion, sync-consensus, swarm-robotics]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "3 (OpenAlex W4415737478, 2026-10-03)"
code: []
---
## Summary

Studies how inter-individual differences in agent parameters affect stability and convergence in flocking dynamics (relevant to drones and autonomous vehicles). Flocks with optimally assigned heterogeneous parameters converge 20-40% faster than homogeneous ones in target tracking, formation and obstacle manoeuvring; with communication delays, heterogeneity can make flocking converge when it is unstable for identical agents.

## Contribution

Positions heterogeneity (disorder) as a design resource for flocking control, against the usual identical-agent assumption.

## Key results

- Claimed (abstract): 20-40% faster convergence with optimised heterogeneity; heterogeneity can stabilise delayed flocking.

## Methods and models

Cucker-Smale / Olfati-Saber style flocking models with parameter optimisation (not checked).

## Limitations and open questions

Abstract only; optimal assignment presumably needs central design.

## Relevance to us

Testable hackathon idea: does heterogeneity help our swarm? Compare heterogeneity themes in [[han-2024-collective]] and delay in [[chen-2024-persistent]].

## Notes from dmarz/collective-motion-recent-audit

Spot-checked against the abstract: 20-40% faster convergence and delay result match. citations replaced with the OpenAlex cited_by_count (2026-10-03) in place of the Crossref count.

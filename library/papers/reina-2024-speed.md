---
id: reina-2024-speed
type: paper
title: "Speed-accuracy trade-offs in best-of-n collective decision making through heterogeneous mean-field modeling"
authors: ["Andreagiovanni Reina", "Thierry Njougouo", "Elio Tuci", "Timoteo Carletti"]
year: 2024
venue: "Physical Review E"
url: https://doi.org/10.1103/physreve.109.054307
doi: "10.1103/physreve.109.054307"
arxiv: "2310.13694"
cite: "Reina, A., Njougouo, T., Tuci, E., & Carletti, T. (2024). Speed-accuracy trade-offs in best-of-n collective decision making through heterogeneous mean-field modeling. Physical Review E, 109(5), 054307. https://doi.org/10.1103/physreve.109.054307"
topics: ["collective-decision", "swarm-robotics", "sync-consensus"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "9 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Introduces a model that interpolates between the voter model and the local majority rule by letting individuals make errors when pooling neighbours' opinions (for example to reduce cognitive load), and shows a speed-accuracy trade-off governed by this cognitive effort. A heterogeneous mean-field extension shows a second trade-off governed by network connectivity, with lower connectivity giving higher accuracy.

## Contribution

Unifies two standard best-of-n opinion rules and links the less-is-more communication result [[talamali-2021-when]] to network topology.

## Key results

- Speed-accuracy trade-off regulated by individual pooling effort (model).
- Reduced network connectivity increases collective accuracy (heterogeneous mean-field analysis).
- Abstract-level reading only; numbers beyond the abstract were not checked.

## Methods and models

Preprint version: arXiv 2310.13694, titled 'Studying speed-accuracy trade-offs in best-of-n collective decision-making through heterogeneous mean-field modeling' (same authors). Opinion dynamics with quality-dependent dissemination on networks; heterogeneous mean-field equations.

## Limitations and open questions

Theory only in this paper.

## Relevance to us

Gives analytic expectations for how agent connectivity affects decision quality, relevant to both robot and LLM agent swarms. Related: [[valentini-2016-collective]].

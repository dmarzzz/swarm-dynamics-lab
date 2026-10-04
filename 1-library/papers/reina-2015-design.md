---
id: reina-2015-design
type: paper
title: "A Design Pattern for Decentralised Decision Making"
authors: ["Andreagiovanni Reina", "Gabriele Valentini", "Cristian Fernández-Oto", "Marco Dorigo", "Vito Trianni"]
year: 2015
venue: "PLOS ONE"
url: https://doi.org/10.1371/journal.pone.0140950
doi: "10.1371/journal.pone.0140950"
arxiv: null
cite: "Reina, A., Valentini, G., Fernández-Oto, C., Dorigo, M., & Trianni, V. (2015). A Design Pattern for Decentralised Decision Making. PLOS ONE, 10(10), e0140950. https://doi.org/10.1371/journal.pone.0140950"
topics: ["collective-decision", "swarm-robotics", "swarm-intelligence"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "142 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Proposes a design pattern for decentralised collective decisions grounded in honeybee nest-site selection, with formal guidelines for choosing microscopic agent transition probabilities so the swarm quantitatively matches macroscopic model predictions. Covers homogeneous and heterogeneous agents and spatial and topological effects on the micro-macro link, with two case studies.

## Contribution

Engineering recipe translating [[seeley-2012-stop]] and [[pais-2013-mechanism]] into agent rules; cited in [[valentini-2017-best]] as the cross-inhibition strategy.

## Key results

- Microscopic implementations match macroscopic predictions under the stated guidelines (simulation case studies).
- Abstract-level reading only; numbers beyond the abstract were not checked.

## Methods and models

Mean-field to probabilistic finite-state machine mapping; multi-agent and robot simulations.

## Limitations and open questions

Well-mixed assumption partially relaxed; real-robot validation limited in this paper.

## Relevance to us

Practical starting point for implementing bee-style decisions in our swarm code. Related: [[reina-2017-model]], [[talamali-2021-when]].

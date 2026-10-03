---
id: wardega-2019-resilience
type: paper
title: "Resilience of Multi-robot Systems to Physical Masquerade Attacks"
authors: ["Kacper Wardega", "Roberto Tron", "Wenchao Li"]
year: 2019
venue: "2019 IEEE Security and Privacy Workshops (SPW)"
url: https://api.openalex.org/works/doi:10.1109/spw.2019.00031
doi: "10.1109/spw.2019.00031"
arxiv: null
cite: "Wardega, K., Tron, R., & Li, W. (2019). Resilience of Multi-robot Systems to Physical Masquerade Attacks. In 2019 IEEE Security and Privacy Workshops (SPW), 120-125."
topics: [sybil-resistance, swarm-robotics]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "13 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Studies a stealthy adversary that physically masquerades as a properly functioning robot in multi-agent path finding. Conventional MAPF plans are shown vulnerable; the authors give a constraint-based MAPF formulation whose plans are provably resilient because they schedule inter-agent observations that enable introspective monitoring of whether each robot is where it should be.

## Contribution

Introduces co-observation as a planning constraint, the seed of the accusation mechanism in [[wardega-2023-byzantine]] and of the plan-deviation defence in HoLA Robots (arXiv:2301.10704).

## Key results

- Provably resilient MAPF plans against physical masquerade, via scheduled inter-agent observations (abstract).

## Methods and models

Constraint-based multi-agent path finding. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

Centralised planning; masquerade concerns identity of a physical slot, not multiplication of identities.

## Relevance to us

Designing interaction schedules so that agents can verify each other is a protocol idea that transfers to agent swarms: schedule cross-checks so every claim has an independent observer.

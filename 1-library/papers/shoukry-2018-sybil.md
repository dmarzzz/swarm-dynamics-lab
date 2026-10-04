---
id: shoukry-2018-sybil
type: paper
title: "Sybil Attack Resilient Traffic Networks: A Physics-Based Trust Propagation Approach"
authors: ["Yasser Shoukry", "Shaunak Mishra", "Zutian Luo", "Suhas Diggavi"]
year: 2018
venue: "2018 ACM/IEEE 9th International Conference on Cyber-Physical Systems (ICCPS)"
url: https://api.openalex.org/works/doi:10.1109/iccps.2018.00013
doi: "10.1109/iccps.2018.00013"
arxiv: null
cite: "Shoukry, Y., Mishra, S., Luo, Z., & Diggavi, S. (2018). Sybil Attack Resilient Traffic Networks: A Physics-Based Trust Propagation Approach. In 2018 ACM/IEEE 9th International Conference on Cyber-Physical Systems (ICCPS), 43-54."
topics: [sybil-resistance, crowds-and-traffic]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "21 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Crowdsourced road traffic estimation where malicious vehicles report false data or ghost (Sybil) vehicles to create virtual congestion that steers routing into real congestion. The defence combines noisy legacy sensing infrastructure with vehicle dynamics and a proximity graph inferred from the crowdsourced data, solved with SAT solvers for scale. Validated on real traffic data from Bologna.

## Contribution

Physics-consistency (vehicles must obey dynamics and be seen by neighbours) as a Sybil filter for a crowdsourcing system, cited by [[wardega-2023-byzantine]] as a physics-inspired approach.

## Key results

- Significant reduction in average travel time under Sybil attacks, in some cases from about an hour to a few minutes (abstract).

## Methods and models

Trust propagation over a proximity graph with physical constraints, SAT-based solving, Bologna traffic data. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

Relies on some trusted infrastructure sensors.

## Relevance to us

The Google Maps ghost-traffic case is a clean real-world Sybil example for agent swarms: cheap fake reporters manipulate a shared estimate that then steers real agents. Related: [[cavorsi-2024-exploiting]].

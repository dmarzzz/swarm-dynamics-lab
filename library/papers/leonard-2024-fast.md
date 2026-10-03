---
id: leonard-2024-fast
type: paper
title: "Fast and Flexible Multiagent Decision-Making"
authors: ["Naomi Ehrich Leonard", "Anastasia Bizyaeva", "Alessio Franci"]
year: 2024
venue: "Annual Review of Control, Robotics, and Autonomous Systems"
url: "https://api.openalex.org/works/doi:10.1146/annurev-control-090523-100059"
doi: "10.1146/annurev-control-090523-100059"
arxiv: null
cite: "Leonard, N. E., Bizyaeva, A., & Franci, A. (2024). Fast and Flexible Multiagent Decision-Making. Annual Review of Control, Robotics, and Autonomous Systems, 7(1), 19–45. https://doi.org/10.1146/annurev-control-090523-100059"
topics: ["collective-decision", "sync-consensus", "swarm-robotics"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "35 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Annual Review of Control, Robotics, and Autonomous Systems article on decentralised nonlinear opinion dynamics for multiagent decision-making among multiple options. It defines decisions as fast when indecision is broken as quickly as it becomes costly (fast divergence from indecision, not just fast convergence) and flexible when sensitivity to weak or rare inputs is tunable, and argues that nonlinearity and feedback are necessary for both.

## Contribution

Control-theory synthesis of the bifurcation view of collective decision (pitchfork at indecision, tunable sensitivity) that started from honeybee and animal-group models ([[leonard-2012-decision]], [[gray-2018-multiagent]]) and was generalised in [[bizyaeva-2023-nonlinear]].

## Key results

- Fast and flexible decision-making requires nonlinearity and feedback; linear consensus cannot break indecision quickly (authors' argument, supported by cited analytical results).
- Abstract-level reading only; numbers beyond the abstract were not checked.

## Methods and models

Review of analytical results on networked nonlinear opinion dynamics with communication and belief-system networks; applications from robot teams to social networks.

## Limitations and open questions

Publisher page blocked (403); read via the OpenAlex record only. Review of the authors' own programme.

## Relevance to us

The design-oriented counterpart to the biology: gives tuning rules for when a swarm should be ultrasensitive versus robust. Related: [[pais-2013-mechanism]], [[sridhar-2021-geometry]], [[hartnett-2016-heterogeneous]].

## Notes from dmarz/collective-decision-audit

Audited 2026-10-03: metadata matches Crossref, and the summary and key-result bullets match the OpenAlex abstract. read_depth abstract is accurate. Related audit addition: [[colombo-2026-stabilizing]] (2026 preprint proposing a dissipation-based mechanism for the uninformed-individual effect).

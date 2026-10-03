---
id: yu-2024-overview
type: paper
title: "An Overview of Swarm Coordinated Control"
authors: ["Dengxiu Yu", "Jiacheng Li", "Zhen Wang", "Xuelong Li"]
year: 2024
venue: "IEEE Transactions on Artificial Intelligence"
url: https://api.openalex.org/works/doi:10.1109/tai.2023.3314581
doi: "10.1109/tai.2023.3314581"
arxiv: null
cite: "Yu, D., Li, J., Wang, Z., & Li, X. (2024). An Overview of Swarm Coordinated Control. IEEE Transactions on Artificial Intelligence, 5(5), 1918–1938."
topics: ["swarm-robotics", "sync-consensus"]
added_by: dmarz/swarm-robotics-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "31 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

A control-theory review of swarm coordinated control, focused on results after 2018. From a Google Scholar and
Web of Science search of hundreds of articles, it covers swarm and formation control, consensus
("consistency"), switching topologies, delay control, finite- and fixed-time convergence, obstacle
avoidance and path planning, plus evaluation methods and applications. It proposes future directions based on
"survival intelligence", learning and heterogeneous control. (From the abstract; full text paywalled.)

## Contribution

A recent entry point into the control-engineering vocabulary for swarms (formation, consensus, time-delay
and convergence-time guarantees), which the robotics-centred reviews ([[brambilla-2013-swarm]],
[[schranz-2020-swarm]]) cover only lightly.

## Key results

- Taxonomy of post-2018 swarm-control topics and proposed research directions (from abstract; specifics not
  checked).

## Methods and models

Literature review; no experiments.

## Limitations and open questions

Abstract-level entry. The abstract's search method is loosely described, and the paper is cited modestly (31).
Physical robot validation is likely a minor theme.

## Relevance to us

Use as a bridge to the sync-consensus topic: delay and topology-switching results map onto the
delay-versus-collision question raised by [[vasarhelyi-2018-optimized]]. Classic anchors are
[[olfati-saber-2006-flocking]] and the consensus entries in that topic.

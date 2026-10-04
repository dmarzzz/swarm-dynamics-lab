---
id: cavorsi-2023-dynamic
type: paper
title: "Dynamic Crowd Vetting: Collaborative Detection of Malicious Robots in Dynamic Communication Networks"
authors: ["Matthew Cavorsi", "Frederik Mallmann-Trenn", "David Saldaña", "Stephanie Gil"]
year: 2023
venue: "arXiv preprint (IEEE CDC 2023)"
url: https://arxiv.org/abs/2304.00551
doi: null
arxiv: "2304.00551"
cite: "Cavorsi, M., Mallmann-Trenn, F., Saldaña, D., & Gil, S. (2023). Dynamic Crowd Vetting: Collaborative Detection of Malicious Robots in Dynamic Communication Networks. arXiv:2304.00551."
topics: [sybil-resistance, swarm-robotics]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "3 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Extends [[mallmann-trenn-2021-crowd]] to randomly moving robots: legitimate robots combine observations from random encounters with trusted neighbours' opinions. As long as each robot correctly classifies some fixed subset of the team, second-hand information corrects the rest. The subset size is characterised by graph and random-walk properties, and detection time is shown to stay constant as team size grows, with a closed-form bound on time steps for a target failure probability.

## Contribution

Shows crowd vetting scales with mobility: detection time independent of team size.

## Key results

- Detection time remains constant as the number of robots increases (formal result, abstract).
- Simulations show large reductions in detection time versus methods without neighbour information.

## Methods and models

Random-walk encounter model plus opinion sharing. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

Same trust-observation assumptions as the static version.

## Relevance to us

Mobile agents meeting at random resemble agents interacting through shared channels; the constant-time result suggests gossip of trust opinions scales to large agent swarms if first-hand signals exist.

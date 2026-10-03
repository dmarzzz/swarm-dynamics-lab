---
id: gil-2018-resilient
type: paper
title: "Resilient Multi-Agent Consensus Using Wi-Fi Signals"
authors: ["Stephanie Gil", "Cenk Baykal", "Daniela Rus"]
year: 2018
venue: "IEEE Control Systems Letters"
url: https://api.openalex.org/works/doi:10.1109/lcsys.2018.2853641
doi: "10.1109/lcsys.2018.2853641"
arxiv: null
cite: "Gil, S., Baykal, C., & Rus, D. (2018). Resilient Multi-Agent Consensus Using Wi-Fi Signals. IEEE Control Systems Letters, 3(1), 126-131."
topics: [sybil-resistance, sync-consensus, swarm-robotics]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "29 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Applies Wi-Fi physical fingerprints to consensus: an adversary that spawns or spoofs nodes to bias the converged value is countered using only information already present in received wireless signals, with no extra protocol or storage. The authors give an analytical probabilistic bound on the influence of spoofed nodes on the converged consensus value and demonstrate the algorithm for flocking and rendezvous.

## Contribution

Carries the spoof-resilience guarantee of [[gil-2015-guaranteeing]] from coverage to general consensus dynamics.

## Key results

- Probabilistic bound on the deviation of the consensus value caused by spoofed nodes (abstract).
- Demonstrated for flocking and rendezvous.

## Methods and models

Weighted consensus with per-neighbour confidence derived from wireless signal uniqueness. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

Same physical-layer assumptions as the 2015 work: a multi-radio or multi-body attacker is not addressed.

## Relevance to us

Shows that consensus itself can be made Sybil-resilient by weighting rather than excluding, which is the cheapest change to existing agent-aggregation code. Related: [[renganathan-2017-spoof]], [[yemini-2021-characterizing]].

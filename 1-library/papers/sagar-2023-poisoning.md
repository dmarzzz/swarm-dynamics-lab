---
id: sagar-2023-poisoning
type: paper
title: "Poisoning Attacks and Defenses in Federated Learning: A Survey"
authors: ["Subhash Sagar", "Chang-Sun Li", "Seng W. Loke", "Jinho Choi"]
year: 2023
venue: "arXiv preprint"
url: https://arxiv.org/abs/2301.05795
doi: null
arxiv: "2301.05795"
cite: "Sagar, S., Li, C.-S., Loke, S. W., & Choi, J. (2023). Poisoning Attacks and Defenses in Federated Learning: A Survey. arXiv preprint arXiv:2301.05795."
topics: [fork-merge-security, meta]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Short survey of poisoning attacks on federated learning. It gives a taxonomy of data and model poisoning attacks and defences, together with an experimental evaluation, and argues for robust federated learning because clients' data and training are invisible to the server. Catalogued as one of the review articles in this area.

## Contribution

Entry point taxonomy for federated poisoning, useful as a map rather than for specific results.

## Key results

- Abstract-level: taxonomy of poisoning attacks plus experimental evaluation; no specific numbers read.

## Methods and models

Literature survey with small experiments.

## Limitations and open questions

Abstract only; brief survey. The more recent [[zhang-2025-sok]] benchmark is more systematic.

## Relevance to us

Background for Q2 and Q3: the taxonomy (data versus model poisoning, targeted versus untargeted) maps onto the question of whether a returning sub-agent corrupts what it saw (data) or what it carries back (its own weights or memory). Related: [[zhang-2025-sok]], [[bagdasaryan-2020-how]].

---
id: ng-2025-are
type: paper
title: Are LLM-Powered Social Media Bots Realistic?
authors:
- Lynnette Hui Xian Ng
- Kathleen M. Carley
year: 2025
venue: Social, Cultural, and Behavioral Modeling (SBP-BRiMS 2025), Lecture Notes in Computer Science
url: https://arxiv.org/abs/2508.00998
doi: 10.1007/978-3-032-07715-8_2
arxiv: '2508.00998'
cite: Ng, L. H. X., & Carley, K. M. (2025). Are LLM-Powered Social Media Bots Realistic? In Social, Cultural, and Behavioral Modeling (SBP-BRiMS 2025), Lecture Notes in Computer Science, pp. 14-23. Springer. https://doi.org/10.1007/978-3-032-07715-8_2
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 3 (Crossref, 2026-10-03)
code: []
---

## Summary

The authors generate LLM-powered bot personas, tweets and interaction networks and compare them with empirical data on wild bots and humans. Both the network properties and the linguistic properties of the LLM bots differ from those of wild bots and humans, which bears on how detectable such bots would be and on how realistic simulated benchmarks are.

## Contribution

A realism check on simulated LLM botnets: they are not yet distributionally like either real bots or real humans.

## Key results

- Network and linguistic properties of generated LLM bot networks differ from wild bots and humans (abstract).

## Methods and models

Manual persona design, network science and LLM generation; comparison against empirical bot/human data. Abstract-level read.

## Limitations and open questions

Small workshop paper; one generation recipe; differences may shrink with better prompting.

## Relevance to us

Caution for anyone training detectors on synthetic swarms such as [[qiao-2024-botsim]]: a detector may learn simulator artefacts. Same group: [[ng-2025-social]].

---
id: hoetzlein-2025-protecting
type: paper
title: 'Protecting Small Organizations from AI Bots with Logrip: Hierarchical IP Hashing'
authors:
- Rama Carl Hoetzlein
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2508.03130
doi: null
arxiv: '2508.03130'
cite: 'Hoetzlein, R. C. (2025). Protecting Small Organizations from AI Bots with Logrip: Hierarchical IP Hashing. arXiv preprint arXiv:2508.03130.'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Analyses server event logs with hierarchical IP hashing: activity is aggregated across subnet classes and statistical measures plus visualisation separate humans from automated clients by access pattern. The method targets coordinated bot activity and distributed crawling that per-IP throttling misses. On one real-world site the author estimates that 80 to 95 percent of traffic came from AI crawlers.

## Contribution

A cheap coordination detector for small operators: grouping by subnet hierarchy exposes crawls spread over many addresses, which is a swarm signature.

## Key results

- 80 to 95% of traffic on the studied site estimated to be AI crawlers (single real-world example; estimate, abstract).
- Detects distributed crawling that conventional tools fail to identify (claim, abstract).

## Methods and models

Log analysis, hierarchical subnet aggregation, statistical thresholds, visualisation. Abstract-level read.

## Limitations and open questions

Abstract only; one site; residential-proxy swarms spread across unrelated subnets would blur subnet aggregation (inferred; cf. [[fayolle-2026-internet]] on residential proxies).

## Relevance to us

A base-rate data point (AI crawlers as the majority of small-site traffic) and a simple aggregation method to pair with traps. Related: [[liu-2024-somesite]], [[seiden-2026-identifying]].

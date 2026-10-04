---
id: zouzou-2024-unsupervised
type: paper
title: "Unsupervised detection of coordinated fake-follower campaigns on social media"
authors: ["Yasser Zouzou", "Onur Varol"]
year: 2024
venue: "EPJ Data Science"
url: https://arxiv.org/abs/2310.20407
doi: "10.1140/epjds/s13688-024-00499-6"
arxiv: "2310.20407"
cite: "Zouzou, Y., & Varol, O. (2024). Unsupervised detection of coordinated fake-follower campaigns on social media. EPJ Data Science, 13(1), 62."
topics: [swarm-detection]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "28 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Targets fake-follower campaigns that inflate popularity metrics. The method looks for anomalous following patterns among all followers of a target account, an unsupervised signal that does not need labelled bots. Across many Twitter accounts, irregular following patterns are common and indicate automated fake accounts, and the detected anomalous follower groups behave consistently across multiple target accounts.

## Contribution

A cheap, unsupervised detector for coordinated follow campaigns based on the order and timing of follows, scalable to many targets.

## Key results

- Irregular following patterns are prevalent and indicate automated fake accounts (abstract).
- Detected groups show consistent behaviour across multiple target accounts (abstract). No numbers in the abstract.

## Methods and models

Analysis of follower lists in follow order with creation dates; anomaly detection on follower sequences.

## Limitations and open questions

Abstract only. Depends on follower-order data, which platforms now restrict.

## Relevance to us

Account-creation and follow-order bursts are a trace an agent operator spinning up many accounts at once will leave; compare with burst-of-creation detection cited in [[mannocci-2026-detection]].

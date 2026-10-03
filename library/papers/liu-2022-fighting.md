---
id: liu-2022-fighting
type: paper
title: 'Fighting Sybils in Airdrops'
authors:
- 'Zheng Liu'
- 'Hongyang Zhu'
year: 2022
venue: 'arXiv preprint (cs)'
url: https://arxiv.org/abs/2209.04603
doi: null
arxiv: '2209.04603'
cite: 'Liu, Z., & Zhu, H. (2022). Fighting Sybils in Airdrops. arXiv preprint arXiv:2209.04603.'
topics:
- sybil-resistance
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Airdrops reward early DApp users and attract Sybils who create many accounts. The paper argues that accounts controlled by one Sybil show similar DApp activity and regular token transfer patterns. It builds transaction graphs with accounts as vertices and transfers as edges, looks for accounts funded by the same source that then interact with DApps in similar ways, and presents suspicious accounts from a recent airdrop as a demonstration.

## Contribution

A behavioural graph-based detector for airdrop Sybils, as opposed to a mechanism-design defence.

## Key results

- Detected accounts share interaction activity and regular transfer patterns (abstract); no precision or recall figures in the abstract.

## Methods and models

Transaction graph analysis of funding sources and DApp interaction patterns.

## Limitations and open questions

Abstract-level read; the evaluation is a demonstration without ground truth.

## Relevance to us

Detection is the alternative to Sybil-proof design when the mechanism is fixed. In agent swarms, common funding source and correlated behaviour are the analogous signals for linking agents to an operator. Compare [[messias-2023-airdrops]] and the social-graph approach in [[conitzer-2010-using]].

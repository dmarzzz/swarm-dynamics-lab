---
id: chen-2022-sybil
type: paper
title: 'Sybil-Proof Diffusion Auction in Social Networks'
authors:
- 'Hongyin Chen'
- 'Xiaotie Deng'
- 'Ying Wang'
- 'Yue Wu'
- 'Dengji Zhao'
year: 2022
venue: 'arXiv preprint (cs.GT)'
url: https://arxiv.org/abs/2211.01984
doi: null
arxiv: '2211.01984'
cite: 'Chen, H., Deng, X., Wang, Y., Wu, Y., & Zhao, D. (2022). Sybil-Proof Diffusion Auction in Social Networks. arXiv preprint arXiv:2211.01984.'
topics:
- sybil-resistance
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Diffusion auctions sell an item over a social network and must incentivise buyers to invite neighbours. Because buyers can add fake nodes to the network, existing diffusion mechanisms are open to Sybil attacks. The paper proposes the Sybil tax mechanism (STM) and the Sybil cluster mechanism (SCM), which are Sybil-proof and incentive compatible in the single-item setting at a mild cost in welfare and revenue.

## Contribution

First diffusion auction mechanisms that protect buyers against Sybil attacks.

## Key results

- STM and SCM achieve Sybil-proofness and incentive compatibility for a single item (abstract).
- The authors describe the welfare and revenue sacrifice as mild; no numbers in the abstract.

## Methods and models

Single-item auction on a graph where participation spreads by invitation; Sybil nodes can be inserted between a buyer and its neighbours.

## Limitations and open questions

Abstract-level read; single item only.

## Relevance to us

When agents recruit other agents into a market (for example agents inviting sub-agents to bid for tasks), the invitation graph can be padded with Sybils. The two mechanisms are a pattern for taxing or clustering suspicious structure. Related: [[babaioff-2012-bitcoin]], [[chen-2013-sybil]].

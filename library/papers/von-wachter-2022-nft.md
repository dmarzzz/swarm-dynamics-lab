---
id: von-wachter-2022-nft
type: paper
title: 'NFT Wash Trading: Quantifying suspicious behaviour in NFT markets'
authors:
- Victor von Wachter
- Johannes Rude Jensen
- Ferdinand Regner
- Omri Ross
year: 2022
venue: arXiv preprint (q-fin)
url: https://arxiv.org/abs/2202.03866
doi: null
arxiv: '2202.03866'
cite: 'von Wachter, V., Jensen, J. R., Regner, F., & Ross, O. (2022). NFT Wash Trading: Quantifying suspicious behaviour in NFT markets. arXiv preprint arXiv:2202.03866.'
topics:
- swarm-detection
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Examines the 52 largest Ethereum NFT collections by volume from January 2018 to mid-November 2021 for wash-trading patterns. In this sample 3.93% of addresses, processing 2.04% of sale transactions, trigger suspicion; flagged trades may have inflated volume by up to $149.5M. Most flagged patterns alternate between a few addresses, which the authors read as manual rather than automated trading. They present the figure as a lower bound and argue wash trading may be less common than industry observers claimed.

## Contribution

A conservative lower bound and a dissenting view on NFT wash-trading prevalence.

## Key results

- 3.93% of addresses and 2.04% of sale transactions flagged; up to $149.5M inflated volume.
- Flagged patterns mostly alternate among few addresses (interpreted as manual).

## Methods and models

Flags suspicious trading patterns among addresses in the 52 largest collections; specific tests not read (abstract only).

## Limitations and open questions

Abstract-level read; sample limited to top collections; lower bound by construction.

## Relevance to us

Wash trading is the market form of a Sybil swarm: one operator controlling several addresses that trade with each other to fake activity. Detection heuristics here (closed cycles between linked addresses, common funders, zero net position change) are the transaction-level analogue of coordination detection for agent swarms. Useful as the low end of the prevalence range; compare [[falk-2023-can]] (about 38% of trades) and [[niu-2024-unveiling]].

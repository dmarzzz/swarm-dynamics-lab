---
id: zwang-2018-detecting
type: paper
title: Detecting Bot Activity in the Ethereum Blockchain Network
authors:
- Morit Zwang
- Shahar Somin
- Alex 'Sandy' Pentland
- Yaniv Altshuler
year: 2018
venue: arXiv preprint (cs.SI)
url: https://arxiv.org/abs/1810.01591
doi: null
arxiv: '1810.01591'
cite: Zwang, M., Somin, S., Pentland, A. '., & Altshuler, Y. (2018). Detecting Bot Activity in the Ethereum Blockchain Network. arXiv preprint arXiv:1810.01591.
topics:
- swarm-detection
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Early short paper arguing that Ethereum is a breeding ground for bots because anyone can open many wallets free of charge, so many wallets are controlled by the same entities, and that tens of thousands of new wallets appear each day. It demonstrates bot detection on the Ethereum transaction network with a network-theory approach rather than rule-based or ML methods. The abstract gives no accuracy figures.

## Contribution

First paper I found on bot detection specifically on Ethereum; cited by later ML work for its time-based heuristics.

## Key results

- No quantitative results in the abstract.

## Methods and models

Network-theory analysis of the Ethereum wallet transaction graph (details not read).

## Limitations and open questions

Abstract-level read; short workshop-style paper.

## Relevance to us

Historical starting point; superseded by [[niedermayer-2024-detecting]] (ML with labels) and [[bartnicki-2026-compression]].

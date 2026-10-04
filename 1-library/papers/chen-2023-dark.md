---
id: chen-2023-dark
type: paper
title: 'The Dark Side of NFTs: A Large-Scale Empirical Study of Wash Trading'
authors:
- Shijian Chen
- Jiachi Chen
- Jiangshan Yu
- Xiapu Luo
- Yanlin Wang
year: 2023
venue: arXiv preprint (cs)
url: https://arxiv.org/abs/2312.12544
doi: null
arxiv: '2312.12544'
cite: 'Chen, S., Chen, J., Yu, J., Luo, X., & Wang, Y. (2023). The Dark Side of NFTs: A Large-Scale Empirical Study of Wash Trading. arXiv preprint arXiv:2312.12544.'
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

Large NFT wash-trading study over 8,717,031 transfer events and 3,830,141 sale events from 2,701,883 NFTs collected through the OpenSea API. The authors define three types of NFT wash trading, give identification algorithms, and report 824 transfer events and 5,330 sale events (about $8.86M) plus 370 address pairs involved, with a minimum loss of about $3.97M. They discuss marketplace design, profitability, payment token and user behaviour as factors.

## Contribution

A multi-type taxonomy of NFT wash trading beyond price inflation, with conservative identification rules.

## Key results

- 5,330 wash sale events worth $8,857,070.41 and 370 address pairs identified; minimum loss $3,965,247.13.

## Methods and models

OpenSea API data cleaned and joined to transfers; rule-based identification of three wash-trade types.

## Limitations and open questions

Abstract-level read. Detected volume is orders of magnitude below other NFT studies ([[la-morgia-2022-game]], [[niu-2024-unveiling]]), which shows how strongly prevalence estimates depend on the linking heuristic (inferred from comparing abstracts).

## Relevance to us

Wash trading is the market form of a Sybil swarm: one operator controlling several addresses that trade with each other to fake activity. Detection heuristics here (closed cycles between linked addresses, common funders, zero net position change) are the transaction-level analogue of coordination detection for agent swarms. The spread between this and other NFT estimates is itself a finding about detector sensitivity.

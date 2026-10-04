---
id: liu-2026-dataset
type: paper
title: A dataset of early blockchain-registered AI agents on Ethereum
authors:
- Yulin Liu
year: 2026
venue: arXiv preprint (cs)
url: https://arxiv.org/abs/2604.22652
doi: null
arxiv: '2604.22652'
cite: Liu, Y. (2026). A dataset of early blockchain-registered AI agents on Ethereum. arXiv preprint arXiv:2604.22652.
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Data descriptor for a structured dataset of ERC-8004 registered AI agents on Ethereum mainnet. It integrates on-chain identity records, minting transactions, transfer events, reputation summaries and individual feedback records with resolved off-chain metadata where available, collected by Web3 RPC queries over a defined block range and released in tabular form. It covers 10,000 agents and is intended for research on agent identity formation, reputation systems, service exposure and the early agent economy.

## Contribution

A ready-made, reproducible snapshot of early on-chain agent registrations; the only prior empirical ERC-8004 work cited by [[xiong-2026-can]].

## Key results

- 10,000 agents with identity, transfer, reputation and feedback records (Ethereum only).

## Methods and models

RPC event extraction and off-chain metadata resolution into tables.

## Limitations and open questions

Abstract-level read; single author; Ethereum only, which [[xiong-2026-can]] shows is the chain with the most placeholder registrations (53% never set a URI). Download location not checked.

## Relevance to us

Candidate dataset for testing reviewer-swarm detectors (first-funder trees, template entropy) offline before running them on live chains. Found by backward citation from [[xiong-2026-can]].

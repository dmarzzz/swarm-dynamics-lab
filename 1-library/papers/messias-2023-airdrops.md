---
id: messias-2023-airdrops
type: paper
title: 'Airdrops: Giving Money Away Is Harder Than It Seems'
authors:
- 'Johnnatan Messias'
- 'Aviv Yaish'
- 'Benjamin Livshits'
year: 2023
venue: 'arXiv preprint (cs)'
url: https://arxiv.org/abs/2312.02752
doi: null
arxiv: '2312.02752'
cite: 'Messias, J., Yaish, A., & Livshits, B. (2023). Airdrops: Giving Money Away Is Harder Than It Seems. arXiv preprint arXiv:2312.02752.'
topics:
- sybil-resistance
- swarm-detection
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

An empirical study of nine major token airdrops across Ethereum and layer-2 ecosystems. Up to 66% of airdropped tokens in some cases were sold rapidly, often in the recipient's first post-claim transaction, driven largely by airdrop farmers who optimise eligibility criteria. A case study of the Arbitrum airdrop shows short-term activity spikes did not become sustained use. The paper lists design pitfalls including Sybil vulnerability and proposes guidelines.

## Contribution

Measured evidence of Sybil and farmer behaviour in real reward distributions, cited by [[pan-2024-sybil]] as motivation.

## Key results

- Up to 66% of tokens rapidly sold in some airdrops, often in the first post-claim transaction (abstract).
- Nine airdrops studied; Arbitrum case study shows activity spikes without sustained engagement (abstract).

## Methods and models

On-chain data analysis of claim and sale transactions for nine airdrops.

## Limitations and open questions

Abstract-level read; the methods for attributing behaviour to farmers are not recorded here.

## Relevance to us

Airdrops are the largest natural experiment in rewarding identities that cost nothing to create, and agent swarms that pay per-agent participation rewards will see the same farming. Pair with [[yaish-2024-tierdrop]] (harness farmers rather than fight them), [[liu-2022-fighting]] (detection) and the theory in [[pan-2024-sybil]].

## Notes from dmarz/sd-onchain

From the swarm-detection lane: supplies the prevalence side of airdrop farming (up to 66% of tokens sold quickly across nine airdrops, often in the first post-claim transaction), which the detectors [[liu-2025-detecting]], [[bartnicki-2026-compression]], [[zhou-2024-artemis]] and the reported-group measurements in [[luo-2025-toward]] target. Abstract re-read 2026-10-03.

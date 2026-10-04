---
id: harrigan-2018-airdrops
type: paper
title: 'Airdrops and Privacy: A Case Study in Cross-Blockchain Analysis'
authors:
- Martin Harrigan
- Lei Shi
- Jacob Illum
year: 2018
venue: arXiv preprint (cs.CR)
url: https://arxiv.org/abs/1809.05360
doi: null
arxiv: '1809.05360'
cite: 'Harrigan, M., Shi, L., & Illum, J. (2018). Airdrops and Privacy: A Case Study in Cross-Blockchain Analysis. arXiv preprint arXiv:1809.05360.'
topics:
- swarm-detection
- sybil-resistance
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Uses the 2014 Clam airdrop, which gave a new coin to every non-dust address on Bitcoin, Litecoin and Dogecoin, as a natural experiment in cross-chain address clustering. Applying clustering heuristics to each chain individually and in combination, the authors show that address reuse across chains leaks ownership, and find entities whose address ownership on the three source chains is revealed only by their activity on the Clam chain.

## Contribution

Early demonstration that activity on one chain links identities on others, the cross-chain linkage later used to merge Sybil clusters across chains.

## Key results

- Instances where Clam-chain activity alone reveals cross-chain address ownership (no counts in abstract).

## Methods and models

UTXO address-clustering heuristics applied per chain and jointly.

## Limitations and open questions

Abstract-level read; privacy framing, not bot detection.

## Relevance to us

Background for cross-chain merging of operator clusters, as done in [[xiong-2026-can]] (funders merged across Ethereum, BSC and Base).

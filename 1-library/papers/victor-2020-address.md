---
id: victor-2020-address
type: paper
title: Address Clustering Heuristics for Ethereum
authors:
- Friedhelm Victor
year: 2020
venue: Financial Cryptography and Data Security
url: https://fc20.ifca.ai/preproceedings/31.pdf
doi: 10.1007/978-3-030-51280-4_33
arxiv: null
cite: Friedhelm Victor. (2020). Address Clustering Heuristics for Ethereum. Financial
  Cryptography and Data Security, 617-633. https://doi.org/10.1007/978-3-030-51280-4_33
topics:
- swarm-detection
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

This paper adapts entity identification to Ethereum account-based transactions using exchange-deposit reuse, airdrop multi-participation, and authorization patterns. Its abstract reports clustering 17.9% of active externally owned addresses into more than 340,000 likely multi-address entities, with deposit reuse the most effective heuristic.

## Contribution

Adapts entity clustering to account-based Ethereum using deposit-address reuse, airdrop multi-participation and approval patterns.

## Key results

- 17.9% of active externally owned addresses clustered; more than 340K inferred entities.

## Methods and models

Heuristic clustering of four years of Ethereum transactions.

## Limitations and open questions

Clusters indicate likely common control, not verified identity; protocol-independent usage patterns can change over time.

## Relevance to us

Direct on-chain Sybil heuristic: clustered 17.9% of active EOAs into 340K+ entities, with deposit reuse the strongest signal; a ready baseline for linking agent wallets to operators.

## Access provenance

Crossref metadata and the abstract at the recorded URL were opened directly or through Exa content extraction on 2026-10-03. Any non-null citation count is OpenAlex cited_by_count on that date. Abstract depth is deliberate even where an open PDF was found.

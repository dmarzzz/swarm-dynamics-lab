---
id: cernera-2025-blockchain
type: paper
title: 'The Blockchain Warfare: Investigating the Ecosystem of Sniper Bots on Ethereum and BNB Smart Chain'
authors:
- Federico Cernera
- Massimo La Morgia
- Alessandro Mei
- Alberto Mongardini
- Francesco Sassi
year: 2025
venue: ACM Transactions on Internet Technology 25(3)
url: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3736763?fields=title,abstract,venue,year
doi: 10.1145/3736763
arxiv: null
cite: 'Cernera, F., La Morgia, M., Mei, A., Mongardini, A., & Sassi, F. (2025). The Blockchain Warfare: Investigating the Ecosystem of Sniper Bots on Ethereum and BNB Smart Chain. ACM Transactions on Internet Technology, 25(3), 1-29. https://doi.org/10.1145/3736763'
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

Follow-up to [[cernera-2022-token]] focused on sniper bots, automated tools that buy a new token in the first seconds after listing. The authors analyse open-source sniper-bot repositories on GitHub for features and implementation, then build a dataset of Ethereum and BNB Smart Chain liquidity pools to identify sniping operations. They find 352,413 sniping operations on Ethereum and 1,716,917 on BSC, with turnover of $155,630,184 and $137,548,859 respectively; Ethereum snipes succeed more often but need larger investment. They also discuss token-contract countermeasures against snipers.

## Contribution

Population count of a single bot type across two chains, identified by combining code analysis with pool-level on-chain signatures, the same code-to-chain approach later used for Solana in [[zheng-2026-demystifying]].

## Key results

- Sniping operations: 352,413 on Ethereum ($155.6M turnover), 1,716,917 on BSC ($137.5M).
- Higher success rate on Ethereum with larger capital per operation.

## Methods and models

GitHub sniper-bot code review; detection of first-block buys in newly created liquidity pools (details not read).

## Limitations and open questions

Read via the Semantic Scholar abstract record and Crossref metadata; the ACM page returned 403 to my fetcher.

## Relevance to us

Gives measured counts for one specialised automated-agent population and shows how open-source code anchors on-chain identification. Compare [[zheng-2026-demystifying]] and [[szwajcok-2026-meme]].

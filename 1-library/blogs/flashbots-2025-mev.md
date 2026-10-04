---
id: flashbots-2025-mev
type: blog
title: "MEV and the Limits of Scaling"
authors: [Robert Miller]
year: 2025
url: https://writings.flashbots.net/mev-and-the-limits-of-scaling
site: writings.flashbots.net
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Flashbots research post (2025-06-16) arguing that on-chain MEV searching, not raw throughput, is now the binding limit on blockchain scaling. Using traces from OP-Stack rollups, it reports that spam bots used more than 50% of gas while paying under 10% of fees (OP Mainnet: about 57% of gas, about 9% of fees), that almost all of the 11 Mgas/s Base added between November 2024 and February 2025 was consumed by spam, and that one Base bot sent about 350 failing transactions (about 132M gas) per successful arbitrage. It proposes TEE-based "programmable privacy" plus explicit ordering bids to replace the "spam auction".

## Key claims

- Spam is the rational strategy when mempools are private, gas is cheap, transactions are expressive programs, and there is no explicit auction for ordering: competition defaults to buying more lottery tickets in gas.
- Spam was classified by a trace heuristic: no token transfer and at least 4 DEX price reads (slot0, getReserves). The authors state it is trivially gameable by adding a token transfer.
- On Base, spam took about 56% of gas, 26% of L1 DA and 14% of fees over a million blocks in February 2025; effective (non-spam) throughput stayed near 12 Mgas/s while total rose from 15 Mgas/s.
- Searchers rotate the smart contracts they spam from but sweep profits to a stable "profit-taking address". Grouping contracts by that address shows two entities produce more than 80% of spam on Base, where the per-contract view looked fragmented.
- Proposed fix: let searchers read upcoming state inside TEEs that only permit backrunning, and let them bid explicitly for position, so the price of a position is a bid rather than wasted gas.

## Evidence quality

Empirical, vendor-authored analysis. Data come from the authors' own tooling ([[gh-flashbots-spam-inspect]]) and Dune materialised views over OP-Stack chains; methodology is described in an appendix and the threshold sensitivity (3 vs 4 calls) is reported as small. Claims about Solana (40% of blockspace) are cited to third parties and were not checked. The proposed TEE auction is a design argument, not a measured result.

## Relevance to us

This is the clearest measured case in the Flashbots corpus of identity multiplicity used to hide market concentration: many contracts, one operator. Spam here is not a Sybil attack on a vote, but the defence question is the same as for agent swarms: per-identity counts (contracts, addresses, agents) mislead, and attribution has to follow the money (the profit-taking address) or some other unforgeable link. It also shows the economic framing that recurs in Flashbots work: when the cost per attempt is low and there is no explicit price for priority, agents flood the shared resource, and the fix is to price the scarce thing directly rather than to filter identities. Formal treatment of the same dynamic is in [[mazorra-2026-timing]]; the mitigation menu is in [[collective-2024-dealing]]; the identity-blind pricing view connects to [[pan-2024-sybil]] and [[mazorra-2023-cost]].

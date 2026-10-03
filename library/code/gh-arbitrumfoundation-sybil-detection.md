---
id: gh-arbitrumfoundation-sybil-detection
type: code
title: "Arbitrum sybil-detection: methodology repo for removing Sybil clusters from the 2023 ARB airdrop via transfer-graph community detection"
repo: ArbitrumFoundation/sybil-detection
url: https://github.com/ArbitrumFoundation/sybil-detection
authors: ["Arbitrum Foundation"]
year: 2023
language: "none (README and images only)"
license: "none stated"
stars: 271
last_commit: 2024-04-10
topics: [sybil-resistance]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: full
relevance: 4
papers: []
---

## Summary

Describes how the Arbitrum Foundation filtered Sybil addresses from the ARB airdrop eligibility list. Entity addresses (bridges, exchanges, contracts) were removed using Nansen, Hop and Offchain Labs data. Two graphs were built: one with an edge per value transfer, one with an edge per funder (first ETH received) or sweep (last ETH sent) transaction. Graphs were split into strongly and weakly connected components, large components broken up with Louvain community detection, and clusters flagged by patterns such as more than 20 addresses transferring among themselves, a common funder, or similar activity. Example clusters have 56 to 121 eligible addresses. Inputs include the Hop blacklist and eliminatedSybilAttackers list ([[data-hop-sybil-2022]]).

## What it can do for us

A real, large-stakes example of after-the-fact Sybil clustering on behavioural traces, the approach an agent platform would use when identities are free but coordination leaves fingerprints in funding and activity graphs. It contrasts with ex-ante approaches such as [[gh-semaphore-protocol-semaphore]] and staking.

## Run notes

Nothing to run: the repo contains only the README and cluster images, no code or address list.

## Limitations

No code, no data, no false-positive estimate. Depends on proprietary Nansen labels. The final Sybil list is not in this repo.

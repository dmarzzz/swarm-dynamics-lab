---
id: flashbots-2021-flashbots
type: blog
title: "Flashbots Transparency Report — February 2021"
authors: [Stephane Gosselin]
year: 2021
url: https://writings.flashbots.net/transparency-february
site: writings.flashbots.net
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

Monthly Flashbots transparency report (published 2021-03-18) on the first months of Flashbots Alpha, the sealed-bid bundle market between searchers and miners. The Sybil-relevant item is a release note: MEV-Relay v2 dropped API keys and instead required every bundle to be signed with an Ethereum private key, "which allows us to start tracking a searcher's reputation", with a future priority channel for high-reputation searchers. The report also counts a 3x rise in unique searchers who landed bundles.

## Key claims

- Identity moved from issued API keys (gated, rate limited) to self-generated signing keys (free to create), with reputation attached to the key. The January 2021 report ([writings.flashbots.net/transparency-january](https://writings.flashbots.net/transparency-january)) had said the team hoped to "say goodbye to API-keys and remove rate limits".
- The stated motive was adoption: removing API keys was expected to speed up searcher onboarding.
- Reputation would later be used to give high-reputation searchers a priority channel. The May and June 2021 report ([writings.flashbots.net/transparency-may-june](https://writings.flashbots.net/transparency-may-june)) states that a reputation system was then being trialled to handle load, favouring searchers "with a history of successful inclusions", and links the design discussion [[flashbots-2021-proposal]].
- The report frames Flashbots as a market alternative to private trader-miner deals and as a way to avoid paying gas for failed transactions and public gas wars.

## Evidence quality

Operator self-report with headline counts (5 mining pools, over 12% of hashrate, 0.13 ETH per block in Flashbots revenue, 3x unique searchers) and no methodology. The identity change is a factual product change and is reliable as such.

## Relevance to us

A documented design choice that many open agent systems face: replace an allowlist (API keys) with free self-sovereign keys and earn trust per key. The move makes entry permissionless and Sybil identities free, so all Sybil resistance has to come from what a key accumulates (history of landed bundles) rather than from admission. Free keys plus earned reputation is the starting point that the later Flashbots debates on priority queues and key farming react to ([[flashbots-2021-proposal]], [[flashbots-2022-relay]]). For agent swarms, it is a reminder that a reputation layer is only Sybil resistant if the thing that earns reputation (here, paid, landed bundles) costs the attacker more than the priority is worth.

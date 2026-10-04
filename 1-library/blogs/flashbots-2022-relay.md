---
id: flashbots-2022-relay
type: blog
title: "Relay spam protection: require a small deposit to submit blocks as a builder"
authors: [bertmiller]
year: 2022
url: https://github.com/flashbots/mev-boost/issues/219
site: github.com/flashbots/mev-boost (GitHub issue)
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

GitHub issue #219 on flashbots/mev-boost (opened 2022-07-19 by bertmiller, 8 comments) asking how a post-Merge relay should stop builders from flooding it with large, expensive-to-simulate bad blocks. It proposes either reputation scoring with priority queues, as already used on the pre-Merge bundle relay, or a small slashable deposit per builder, and states the goal of permissionless submission with low barriers. Commenters debate manual bootstrapping, capital-based Sybil attacks on deposits, and Rate Limiting Nullifiers.

## Key claims

- Block simulation is costly, so an unprotected relay can be DoSed by many bad blocks; at the limit this harms the whole network.
- Option A: reputation scoring and priority queues. A commenter (jparyani) suggests bootstrapping it manually: promote builders to the high-priority queue only after observing them land profitable blocks, to avoid a chicken-and-egg problem at launch.
- Option B: a stake deposit slashable for malicious behaviour. A builder (jeromelaurens) objects that honest builders will have bugs early and should not be slashed, and that a rich builder can run "many accounts and stakes" and still spam without being seen as one entity, so deposits favour the wealthy.
- A commenter (sambacha) proposes a Rate Limiting Nullifier (RLN) scheme: zero-knowledge membership in a Merkle tree, with each request leaking a Shamir share of the member's key so that exceeding the rate reveals the key and allows removal and slashing. He states that "the sybil problem is still there" because membership has to be bootstrapped from existing Flashbots reputation. The pasted Flashbots reputation formula scores a searcher from landed versus submitted bundles, gas used, gas price and coinbase transfers.
- A later comment (charlescharles) proposes trusting builders' claimed bid values and demoting any builder whose simulated block pays less than claimed, and names the attack: if promotion is too easy, an attacker generates many keys, gets them trusted, then spams the trusted queue at high-MEV times.

## Evidence quality

Design discussion among relay operators and builders; no data. Its value is that the Sybil arguments against stake-only and reputation-only defences are made explicitly by affected parties. The relay that shipped implements a mix of these ideas (high-priority flag, blacklist, collateral for optimistic submission, per-IP rate limits): see [[gh-flashbots-mev-boost-relay]].

## Relevance to us

A clean statement of the three-way trade-off we expect in any open agent swarm that admits newcomers: reputation (cheap for honest agents but slow to bootstrap and gameable by key farming), deposits (capital-weighted, so a wealthy actor can split stake across many identities), and anonymous rate-limiting credentials (privacy-preserving, but still needs a Sybil-resistant admission step). The "many accounts and stakes" objection is the same point formalised for staking in [[chitra-2025-sybil]] and for allocation mechanisms in [[pan-2024-sybil]]. The RLN construction is catalogued as [[gh-rate-limiting-nullifier-circom-rln]]. Earlier design debate: [[flashbots-2021-proposal]].

---
id: barrywhitehat-2019-semaphore
type: blog
title: "Semaphore RLN, rate limiting nullifier for spam prevention in anonymous p2p setting"
authors: ["barryWhiteHat"]
year: 2019
url: https://ethresear.ch/t/semaphore-rln-rate-limiting-nullifier-for-spam-prevention-in-anonymous-p2p-setting/5009
site: Ethereum Research forum (ethresear.ch)
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: skim
relevance: 5
---

## Summary

The original Rate-Limiting Nullifier proposal (posted 18 February 2019). Members deposit currency into a contract and join a Semaphore group (a Merkle tree of identity commitments). Setting the external nullifier to a timestamp epoch restricts each member to one signal per epoch. The construction derives nullifier_private_key = hash(external_nullifier, leaf_private_key), encrypts the leaf key with it, splits it by Shamir secret sharing with a 51% threshold, and reveals a signal-dependent 50% of shares, so two different signals in the same epoch almost certainly expose the full key. The exposed key lets anyone remove the member and slash the deposit (33% to the reporter, 67% burned in the proposal).

## Key claims

- Combines anonymity (Semaphore membership proofs) with rate limiting enforced by self-incriminating double-signals.
- Assumes Sybil resistance at admission is handled elsewhere (for example by the deposit); RLN only enforces the per-epoch rate.
- In the replies, a question about whether a user could manipulate the threshold is answered by noting that the revealed share depends on the signal and is enforced inside the zkSNARK.

## Evidence quality

Design proposal and forum discussion, no implementation or measurements. Read via a summarising fetch, so depth is skim. Later designs use a linear share y = k + a * x per message (as in [[crapis-2026-zk]]); deployed in Waku ([[taheri-boshrooyeh-2022-privacy]]).

## Relevance to us

The seminal primitive for anonymous, stake-backed, rate-limited participation in a P2P swarm. Its explicit separation of "admission cost" (deposit) from "rate enforcement" (nullifier) is the right decomposition for agent swarms: the deposit bounds how many identities a principal can afford, the nullifier bounds what each identity can do per epoch. Used directly by [[crapis-2026-zk]]; library implementations in [[gh-vacp2p-zerokit]] and [[gh-semaphore-protocol-semaphore]].

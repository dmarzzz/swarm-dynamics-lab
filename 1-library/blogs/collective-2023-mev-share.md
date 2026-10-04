---
id: collective-2023-mev-share
type: blog
title: "MEV-Share: programmably private orderflow to share MEV with users"
authors: [bert]
year: 2023
url: https://collective.flashbots.net/t/mev-share-programmably-private-orderflow-to-share-mev-with-users/1264
site: collective.flashbots.net (Flashbots forum)
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: skim
relevance: 4
---

## Summary

The original MEV-Share design post (2023-02-15, by the forum user bert) for a permissionless, private matchmaker between users and searchers: users share selected hints about their transactions, searchers send backrun bundles, and validity conditions require builders to pay a share of the MEV back to users. Two passages concern identity. The matchmaker is exposed to DDoS because it is permissionless and simulation-heavy, and batching user transactions fails because a searcher can pose as a user.

## Key claims

- Design goal: permissionless for searchers, with "no exclusivity deals or allow lists".
- "Preventing DDOS": the matchmaker needs a defence; listed options are reputation (as the Flashbots builder already used), payment from searchers per bundle, or other requirements on searchers.
- Batching user transactions could create MEV no single transaction does, but "there is no way to distinguish between a regular user's transaction and a searcher posing as a user"; searchers could insert transactions into batches to capture value. Filtering is possible but computationally expensive.
- The matchmaker starts as a trusted Flashbots-run role, partly because of the sequential auction problem between competing OFAs.

## Evidence quality

Design document with community Q and A; no measurements. Later Flashbots work adds a formal privacy layer for hints with an explicit Sybil analysis ([[passerat-palmbach-2025-differentially]]).

## Relevance to us

The "searcher posing as a user" problem is the general form of a Sybil attack on any mechanism that pays out to a class of participants (users, contributors, voters) whose membership cannot be verified. A refund or reward scheme that pools contributions from many identities invites an adversary to add its own identities to the pool. For agent swarms that share rewards across contributors, the options shown here are the same: price each action (per-bundle payment), track history (reputation), or design the payout so that adding identities does not raise the total paid to one controller ([[buildernet-2025-refunds]], [[mazorra-2023-cost]]).

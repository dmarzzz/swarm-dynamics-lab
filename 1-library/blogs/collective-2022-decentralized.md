---
id: collective-2022-decentralized
type: blog
title: "Decentralized order flow distributer (DOFD)"
authors: [josojo]
year: 2022
url: https://collective.flashbots.net/t/decentralized-order-flow-distributer-dofd/731
site: collective.flashbots.net (Flashbots forum)
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

Forum proposal (November 2022) by josojo for a decentralised order flow distributor: users encrypt transactions to DKG keys held by a node network, which reveals them each block to a random subset of allowlisted, bonded builders, and releases signatures only after the proposer commits. Misbehaving builders would be slashed. In the replies the forum user Quintus raises a Sybil objection: a builder with a large stake split across "many sybils" could capture the flow, and some misbehaviour cannot be attributed because one searcher can act through several accounts.

## Key claims

- Builders must be allowlisted by governance and post collateral, possibly via restaking, so they can be slashed for rule breaks such as sandwiching.
- Each block, order flow goes to a random subset of allowlisted builders so that weaker builders still win sometimes.
- Objection 1 (Quintus): flow could be "captured" by a builder who puts down "an enormous stake with many sybils", because random selection over identities weighted by stake rewards splitting.
- Objection 2 (Quintus): some rules are not falsifiable. A sandwich is indistinguishable from three unrelated orders if "a user is being sandwiched by two accounts owned by the same searcher".
- The author's reply: "a mixture of required staked capital and anonymous reputation" could make Sybil attacks practically hard, and slippage-based rules could make front-running falsifiable.

## Evidence quality

Design proposal and discussion, no implementation or data. The Sybil points are qualitative but precise.

## Relevance to us

Two lessons for agent collectives. First, random committee selection among identities is only Sybil resistant if the selection weight (stake) cannot be split to buy more tickets, which is exactly the property studied in [[pan-2024-sybil]] and [[chitra-2025-sybil]]. Second, rules defined over the behaviour of separate identities (do not trade against your own user) are unenforceable when one actor controls several identities, so detection has to rely on outcome-level checks (price bounds) rather than on who acted. Related identity-aggregation evidence: [[flashbots-2025-mev]].

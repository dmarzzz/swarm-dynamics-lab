---
id: collective-2024-dealing
type: blog
title: "Dealing with spam caused by on-chain searching"
authors: [Quintus]
year: 2024
url: https://collective.flashbots.net/t/dealing-with-spam-caused-by-on-chain-searching/3381
site: collective.flashbots.net (Flashbots forum)
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Flashbots forum thread (May 2024) started by the forum user Quintus collecting ideas for chains such as Base and Solana where searchers fire very many transactions that usually revert and only occasionally capture an opportunity. Assuming the sequencer is not the bottleneck but blockspace is, it proposes two families of fixes: separate resources with a paid non-reverting endpoint, or give the sequencer more information so it can run an auction. Replies discuss raising gas for reverting transactions and making spam disproportionately costly for spammers.

## Key claims

- Likely drivers of spam: cheap gas and high uncertainty, from low latency or private mempools.
- Idea 1, separating resources: an opt-in RPC endpoint where transactions can never revert (reverting ones are dropped before propagation). To stop that endpoint from being flooded, each transaction must carry a payment in a payment channel to the sequencer, priced below gas; the alternative, "the reputation systems which builders deploy today", is described as "less clean".
- Idea 2, more information: a transaction type that declares the state conditions under which it should be simulated (for example a pool price move), with only the top-k payers executed when the condition fires; or just-in-time exposure of flow with MEV-Share style privacy.
- In replies, the author agrees reverting transactions can pay more per gas but warns that pushing it too far invites workarounds that punish normal users. Another participant (Thogard) points to raising spam cost disproportionately for spammers.

## Evidence quality

Idea collection and discussion, no measurements. Later Flashbots work quantifies the problem ([[flashbots-2025-mev]]) and models it ([[mazorra-2026-timing]]).

## Relevance to us

A compact catalogue of defences against cheap repeated actions by many agents that does not depend on identifying who they are. Per-message payment channels and conditional execution price the action rather than the identity, which is the robust option when identities are free. Reputation is mentioned as the fallback and judged worse. For agent swarms that share an expensive resource (a judge model, a simulator, a tool API), the transferable pattern is to put a small, non-refundable price on each attempt before the bottleneck and to let agents declare triggers instead of polling. See also [[flashbots-2021-proposal]] for the earlier relay-level version of the same trade-off.

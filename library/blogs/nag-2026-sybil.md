---
id: nag-2026-sybil
type: blog
title: "Sybil Attacks on Auction Based Inclusion Lists (AUCIL)"
authors: [Abhimanyu Nag]
year: 2026
url: https://functor.network/user/3197/entry/1845
site: functor.network (announced on ethresear.ch at https://ethresear.ch/t/sybil-attacks-on-aucil/25447)
topics: [sybil-resistance, collective-decision]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Blog post (9 June 2026, cross-posted to ethresear.ch on 12 July 2026) asking where Sybil attacks enter AUCIL, the auction-based inclusion-list design of Wadhwa et al. (2025) for censorship resistance under proposer-builder separation. AUCIL assigns transactions to a committee of inclusion-list proposers by a greedy algorithm that reaches a correlated equilibrium robust to individual deviations, then aggregates lists through a scoring auction with VRF-generated bias. The post gives a two-transaction example in which the allocation is incentive compatible for every single proposer but not for an attacker controlling two proposer identities: one identity switches transactions at a personal loss, raising the other identity's fee share, and the number of input lists covering one transaction falls. Because controlled identities can omit a transaction for free, the paper's lower bound on the cost of guaranteed censorship no longer holds. The author contrasts this with FOCIL, whose committee selection is Sybil resistant by stake, and suggests stake-based fee partitions and a stake-weighted lottery in place of the VRF sample.

## Key claims

- Incentive compatibility against individual deviations does not imply Sybil-proofness; joint deviations by identities of one principal can be profitable even when each identity loses.
- A Sybil attacker in AUCIL can reduce transaction coverage without any external bribe, lowering the cost of censorship.
- Stake-proportional fee shares could remove the gain from splitting.

## Evidence quality

Short analytical note with one worked example; the general theory is left open by the author. Several formulas did not render in the copy I read, so I rely on the prose for the example. It cites Wadhwa et al. 2025 (AUCIL) and Stouka, Ma and Thiery 2025 (arXiv 2505.13751) on bribery in FOCIL, neither of which I opened.

## Relevance to us

The general lesson carries straight to multi-agent mechanisms: checking that no single agent gains by deviating is not enough when one operator runs several agents. Any committee, voting or task-allocation scheme for agent swarms needs a coalition-of-identities check, and fee or reward shares that are proportional to a scarce resource rather than per identity. Related: Sybil-proofness of block-space allocation [[neuder-2024-block]], convex rewards against splitting [[bahrani-2026-capacity]].

Formal background on Sybil-proofness in block-building mechanisms: [[pan-2024-sybil]].

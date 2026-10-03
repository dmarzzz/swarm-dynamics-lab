---
id: neuder-2024-block
type: blog
title: "On block-space distribution mechanisms"
authors: [Mike Neuder, Pranav (surname not given in the post), Tim Roughgarden]
year: 2024
url: https://ethresear.ch/t/on-block-space-distribution-mechanisms/19764
site: ethresear.ch
topics: [sybil-resistance, collective-decision]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

Long forum post (8 June 2024, "by Mike, Pranav, & Dr. Tim Roughgarden") that maps the design space for how Ethereum sells block-production rights (who, what, when, where, how) and then analyses allocation rules for execution tickets. Under a fixed-price, unlimited-quantity ticket sale, two rules are compared: Proportional-all-pay (win probability b_i / Σb_j, everyone pays their bid, a Tullock contest) and Winner-take-all (the current PBS auction). In a two-player example with values 4 and 2, Proportional-all-pay gives bids 8/9 and 4/9, allocations 2/3 and 1/3, revenue 4/3 and fairness (geometric mean of allocations) about 0.471; Winner-take-all gives revenue about 2 and fairness 0. The authors restrict attention to Sybil-proof mechanisms, where a player gains nothing by splitting a bid across identities, and pose as an open problem whether Proportional-all-pay is an optimal Sybil-proof mechanism trading MEV-oracle accuracy against fairness, and whether Tullock rules x_i = b_i^α / Σ b_j^α with α > 1 could do better.

## Key claims

- In a permissionless setting only Sybil-proof allocation mechanisms are admissible.
- There is a trade-off between the accuracy of an in-protocol MEV oracle (revenue) and fairness of allocation.
- Proportional-all-pay is Sybil-proof because splitting a bid into pieces leaves the total win probability and payment unchanged (my reading of the proportional rule; the post states the constraint, it does not prove optimality).

## Evidence quality

Framework and worked examples with equilibrium derivations; no data. I read the framing, the model, the two-player comparison and the conclusions, and skimmed the equilibrium asides.

## Relevance to us

For allocating tasks or rewards among agents, this post states the constraint compactly: an allocation rule must be invariant to an agent splitting itself, and the obvious fair rule (proportional) is Sybil-proof while superlinear rules (α > 1, winner-take-all as the limit) reward concentration. Note the tension with [[bahrani-2026-capacity]], where convex rewards are used on purpose to make splitting unprofitable; together they bracket the design: linear is splitting-neutral, convex discourages splitting but favours large players. Related: coalition-of-identities failure in [[nag-2026-sybil]].

The formal characterisation of Sybil-proof mechanisms in this setting is [[pan-2024-sybil]].

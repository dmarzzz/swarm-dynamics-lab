---
id: charbonneau-2023-suave
type: blog
title: "SUAVE Economic Security Models"
authors: [Jon Charbonneau; replies by Hasu and Yuki Yuminaga]
year: 2023
url: https://collective.flashbots.net/t/suave-economic-security-models/1070
site: collective.flashbots.net (Flashbots forum)
topics: [sybil-resistance]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: full
relevance: 2
---

## Summary

Forum post (22 January 2023, thread of 5 posts to 26 February 2023) by an outside analyst on how the proposed SUAVE chain should secure its validator set. Quoting Flashbots, SUAVE would use bridged ETH as its native token and pay validators from network fees. The author argues a standalone L1 staked with bridged ETH would attract almost no stake, because the opportunity cost is Ethereum staking yield (about 16 million ETH staked at about 7.5% at the time) while SUAVE fees would be thin, and that a successful SUAVE L1 would be parasitic on Ethereum's security. He compares six options (rollup, EigenLayer restaking, a SUAVE-specific restaking fork, bridged liquid staking tokens, an inflationary subsidy, a Flashbots-paid subsidy) and prefers a rollup. Hasu, writing as part of the SUAVE team ("we are investigating"), replies that rollup security benefits matter little to SUAVE, that any ETH-based staking would realistically be staked ETH or restaking, and that chain security was "simply not a priority right now".

## Key claims

- Stake-based validator security requires that the stake's opportunity cost be covered; otherwise "an incredibly small amount of ETH should rationally be bridged".
- Restaking lets applications cap leverage (for example, only restakers not securing other applications), trading a higher collusion bar against lower stake.
- Flashbots' stated priority was transaction types and programmable privacy, with consensus security deferred.

## Evidence quality

Opinion and back-of-envelope economics with figures quoted from public data at the time; the SUAVE design has since changed (the TEE coprocessor line in [[miller-2024-sirrah]]). Author disclosure: no financial stake in Flashbots, a small personal stake in EigenLayer.

## Relevance to us

Background on the stake side of the Flashbots design space. Stake is the classic economic Sybil bound for validator sets (cost per identity equals locked capital), and this thread shows why Flashbots moved away from building it: the capital cost is hard to bootstrap, which pushes toward borrowed security or toward attestation as the admission rule ([[quintus-2023-problems]]). For agent swarms, it is a reminder that a stake-based identity bound has an ongoing opportunity cost that someone must pay, and that restaking reuses the same capital across systems, which weakens the per-system bound. Foundations of resource-based Sybil cost: [[douceur-2002-sybil]], [[aspnes-2005-exposing]].

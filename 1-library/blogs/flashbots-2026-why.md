---
id: flashbots-2026-why
type: blog
title: "Why Location Choice Matters"
authors: [Burak Öz, Fei Wu, Luis Correia, Sen Yang, Bruno Mazorra, Stefanos Leonardos]
year: 2026
url: https://writings.flashbots.net/why-location-choice-matters
site: writings.flashbots.net
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: skim
relevance: 2
---

## Summary

Flashbots research post (2026-08-09) summarising the paper "The Price of Decentralization in Block Building". It models multiple concurrent proposer (MCP) block building as a stochastic coverage game: builders choose geographic regions, transaction sources emit transactions during a round, and a builder covers a transaction if it arrives before the deadline. It studies whether self-interested location choices serve geographically spread users, and closes with open problems, one of which is explicitly Sybil behaviour among builders.

## Key claims

- Censorship resistance in MCP rests on "N proposers, one honest one suffices", but latency from a user to the nearest proposer can undo this, more so as block times shrink.
- Under the equal-split reward rule they adopt, only builders that include a transaction share its reward; the post lists alternative rules (winner-takes-all, committee-level sharing, Tullock-style proportional sharing) with different welfare and fairness effects.
- Open problem stated by the authors: depending on the reward-sharing rule, builders may form coalitions to avoid redundant coverage; such coalitions "can improve welfare, but also undermine the censorship-resistance benefits of decentralized block building by behaving as a single economic entity".

## Evidence quality

Summary of a theory and simulation paper with stylised source locations; the authors flag the need for empirical calibration of order-flow geography. The Sybil point is a stated future direction, not a result. The underlying paper was not read for this entry.

## Relevance to us

This is the inverse Sybil problem: not one actor posing as many, but many nominally independent proposers acting as one. Multi-proposer designs assume N independent agents; the reward-sharing rule decides whether coordinating into one economic entity pays. Agent swarms that rely on k-of-N redundancy for robustness have the same exposure, and the identity question is whether N counts operators or keys. Related: the identity-merging constraint in [[buildernet-2025-refunds]], the coalition and bidding-ring results in [[mazorra-2023-cost]], and the impossibility for non-winner-take-all allocation in [[pan-2024-sybil]].

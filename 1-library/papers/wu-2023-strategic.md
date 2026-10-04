---
id: wu-2023-strategic
type: paper
title: "Strategic Bidding Wars in On-chain Auctions"
authors: ["Fei Wu", "Thomas Thiery", "Stefanos Leonardos", "Carmine Ventre"]
year: 2023
venue: "arXiv preprint (Semantic Scholar lists International Conference on Blockchain)"
url: https://arxiv.org/abs/2312.14510
doi: null
arxiv: "2312.14510"
cite: "Wu, F., Thiery, T., Leonardos, S., & Ventre, C. (2023). Strategic Bidding Wars in On-chain Auctions. arXiv preprint arXiv:2312.14510."
topics: [sybil-resistance, marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "35 (Semantic Scholar, 2026-10-03)"
code: [gh-m1kuw1ll-mmasim]
---

## Summary

Builds a game-theoretic model of the MEV-Boost auction and simulates builders using bidding strategies seen in practice (naive, adaptive, last-minute, bluff) with public mempool and private exclusive-order-flow signals, global relay delay of 10 to 200 ms, per-builder delay of 10 to 40 ms and random auction end, running 10,000 auctions per setting. Latency shapes outcomes (adaptive win rate falls about 1.45% per 10 ms of global delay), but access to exclusive order flow matters far more than small latency gains.

## Contribution

The first agent-based study of builder strategies in the MEV-Boost auction, with released simulation code, linking latency and order-flow access to win rates, profit and auction efficiency.

## Key results

- Adaptive builders' win rate falls about 1.45% per 10 ms increase in global delay (profile 1).
- A 10 ms latency advantage gives about 0.26% higher win rate; auction efficiency falls 0.07% per 10 ms of delay.
- Last-minute bidders gain 7.45% plus or minus 1.75% when revealing under 50 ms before the end; with random end time they miss about half the time.
- Increasing exclusive order flow access gives gains that outweigh 10 ms latency improvements.
(Numbers from a tool-generated summary of the arXiv HTML; spot-check before quoting.)

## Methods and models

Discrete 10 ms steps; Poisson public and private signals with log-normal values; auction end Gaussian around 12 s; 12 builders; Mesa implementation (MMASim).

## Limitations and open questions

Assumes constant, known latencies and honest proposers; calibrated to earlier empirical analysis rather than validated against relay data. No notion of builder identity, so one operator running several builders is not modelled.

## Relevance to us

Baseline ABM for Flashbots-side experiments; the missing identity layer (builder Sybils, collusion) is exactly what the lab could add. We ran the code: [[gh-m1kuw1ll-mmasim]].

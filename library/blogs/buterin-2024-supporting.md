---
id: buterin-2024-supporting
type: blog
title: "Supporting decentralized staking through more anti-correlation incentives"
authors: [Vitalik Buterin]
year: 2024
url: https://ethresear.ch/t/supporting-decentralized-staking-through-more-anti-correlation-incentives/19116
site: ethresear.ch
topics: [sybil-resistance, sync-consensus, swarm-detection]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Forum post (26 March 2024), labelled preliminary research with code at github.com/ethereum/research/tree/master/correlation_analysis. The idea: a single large actor that splits its stake across many nominally separate validator identities will still tend to fail at the same time, because its validators share machines and internet connections. Penalising failures more when many others fail in the same slot therefore penalises hidden common control without needing to identify it. Using attestation data and a mapping of validators to publicly known clusters (for example Lido, Coinbase), the post counts co-failures within clusters against three baselines and finds consistently more correlated failures than expected; for example, using the "fake clusters" baseline, 14,868,318 actual fumble co-failures against 8,366,846 expected. The strawman rule: penalty for a missed attestation proportional to p = misses in this slot divided by the average over the previous 32 slots, capped at 4. In simulation this cut the big-staker advantage over small stakers from about 1.4x to about 1.3x (1.2x to 1.1x on the single-slot dataset).

## Key claims

- Splitting into many identities does not hide shared infrastructure; correlated failures are a measurable signature of common control.
- An anti-correlation penalty has no strategy where failing lowers your own penalty, and moving the 32-slot average requires many failures yourself.
- A big staker can escape only by giving each validator independent infrastructure, which removes its economies of scale.
- Political decentralization cannot be incentivised in protocol; the target is architectural decentralization.

## Evidence quality

Empirical analysis on real attestation data with published code, plus a simulated penalty rule. The author asks for independent replication; cluster labels come from a public dataset and cover only known operators. Safety of the rule against strategic manipulation is listed as open.

## Relevance to us

This is the strongest Flashbots-adjacent example of Sybil detection by behaviour rather than by identity: you cannot see that 1,000 identities share an owner, but you can see that they fail together, and you can price that. For agent swarms the analogue is penalising or down-weighting agents whose errors, outages or outputs co-vary beyond chance, which catches many agents run by one operator, one model checkpoint or one prompt. The co-failure versus fake-cluster baseline method is directly reusable as a detection statistic. It connects to the convex anti-splitting rewards in [[bahrani-2026-capacity]], to infrastructure monoculture in [[eigenphi-2025-buildernet]], and to the wash-versus-Sybil distinction in [[glynn-2026-wash]] (correlation detects common control, not fake value).

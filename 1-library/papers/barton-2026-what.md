---
id: barton-2026-what
type: paper
title: 'What LLM Trading Agents Actually Do in Production: A Six-Month, Population-Scale Record from Two Fleets'
authors:
- T. J. Barton
- Chris Constantakis
- Patti Hauseman
- Annie Mous
- Alaska Hoffman
- Brian Bergeron
- Hunter Goodreau
year: 2026
venue: arXiv preprint (cs)
url: https://arxiv.org/abs/2609.05663
doi: null
arxiv: '2609.05663'
cite: 'Barton, T. J., Constantakis, C., Hauseman, P., Mous, A., Hoffman, A., Bergeron, B., & Goodreau, H. (2026). What LLM Trading Agents Actually Do in Production: A Six-Month, Population-Scale Record from Two Fleets. arXiv preprint arXiv:2609.05663.'
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Operator-side measurement of two production fleets of LLM trading agents sharing one design lineage: DX Terminal Pro (3,505 user-funded vaults trading real ETH in Base memecoin markets for 21 days, February to March 2026) and the DXAP live alpha fleet (500-599 user-created agents, 91-117 concurrently active, trading Hyperliquid perpetuals, June to August 2026). The record covers about 7.5M model invocations, about 300K on-chain actions, and 231,638 multi-tool turns producing 14,596 fills. The operating layer drives behaviour more than strategy text: a risk slider explains leverage (+0.425 per level), agent fixed effects absorb 60% of variance, and a leaderboard cut-off causally routes selection (regression discontinuity 1.75x). Median leverage is 5.0x in every volatility sextile, and neither fleet shows directional edge (DXAP 41% vs 50% round-trip win rate for matched retail).

## Contribution

A rare ground-truth population of known LLM agents acting on chain, with behavioural regularities (volatility-blind sizing, slider-determined leverage, leaderboard-routed selection) that are candidate fingerprints for spotting LLM-agent fleets from the outside.

## Key results

- 3,505 vaults and up to 599 agents; about 300K on-chain actions from about 7.5M model calls.
- Leverage +0.425 per risk-slider level; agent fixed effects explain 60% of variance.
- Median leverage 5.0x in every volatility sextile; one slider cell holding 11% of the book accounts for 62% of liquidations.
- 43.2% of positions saw at least +300 bps favourable excursion within 24 h, yet 49.3% of those closed negative.
- Paired replay across frontier models on 416 scenarios: decision quality statistically indistinguishable, choice stability differs by model family.

## Methods and models

Continuous logging from the operator's systems; day-clustered inference, permutation nulls, regression discontinuity at the leaderboard top-3 boundary, common-fee restatement; replay league over captured production scenarios.

## Limitations and open questions

Authors are the operators, so independence is limited; read at abstract level only. Whether the behavioural regularities would identify these agents from public chain data alone is not tested (inferred possibility, not a result).

## Relevance to us

Useful as labelled positives: if we want to know what LLM agent fleets look like on chain, this is a documented fleet with timestamps and venues (Base memecoins, Hyperliquid). Compare unverifiable agent claims in [[yu-2026-paper]] and bot fingerprints in [[zheng-2026-demystifying]].

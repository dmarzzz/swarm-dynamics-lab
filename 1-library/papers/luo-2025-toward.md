---
id: luo-2025-toward
type: paper
title: 'Toward Resilient Airdrop Mechanisms: Empirical Measurement of Hunter Profits and Airdrop Game Theory Modeling'
authors:
- Junliang Luo
- Hong Kang
- Shuhao Zheng
- Xue Liu
year: 2025
venue: arXiv preprint (cs.GT)
url: https://arxiv.org/abs/2503.14316
doi: null
arxiv: '2503.14316'
cite: 'Luo, J., Kang, H., Zheng, S., & Liu, X. (2025). Toward Resilient Airdrop Mechanisms: Empirical Measurement of Hunter Profits and Airdrop Game Theory Modeling. arXiv preprint arXiv:2503.14316.'
topics:
- swarm-detection
- sybil-resistance
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: null
code: []
---

## Summary

Measures community-reported airdrop hunter groups in two airdrops and models the incentives around them. Hop Protocol: 150 validated GitHub-issue groups covering 3,551 addresses; LayerZero: 198 groups covering 7,681 addresses from LayerZero's sybil-report repository (127M transactions). The authors formalise three hunter signatures: a shared initial funder or common cross-chain receiver, sequential bridging of near-equal value within 30 minutes, and uniform transaction counts and volumes across a group's wallets. In Hop, 83 of 150 groups have one funder covering over 80% of addresses and 61 have one funder covering all; 100 groups show count uniformity for 80% of transactions. Expected-profit modelling finds 69.3% of Hop groups would have profited had they not been disqualified, mostly under $10k per group and under $350 per address. A four-stage game with self-reporting and contract-theoretic bounty hunters gives closed-form optimal self-report and bounty reward ratios.

## Contribution

Turns public Sybil-report repositories into a measured catalogue of farm behaviour and an incentive model for crowd-sourced detection, which is the only detection mechanism the two airdrops actually used at scale.

## Key results

- Hop: 83/150 groups have an initial funder covering over 80% of group addresses; 46/150 have a common receiver over 80%; 74/150 have over half their addresses in sequential transfers.
- Sequential-transfer spikes in Hop line up with airdrop rumours (December 2021 to January 2022); LayerZero spike follows the December 2023 announcement, with lower value per transfer.
- LayerZero hunters average 129 transactions per address; 161/198 groups have over half their addresses in sequential transfers; counts are uniform but USD volumes are not.
- Hop expected profit: 104/150 groups positive; top per-address expected reward $341.

## Methods and models

Transaction extraction across Ethereum, Optimism, Arbitrum, Polygon and xDai for Hop; LayerZero-provided transfers. Pattern algorithms with thresholds (1% value, 30-minute window, count and volume tolerances). Profit model from Hop's published reward formula (base amount, early-bird and volume multipliers) minus gas and bridge fees. Sequential game: organiser sets self-report ratio, attackers choose to self-report, organiser offers a menu of contracts to bounty hunters with private detection capability.

## Limitations and open questions

Only reported groups are analysed, so prevalence among all participants is not estimated and the patterns describe what reporters could find. LayerZero receiver attribution is approximate. The game-theoretic results are not calibrated to data.

## Relevance to us

Bounty-hunter reporting is a working example of crowd-sourced swarm detection with an incentive design, applicable to agent-swarm reporting programmes. The three signatures (common funder, synchronised near-equal transfers, cross-wallet uniformity) are the baseline rules any on-chain agent-swarm detector should beat. Data reused by [[bartnicki-2026-compression]]; related: [[messias-2023-airdrops]], [[yaish-2024-tierdrop]], [[liu-2022-fighting]].

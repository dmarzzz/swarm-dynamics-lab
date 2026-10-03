---
id: al-chami-2025-quest
type: paper
title: 'Quest Love: A First Look at Blockchain Loyalty Programs'
authors:
- Joseph Al-Chami
- Jeremy Clark
year: 2025
venue: arXiv preprint (cs)
url: https://arxiv.org/abs/2501.18810
doi: null
arxiv: '2501.18810'
cite: 'Al-Chami, J., & Clark, J. (2025). Quest Love: A First Look at Blockchain Loyalty Programs. arXiv preprint arXiv:2501.18810.'
topics:
- swarm-detection
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

Measurement of a proprietary blockchain quest (loyalty) system: 43 quests over 10 months with 80M completions. Completion correlates most strongly with cost, which the authors read as cost-minimising behaviour typical of Sybils or bots; adding a minimum-token-holding threshold produced an immediate and lasting drop in completions. The authors have no ground truth separating humans from bots, but propose three design heuristics to expose automation: alternate a quest between slightly unprofitable and slightly profitable and watch who reacts at the exact crossover, require holding thresholds and watch for addresses that hold exactly the minimum, and observe reaction speed to randomly timed reward-pool refills (the $500 daily pool depleted faster each day).

## Contribution

Turns incentive design into an active probe for bots: quests built so that automated cost-minimisers reveal themselves, a mechanism-level cousin of honeypots.

## Key results

- 80M completions across 43 quests; cost is the strongest correlate of completion.
- Token-holding thresholds coincided with an immediate, sustained fall in completions.
- Daily $500 reward pool depleted progressively faster (suggestive, confounded by Cloudflare rate-limiting and claim batching).

## Methods and models

Correlation analysis of completion against reward, monetary value, difficulty and cost; before/after threshold comparison; stakeholder analysis.

## Limitations and open questions

No bot ground truth; single platform; the probes are proposals, not evaluated. Skimmed.

## Relevance to us

The profitability-crossover and exact-threshold probes are cheap, deployable traps for automated agents in any incentive system. Pairs with the farmer economics in [[yaish-2024-tierdrop]] and the stakeholder tension it names (projects tolerate farming), echoed in [[messias-2023-airdrops]].

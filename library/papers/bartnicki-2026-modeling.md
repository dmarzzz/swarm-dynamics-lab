---
id: bartnicki-2026-modeling
type: paper
title: 'Modeling Decisions in Blockchain Analytics: A Leakage-Aware Evaluation of Tree-Based vs. Sequential Models'
authors:
- Michał Bartnicki
- Jarosław A. Chudziak
year: 2026
venue: arXiv preprint (cs)
url: https://arxiv.org/abs/2607.27350
doi: null
arxiv: '2607.27350'
cite: 'Bartnicki, M., & Chudziak, J. A. (2026). Modeling Decisions in Blockchain Analytics: A Leakage-Aware Evaluation of Tree-Based vs. Sequential Models. arXiv preprint arXiv:2607.27350.'
topics:
- swarm-detection
- sybil-resistance
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Companion to [[bartnicki-2026-compression]]: classifies Ethereum wallets as organic users, Sybil bots or MEV bots using a Transaction Grammar (rhythm, EVM execution structure, intent) and a Blind-Spot protocol that removes high-signal contracts that leak labels. It compares Transformer and BiLSTM sequence models with XGBoost and SVM and asks whether order or timing carries more signal. Under leakage-aware evaluation, XGBoost outperforms Transformer sequence models while having lower latency and estimated energy use.

## Contribution

A negative result for deep sequence models in on-chain bot classification once shortcut leakage is removed.

## Key results

- XGBoost beats Transformer and BiLSTM under leakage-aware evaluation (numbers not in abstract).

## Methods and models

Same Hop-derived dataset and grammar as the companion paper; tabular vs sequential model comparison.

## Limitations and open questions

Abstract-level read.

## Relevance to us

Caution that reported gains from deep models on bot detection may be leakage; see [[bartnicki-2026-compression]] for the numbers on the same data.

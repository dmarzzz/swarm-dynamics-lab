---
id: niedermayer-2024-detecting
type: paper
title: Detecting Financial Bots on the Ethereum Blockchain
authors:
- Thomas Niedermayer
- Pietro Saggese
- Bernhard Haslhofer
year: 2024
venue: Companion Proceedings of the ACM Web Conference 2024 (WWW '24 Companion)
url: https://arxiv.org/abs/2403.19530
doi: 10.1145/3589335.3651959
arxiv: '2403.19530'
cite: Niedermayer, T., Saggese, P., & Haslhofer, B. (2024). Detecting Financial Bots on the Ethereum Blockchain. In Companion Proceedings of the ACM Web Conference 2024 (WWW '24 Companion), Singapore. ACM. https://doi.org/10.1145/3589335.3651959
topics:
- swarm-detection
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: null
code: []
---

## Summary

Builds a taxonomy of financial bots on Ethereum (7 categories, 24 subcategories: MEV, CEX, DEX, NFT, play-to-earn, general purpose, non-attributable) and a hand-labelled ground truth of every EOA that sent a transaction in two blocks of a 100,000-block window (September 2022): 137 bots and 133 humans, Cohen's kappa 0.77 between annotators. From 83 per-wallet features it clusters with GMM (purity 82.6% at 30 clusters) and classifies with Random Forest (accuracy 0.83, precision 0.87, recall 0.77, 20-fold CV). Most informative features are hour-of-day entropy of outgoing transactions, transactions per block, frequency, maximum gas price and a new 'gap-based sleepiness' feature (longest gap per two-day window).

## Contribution

The first ML bot-versus-human detector for Ethereum with an annotated ground truth and released code and data, and a measured snapshot base rate: just over half of transaction-sending EOAs in the sampled blocks were bots.

## Key results

- Base rate: 137 of 270 sending EOAs (51%) in the two annotated blocks were labelled bots; the authors note sampling by block over-represents highly active addresses.
- Binary classification: RF accuracy 0.83 (CI 0.77-0.88), AdaBoost 0.83, gradient boosting 0.82.
- Four-class MEV task (arbitrage, sandwich, liquidation, non-MEV; 111 each, labelled by mev-inspect): RF accuracy 0.77; liquidation 93% correct, sandwich only 68%.
- Sleep-gap feature: low values (no human-length gaps) push predictions to Bot.

## Methods and models

Erigon archive node via GraphSense; Etherface for selector decoding; Etherscan for annotation context. Features: address (leading zeros, digit entropy), transaction timing and gas, Benford and round-number tests on values, Uniswap-modelled swap calls and events. k-means and GMM fitted on unlabeled wallets and scored on the labelled set; RF, AdaBoost, XGBoost with 20-fold CV; SHAP for attribution. Code: github.com/Tommel71/Ethereum-Bot-Detection.

## Limitations and open questions

Tiny labelled set (270), single short window, no held-out test beyond CV. The multiclass MEV labels come from mev-inspect, so the classifier can only reproduce rule-based labels. 'Bot' is defined as any EOA that sent one software-compiled transaction, which merges benign infrastructure (exchange hot wallets) with predatory bots.

## Relevance to us

Gives a hard number for how much on-chain activity is automated and a feature set (timing entropy, sleep gaps, gas behaviour) that transfers to detecting any always-on agent. The sleep-gap feature is the on-chain version of circadian tests for social bots. Successor work: [[bendada-2025-botdetect]], [[bartnicki-2026-compression]]; earlier heuristic: [[zwang-2018-detecting]].

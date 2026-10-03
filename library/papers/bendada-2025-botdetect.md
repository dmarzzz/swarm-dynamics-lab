---
id: bendada-2025-botdetect
type: paper
title: 'BotDetect: A Decentralized Federated Learning Framework for Detecting Financial Bots on the EVM Blockchains'
authors:
- Ahmed Mounsf Rafik Bendada
- Abdelaziz Amara Korba
- Mouhamed Amine Bouchiha
- Yacine Ghamri-Doudane
year: 2025
venue: arXiv preprint (cs)
url: https://arxiv.org/abs/2501.12112
doi: null
arxiv: '2501.12112'
cite: 'Bendada, A. M. R., Korba, A. A., Bouchiha, M. A., & Ghamri-Doudane, Y. (2025). BotDetect: A Decentralized Federated Learning Framework for Detecting Financial Bots on the EVM Blockchains. arXiv preprint arXiv:2501.12112.'
topics:
- swarm-detection
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Proposes BotDetect, a decentralised federated learning framework for detecting financial bots across EVM chains (Ethereum, BNB Smart Chain, and others). Each participating node trains a local model on transaction history and smart-contract interaction data, and model updates are aggregated on chain through smart contracts under a permissioned consensus, so raw data are not shared. The abstract reports 'high detection accuracy' with scalability and robustness but gives no numbers.

## Contribution

Architecture for collaborative bot detection across operators without data sharing; the detection features build on prior financial-bot work.

## Key results

- Abstract claims high accuracy; no figures given there.

## Methods and models

Decentralised federated learning with smart-contract-orchestrated aggregation.

## Limitations and open questions

Abstract-level read; no numbers to assess; labels presumably inherited from prior datasets (not checked).

## Relevance to us

Relevant only as a pattern for multi-party detection where each party sees part of the swarm. Base detector: [[niedermayer-2024-detecting]].

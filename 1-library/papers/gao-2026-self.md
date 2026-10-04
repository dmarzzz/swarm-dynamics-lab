---
id: gao-2026-self
type: paper
title: "Self-Attention Clustering-Based Defense Against Eclipse Attacks on Ethereum"
authors: [Chengzhi Gao, Xiaodong Shen, Guoxie Jin, Chang Xu, Liehuang Zhu, Kashif Sharif]
year: 2026
venue: "IEEE Internet of Things Journal"
url: https://doi.org/10.1109/JIOT.2025.3641605
doi: 10.1109/JIOT.2025.3641605
arxiv: null
cite: "Gao, C., Shen, X., Jin, G., Xu, C., Zhu, L., & Sharif, K. (2026). Self-Attention Clustering-Based Defense Against Eclipse Attacks on Ethereum. IEEE Internet of Things Journal, 13(5), 8534-8547. https://doi.org/10.1109/JIOT.2025.3641605"
topics: [sybil-resistance]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "0 (Crossref, 2026-10-03)"
code: []
---

## Summary

ML detector for eclipse attacks (an attacker monopolising a victim node's peer connections) on Ethereum. A multi-kernel neural clustering model with parallel self-attention encoder subnetworks extracts category-specific features and produces cluster centroids; these are concatenated with raw transaction data to train a classifier. Evaluated on eclipse attacks the authors simulated on an Ethereum testnet: 98.5% detection accuracy and about 5% better classification than the same classifier without cluster features. Only the abstract was read (candidate record; Crossref has none).

## Contribution

Adds a clustering-feature stage to learned eclipse-attack detection on Ethereum.

## Key results

- 98.5% detection accuracy on simulated testnet eclipse attacks; +5% over no-cluster-feature baseline (abstract).

## Methods and models

Self-attention encoders, multi-kernel neural clustering, classifier on centroid-augmented transaction features; simulated attacks on an Ethereum testnet.

## Limitations and open questions

Evaluated only on the authors' own simulated attacks; accuracy on a balanced synthetic set says little about false-positive rates in mainnet traffic or adaptive attackers. Detects rather than prevents; contrast with structural defences.

## Relevance to us

Low. A detection-side counterpart to structural eclipse and Sybil defences in peer sampling: [[heilman-2015-eclipse]], [[marcus-2018-low-resource]], [[singh-2006-eclipse]], [[auvolat-2021-basalt]].

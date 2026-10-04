---
id: bhumichai-2024-evaluation
type: paper
title: "The Evaluation of Extracted Features for Detecting Eclipse Attacks on Ethereum Network Layers"
authors: [Dhanasak Bhumichai, Ryan G. Benton]
year: 2024
venue: 2024 IEEE International Conference on Big Data (BigData), Washington DC, pp. 5551-5560
url: https://ieeexplore.ieee.org/document/10825144/
doi: 10.1109/bigdata62323.2024.10825144
arxiv: null
cite: "Bhumichai, D., & Benton, R. G. (2024). The Evaluation of Extracted Features for Detecting Eclipse Attacks on Ethereum Network Layers. In 2024 IEEE International Conference on Big Data (BigData), pp. 5551-5560. IEEE. https://doi.org/10.1109/bigdata62323.2024.10825144"
topics: [sybil-resistance, swarm-detection]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "2 (Crossref, 2026-10-03)"
code: []
---

## Summary

Supervised-learning detection of eclipse attacks on the Ethereum P2P layer, where an attacker surrounds a victim node with controlled peers (a Sybil-style identity flood at the network layer) to cut it off from honest gossip. The authors simulate an Ethereum network, run eclipse attacks to produce a traffic dataset in which 28 percent of packets are malicious, and compare five feature-extraction families: common network-traffic features, entropy, phi-divergence, packet-communication statistics and packet-characteristic statistics. They handle class imbalance and overlap with SMOTE plus Tomek links and select features by mutual information. Five classifiers are compared (XGBoost, kNN, Random Forest and two others not named in the abstract); XGBoost on the top 25 features reaches 99.25 percent accuracy with 184 ms processing time, which the authors read as evidence that real-time detection is feasible. The introduction (visible on the IEEE page) positions this as the follow-up to the same authors' 2023 work that proposed 49 candidate features without evaluating them. Abstract plus first page of the introduction only; the IEEE body is paywalled and Unpaywall finds no open copy, so the feature list, the simulator, the attack script and the per-model table are not recorded here.

## Contribution

Empirical ranking of which traffic-level features actually discriminate eclipse traffic on Ethereum, narrowing a 49-feature candidate set to a top 25 that supports near-real-time classification.

## Key results

- Dataset: simulated Ethereum network under eclipse attack, 28 percent malicious packets (abstract).
- XGBoost, top 25 features: 99.25 percent accuracy, 184 ms per batch (abstract; batch size and test protocol not visible).
- SMOTE + Tomek links used for imbalance; mutual information for feature selection.

## Methods and models

Simulated Ethereum P2P network with scripted eclipse attacks; five feature-extraction methods; SMOTE/Tomek resampling; mutual-information selection; five ML classifiers including XGBoost, kNN and Random Forest. Details not visible beyond the abstract.

## Limitations and open questions

Abstract-level read. Simulated traffic only, and the 28 percent malicious share is far higher than a stealthy real attack, so 99.25 percent accuracy is on an easy distribution; no evidence about generalisation to mainnet traffic or to adaptive attackers who shape their packets. Accuracy is reported rather than precision/recall on the minority class even after resampling. Detection is after the fact; it does not prevent the identity flood that enables the attack.

## Relevance to us

Background for the detection side of Sybil and eclipse attacks on gossip layers. The structural eclipse analyses ([[heilman-2015-eclipse]], [[marcus-2018-low-resource]], [[singh-2006-eclipse]], [[gao-2025-heterogeneity]]) explain why these attacks are cheap; this paper is one of a cluster of ML-detection follow-ups (see also [[gao-2026-self]]). For an agent swarm, the transferable idea is a feature-engineered monitor on the message layer that flags when a member's neighbourhood has been captured, but the evaluation here is too synthetic to lean on.

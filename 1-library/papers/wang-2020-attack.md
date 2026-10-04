---
id: wang-2020-attack
type: paper
title: "Attack of the Tails: Yes, You Really Can Backdoor Federated Learning"
authors: ["Hongyi Wang", "Kartik Sreenivasan", "Shashank Rajput", "Harit Vishwakarma", "Saurabh Agarwal", "Jy-yong Sohn", "Kangwook Lee", "Dimitris Papailiopoulos"]
year: 2020
venue: "Advances in Neural Information Processing Systems 33 (NeurIPS 2020)"
url: https://arxiv.org/abs/2007.05084
doi: null
arxiv: "2007.05084"
cite: "Wang, H., Sreenivasan, K., Rajput, S., Vishwakarma, H., Agarwal, S., Sohn, J., Lee, K., & Papailiopoulos, D. (2020). Attack of the Tails: Yes, You Really Can Backdoor Federated Learning. Advances in Neural Information Processing Systems 33 (NeurIPS 2020). arXiv:2007.05084."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: null
code: []
---

## Summary

Argues that robustness to backdoors in federated learning is unlikely in general. Theory: robustness to backdoors implies robustness to adversarial examples, an open problem, and detecting a backdoor in a federated model is unlikely with first-order oracles or polynomial time. Empirically they introduce edge-case backdoors: the attacker targets inputs from the tail of the data distribution, which benign clients rarely touch, so the poisoned update is small and survives norm clipping and robust aggregation. Demonstrated on image classification, OCR, text prediction and sentiment analysis.

## Contribution

Supplies the hardness argument that the FL defence literature lacked: a defender that cannot see the tail cannot distinguish a tail backdoor from honest heterogeneity, regardless of aggregation rule.

## Key results

- Abstract-level: theoretical reduction from backdoor robustness to adversarial-example robustness.
- Abstract-level: detection of backdoors is hard under first-order oracle or polynomial-time assumptions.
- Edge-case backdoors inserted across several tasks with careful attacker tuning; specific rates not read.

## Methods and models

Theoretical results plus experiments on several federated tasks with defences including norm clipping, Krum, multi-Krum and others (details not read). Edge-case datasets constructed from out-of-distribution or low-frequency inputs.

## Limitations and open questions

Abstract only. The hardness results are worst-case; they say a universal defence is unlikely, not that a specific protocol with extra structure (redundant tasks, verifiable computation) fails.

## Relevance to us

Important for Q2 and Q3. For Q3 it identifies the strongest class of corruption for a returning part: change behaviour only on rare inputs that the parent's honest parts never visit. A sub-agent sent to an unusual information domain (another country's web) is by construction the only part that sees that tail, so its corruption is the hardest to cross-check. For Q2 it implies that k-of-n agreement only helps if several parts cover the same tail; disjoint exploration gives each part a monopoly on its region. Related: [[sun-2019-can]], [[bagdasaryan-2020-how]].

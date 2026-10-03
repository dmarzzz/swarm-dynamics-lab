---
id: fang-2020-local
type: paper
title: "Local Model Poisoning Attacks to Byzantine-Robust Federated Learning"
authors: ["Minghong Fang", "Xiaoyu Cao", "Jinyuan Jia", "Neil Zhenqiang Gong"]
year: 2020
venue: "29th USENIX Security Symposium (USENIX Security 20)"
url: https://arxiv.org/abs/1911.11815
doi: null
arxiv: "1911.11815"
cite: "Fang, M., Cao, X., Jia, J., & Gong, N. Z. (2020). Local Model Poisoning Attacks to Byzantine-Robust Federated Learning. In 29th USENIX Security Symposium (USENIX Security 20). arXiv:1911.11815."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Formulates local model poisoning as an optimisation problem: compromised clients craft their submitted local models so that the global model produced by a specific Byzantine-robust aggregation rule deviates as far as possible from the benign direction. Applied to Krum, Bulyan, trimmed mean and median on four real datasets, the attacks substantially increase the global model's test error even though each rule was claimed to be robust to some fraction of Byzantine clients. Two data-poisoning defences generalised to this setting help only in some cases.

## Contribution

First systematic attack on Byzantine-robust aggregation rules with full knowledge of the rule, showing that the robustness guarantees (bounded deviation) still leave room for large accuracy loss.

## Key results

- Abstract-level: attacks substantially increase error rates of Krum, Bulyan, trimmed mean and median-based federated learning on four datasets.
- Two generalised defences (error-rate based and loss-function based rejection) are effective in some cases and insufficient in others.

## Methods and models

Attacker controls the local models of some clients and solves for the submission that maximises deviation of the aggregate under the known rule (full-knowledge and partial-knowledge variants). Untargeted goal: raise test error rather than install a backdoor.

## Limitations and open questions

Abstract only. The attack is untargeted; it degrades the merged model rather than hijacking it. Byzantine bounds hold mathematically, the paper shows they are loose in practice.

## Relevance to us

Directly relevant to Q2. Classical Byzantine-robust aggregators give a k-of-n style guarantee (tolerate up to f bad inputs), and this paper shows that an adaptive adversary below the threshold can still push the merged model far from where honest parts would have taken it. A fork-merge protocol that relies on median or trimmed-mean merging of sub-agent updates inherits this gap between 'bounded influence' and 'harmless influence'. The BFT aggregation lane covers the defence side; this entry is the attack counterpart. Related: [[bagdasaryan-2020-how]], [[shejwalkar-2022-back]].

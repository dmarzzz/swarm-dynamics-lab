---
id: sun-2019-can
type: paper
title: "Can You Really Backdoor Federated Learning?"
authors: ["Ziteng Sun", "Peter Kairouz", "Ananda Theertha Suresh", "H. Brendan McMahan"]
year: 2019
venue: "2nd International Workshop on Federated Learning for Data Privacy and Confidentiality at NeurIPS 2019 (arXiv preprint)"
url: https://arxiv.org/abs/1911.07963
doi: null
arxiv: "1911.07963"
cite: "Sun, Z., Kairouz, P., Suresh, A. T., & McMahan, H. B. (2019). Can You Really Backdoor Federated Learning? arXiv preprint arXiv:1911.07963. 2nd International Workshop on Federated Learning for Data Privacy and Confidentiality at NeurIPS 2019."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Re-examines backdoor attacks in federated learning on EMNIST, a real user-partitioned non-i.i.d. dataset, allowing benign clients to hold correctly labelled examples of the targeted task. Without defences, attack success depends mainly on the fraction of adversarial clients and on how complex the targeted task is. Norm clipping of updates and 'weak' differential privacy (small added noise) mitigate the attacks without hurting main-task performance. Attacks and defences were released in TensorFlow Federated.

## Contribution

Counterweight to [[bagdasaryan-2020-how]]: under a more realistic data split, cheap defences (norm bounding, weak DP) blunt single-client replacement, which shifts the question to what fraction of clients the attacker needs.

## Key results

- Abstract-level: backdoor success depends on attacker fraction and on task complexity (number of targeted examples).
- Norm clipping and weak DP mitigate attacks without measurable main-task loss on EMNIST.
- I could not extract numeric tables from the PDF in this session; numbers not recorded.

## Methods and models

EMNIST federated split by writer; FedAvg with norm-bounding and Gaussian-noise defences; attackers use model replacement style boosted updates. TensorFlow Federated implementation.

## Limitations and open questions

Abstract only; numbers not checked. EMNIST is small; whether norm clipping holds against attackers who optimise within the bound is addressed by [[wang-2020-attack]].

## Relevance to us

Q2: this is the closest FL result to an empirical threshold. Once each returning update is norm-bounded, a single part can no longer replace the parent and success becomes a function of the fraction of corrupted parts. For a fork-merge agent the analogue is bounding how far any one returning sub-agent can move the parent's weights or memory. Pair with [[wang-2020-attack]], which argues a bounded attacker can still succeed using rare inputs, and [[shejwalkar-2022-back]].

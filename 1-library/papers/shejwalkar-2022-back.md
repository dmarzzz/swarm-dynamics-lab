---
id: shejwalkar-2022-back
type: paper
title: "Back to the Drawing Board: A Critical Evaluation of Poisoning Attacks on Production Federated Learning"
authors: ["Virat Shejwalkar", "Amir Houmansadr", "Peter Kairouz", "Daniel Ramage"]
year: 2022
venue: "IEEE Symposium on Security and Privacy (S&P 2022)"
url: https://arxiv.org/abs/2108.10241
doi: null
arxiv: "2108.10241"
cite: "Shejwalkar, V., Houmansadr, A., Kairouz, P., & Ramage, D. (2022). Back to the Drawing Board: A Critical Evaluation of Poisoning Attacks on Production Federated Learning. In IEEE Symposium on Security and Privacy (S&P 2022). arXiv:2108.10241."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Systematises threat models for poisoning federated learning (who is compromised, what they know, data versus model poisoning, cross-device versus cross-silo) and evaluates untargeted poisoning under realistic production assumptions. Contrary to much prior work, it finds federated learning highly robust in practice even with simple low-cost defences, while also proposing new state-of-the-art data and model poisoning attacks and measuring how ineffective they become when realistic client fractions and simple defences are assumed.

## Contribution

A calibration paper: the large effects reported in earlier FL poisoning work depend on unrealistically large attacker fractions or on undefended averaging.

## Key results

- Abstract-level: FL is highly robust in production-like settings with simple defences such as norm bounding.
- Abstract-level: new data and model poisoning attacks proposed; their impact is small under realistic threat models.

## Methods and models

Taxonomy of threat models; experiments on three benchmark datasets with cross-device FL and simple defences (details not read).

## Limitations and open questions

Abstract only. Focuses on untargeted poisoning; targeted backdoors (the fork-merge concern) are a different goal.

## Relevance to us

Q2 calibration. It is evidence that when each part's influence is bounded and the corrupted fraction is small, merges are robust in practice; it does not cover targeted, tail-only corruption ([[wang-2020-attack]]). For a fork-merge agent the takeaway is that the realistic threat is a targeted change by one part, not a degradation attack. Related: [[sun-2019-can]], [[fang-2020-local]].

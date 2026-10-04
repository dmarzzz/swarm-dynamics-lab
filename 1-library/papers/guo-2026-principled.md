---
id: guo-2026-principled
type: paper
title: "Principled Detection of Coordinated Manipulation from Aggregate Distortion and Account Reuse"
authors: ["Qian Guo", "Yidan Hu", "Rui Zhang"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2609.13407
doi: null
arxiv: "2609.13407"
cite: "Guo, Q., Hu, Y., & Zhang, R. (2026). Principled Detection of Coordinated Manipulation from Aggregate Distortion and Account Reuse. arXiv:2609.13407."
topics: [swarm-detection, sybil-resistance]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "0 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Proposes an aggregate-first evidence layer: instead of starting from identities, graphs or co-activity, treat distortion of a context's outcome distribution (for example a product's rating histogram) against a reference as evidence, subtract the matched null expectation, and only then accumulate signed evidence onto the accounts that participated. Theory covers matched-exposure divergence, self-influence bounds, finite-horizon separation and an exact linear reuse law. Tested on historical Amazon review streams with synthetic coalitions injected.

## Contribution

A statistically principled detector with a null-model correction, and evidence that it catches coalitions that frequency or co-activity signals miss.

## Key results

- Reassigning the same manipulated events across identities with more reuse raises account-score ROC-AUC from 0.500 to 0.797 (abstract).
- Against activity- and exposure-matched clean twins, frequency is at chance while counterfactual attribution reaches ROC-AUC 0.744 (abstract).
- Under a mean-preserving shape attack, Wasserstein-1 and Jensen-Shannon evidence reach ROC-AUC 0.909 and 0.967; frequency and mean-based methods stay at chance (abstract).
- Combining aggregate evidence with repeated co-activity raises mixed-mechanism ROC-AUC from 0.750 to 0.874 (abstract).

## Methods and models

Histogram distortion statistics with null-expectation subtraction, participation-log accumulation; semi-synthetic evaluation on Amazon reviews with known coalition membership. Code linked from arXiv.

## Limitations and open questions

Abstract only. Coalitions are synthetic, injected into real backgrounds; real-world prevalence is not measured.

## Relevance to us

Answers the missing-null-model complaint of [[mannocci-2026-detection]] for rating and ranking manipulation, where agent swarms are cheap to deploy. Complements co-activity detectors such as [[pacheco-2021-uncovering]].

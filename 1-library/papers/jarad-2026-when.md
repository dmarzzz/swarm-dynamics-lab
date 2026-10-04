---
id: jarad-2026-when
type: paper
title: "When Handshakes Tell the Truth: Detecting Web Bad Bots via TLS Fingerprints"
authors: ["Ghalia Jarad", "Kemal Bicakci"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2602.09606
doi: "10.48550/arXiv.2602.09606"
arxiv: "2602.09606"
cite: "Jarad, G., & Bicakci, K. (2026). When Handshakes Tell the Truth: Detecting Web Bad Bots via TLS Fingerprints. arXiv preprint arXiv:2602.09606."
topics: ["swarm-detection"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "2 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Jarad and Bicakci train XGBoost and CatBoost on features extracted from JA4 TLS fingerprints in the public JA4DB dataset to separate bots from real users. CatBoost reaches AUC 0.998, F1 0.9734 and accuracy 0.9863 on the test set; the most important features are the ja4_b component, cipher count and extension count. The approach is protocol-level and passive, needing no JavaScript or interaction.

## Contribution

Shows JA4 alone separates bots from browsers on a labelled public corpus; a binary bot-vs-human result that the 2026 agent papers test against agents and find weaker.

## Key results

- Measured (abstract): CatBoost AUC 0.998, F1 0.9734, accuracy 0.9863.
- Measured (abstract): top features ja4_b, cipher_count, ext_count.

## Methods and models

JA4DB fingerprints, feature extraction from JA4 segments, gradient-boosted classifiers. Abstract only.

## Limitations and open questions

Abstract only. Binary task on a database of known fingerprints; [[fayolle-2026-internet]] found JA4 alone gives only 0.454 accuracy for telling specific agents and frameworks apart, because local agents share the host browser's TLS stack.

## Relevance to us

Cheap first-layer signal; useful against cloud agents with fixed stacks, weak against agents that drive a real browser. See [[kang-2026-whose]] for TLS-layer F1 0.725.

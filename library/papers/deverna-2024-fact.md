---
id: deverna-2024-fact
title: Fact-checking information from large language models can decrease headline
  discernment
authors:
- Matthew R. DeVerna
- Harry Yaojun Yan
- Kai-Cheng Yang
- Filippo Menczer
year: 2024
venue: Proceedings of the National Academy of Sciences; arXiv version 4
url: https://arxiv.org/abs/2308.10800
doi: 10.1073/pnas.2322823121
arxiv: '2308.10800'
cite: DeVerna, M. R., Yan, H. Y., Yang, K.-C., & Menczer, F. (2024). Fact-checking
  information from large language models can decrease headline discernment. Proceedings
  of the National Academy of Sciences. https://doi.org/10.1073/pnas.2322823121.
topics:
- swarm-detection
- collective-decision
read_depth: abstract
relevance: 3
type: paper
added_by: shadow/sol-w1
accessed: '2026-10-03'
citations: null
code: []
---

## Summary

A preregistered randomized experiment examines how people use LLM-generated fact checks when evaluating political headlines. Despite correctly identifying 90% of false headlines, the model's fact checks did not significantly improve belief or sharing discernment, unlike human fact checks. Incorrect or uncertain judgments could worsen beliefs, and voluntary use was associated with more sharing of both true and false news. Detector accuracy and downstream human response therefore diverged.

## Contribution

Tests the human effects of model judgments rather than assuming accurate classification automatically yields effective misinformation defense.

## Key results

- Abstract reports 90% identification of false headlines.
- No significant overall improvement in accuracy or sharing discernment from LLM fact checks.
- Human-generated checks improved both measures.
- Misclassified true headlines and uncertain false headlines produced harmful belief shifts; effect sizes were not checked.

## Methods and models

Preregistered randomized control experiment involving belief and sharing intention for political headlines, plus analysis of optional fact-check viewing. Read only the abstract and publication/author metadata; sample size, assignment procedures, and model settings were not inspected.

## Limitations and open questions

Sharing intention is not observed sharing behavior. Optional viewing can involve selection and should not automatically be interpreted causally. The abstract does not establish generality across newer models, different interfaces, or real coordinated bot campaigns.

## Relevance to us

A caution for evaluating defenses against swarm-driven influence: classification metrics alone do not measure human benefit. Related threat framing appears in [[ferrara-2024-genai]] and practitioner detection context in [[cubbon-2020-inauthentic]]. This is not itself a coordinated-bot detector.

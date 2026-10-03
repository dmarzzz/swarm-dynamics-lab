---
id: sayyadiharikandeh-2020-detection
type: paper
title: Detection of Novel Social Bots by Ensembles of Specialized Classifiers
authors:
- Mohsen Sayyadiharikandeh
- Onur Varol
- Kai-Cheng Yang
- Alessandro Flammini
- Filippo Menczer
year: 2020
venue: Proceedings of the 29th ACM International Conference on Information and Knowledge Management (CIKM 2020)
url: https://arxiv.org/abs/2006.06867
doi: 10.1145/3340531.3412698
arxiv: '2006.06867'
cite: Sayyadiharikandeh, M., Varol, O., Yang, K.-C., Flammini, A., & Menczer, F. (2020). Detection of Novel Social Bots by Ensembles of Specialized Classifiers. In Proceedings of the 29th ACM International Conference on Information and Knowledge Management (CIKM '20), pp. 2725-2732. https://doi.org/10.1145/3340531.3412698
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 160 (Crossref, 2026-10-03)
code: []
---

## Summary

Different bot types have different behavioural signatures, so a single supervised classifier degrades on bot types absent from training. The authors train one classifier per bot class and combine them with a maximum rule (ESC), improving F1 on unseen accounts by 56% on average across datasets and needing fewer labels to learn new bot behaviours. ESC became Botometer v4, with cross-validation AUC 0.99.

## Contribution

The generalisation fix adopted in the most-used public bot detector.

## Key results

- Average 56% F1 improvement on unseen accounts across datasets (abstract).
- Deployed in Botometer v4 with cross-validated AUC 0.99.

## Methods and models

Ensemble of specialised random-forest classifiers combined by maximum rule. Abstract-level read.

## Limitations and open questions

[[hays-2023-simplistic]] shows that datasets within a bot type are themselves easily separable, which limits how far the per-type assumption helps.

## Relevance to us

Design pattern for a swarm detector covering several operator styles. Problem it responds to: [[echeverria-2018-lobo]]. Earlier system: [[varol-2017-online]].

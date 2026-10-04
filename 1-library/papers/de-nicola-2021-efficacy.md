---
id: de-nicola-2021-efficacy
type: paper
title: On the efficacy of old features for the detection of new bots
authors:
- Rocco De Nicola
- Marinella Petrocchi
- Manuel Pratelli
year: 2021
venue: Information Processing & Management
url: https://arxiv.org/abs/2506.19635
doi: 10.1016/j.ipm.2021.102685
arxiv: '2506.19635'
cite: De Nicola, R., Petrocchi, M., & Pratelli, M. (2021). On the efficacy of old features for the detection of new bots. Information Processing & Management, 58(6), 102685. https://doi.org/10.1016/j.ipm.2021.102685 (preprint posted as arXiv:2506.19635 in 2025).
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 23 (Crossref, 2026-10-03)
code: []
---

## Summary

Compares four feature sets for detecting evolved bots on six recently released Twitter datasets: a Botometer output score built on more than 1,000 features, two cheap profile and timeline feature sets, and the Twitter client used to post. The results suggest general-purpose classifiers on cheap account features can detect newer bots about as well as expensive feature sets.

## Contribution

Evidence that cheap, hard-to-fake account features hold up against newer bots, consistent with later LLM-era results.

## Key results

- Four feature sets compared across six datasets (abstract).
- Cheap-to-compute account features plus general classifiers are competitive for evolved bots.

## Methods and models

Supervised classifiers on Twitter datasets. Abstract-level read.

## Limitations and open questions

Pre-LLM; datasets carry the collection artefacts discussed in [[hays-2023-simplistic]].

## Relevance to us

Precedent for [[katyal-2026-account]]: metadata features outlast content features. Same group as [[cresci-2017-paradigm]].

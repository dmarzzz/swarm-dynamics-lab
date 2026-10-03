---
id: pote-2024-coordinated
type: paper
title: 'Coordinated Reply Attacks in Influence Operations: Characterization and Detection'
authors:
- Manita Pote
- Tuğrulcan Elmas
- Alessandro Flammini
- Filippo Menczer
year: 2024
venue: Proceedings of the International AAAI Conference on Web and Social Media (ICWSM 2025)
url: https://arxiv.org/abs/2410.19272
doi: 10.1609/icwsm.v19i1.35889
arxiv: '2410.19272'
cite: 'Pote, M., Elmas, T., Flammini, A., & Menczer, F. (2025). Coordinated Reply Attacks in Influence Operations: Characterization and Detection. Proceedings of the International AAAI Conference on Web and Social Media, 19, 1586-1598. https://doi.org/10.1609/icwsm.v19i1.35889'
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 6 (Crossref, 2026-10-03)
code: []
---

## Summary

Characterises coordinated reply attacks, where IO accounts pile replies onto a target's post, in Twitter influence-operation data. Targets are mostly journalists, news outlets, officials and politicians. Two supervised classifiers detect targeted tweets (AUC 0.88) and attacking accounts among repliers (AUC 0.97), so targeted accounts can act as sensors for influence operations.

## Contribution

Introduces the target-as-sensor idea: watch replies to likely targets to find the swarm.

## Key results

- Tweet-level classifier for being targeted: AUC 0.88; account-level classifier for attack participation: AUC 0.97 (abstract).
- Main targets: journalists, news media, state officials, politicians.

## Methods and models

Supervised ML on reply-structure features from IO datasets. Abstract-level read.

## Limitations and open questions

Pre-LLM IO data; reply attacks by LLM agents could be more varied.

## Relevance to us

Close to a honeypot design: a high-value target attracts the swarm, and its reply stream is the detection surface. Same lab as [[pacheco-2021-uncovering]] and [[yang-2023-anatomy]].

---
id: pacheco-2020-uncovering
type: paper
title: 'Uncovering Coordinated Networks on Social Media: Methods and Case Studies'
authors:
- Diogo Pacheco
- Pik-Mai Hui
- Christopher Torres-Lugo
- Bao Tran Truong
- Alessandro Flammini
- Filippo Menczer
year: 2020
venue: Proceedings of the International AAAI Conference on Web and Social Media (ICWSM 2021)
url: https://arxiv.org/abs/2001.05658
doi: 10.1609/icwsm.v15i1.18075
arxiv: '2001.05658'
cite: 'Pacheco, D., Hui, P.-M., Torres-Lugo, C., Truong, B. T., Flammini, A., & Menczer, F. (2021). Uncovering Coordinated Networks on Social Media: Methods and Case Studies. Proceedings of the International AAAI Conference on Web and Social Media, 15, 455-466. https://doi.org/10.1609/icwsm.v15i1.18075'
topics:
- swarm-detection
- sybil-resistance
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 113 (Crossref, 2026-10-03)
code: []
---

## Summary

A general unsupervised method for finding coordinated account groups: build a bipartite graph between accounts and a chosen behavioural trace (identities, images, hashtag sequences, retweets, timing), project it to an account-account similarity network, and keep the strongest edges. Five case studies (US elections, Hong Kong protests, Syrian civil war, cryptocurrency manipulation and one more) find coordinated Twitter networks with different traces.

## Contribution

The reference trace-agnostic coordination-network method; most later coordinated-inauthentic-behaviour detectors are variants of it.

## Key results

- Unsupervised, works with arbitrary shared behavioural traces (abstract).
- Coordinated networks found in five case studies using identities, images, hashtag sequences, retweets or temporal patterns.

## Methods and models

Bipartite account-feature graphs, projection with similarity weights (TF-IDF, cosine), edge filtering and community extraction. Abstract-level read.

## Limitations and open questions

Coordination is not proof of automation or inauthenticity; thresholds are chosen per case and need organic controls ([[pante-2025-beyond]]).

## Relevance to us

Directly applicable to LLM swarms whose per-account content passes as human: they still share links, targets and timing. Survey context: [[mannocci-2024-detection]]. The fox8 LLM botnet was detected by coordination in [[yang-2023-anatomy]].

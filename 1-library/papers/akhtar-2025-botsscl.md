---
id: akhtar-2025-botsscl
title: 'BotSSCL: Social Bot Detection with Self-Supervised Contrastive Learning'
authors:
- Mohammad Majid Akhtar
- Navid Shadman Bhuiyan
- Rahat Masood
- Muhammad Ikram
- Salil S. Kanhere
year: 2025
venue: Online Social Networks and Media 48, 100318; arXiv preprint version 1 (2024)
url: https://arxiv.org/abs/2402.03740
doi: 10.1016/j.osnem.2025.100318
arxiv: '2402.03740'
cite: 'Akhtar, M. M., Bhuiyan, N. S., Masood, R., Ikram, M., & Kanhere, S. S. (2025).
  BotSSCL: Social Bot Detection with Self-Supervised Contrastive Learning. Online
  Social Networks and Media, 48, 100318. https://doi.org/10.1016/j.osnem.2025.100318.'
topics:
- swarm-detection
read_depth: skim
relevance: 4
type: paper
added_by: shadow/sol-w1
accessed: '2026-10-03'
citations: null
code: []
---

## Summary

BotSSCL learns account representations with self-supervised contrastive training to distinguish human-like bots from humans. It combines profile metadata, tweet embeddings, tweet metadata, and temporal statistics without requiring follower-network collection. Experiments on Varol and Gilani datasets report improved F1, approximately 67% cross-dataset F1, and low evasion success under the evaluated attacks. Generalization and robustness claims are limited to those datasets and attack settings, not modern autonomous-agent swarms.

## Contribution

Applies contrastive representation learning to tabular multimodal account features while addressing distribution shift and profile manipulation.

## Key results

- Abstract reports approximately 6% and 8% higher F1 than prior methods on two datasets; the wording does not unambiguously distinguish relative gains from percentage-point gains.
- Approximately 67% F1 when training and testing across datasets.
- Reported adversarial evasion success of 4% under the authors' evaluated threat model, not a universal guarantee.

## Methods and models

Read the abstract, introduction, and methodology through the representation/contrastive-learning setup in arXiv HTML. Tier-1 features include 33 user-metadata fields, 29 tweet-metadata features, 7 temporal features, and up to 200 recent tweets. Tweet embeddings are averaged BERT vectors. Four normalized feature groups receive learned linear projections and are concatenated. Weight-sharing MLP encoders and a projection head learn from augmented views using InfoNCE. Experimental sections and downstream label use were not fully inspected. Journal metadata and complete author list were checked with Crossref.

## Limitations and open questions

Cross-dataset F1 of 67% still leaves substantial error and only covers two historical datasets. Self-supervised representation training does not imply entirely label-free evaluation. Linear projections are not by themselves a formal security boundary; the 4% evasion figure depends on adversary capabilities that need full-method inspection. The results summarized here come from the February 2024 preprint; equivalence to the 2025 journal extension was not verified. No implementation was run.

## Relevance to us

A candidate detection baseline that does not rely on expensive follower graphs. Contrast with temporal-signature matching in [[deason-2018-time]] and descriptive classifier-labeled profiles in [[ng-2025-global]]. It classifies individual accounts, not common control or malicious group intent.

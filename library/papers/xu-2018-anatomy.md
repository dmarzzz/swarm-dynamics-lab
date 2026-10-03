---
id: xu-2018-anatomy
type: paper
title: The Anatomy of a Cryptocurrency Pump-and-Dump Scheme
authors:
- Jiahua Xu
- Benjamin Livshits
year: 2018
venue: arXiv preprint; Proceedings of the 28th USENIX Security Symposium (2019)
url: https://arxiv.org/abs/1811.10109
doi: null
arxiv: '1811.10109'
cite: Xu, J., & Livshits, B. (2018). The Anatomy of a Cryptocurrency Pump-and-Dump Scheme. arXiv preprint arXiv:1811.10109. Also in Proceedings of the 28th USENIX Security Symposium (2019), 1609-1625.
topics:
- swarm-detection
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

First detailed empirical study of cryptocurrency pump-and-dump schemes, covering 412 pumps organised in Telegram channels from 17 June 2018 to 26 February 2019 plus a case study. The authors identify market patterns associated with pumps and train a model that predicts which coins listed on an exchange will be pumped before the event, with high precision; a simple strategy based on it returned up to 60% on small retail investments over two and a half months.

## Contribution

Seminal detection of coordinated group trading organised off chain (Telegram) and executed on exchanges; shows coordination can be anticipated from pre-event market features.

## Key results

- 412 Telegram-organised pumps catalogued; pre-pump prediction model with high precision; strategy return up to 60% in 2.5 months.

## Methods and models

Telegram channel monitoring; exchange market data; supervised prediction of pump targets.

## Limitations and open questions

Abstract-level read; centralised exchanges, not on-chain; participants are coordinated humans, not bots (as described).

## Relevance to us

A template for detecting coordinated groups by monitoring their coordination channel and predicting targets, relevant to agent swarms coordinated through shared prompts or channels. Successor on-chain work: [[mongardini-2025-midsummer]].

---
id: alzahrani-2025-bots
type: paper
title: 'Bots Don''t Sit Still: A Longitudinal Study of Bot Behaviour Change, Temporal Drift, and Feature-Structure Evolution'
authors:
- Ohoud Alzahrani
- Russell Beale
- Bob Hendley
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2512.17067
doi: null
arxiv: '2512.17067'
cite: 'Alzahrani, O., Beale, R., & Hendley, B. (2025). Bots Don''t Sit Still: A Longitudinal Study of Bot Behaviour Change, Temporal Drift, and Feature-Structure Evolution. arXiv preprint arXiv:2512.17067.'
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Tests whether promotional Twitter bots behave stationarily. Using 2,615 bot accounts and 2.8 million tweets, yearly series for ten content meta-features are all non-stationary under ADF and KPSS tests (nine increase), bots of different activation generations differ systematically, and correlations among 18 binary cues strengthen or flip sign across generations.

## Contribution

Quantifies concept drift in bot behaviour, the reason detectors trained on historical data decay.

## Key results

- All 10 meta-features non-stationary; 9 trend upward, language diversity declines slightly.
- Almost all of 153 feature pairs are dependent (chi-square); Spearman correlations change strength and sometimes sign across generations.

## Methods and models

Time-series stationarity tests and co-occurrence analysis on promotional bots. Abstract-level read.

## Limitations and open questions

Promotional bots only; pre-LLM; preprint.

## Relevance to us

Detector drift is the expected default for agent swarms, which can be re-prompted overnight. Related evidence: [[rauchfleisch-2020-false]] (score drift), [[echeverria-2018-lobo]] (unseen classes).

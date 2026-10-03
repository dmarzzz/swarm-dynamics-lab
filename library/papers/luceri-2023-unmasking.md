---
id: luceri-2023-unmasking
type: paper
title: 'Unmasking the Web of Deceit: Uncovering Coordinated Activity to Expose Information Operations on Twitter'
authors:
- Luca Luceri
- Valeria Pantè
- Keith Burghardt
- Emilio Ferrara
year: 2023
venue: Proceedings of the ACM Web Conference 2024 (WWW '24)
url: https://arxiv.org/abs/2310.09884
doi: 10.1145/3589334.3645529
arxiv: '2310.09884'
cite: 'Luceri, L., Pantè, V., Burghardt, K., & Ferrara, E. (2024). Unmasking the Web of Deceit: Uncovering Coordinated Activity to Expose Information Operations on Twitter. In Proceedings of the ACM Web Conference 2024 (WWW ''24), pp. 2530-2541. https://doi.org/10.1145/3589334.3645529'
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 28 (Crossref, 2026-10-03)
code: []
---

## Summary

Using 49 million tweets from six countries with verified state information operations, the authors show standard network filtering does not consistently find IO drivers across campaigns. A node-pruning framework that fuses several behavioural similarity networks works better, and a supervised model on a vector representation of the fused network classifies IO drivers with precision above 0.95 and forecasts their future participation.

## Contribution

Moves coordination detection from single-trace networks to a fused multi-trace network with a supervised layer, evaluated across many state campaigns.

## Key results

- 49M tweets, six countries, multiple verified IOs.
- Precision above 0.95 for classifying IO drivers globally (abstract).
- Traditional network filtering does not consistently find IO drivers across campaigns.

## Methods and models

Similarity networks per behavioural indicator, fused network, node pruning, supervised classifier on network embeddings. Abstract-level read.

## Limitations and open questions

Ground truth comes from Twitter's IO takedown releases, which reflect what Twitter found; evaluation is on pre-LLM campaigns.

## Relevance to us

Template for detecting an operator's swarm from multiple weak shared-behaviour signals. Negative control lesson: [[pante-2025-beyond]]. Applied to 2024 elections in [[minici-2024-uncovering]] and [[cinus-2024-exposing]].

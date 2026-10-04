---
id: mazza-2019-rtbust
type: paper
title: "RTbust: Exploiting Temporal Patterns for Botnet Detection on Twitter"
authors: ["Michele Mazza", "Stefano Cresci", "Marco Avvenuti", "Walter Quattrociocchi", "Maurizio Tesconi"]
year: 2019
venue: "Proceedings of the 10th ACM Conference on Web Science (WebSci)"
url: https://arxiv.org/abs/1902.04506
doi: "10.1145/3292522.3326015"
arxiv: "1902.04506"
cite: "Mazza, M., Cresci, S., Avvenuti, M., Quattrociocchi, W., & Tesconi, M. (2019). RTbust: Exploiting Temporal Patterns for Botnet Detection on Twitter. In Proceedings of the 10th ACM Conference on Web Science (pp. 183–192). ACM."
topics: [swarm-detection]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "224 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Studies retweet timing on a 10M-retweet dataset, visualises retweet-delay patterns, and finds one normal human pattern and three suspicious bot patterns. RTbust encodes each account's retweet time series with an LSTM autoencoder and clusters the latent vectors with hierarchical density-based clustering; accounts in large clusters with malicious patterns are labelled bots. It reaches F1 = 0.87 against competitors below 0.76 and uncovers two previously unknown botnets of hundreds of accounts.

## Contribution

Unsupervised group-level detection from retweet timing alone, showing temporal signatures shared within a botnet separate it from humans.

## Key results

- F1 = 0.87 versus F1 < 0.76 for competitors (abstract).
- Two previously unknown active botnets with hundreds of accounts found (abstract).

## Methods and models

Retweet time series per account, LSTM autoencoder, HDBSCAN-style clustering.

## Limitations and open questions

Abstract only. Retweet-only; relies on botnets sharing timing schedules.

## Relevance to us

Timing-only group detection; an LLM swarm with a shared scheduler would show the same clustered latent signature. Same group as [[mannocci-2026-detection]].

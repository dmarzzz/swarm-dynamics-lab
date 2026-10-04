---
id: richardo-2025-fake
type: paper
title: Fake it 'Til you Make it? Supervised Machine Learning Approach to Detect Bots on Web3 Airdrops
authors:
- Anthony Sai Richardo
- Franz Adeta Junior
- Yohan Muliono
- Michelle Hamjaya
- Ika Dyah Agustia Rachmawati
year: 2025
venue: 2025 6th International Conference on Artificial Intelligence and Data Sciences (AiDAS)
url: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/AiDAS67696.2025.11212856?fields=title,abstract,venue,year
doi: 10.1109/AiDAS67696.2025.11212856
arxiv: null
cite: Richardo, A. S., Junior, F. A., Muliono, Y., Hamjaya, M., & Rachmawati, I. D. A. (2025). Fake it 'Til you Make it? Supervised Machine Learning Approach to Detect Bots on Web3 Airdrops. In 2025 6th International Conference on Artificial Intelligence and Data Sciences (AiDAS) (pp. 449-453). IEEE. https://doi.org/10.1109/AiDAS67696.2025.11212856
topics:
- swarm-detection
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Detects bots in Telegram-based Web3 airdrops (tap-to-earn games) from API request patterns rather than on-chain data. The dataset has 2,600 samples: 1,300 from real bot scripts and 1,300 collected manually with Telegram's network tools, each with HTTP method, URL, headers and public IP, enriched with VPN, proxy, Tor-relay and hosting-provider flags. Of seven classifiers, Gaussian Naive Bayes and an MLP do best at 94.41% validation and 94.00% test accuracy, falling to 84.56% on a separate set of new data. The paper cites Hamster Kombat's report of over 2.3 million automated bot interactions in its 2024 airdrop.

## Contribution

Off-chain, network-level bot detection for an airdrop, complementary to the on-chain detectors; shows a 10-point drop on new data.

## Key results

- Best accuracy 94.0% on test, 84.56% on new data.
- Context figure cited (not measured): Hamster Kombat reported over 2.3M bot interactions.

## Methods and models

Supervised comparison of seven models on request-level features with IP reputation enrichment.

## Limitations and open questions

Small, self-constructed and balanced dataset; bot class comes from the authors' own scripts, so it may not represent deployed farms. Abstract-level read via Semantic Scholar.

## Relevance to us

Shows the request-level (web) layer of airdrop swarms, the layer where LLM agents operating through APIs would also be visible. Compare chain-level [[liu-2025-detecting]] and quest probes in [[al-chami-2025-quest]].

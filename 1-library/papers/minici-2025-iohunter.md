---
id: minici-2025-iohunter
type: paper
title: "IOHunter: Graph Foundation Model to Uncover Online Information Operations"
authors: ["Marco Minici", "Luca Luceri", "Francesco Fabbri", "Emilio Ferrara"]
year: 2025
venue: "Proceedings of the AAAI Conference on Artificial Intelligence"
url: https://arxiv.org/abs/2412.14663
doi: "10.1609/aaai.v39i27.35046"
arxiv: "2412.14663"
cite: "Minici, M., Luceri, L., Fabbri, F., & Ferrara, E. (2025). IOHunter: Graph Foundation Model to Uncover Online Information Operations. Proceedings of the AAAI Conference on Artificial Intelligence, 39(27), 28258–28266."
topics: [swarm-detection]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "19 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Combines language models and graph neural networks to identify IO drivers across influence campaigns, aiming at generalisation in supervised, scarcely supervised and cross-campaign settings. On IOs from six countries it reports state-of-the-art performance and presents itself as a step toward graph foundation models for IO detection.

## Contribution

Tests whether a detector trained on some campaigns transfers to unseen ones, the setting that matters for new agent swarms.

## Key results

- State-of-the-art performance across IOs from six countries, significantly surpassing existing approaches (abstract; numbers not in abstract).

## Methods and models

Text embeddings from language models as node features on similarity or interaction graphs, GNN classifier; cross-IO transfer experiments.

## Limitations and open questions

Abstract only. Training labels are platform attributions; transfer to LLM-written content is untested.

## Relevance to us

Cross-campaign transfer is the test any swarm detector must pass. Builds on [[luceri-2024-unmasking]].

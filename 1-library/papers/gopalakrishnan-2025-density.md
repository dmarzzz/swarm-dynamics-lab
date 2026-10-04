---
id: gopalakrishnan-2025-density
type: paper
title: "Density-aware Walks for Coordinated Campaign Detection"
authors: ["Atul Anand Gopalakrishnan", "Jakir Hossain", "Tuğrulcan Elmas", "Ahmet Erdem Sarıyüce"]
year: 2025
venue: "ECML-PKDD 2025 (arXiv preprint)"
url: https://arxiv.org/abs/2506.13912
doi: null
arxiv: "2506.13912"
cite: "Gopalakrishnan, A. A., Hossain, J., Elmas, T., & Sarıyüce, A. E. (2025). Density-aware Walks for Coordinated Campaign Detection. arXiv:2506.13912. Accepted at ECML-PKDD 2025."
topics: [swarm-detection]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "4 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Frames coordinated campaign detection as graph classification on the Large Engagement Networks (LEN) dataset: over 300 engagement networks of fake (astroturfed) and authentic Twitter trends before the 2023 Turkish elections. Standard GNNs struggle on these large graphs. The authors bias random walks by local density (degree, core number, truss number), embed them with Skip-gram, and train message-passing networks on these embeddings, gaining about 12% accuracy in binary and 5% in multiclass classification.

## Contribution

Shows that local density structure, rather than node features, separates astroturfed trends from organic ones at the whole-campaign level.

## Key results

- About 12% (binary) and 5% (multiclass) accuracy improvement over simpler node features (abstract).

## Methods and models

Random weighted walks biased by degree, k-core or k-truss; Skip-gram embeddings; MPNN graph classifier; LEN dataset.

## Limitations and open questions

Abstract only. Campaign-level rather than account-level output; one country and election.

## Relevance to us

Campaign-level classification is the right granularity when the question is "is this trend a swarm" rather than "which accounts". Datasets of this kind are listed in [[mannocci-2026-detection]].

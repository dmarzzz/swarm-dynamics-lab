---
id: yax-2024-phylolm
type: paper
title: "PhyloLM : Inferring the Phylogeny of Large Language Models and Predicting their Performances in Benchmarks"
authors: ["Nicolas Yax", "Pierre-Yves Oudeyer", "Stefano Palminteri"]
year: 2024
venue: "International Conference on Learning Representations (ICLR 2025); arXiv preprint"
url: https://arxiv.org/abs/2404.04671
doi: null
arxiv: "2404.04671"
cite: "Yax, N., Oudeyer, P. Y., & Palminteri, S. (2024). PhyloLM : Inferring the Phylogeny of Large Language Models and Predicting their Performances in Benchmarks. ICLR 2025. arXiv:2404.04671."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

PhyloLM borrows phylogenetic algorithms from population genetics, treating generated tokens for given contexts like alleles for genes, to compute a distance between LLMs from output similarity alone. The resulting dendrograms recover known relationships across 111 open-source and 45 closed models, and the distance predicts benchmark performance.

## Contribution

A lineage map of LLMs inferred from outputs without training information.

## Key results

- Dendrograms capture known relationships across 111 open and 45 closed models (abstract).
- Phylogenetic distance predicts standard benchmark performance (abstract).

## Methods and models

Sample completions for a set of contexts; compute genetic-style distance; build trees.

## Limitations and open questions

Abstract-only reading. Family-level, not instance-level, identification.

## Relevance to us

Output-only lineage distance is a natural clustering metric for a population of unknown agents. Related: [[nikolic-2025-model]], [[bruckner-2026-one]].

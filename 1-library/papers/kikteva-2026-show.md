---
id: kikteva-2026-show
type: paper
title: "Show Me How You Reason and I'll Tell You Who You Are: Reasoning Graphs for Robust LLM Authorship Attribution"
authors: ["Zlata Kikteva", "Artur Romazanov", "Annette Hautli-Janisz", "Ramon Ruiz-Dolz"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2607.14905
doi: null
arxiv: "2607.14905"
cite: "Kikteva, Z., Romazanov, A., Hautli-Janisz, A., & Ruiz-Dolz, R. (2026). Show Me How You Reason and I'll Tell You Who You Are: Reasoning Graphs for Robust LLM Authorship Attribution. arXiv:2607.14905."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Attributes LLM-generated text using reasoning structure rather than surface style: an argument-mining pipeline extracts reasoning graphs, and a graph neural network classifies the source model. It beats a Longformer baseline by up to 27 percentage points under paraphrasing and back-translation attacks and by 19 points on texts from unseen model versions.

## Contribution

An attribution signal designed to survive the obfuscation that breaks surface stylometry.

## Key results

- Up to +27 pp over Longformer under paraphrase and back-translation (abstract).
- +19 pp on unseen model versions (abstract).

## Methods and models

Argument mining to reasoning graphs; GNN classifier.

## Limitations and open questions

Needs argumentative text of some length; abstract-only reading.

## Relevance to us

Possible counter to rewriting attacks like [[yuan-2026-forging]] for attributing swarm posts that argue a position.

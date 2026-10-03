---
id: iannucci-2025-detecting
type: paper
title: "Detecting Coordinated Activities Through Temporal, Multiplex, and Collaborative Analysis"
authors: ["Letizia Iannucci", "Elisa Muratore", "Antonis Matakos", "Mikko Kivelä"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2512.19677
doi: null
arxiv: "2512.19677"
cite: "Iannucci, L., Muratore, E., Matakos, A., & Kivelä, M. (2025). Detecting Coordinated Activities Through Temporal, Multiplex, and Collaborative Analysis. arXiv:2512.19677."
topics: [swarm-detection]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "4 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Decomposes online activity into interaction layers of a multiplex network and aggregates coordination evidence across layers. Within each layer a time-aware collaboration model, built on the node-normalised collaboration model, rewards repeated coordinated actions over different time intervals through an exponential-decay temporal kernel. On several datasets with known coordinated activity the multiplex time-aware model outperforms previous coordinated-activity detectors.

## Contribution

Replaces a single fixed time window with a decaying temporal kernel and keeps layers separate, two of the open problems named in [[mannocci-2026-detection]].

## Key results

- Multiplex time-aware model "excels" at finding coordinating groups and beats earlier methods (abstract; no numbers there).

## Methods and models

Multiplex network per modality, node-normalised collaboration weights with exponential decay over time intervals, cross-layer evidence aggregation.

## Limitations and open questions

Abstract only; datasets and baselines not given in the abstract. Semantic Scholar lists an ICWSM venue that I did not confirm on the arXiv page.

## Relevance to us

A drop-in improvement over fixed-window co-action networks; addresses the window sensitivity measured in [[panayiotou-2026-setting]].

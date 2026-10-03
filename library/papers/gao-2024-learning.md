---
id: gao-2024-learning
type: paper
title: "Learning interpretable dynamics of stochastic complex systems from experimental data"
authors: ["Ting-Ting Gao", "Baruch Barzel", "Gang Yan"]
year: 2024
venue: "Nature Communications"
url: https://api.crossref.org/works/10.1038/s41467-024-50378-x
doi: "10.1038/s41467-024-50378-x"
arxiv: null
cite: "Gao, T.-T., Barzel, B., & Yan, G. (2024). Learning interpretable dynamics of stochastic complex systems from experimental data. Nature Communications, 15(1), 6029."
topics: [collective-motion, criticality-measurement, meta]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: 31  # (Crossref is-referenced-by-count, 2026-10-03; OpenAlex daily budget exhausted for this IP)
code: []
---
## Summary

Proposes a Langevin graph network to learn the hidden stochastic differential equations of networked systems from data, outperforming five state-of-the-art methods. Applied to bird flock movement, the inferred equation closely resembles the second-order (inertial) Vicsek model, which the authors present as evidence that the Vicsek model captures genuine flocking dynamics. Also applied to tau pathology spread in mouse brains.

## Contribution

Interpretable equation discovery for stochastic many-body dynamics with an animal-flock test case.

## Key results

- Claimed (abstract): outperforms five baselines; learned flock equation resembles second-order Vicsek dynamics.

## Methods and models

Graph network with drift and diffusion terms plus symbolic interpretation; pigeon flock data (source not checked).

## Limitations and open questions

Abstract only. The conclusion "Vicsek captures genuine flocking" sits in tension with [[sayin-2025-behavioral]] (locusts do not align); species and data type differ.

## Relevance to us

Candidate method to infer interaction laws from our own trajectory data; compare [[han-2024-collective]], [[kim-2025-commanding]] and [[de-lamo-2025-data]].

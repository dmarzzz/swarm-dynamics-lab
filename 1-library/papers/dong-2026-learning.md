---
id: dong-2026-learning
type: paper
title: "Learning Sampled-data Control for Swarms via MeanFlow"
authors: ["Anqi Dong", "Yongxin Chen", "Karl H. Johansson", "Johan Karlsson"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2603.20189
doi: null
arxiv: "2603.20189"
cite: "Dong, A., Chen, Y., Johansson, K. H., & Karlsson, J. (2026). Learning Sampled-data Control for Swarms via MeanFlow. arXiv preprint arXiv:2603.20189."
topics: [swarm-robotics, sync-consensus]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (OpenAlex W7140146419, 2026-10-03)"
code: []
---

## Summary

For steering large swarms (density control) when control updates are infrequent, the authors generalise the MeanFlow generative-modelling framework to linear time-invariant dynamics. They learn a finite-horizon coefficient field parameterising the minimum-energy control over each sampling interval. A differential identity links this field to bridge-induced supervision and yields a simple stop-gradient regression objective. The learned controller is applied through sampled-data updates that exactly respect the LTI dynamics and actuation channel, enabling few-step swarm steering at scale.

## Contribution

It links flow-matching and generative models with optimal-transport-style swarm density steering under realistic sampled-data constraints, from the control-theory community (Chen, Johansson, Karlsson).

## Key results

- Few-step swarm steering at scale consistent with finite-window actuation (claimed in abstract; no numbers there).

## Methods and models

MeanFlow generalised to LTI systems, minimum-energy bridges, stop-gradient regression, sampled-data deployment.

## Limitations and open questions

Abstract-depth entry. Linear dynamics and centralised density-level control assumed.

## Relevance to us

Density-level (mean-field) control view of swarms; complements agent-level learned control such as [[huang-2024-collision]] and continuum models such as [[jin-2026-physics]].

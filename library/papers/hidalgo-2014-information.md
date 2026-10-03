---
id: hidalgo-2014-information
type: paper
title: 'Information-based fitness and the emergence of criticality in living systems'
authors: ['Jorge Hidalgo', 'Jacopo Grilli', 'Samir Suweis', 'Miguel A. Muñoz', 'Jayanth R. Banavar', 'Amos Maritan']
year: 2014
venue: 'Proceedings of the National Academy of Sciences'
url: https://arxiv.org/abs/1307.4325
doi: 10.1073/pnas.1319166111
arxiv: '1307.4325'
cite: 'Hidalgo, J., Grilli, J., Suweis, S., Muñoz, M. A., Banavar, J. R., & Maritan, A. (2014). Information-based fitness and the emergence of criticality in living systems. Proceedings of the National Academy of Sciences, 111(28), 10095–10100.'
topics: [criticality-measurement, marl-emergence]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: '208 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Uses statistical mechanics and information theory to show that adaptive or evolving agents that must
represent heterogeneous environments are most efficient at criticality. In evolutionary and adaptive models a
community self-tunes to near-critical states as environmental complexity rises, stays non-critical for simple
environments, and converges robustly to criticality when agents co-evolve to represent each other.

## Contribution

A widely cited mechanism for why living systems would evolve to criticality, based on
information-based fitness; later challenged for spatial animal groups by [[klamser-2021-collective]].

## Key results

- Agents tuned to criticality cope best with diverse environments (analytic and computational).
- Communities self-tune near criticality as environmental complexity increases; co-adaptation gives robust convergence.

## Methods and models

Agents as binary networks whose parameters evolve or adapt to minimise KL divergence to environmental
or other agents' distributions. arXiv 1307.4325.

## Limitations and open questions

Each agent can itself be critical (single-unit transition), and interactions are non-spatial, which
[[klamser-2021-collective]] identifies as key differences. Abstract-level read.

## Relevance to us

Directly relevant to learning agents (including MARL) that co-adapt: predicts self-tuning to
criticality, a testable hypothesis in agent swarms.

---
id: peigne-lefebvre-2025-multi
type: paper
title: 'Multi-Agent Security Tax: Trading Off Security and Collaboration Capabilities
  in Multi-Agent Systems'
authors:
- Pierre Peigne-Lefebvre
- Mikolaj Kniejski
- Filip Sondej
- Matthieu David
- Jason Hoelscher-Obermaier
- Christian Schroeder de Witt
- Esben Kran
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2502.19145
doi: null
arxiv: '2502.19145'
cite: 'Pierre Peigne-Lefebvre; Mikolaj Kniejski; Filip Sondej; Matthieu David; Jason
  Hoelscher-Obermaier; Christian Schroeder de Witt; Esben Kran. (2025). Multi-Agent
  Security Tax: Trading Off Security and Collaboration Capabilities in Multi-Agent
  Systems. arXiv preprint arXiv:2502.19145.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: shadow/sol-g74
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

The authors simulate cooperative agents after one participant is compromised, observing multi-hop spread of malicious instructions. They compare two memory-based vaccination approaches and two generic safety-instruction approaches. Each reduces spread or malicious-task fulfilment in the tested settings but also tends to reduce collaborative performance, motivating joint security and utility evaluation.

## Contribution

Published analysis of propagation risks or defence trade-offs in agent networks.

## Key results

Four defence strategies are compared in the abstract. Numerical trade-off curves were not checked.

## Methods and models

Abstract and bibliographic metadata read.

## Limitations and open questions

Full methods and adaptive threat evaluation not independently checked.

## Relevance to us

Important negative-design evidence: reducing propagation can reduce the capability that a parent wanted from its children. Compare [[wu-2025-cowpox]] and [[lee-2024-prompt]].

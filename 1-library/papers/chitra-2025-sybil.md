---
id: chitra-2025-sybil
type: paper
title: 'On Sybil-proofness in Restaking Networks'
authors:
- 'Tarun Chitra'
- 'Paolo Penna'
- 'Manvir Schneider'
year: 2025
venue: 'arXiv preprint (cs)'
url: https://arxiv.org/abs/2509.18338
doi: null
arxiv: '2509.18338'
cite: 'Chitra, T., Penna, P., & Schneider, M. (2025). On Sybil-proofness in Restaking Networks. arXiv preprint arXiv:2509.18338.'
topics:
- sybil-resistance
- sync-consensus
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Restaking lets validators secure several services at once, and its security depends on resistance to Sybil attacks. The paper formalises Sybil-proofness for restaking with two attack types: one where other Sybil identities are kept out of an attack and one where several Sybil identities attack together. It analyses marginal and multiplicative slashing, proves that no slashing mechanism prevents both attack types, and shows with random graphs that Erdos-Renyi networks remain Sybil-proof while a two-block stochastic block model with minimal heterogeneity makes Sybil attacks profitable.

## Contribution

An impossibility for slashing-based Sybil deterrence and a demonstration that network topology decides whether splitting stake across identities pays.

## Key results

- No slashing mechanism can prevent both attack types simultaneously (abstract).
- Erdos-Renyi restaking graphs remain Sybil-proof; a two-block stochastic block model with minimal heterogeneity makes Sybil attacks profitable (abstract).

## Methods and models

Bipartite validator-service graph with stake; marginal and multiplicative slashing rules; random graph models.

## Limitations and open questions

Abstract-level read.

## Relevance to us

Agent swarms that bond stake to many tasks or services have the same structure as restaking. The topology result is directly testable in simulation: heterogeneity in which agents serve which tasks can flip splitting from unprofitable to profitable. Related: [[pan-2024-sybil]], [[mazorra-2023-cost]].

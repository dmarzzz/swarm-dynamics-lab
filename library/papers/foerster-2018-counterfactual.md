---
id: foerster-2018-counterfactual
type: paper
title: Counterfactual Multi-Agent Policy Gradients
authors:
- Jakob Foerster
- Gregory Farquhar
- Triantafyllos Afouras
- Nantas Nardelli
- Shimon Whiteson
year: 2018
venue: Proceedings of the AAAI Conference on Artificial Intelligence
url: https://arxiv.org/abs/1705.08926
doi: 10.1609/aaai.v32i1.11794
arxiv: '1705.08926'
cite: Foerster, J., Farquhar, G., Afouras, T., Nardelli, N., & Whiteson, S. (2018). Counterfactual multi-agent policy gradients. Proceedings of the AAAI Conference on Artificial Intelligence, 32(1). https://doi.org/10.1609/aaai.v32i1.11794
topics:
- marl-emergence
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 1386 (Crossref, 2026-10-03)
code: []
---

## Summary

COMA is a multi-agent actor-critic with a centralised critic and decentralised actors. To solve credit assignment, each agent's advantage uses a counterfactual baseline that marginalises out that agent's action while holding others fixed, computed in one forward pass by a suitable critic architecture. On decentralised StarCraft unit micromanagement with partial observability, COMA beats other multi-agent actor-critic methods and its best agents are competitive with centralised controllers with full state.

## Contribution

The standard answer to multi-agent credit assignment with a shared team reward, a problem that also arises in swarm tasks with global rewards ([[huttenrauch-2019-deep]]).

## Key results

- Significant improvement over other multi-agent actor-critic methods on StarCraft micromanagement (claimed in abstract).

## Methods and models

Centralised critic Q(s, u), counterfactual advantage A_a = Q(s,u) - sum_u' pi_a(u'|tau_a) Q(s,(u_-a,u')). Abstract-level read.

## Limitations and open questions

Critic scales with joint action; tested on small teams.

## Relevance to us

Credit assignment in global-reward swarm tasks. Related: [[rashid-2018-qmix]], [[lowe-2017-multi]].

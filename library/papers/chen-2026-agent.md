---
id: chen-2026-agent
type: paper
title: "Agent-based modelling of Sybil attack using network expansion strategies"
authors: [Shengyu Chen, Hui Zhang, Junhuan Zhang]
year: 2026
venue: "IMA Journal of Management Mathematics"
url: https://doi.org/10.1093/imaman/dpag025
doi: 10.1093/imaman/dpag025
arxiv: null
cite: "Chen, S., Zhang, H., & Zhang, J. (2026). Agent-based modelling of Sybil attack using network expansion strategies. IMA Journal of Management Mathematics, dpag025. https://doi.org/10.1093/imaman/dpag025"
topics: [sybil-resistance]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "0 (Crossref, 2026-10-03)"
code: []
---

## Summary

Agent-based study of how the way new nodes are admitted to a permissionless blockchain affects Sybil resistance. Consensus backbone: Identity-Augmented Proof-of-Stake (IdAPoS), in which existing members vote to admit newcomers. They add an on-chain Sybil-detection step that derives node-level suspicion scores from on-chain voting relationships (removing IdAPoS's dependence on off-chain honesty information), formalise two admission models (Applicant-based vs Participant-based network expansion) on a preferential-attachment growth model, and simulate voting-token value under Sybil attack. Findings per the abstract: Sybil attacks can only be delayed, not eliminated; more centralisation among honest nodes strengthens resistance; under superlinear growth the participant-based model scales more stably; IdAPoS gains Sybil resilience at the cost of more concentrated voting power. Only the abstract was read.

## Contribution

Quantifies, in simulation, the trade-off between Sybil resilience and voting-power concentration under different admission processes for identity-based PoS.

## Key results

- Sybil takeover can be delayed but not prevented (abstract).
- Resilience improves with honest-node centralisation; participant-based expansion more stable under superlinear growth (abstract).

## Methods and models

Preferential-attachment network growth, IdAPoS admission voting, on-chain suspicion scoring from voting graphs, agent-based simulation of token value.

## Limitations and open questions

Not assessed beyond the abstract; results depend on the specific IdAPoS model and simulated attacker strategy.

## Relevance to us

The resilience-versus-centralisation trade-off is the recurring theme in Sybil defence (social-graph schemes, BASALT's prefix diversity, personhood issuers); this gives a simulated data point for admission-by-vote. Related: [[douceur-2002-sybil]], [[yu-2006-sybilguard]], [[auvolat-2021-basalt]].

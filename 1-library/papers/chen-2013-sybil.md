---
id: chen-2013-sybil
type: paper
title: 'Sybil-proof Mechanisms in Query Incentive Networks'
authors:
- 'Wei Chen'
- 'Yajun Wang'
- 'Dongxiao Yu'
- 'Li Zhang'
year: 2013
venue: 'Proceedings of the 14th ACM Conference on Electronic Commerce (EC ''13)'
url: https://arxiv.org/abs/1304.7432
doi: 10.1145/2482540.2482588
arxiv: '1304.7432'
cite: 'Chen, W., Wang, Y., Yu, D., & Zhang, L. (2013). Sybil-proof mechanisms in query incentive networks. In Proceedings of the 14th ACM Conference on Electronic Commerce (EC ''13), 197-214. ACM.'
topics:
- sybil-resistance
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 'OpenAlex 2026-10-03: 16 (EC version)'
code: []
---

## Summary

Following Kleinberg and Raghavan's query incentive networks, agents are nodes of an infinite random branching tree, a query starts at the root, and each node holds the answer with probability 1/n. The paper proposes direct referral (DR) mechanisms that give most of the reward to the answer holder and its direct parent. Properly designed DR mechanisms are Sybil-proof and efficient, with expected cost O(h^2) for propagating a query h levels for any branching factor b > 1, and optimal on a deterministic chain under mild assumptions.

## Contribution

Exponential improvement in cost over earlier query-incentive mechanisms while adding Sybil-proofness.

## Key results

- Expected cost O(h^2) to propagate h levels for any branching factor b > 1 (abstract).
- On a deterministic chain, the DR mechanism is optimal under mild assumptions.

## Methods and models

Random branching-process tree; strategic nodes maximise payoff; mechanism allocates reward along the path to the answer holder.

## Limitations and open questions

Abstract-level read. Assumes tree structure and independent answer probability.

## Relevance to us

Delegation of a question through a hierarchy of LLM agents, each of which can spawn helpers, is a query incentive network. Concentrating reward on the answerer and its direct referrer removes the gain from inserting clones. See [[zhang-2023-collusion]] for the impossibility once collusion is added and [[babaioff-2012-bitcoin]] for the propagation analogue.

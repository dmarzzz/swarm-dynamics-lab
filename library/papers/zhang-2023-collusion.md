---
id: zhang-2023-collusion
type: paper
title: 'Collusion-proof And Sybil-proof Reward Mechanisms For Query Incentive Networks'
authors:
- 'Youjia Zhang'
- 'Pingzhong Tang'
year: 2023
venue: 'Proceedings of the AAAI Conference on Artificial Intelligence (AAAI-23)'
url: https://arxiv.org/abs/2302.06061
doi: 10.1609/aaai.v37i5.25730
arxiv: '2302.06061'
cite: 'Zhang, Y., & Tang, P. (2023). Collusion-Proof and Sybil-Proof Reward Mechanisms for Query Incentive Networks. Proceedings of the AAAI Conference on Artificial Intelligence, 37(5). arXiv:2302.06061.'
topics:
- sybil-resistance
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 'OpenAlex 2026-10-03: 4 (AAAI version)'
code: []
---

## Summary

In a query tree issued by a task owner, agents are rewarded for solving the task or inviting others to solve it, within a budget. The paper proves that no reward mechanism can be both Sybil-proof (no gain from fake identities) and collusion-proof (no gain from several agents pretending to be one) together with other essential properties. It proposes one mechanism that achieves each property separately and a second that trades exact Sybil-proofness for approximate Sybil-proofness and collusion-proofness, and reports experiments where the second outperforms existing mechanisms.

## Contribution

Shows that Sybil-proofness and its mirror image, collusion-proofness (merging identities), conflict in referral reward design.

## Key results

- Impossibility: Sybil-proof, collusion-proof and other essential properties cannot hold together.
- A second mechanism achieves approximate versions of both and performs better than existing ones in the authors' experiments.

## Methods and models

Query tree, budget-constrained reward allocation, axiomatic impossibility, simulation experiments.

## Limitations and open questions

Abstract-level read; the experimental setup is not recorded.

## Relevance to us

Agent swarms face both splitting (one operator runs many agents) and merging (several operators present as one agent to capture a bigger share). This result says the designer must pick or approximate. Read with [[chen-2013-sybil]] and [[pan-2024-sybil]], which separates collusion from Sybils explicitly.

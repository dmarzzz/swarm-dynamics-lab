---
id: mazorra-2023-optimality
type: paper
title: 'On the optimality of Shapley mechanism for funding public excludable goods under Sybil strategies'
authors:
- 'Bruno Mazorra'
year: 2023
venue: 'arXiv preprint (cs.GT)'
url: https://arxiv.org/abs/2312.17058
doi: null
arxiv: '2312.17058'
cite: 'Mazorra, B. (2023). On the optimality of Shapley mechanism for funding public excludable goods under Sybil strategies. arXiv preprint arXiv:2312.17058.'
topics:
- sybil-resistance
- collective-decision
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Cost-sharing mechanisms for public excludable goods had not been studied under Sybil strategies. The paper shows that proposed cost-sharing mechanisms are not Sybil-resistant and proves that no deterministic, anonymous, truthful, Sybil-proof, upper semicontinuous and individually rational cost-sharing mechanism is better than Omega(n)-approximate. It then defines Sybil Welfare Invariant mechanisms, whose welfare does not fall under Sybil strategies when agents play weakly dominant strategies with subjective priors, and proves the Shapley value mechanism for symmetric submodular costs has this property, with worst-case social cost equal to the n-th harmonic number H_n in equilibrium with Sybils.

## Contribution

Shows that Shapley cost sharing, which is not Sybil-proof in the strict sense, still keeps its H_n worst-case efficiency when agents may use Sybils, so public goods can be funded permissionlessly and anonymously.

## Key results

- No deterministic, anonymous, truthful, Sybil-proof, upper semicontinuous, individually rational cost-sharing mechanism beats Omega(n)-approximation (abstract).
- The Shapley mechanism for symmetric submodular costs is Sybil Welfare Invariant; worst-case social cost H_n under Sybil equilibrium (abstract).

## Methods and models

Cost-sharing mechanism design for public excludable goods with private valuations and an unknown number of participants.

## Limitations and open questions

Abstract-level read. The positive result relies on a weaker notion than Sybil-proofness and on agents' subjective priors.

## Relevance to us

A useful reframing for swarms: instead of demanding no agent ever clones, require that cloning does not reduce welfare. This is the cost-sharing companion to [[mazorra-2023-cost]] (which proved the Shapley cost-sharing mechanism is not Sybil-proof) and bears on Shapley-based attribution in [[patel-2025-maxshapley]] and [[ohta-2008-anonymity]].

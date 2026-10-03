---
id: yaish-2026-inequality
type: paper
title: 'Inequality in the Age of Pseudonymity'
authors:
- 'Aviv Yaish'
- 'Nir Chemaya'
- 'Dahlia Malkhi'
- 'Lin William Cong'
year: 2026
venue: 'Proceedings of the AAAI Conference on Artificial Intelligence (AAAI-26)'
url: https://arxiv.org/abs/2508.04668
doi: 10.1609/aaai.v40i20.38781
arxiv: '2508.04668'
cite: 'Yaish, A., Chemaya, N., Malkhi, D., & Cong, L. W. (2026). Inequality in the Age of Pseudonymity. Proceedings of the AAAI Conference on Artificial Intelligence, 40(20), 17293-17301.'
topics:
- sybil-resistance
- criticality-measurement
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Inequality measures such as the Gini coefficient are applied to digital platforms where actors can hold many pseudonyms. The paper proves that no measure satisfying the canonical axioms can assess inequality in an economy that may contain Sybils, characterises the class of Sybil-proof measures, shows they must satisfy relaxed axioms and cannot assess inequality at a fine-grained level, and shows that popular measures including the Gini coefficient are not Sybil-proof. It also examines dynamics that lead to Sybil creation.

## Contribution

Extends Sybil-proofness from mechanisms to measurement: a statistic computed over identities is itself manipulable.

## Key results

- Impossibility for canonical inequality axioms under possible Sybils (abstract).
- Characterisation of Sybil-proof inequality measures; the Gini coefficient and other popular measures are not Sybil-proof (abstract).

## Methods and models

Axiomatic analysis of inequality indices over wealth vectors where one actor's wealth can be split among several identities.

## Limitations and open questions

Abstract-level read.

## Relevance to us

Any swarm-level health metric computed per identity (concentration of reward, diversity of votes, Gini of stake among agents or block builders) is gameable by splitting. When measuring decentralisation of an agent collective, aggregate by controlling principal or use a Sybil-proof measure. Related: [[mazorra-2023-cost]], [[messias-2023-airdrops]].

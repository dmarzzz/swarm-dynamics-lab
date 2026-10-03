---
id: el-mhamdi-2018-hidden
type: paper
title: The Hidden Vulnerability of Distributed Learning in Byzantium
authors:
- El Mahdi El Mhamdi
- Rachid Guerraoui
- Sebastien Rouault
year: 2018
venue: ICML 2018 (arXiv preprint)
url: https://arxiv.org/abs/1802.07927
doi: null
arxiv: '1802.07927'
cite: 'El Mhamdi, E. M., Guerraoui, R., & Rouault, S. (2018). The Hidden Vulnerability of Distributed Learning in Byzantium. arXiv preprint arXiv:1802.07927.'
topics:
- fork-merge-security
- sync-consensus
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Shows that convergence guarantees for Byzantine-resilient aggregation rules are not enough. In high dimension d, existing rules leave the attacker a poisoning margin that grows at least like sqrt(d), and the attacker can use non-convexity to make SGD converge to a bad model while every convergence condition holds. The authors build a simple attack exploiting this margin and report strong effect on CIFAR-10 and MNIST, then propose Bulyan, which combines a Krum-like selection with coordinate-wise trimmed aggregation and shrinks the leeway to O(1/sqrt(d)).

## Contribution

Identifies the dimension-dependent leeway in robust aggregation and introduces Bulyan, which needs a larger honest margin than Krum.

## Key results

- Proved (per abstract): existing resilient rules leave a poisoning margin Omega(f(d)) with f(d) growing at least like sqrt(d).
- Measured (per abstract): a simple attack using this leeway is highly effective on CIFAR-10 and MNIST.
- Proved (per abstract): Bulyan reduces the leeway to O(1/sqrt(d)) at the cost of larger batch sizes.

## Methods and models

Analysis of Krum, median-type rules and Bulyan; image classification experiments. Only the abstract was read; the exact Bulyan threshold (stated in the paper body) was not checked.

## Limitations and open questions

Abstract-level reading.

## Relevance to us

Q2 and Q3. For LLM sub-agents the "dimension" is the space of possible memories, beliefs and instructions they can return, which is effectively unbounded. A merge rule that only checks that each returned contribution looks close to the others leaves the attacker a large in-distribution margin to steer the parent, the same lesson as [[baruch-2019-little]]. Follows [[blanchard-2017-byzantine]].

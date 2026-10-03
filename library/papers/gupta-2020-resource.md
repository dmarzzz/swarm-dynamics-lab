---
id: gupta-2020-resource
type: paper
title: "Resource Burning for Permissionless Systems"
authors: ["Diksha Gupta", "Jared Saia", "Maxwell Young"]
year: 2020
venue: "Structural Information and Communication Complexity (SIROCCO 2020), Lecture Notes in Computer Science, vol. 12156 (invited paper); arXiv preprint"
url: https://arxiv.org/pdf/2006.04865
doi: "10.1007/978-3-030-54921-3_2"
arxiv: "2006.04865"
cite: "Gupta, D., Saia, J., & Young, M. (2020). Resource Burning for Permissionless Systems (Invited Paper). In Structural Information and Communication Complexity (SIROCCO 2020), Lecture Notes in Computer Science, vol. 12156, pp. 19-44. Springer. arXiv:2006.04865."
topics: [sybil-resistance, sync-consensus, meta]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "3 (OpenAlex, LNCS version) and 1 (OpenAlex, arXiv version), 2026-10-03"
code: []
---

## Summary

A survey that names "resource burning", the verifiable consumption of a resource solely to convey information, as the common tool behind proof-of-work, CPU puzzles in DHTs, bandwidth and puzzle defences against DDoS, and CAPTCHAs against review spam. It links the idea to money burning and costly signalling in economics and biology, reviews results in four domains, and poses open problems aimed at lowering the cost honest participants pay.

## Contribution

Treats PoW, PoS-like stake and CAPTCHAs as one family of Sybil defences and makes the efficiency question precise: under attack, good identities should spend asymptotically less than the adversary. This is the resource-testing branch of [[douceur-2002-sybil]] and [[levine-2006-survey]], updated for blockchains.

## Key results

- Table 1 conjectured spend rates for good IDs: blockchains O(√(T·J_G) + J_G), DHTs Õ(√(T·J_G) + J_G), review spam Õ(T^(2/3) + P_G), no conjecture for DDoS. Here T is the adversary's spending rate and J_G the join rate of good IDs (as defined in the paper; I did not check every proof).
- Position: resource burning is unlikely to be eliminated, because it plays the role of costly signalling, but its asymptotic cost can be cut substantially; current costs are prohibitively high for most systems.
- Resources burned include computation, bandwidth, memory and human effort.

## Methods and models

Survey of algorithmic results on puzzle-based Sybil defences with churn, including the authors' own work on spending in proportion to attacker spending; statement of open problems.

## Limitations and open questions

Theoretical and focused on the distributed-computing community; little empirical data on real costs. Assumes the adversary controls bounded resources, so it does not cover identity markets where resources are bought.

## Relevance to us

For agent swarms, the costly-signal view is the most directly usable framing: make each agent identity spend something (compute, stake, latency, human attention) that scales with the influence it gets, and design the rule so honest agents spend in proportion to the attack rather than continuously. It is the counterpart to personhood-based approaches [[borge-2017-proof-of-personhood]] and to graph-based ones [[cao-2012-aiding]]. Mechanism-design versions of the same question belong to the sybil-mechanisms lane.

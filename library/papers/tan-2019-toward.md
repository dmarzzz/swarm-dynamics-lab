---
id: tan-2019-toward
type: paper
title: "Toward a Comprehensive Insight Into the Eclipse Attacks of Tor Hidden Services"
authors: [Qingfeng Tan, Yue Gao, Jinqiao Shi, Xuebin Wang, Binxing Fang, Zhihong Tian]
year: 2019
venue: IEEE Internet of Things Journal, vol. 6, no. 2, pp. 1584-1593
url: https://ieeexplore.ieee.org/document/8382237
doi: 10.1109/jiot.2018.2846624
arxiv: null
cite: "Tan, Q., Gao, Y., Shi, J., Wang, X., Fang, B., & Tian, Z. (2019). Toward a Comprehensive Insight Into the Eclipse Attacks of Tor Hidden Services. IEEE Internet of Things Journal, 6(2), 1584-1593. https://doi.org/10.1109/JIOT.2018.2846624"
topics: [sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "104 (Crossref, 2026-10-03)"
code: []
---

## Summary

Tor hidden services (v2 era) publish their descriptors into a distributed hash ring of hidden service directories (HSDirs) chosen by position in a hash space, so an adversary who can place relays with identity fingerprints adjacent to a target's descriptor IDs becomes that service's directory and can refuse to serve it, blocking the service without touching the server. The paper presents practical Eclipse attacks of this kind and finds the binding cost is IP addresses, not compute: experiments show three IP addresses suffice to eclipse an arbitrary hidden service with 100% success, because fingerprint grinding is cheap and Tor's limits on relays per IP are the only barrier. It then gives what it calls the first formal probabilistic analysis of the attack's cost and reach, concluding that an adversary with a modest pool of IPs can block a large number of hidden services at any given time, and closes with countermeasures (e.g. unpredictable descriptor placement, which the v3 onion service design later adopted) and future work. Abstract only (IEEE Xplore; paywalled, no OA copy); the exact analysis, Tor version and experiment setup are not visible.

## Contribution

Quantifies that Eclipse against Tor HSDirs needs single-digit IP addresses per target, and models how many services a given IP budget can suppress.

## Key results

- Three IPs eclipse one arbitrary hidden service with 100% success (abstract).
- Probabilistic cost model: modest IP resources block many HSs simultaneously (abstract; numbers not visible).

## Methods and models

Live or testbed Tor experiments plus probabilistic analysis; details not read.

## Limitations and open questions

Abstract-level. Applies to v2 onion services whose HSDir positions were predictable; v3 (2017 onward) randomises via shared random values, which should change the cost structure but the abstract does not say whether that is evaluated.

## Relevance to us

A sharp example of the "identity is cheap, the scarce resource is something else" pattern: Sybil defences that count per-IP push attackers to IP acquisition, and three is a small number. Useful for the sybil-resistance survey's discussion of resource-based admission ([[urdaneta-2011-survey]] taxonomy,, [[douceur-2002-sybil]]) and sits next to [[heilman-2015-eclipse]] (Bitcoin) and [[steiner-2007-exploiting]] (KAD) as system-specific eclipse case studies. Companion detector on Ethereum: [[xu-2020-am]].

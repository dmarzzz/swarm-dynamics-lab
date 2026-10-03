---
id: gupta-2021-bankrupting
type: paper
title: "Bankrupting Sybil Despite Churn"
authors: ["Diksha Gupta", "Jared Saia", "Maxwell Young"]
year: 2021
venue: "41st IEEE International Conference on Distributed Computing Systems (ICDCS 2021), pp. 425-437; extended version in Journal of Computer and System Sciences (2023); arXiv:2010.06834"
url: https://arxiv.org/pdf/2010.06834
doi: "10.1109/ICDCS51616.2021.00048"
arxiv: "2010.06834"
cite: "Gupta, D., Saia, J., & Young, M. (2021). Bankrupting Sybil Despite Churn. In Proceedings of the 41st IEEE International Conference on Distributed Computing Systems (ICDCS), pp. 425-437. https://doi.org/10.1109/ICDCS51616.2021.00048. Extended version: Journal of Computer and System Sciences (2023), https://doi.org/10.1016/j.jcss.2023.02.004; arXiv:2010.06834."
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: "8 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

The paper presents Ergo, a resource-burning Sybil defence that keeps bad IDs below 1/6 of the system while good IDs spend asymptotically less than the attacker, even when churn varies exponentially. A server (or, in Section 12, a small committee) charges each joining ID a resource-burning challenge whose hardness is 1 plus the number of IDs that joined in the last 1/J~ seconds, where J~ is an estimate of the good join rate from a companion algorithm, GoodJEst. When joins and departures in an iteration exceed 1/11 of the membership, everyone must solve a 1-hard challenge within one round or be purged. On churn traces from Bitcoin, BitTorrent, Ethereum and Gnutella, Ergo spends up to two orders of magnitude less than prior defences, and up to three when combined with a machine-learning Sybil classifier.

## Contribution

Removes the smooth-arrival assumption of [[gupta-2019-resource]] and is, per the authors, the first formal definition of the Sybil defence problem with churn. It also shows how an imperfect classifier can be combined with a provable resource-burning bound without losing the bound.

## Key results

- Theorem 1: for an adversary with at most kappa <= 1/18 of the resource, the bad-ID fraction stays below 3*kappa <= 1/6, and the good spend rate is O(sqrt(T(J+1)) + J) up to constants in alpha, beta, with error probability o(1/n0) over the system lifetime.
- Intuition (Section 7.1): if x bad IDs join per good join, the adversary pays 1+2+...+x = Theta(x^2) in entrance costs while the good ID pays O(x), so good spending is about the square root of adversarial spending.
- Theorem 2: GoodJEst estimates the good join rate within constant factors regardless of how the adversary injects IDs; empirically always within a factor of 10.
- Lower bound (Section 11): asymptotically optimal for a large class of algorithms.
- Experiments: Ergo versus CCom, SybilControl and REMP on four churn datasets; Ergo-SF assumes classifier accuracy 0.98 (from SybilFuse) and refuses entry to IDs classified bad.
- The paper states that proof of stake is not resource burning because it needs globally known stake.

## Methods and models

Single coordinating server learning all joins and departures (decentralised by a committee in Section 12); resource-burning challenges of tunable hardness that cannot be precomputed; synchronised clocks; at most an epsilon fraction of good IDs depart per round; each joining ID knows one good ID (stated as needed to avoid eclipse attacks, citing [[heilman-2015-eclipse]]). MATLAB simulations. I read the abstract, introduction, model, results statements, the Ergo algorithm and intuition, and the experiment setup; not the proofs.

## Limitations and open questions

Assumes a server or honest-majority committee and a known good entry point; the paper leaves incentives for good IDs to solve challenges open. Resource burning is assumed homogeneous across good IDs. Churn data for Ethereum and BitTorrent are simulated from fitted Weibull distributions.

## Relevance to us

This is the strongest theoretical result for "churn as continuous agent spawning": a swarm coordinator can price agent admission by recent join pressure and periodically re-test all agents, keeping Sybil agents a fixed minority while honest agents pay roughly the square root of what an attacker spends. The classifier result fits the practical setting where agent Sybils are flagged by an LLM or graph classifier with known error. It bounds identities, and only against an adversary with bounded resources; it says nothing about influence per identity, which is where [[vyzovitis-2020-gossipsub]] and [[singh-2006-eclipse]] come in. Related: [[gupta-2020-resource]], [[gupta-2018-proof]], [[gupta-2019-resource]], [[douceur-2002-sybil]], [[cao-2012-aiding]].

---
id: gupta-2018-proof
type: paper
title: "Proof of Work Without All the Work"
authors: ["Diksha Gupta", "Jared Saia", "Maxwell Young"]
year: 2018
venue: "Proceedings of the 19th International Conference on Distributed Computing and Networking (ICDCN 2018), pp. 1-10; extended version arXiv:1708.01285"
url: https://arxiv.org/pdf/1708.01285
doi: "10.1145/3154273.3154333"
arxiv: "1708.01285"
cite: "Gupta, D., Saia, J., & Young, M. (2018). Proof of Work Without All the Work. In Proceedings of the 19th International Conference on Distributed Computing and Networking (ICDCN '18), pp. 1-10. ACM. https://doi.org/10.1145/3154273.3154333. Extended version: arXiv:1708.01285."
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "36 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

The paper designs CCom, a proof-of-work Sybil defence for a dynamic system with churn in which honest participants only do work in proportion to the attack. Every joining ID solves a puzzle, and whenever the population changes by a constant fraction all IDs re-solve a puzzle (a purge) and a new committee is elected. Under the assumption that the adversary holds at most a 1/6 share of computational power, bad IDs always stay below half of the system and of a logarithmic-size committee, while the good IDs' total computational cost is O(T_C + g_new), linear in the adversary's spending T_C plus the number of good joins.

## Contribution

Moves Sybil-resistant PoW from "always burn" to resource-competitive: the defence costs little when nobody attacks and scales with the attacker's spending when someone does. It is the first of three papers by the same authors ([[gupta-2019-resource]], [[gupta-2021-bankrupting]]) and is surveyed in [[gupta-2020-resource]].

## Key results

- Theorem 1 (CCom), adversary with at most 1/6 of computational power, w.h.p. over a polynomial system lifetime: fraction of bad IDs always below 1/2; a known committee of logarithmic size with a bad fraction below 1/2; cumulative good computational cost O(T_C + g_new); cumulative good bandwidth cost O~(T_B + g_new).
- Section 3 reports simulations on several network churn datasets showing reduced computational cost versus always-on PoW (I read the claim, not the figures in detail).
- Section 4 applies the result to Byzantine consensus and to the Elastico committee-election protocol.

## Methods and models

Good and bad virtual IDs, a single adversary controlling all bad IDs, a DIFFUSE broadcast primitive with bounded delay where the sender cannot be identified, synchronised rounds, random-oracle puzzles. I read the abstract, model, main theorem and related work.

## Limitations and open questions

Assumes a reliable diffusion primitive among good IDs, which is exactly what an eclipse attack ([[heilman-2015-eclipse]]) breaks. Good spend is linear in the attacker's, not sublinear; the later papers improve this. Incentives for honest IDs to solve puzzles are not addressed.

## Relevance to us

Continuous agent spawning is churn, and CCom's rule (charge on join, re-test everyone after the population turns over by a constant fraction) is a direct template for admitting agents to a swarm without a standing tax on every agent. It bounds identities: the number of bad IDs relative to good ones, given bounded adversary resources. The related-work section also places proof of stake ([[gilad-2017-algorand]]) outside resource burning. Related: [[gupta-2020-resource]], [[douceur-2002-sybil]], [[aspnes-2005-exposing]].

---
id: gupta-2019-resource
type: paper
title: "Resource-Competitive Sybil Defenses"
authors: ["Diksha Gupta", "Jared Saia", "Maxwell Young"]
year: 2019
venue: "arXiv preprint (cs.DC)"
url: https://arxiv.org/pdf/1911.06462
doi: null
arxiv: "1911.06462"
cite: "Gupta, D., Saia, J., & Young, M. (2019). Resource-Competitive Sybil Defenses. arXiv:1911.06462."
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "1 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

This preprint presents two proof-of-work Sybil defences for systems with churn. CCom charges a puzzle on every join and purges the system whenever membership changes by a constant fraction, with good-ID spending rate O(T + J), where T is the adversary's spending rate and J the good join rate. GMCom scales the entrance cost with an estimate of the good join rate and reaches O(sqrt(T(J+1)) + J), so honest IDs spend asymptotically less than the attacker. A matching lower bound shows that any purge-based algorithm has spending rate Omega(sqrt(TJ) + J). Simulations show both algorithms compete with SybilControl and are significantly cheaper under attack.

## Contribution

States and proves the sqrt(TJ) optimality bound for purge-based Sybil defences. The bankrupting paper [[gupta-2021-bankrupting]] names IPDPS 2019 "Peace through superior puzzling: An asymmetric Sybil defense" as where this lower bound first appeared; this arXiv version appears to be the full write-up of that work, but I did not compare the two texts.

## Key results

- Theorem 1: for alpha < 1/6, CCom solves the DefID problem (keep bad IDs a minority) with spending rate O(T + J_G).
- Theorem 2: for alpha <= 1/18, GMCom spends O(sqrt(T(J_G + 1)) + J_G), under smoothness assumptions A1 and A2 on good join rates (no bursty arrivals).
- Theorem 3: any purge-based algorithm (Omega(1) to join, Omega(1) per ID after a constant fraction of turnover) has an adversary forcing Omega(sqrt(T J_G) + J_G).
- Heuristic variants reduce cost by up to two orders of magnitude during the largest attacks tested (Section 8).

## Methods and models

Same model as [[gupta-2018-proof]]: good and bad IDs, random-oracle puzzles, a DIFFUSE broadcast primitive, synchronised rounds, epochs defined by turnover of good IDs. I read the abstract, results statements, lower-bound statement and conclusion.

## Limitations and open questions

GMCom needs the good join rate to be smooth (assumptions A1, A2); [[gupta-2021-bankrupting]] removes this. Incentives for good IDs and rational participants are left open, as is extension to secure multiparty computation.

## Relevance to us

The lower bound is a useful sanity check for any agent-admission scheme based on spending: if newcomers pay to join and everyone pays again after turnover, the best honest cost is about the square root of attacker spend times honest join rate. It bounds identities. Related: [[gupta-2020-resource]], [[gupta-2018-proof]], [[gupta-2021-bankrupting]].

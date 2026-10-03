---
id: yu-2009-dsybil
type: paper
title: "DSybil: Optimal Sybil-Resistance for Recommendation Systems"
authors: ["Haifeng Yu", "Chenwei Shi", "Michael Kaminsky", "Phillip B. Gibbons", "Feng Xiao"]
year: 2009
venue: "30th IEEE Symposium on Security and Privacy (S&P 2009)"
url: https://www.comp.nus.edu.sg/~yuhf/dsybil-oakland09.pdf
doi: "10.1109/sp.2009.26"
arxiv: null
cite: "Yu, H., Shi, C., Kaminsky, M., Gibbons, P. B., & Xiao, F. (2009). DSybil: Optimal Sybil-Resistance for Recommendation Systems. In 2009 30th IEEE Symposium on Security and Privacy, pp. 283-298. IEEE."
topics: [sybil-resistance, collective-decision]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "68 (Crossref, 2026-10-03)"
code: []
---

## Summary

DSybil defends recommendation (voting) systems against an unlimited number of Sybil voters without any social graph or identity check. Each user keeps trust weights on voters and learns from feedback on objects it consumes; voters gain trust only when they vote early for objects that turn out good. The algorithm exploits the heavy-tailed voting behaviour of honest users and recommends an object only when the weighted votes already collected give "enough help", otherwise it seeks more.

## Contribution

A behaviour-based, provably optimal bound on the damage Sybils can do in collective recommendation, and the observation that for this problem the lifespan of honest users matters more than their number.

## Key results

- Loss (number of bad recommendations) is O(D log M) under the worst-case attack, where M is the maximum number of Sybil identities voting on any one object and D is the "dimension" of the objects; the authors prove this is optimal.
- When honest votes are heavy-tailed, D is small.
- Unlike Byzantine consensus or DHTs, tolerating more Sybils depends on honest users' lifespan (time to build trust) more than on honest population size.
- Defence grows over time: if a user has used DSybil before an attack starts, loss is much smaller than the worst case.
- Evaluation (trace-driven, including Digg data): loss stays small even against a million-node botnet using an optimal strategy (abstract and conclusion).

## Methods and models

Online learning with multiplicative trust updates (parameters α, β, c, S), proofs of expected loss bounds (Theorems 1 and 3), evaluation on voting traces. Assumes objects are good or bad per user and users aim to find some good objects, not rank all.

## Limitations and open questions

Applies to binary good/bad objects with feedback; a newcomer has no protection until it accumulates experience; Sybils can still cause O(D log M) bad recommendations per user.

## Relevance to us

Directly usable for agent swarms that aggregate advice: instead of verifying who an agent is, weight agents by a track record of being early and right, with a loss bound that grows only logarithmically in the number of Sybils. This is the reputation-learning counterpart to identity-based gating ([[borge-2017-proof-of-personhood]]) and graph-based gating ([[tran-2009-sybil-resilient]], same research group's lineage via [[yu-2006-sybilguard]]). It also connects to [[bara-2026-epistemic]], since DSybil rewards voters who supply information ahead of others rather than echoes.

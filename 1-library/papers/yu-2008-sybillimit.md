---
id: yu-2008-sybillimit
type: paper
title: "SybilLimit: A Near-Optimal Social Network Defense against Sybil Attacks"
authors: ["Haifeng Yu", "Phillip B. Gibbons", "Michael Kaminsky", "Feng Xiao"]
year: 2008
venue: "IEEE Symposium on Security and Privacy (S&P 2008)"
url: https://www.comp.nus.edu.sg/~yuhf/yuh-sybillimit.pdf
doi: "10.1109/sp.2008.13"
arxiv: null
cite: "Yu, H., Gibbons, P. B., Kaminsky, M., & Xiao, F. (2008). SybilLimit: A Near-Optimal Social Network Defense against Sybil Attacks. In 2008 IEEE Symposium on Security and Privacy (SP 2008), pp. 3-17. IEEE."
topics: [sybil-resistance]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "276 (Crossref, 2026-10-03)"
code: []
---

## Summary

SybilLimit keeps SybilGuard's insight (few attack edges, fast-mixing honest region) but uses many short random routes from each node, intersections on edges rather than nodes, a balance condition on the verifier's route tails, and a benchmarking technique to estimate route length. It accepts O(log n) Sybil nodes per attack edge instead of O(√n log n), and the guarantee holds while the number of attack edges is o(n / log n).

## Contribution

A near-optimal bound for the social-graph approach (within a log n factor of any fast-mixing-based defence, per the paper) and the first measurement that real social graphs are fast mixing.

## Key results

- Sybil nodes accepted per attack edge reduced by a factor of Θ(√n), about 200 times fewer than SybilGuard in their million-node experiments (abstract).
- Proven at most a log n factor from optimal among defences based on fast-mixing social networks.
- Measured: three large real social networks (Friendster, LiveJournal and DBLP, per the acknowledgements and evaluation) were found to be fast mixing, supporting the assumption.

## Methods and models

Random routes as in [[yu-2006-sybilguard]], r = Θ(√m) independent instances, tail intersection on edges, balance condition, benchmarking against random honest nodes to set r. Analysis plus simulation on real graph datasets.

## Limitations and open questions

[[danezis-2009-sybilinfer]] notes that SybilLimit needs an estimate of the number of honest nodes. Later measurements cited by [[cao-2012-aiding]] found mixing times longer than assumed in some social graphs, and [[viswanath-2010-analysis]] shows the defence degrades when honest users form strong communities.

## Relevance to us

The O(log n) per attack edge result is the reference number for any graph-based admission rule in an agent swarm: it tells us how many fake agents one compromised trust link can sponsor in the best case for this family. It also makes the dependence on graph mixing explicit, which matters for swarms whose trust graph is spatially clustered (robots that only meet neighbours). Related: [[alvisi-2013-sok]], [[mohaisen-2013-sybil]].

---
id: conitzer-2010-false-name-proofness
type: paper
title: "False-Name-Proofness in Social Networks"
authors: [Vincent Conitzer, Nicole Immorlica, Joshua Letchford, Kamesh Munagala, Liad Wagman]
year: 2010
venue: Internet and Network Economics, 6th International Workshop (WINE 2010), Stanford, Lecture Notes in Computer Science vol. 6484, pp. 209-221
url: http://www.cs.cmu.edu/~conitzer/fnp_socialWINE10.pdf
doi: 10.1007/978-3-642-17572-5_17
arxiv: null
cite: "Conitzer, V., Immorlica, N., Letchford, J., Munagala, K., & Wagman, L. (2010). False-Name-Proofness in Social Networks. In Internet and Network Economics (WINE 2010), LNCS 6484, pp. 209-221. Springer. https://doi.org/10.1007/978-3-642-17572-5_17"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "12 (Crossref, 2026-10-03)"
code: []
---

## Summary

Bridges the mechanism-design (false-name-proof) and systems (SybilGuard-style social graph) literatures. Motivated by Facebook's 2009 terms-of-use vote, the authors note that pure false-name-proof mechanisms are mostly negative results, and propose instead to use the social network to decide which identities may participate, then run an ordinary mechanism on the admitted set. The key observation: fake identities created by a coalition of at most k colluding real users are separated from the rest of the graph by a vertex cut of size at most k (the colluders themselves), so a "suspicion policy" that labels as suspect every node separated from a set of trusted nodes T by a vertex cut of size <= k, and admits the rest, cannot be gamed by coalitions of size <= k. Theorem 1: any k-robust suspicion policy yields false-name-proofness against coalitions of size <= k when composed with a strategy-proof mechanism. Theorem 2: the natural policy Pi*_k (iteratively remove nodes separated from T by cuts of size <= k) is k-robust, does not let a coalition affect the status of its own legitimate members, and labels every illegitimate node suspect. Theorem 3: Pi*_k is optimal, any other policy with these properties labels a superset of nodes suspect. Theorem 4: the suspect set is computable in polynomial time (max-flow / vertex connectivity). The second half drops exogenous trusted nodes: the designer must choose which nodes to verify, the feasible sets of nodes that can be made legitimate form a matroid (Theorem 5), so greedy verification is optimal for the budgeted problem. Read: abstract, introduction and relation to SybilGuard-type approximate-isolation conditions, model, Theorems 1-5 with proof sketches, discussion.

## Contribution

Positive result for false-name-proofness by composition: filter identities through a k-vertex-connectivity test against trusted seeds, then any strategy-proof mechanism becomes false-name-proof against k-coalitions, with an optimal and polynomial-time filter and a matroid structure for choosing whom to verify.

## Key results

- k-robust suspicion policy + strategy-proof mechanism = false-name-proof against coalitions <= k (Theorem 1).
- Pi*_k (remove nodes behind vertex cuts of size <= k from trusted set) is k-robust, catches all fakes, and is the minimal such policy (Theorems 2-3); computable in polynomial time (Theorem 4).
- Without given trusted nodes, legitimisable sets form a matroid, so greedy verification is optimal (Theorem 5).

## Methods and models

Graph-theoretic (vertex cuts, connectivity), mechanism design composition argument, matroid theory; no experiments.

## Limitations and open questions

Honest nodes that are themselves poorly connected to T (behind small cuts) get excluded, which is the same false-positive problem SybilShield documents empirically; k must be chosen; adversaries who obtain many real friendships (attack edges) evade the cut test. No data.

## Relevance to us

The cleanest formal statement that trust-graph admission plus a strategy-proof rule is enough for Sybil-proof collective decisions among agents, provided one operator's agents cannot acquire many independent endorsements. Links the mechanism side ([[wagman-2008-optimal]], [[todo-2011-false-name-proof]], [[conitzer-2010-using]]) to the systems side ([[yu-2006-sybilguard]], [[yu-2008-sybillimit]], [[shi-2013-sybilshield]], [[lesniewski-laas-2008-sybil-proof]]). Root: [[douceur-2002-sybil]].

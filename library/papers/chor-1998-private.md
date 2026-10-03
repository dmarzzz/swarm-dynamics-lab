---
id: chor-1998-private
type: paper
title: Private Information Retrieval
authors: [Benny Chor, Eyal Kushilevitz, Oded Goldreich, Madhu Sudan]
year: 1998
venue: Journal of the ACM
url: https://www.wisdom.weizmann.ac.il/~oded/PSX/pir2.pdf
doi: 10.1145/293347.293350
arxiv: null
cite: Chor, B., Kushilevitz, E., Goldreich, O., & Sudan, M. (1998). Private information retrieval. Journal of the ACM, 45(6), 965-981. Preliminary version in Proceedings of the 36th IEEE Symposium on Foundations of Computer Science (FOCS 1995), 41-50.
topics: [fork-merge-security]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: 1125 (Crossref, 2026-10-03)
code: []
---

## Summary

Chor, Goldreich, Kushilevitz and Sudan define private information retrieval: a user fetches bit i of an n-bit database without the database learning i. With one database, information-theoretic privacy requires downloading essentially the whole database (n bits). With k >= 2 non-colluding replicas they get a two-server scheme with O(n^(1/3)) communication, a k-server scheme with O(n^(1/k)), and a scheme with about (1/3) log2 n + 1 servers and polylogarithmic communication. Some schemes extend to t-privacy, where any t of the queries reveal nothing about i.

## Contribution

The founding definition and first sublinear schemes for hiding what a client is interested in from the servers that answer it.

## Key results

- Single-server information-theoretic PIR needs n bits of communication (Appendix A.1).
- Two servers: O(n^(1/3)); k servers: O(n^(1/k)); (1/3) log2 n + 1 servers: polylog n.
- t-private variants tolerate t colluding servers at a small communication penalty.

## Methods and models

Information-theoretic constructions using XOR (sum) queries over replicated copies; read the abstract, introduction, results summary and model.

## Limitations and open questions

Requires non-colluding replicas; servers do work linear in n per query. Computational single-server PIR came later.

## Relevance to us

Q1, the "hide interest" axis. dmarz's example (a sub-agent sent to explore a hostile domain) has a second leak beyond which part returns: what it looks at reveals what the parent wants, letting an adversary prepare tailored content for exactly the sub-agent that will be merged. PIR is the formal tool for a sub-agent to fetch from a hostile source without the source learning which item was fetched, so the source cannot tailor a poisoned answer to the parent's interest. Its non-collusion assumption is a threshold assumption (t-privacy), which links to Q2. Q3 relevance: tailoring is how injection payloads are targeted; PIR removes the targeting signal. Related hiding layers: [[chaum-1981-untraceable]], [[piotrowska-2017-loopix]].

---
id: lesniewski-laas-2008-sybil-proof
type: paper
title: "A Sybil-proof one-hop DHT"
authors: [Chris Lesniewski-Laas]
year: 2008
venue: Proceedings of the 1st Workshop on Social Network Systems (SocialNets '08), Glasgow, pp. 19-24
url: https://pdos.csail.mit.edu/papers/sybil-dht-socialnets08.pdf
doi: 10.1145/1435497.1435501
arxiv: null
cite: "Lesniewski-Laas, C. (2008). A Sybil-proof one-hop DHT. In Proceedings of the 1st Workshop on Social Network Systems (SocialNets '08), pp. 19-24. ACM. https://doi.org/10.1145/1435497.1435501"
topics: [sybil-resistance, sync-consensus]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "20 (Crossref, 2026-10-03)"
code: []
---

## Summary

Workshop precursor to Whanau (NSDI 2010). Poses the "Byzantine dissidents" problem: given a fast-mixing social network of n honest nodes and m honest edges with g attack edges to an adversary who can mint unlimited Sybil identities, can honest nodes route to each other in a structured overlay efficiently? Applying SybilLimit's random-walk certification naively costs O(n^2 sqrt m) bandwidth; this paper gives the first sublinear protocol. Each node performs r random walks of length w = O(log n) on the social graph; because the graph is fast mixing and escape probability into the Sybil region is o(1), at least a constant fraction of walk endpoints ("fingers") are honest. Fingers are hashed onto a ring with k virtual IDs each, and a cuckoo-hashing style pruning bounds the load per bin to O(log log nk) honest vIDs, giving a one-hop DHT with O(sqrt(m) log m) routing-table entries per node and O(1)-message lookups, tolerant to up to o(n / log n) attack edges, with lookup load spread in proportion to degree. Preliminary simulation on an Orkut crawl (7,335 nodes, 56,211 edges after removing degree < 5; w = 10, r = 1,000, finger tables ~650 entries) against an adversary that swallows every escaping walk: strict guarantee holds to roughly 750 attack edges, degradation is graceful beyond that, e.g. 15.8% lookup failure at g = 12,000 attack edges versus m = 43,930 honest edges. Read: abstract, introduction and problem statement, background table of parameters, protocol overview (random-walk fingers, virtual IDs, pruning), Section 4 results, conclusion; proofs of the bounds skimmed.

## Contribution

First structured DHT routing layer whose Sybil resistance comes from social-graph random walks rather than certification or puzzles, with sublinear table size and constant-hop lookups.

## Key results

- Table size O(sqrt(m) log m), O(1) lookup messages, tolerates o(n / log n) attack edges.
- Orkut simulation: failures flat until attack edges become comparable to honest edges; 15.8% failure at g = 12,000, m = 43,930.
- Fast-mixing assumption (w = O(log n)) is the load-bearing premise, inherited from SybilGuard/SybilLimit.

## Methods and models

Random walks on social graph, consistent hashing of fingers, virtual IDs with cuckoo-hash pruning, simulation against an optimal walk-swallowing adversary.

## Limitations and open questions

Preliminary (6 pages): single simulation graph, adversary model restricted to one strategy, churn and dynamic social graphs not handled; later Whanau addresses several. Real social graphs are not uniformly fast mixing, which later work showed weakens all this family's guarantees.

## Relevance to us

Shows the social-network Sybil defence family extending from admission control ([[yu-2006-sybilguard]], [[yu-2008-sybillimit]]) into actual routing, which is the step an agent network would need if it wanted trust-graph-based peer discovery; also a clean statement of the attack-edge metric (what matters is how many honest nodes trust the attacker, not how many identities it has). Taxonomy context: [[urdaneta-2011-survey]]; social-graph critiques: [[viswanath-2010-analysis]]. Root: [[douceur-2002-sybil]].

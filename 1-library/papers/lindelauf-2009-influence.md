---
id: lindelauf-2009-influence
type: paper
title: "The influence of secrecy on the communication structure of covert networks"
authors: [Roy Lindelauf, Peter Borm, Herbert Hamers]
year: 2009
venue: Social Networks
url: https://repository.tilburguniversity.edu/bitstreams/a1cf257a-d168-4a33-806c-c8900bf2ad45/download
doi: 10.1016/j.socnet.2008.12.003
arxiv: null
cite: "Lindelauf, R., Borm, P., & Hamers, H. (2009). The influence of secrecy on the communication structure of covert networks. Social Networks, 31(2), 126–137."
topics: [fork-merge-security]
added_by: dmarz/fm
accessed: 2026-10-03
read_depth: full
relevance: 3
citations: 94  # Crossref is-referenced-by-count, 2026-10-03
code: []
---

## Summary

Read in full from the February 2008 CentER Discussion Paper 2008-23 preprint (the Social Networks version was not accessible). The authors ask which communication graph a covert organisation should adopt when it must trade secrecy against coordination. Information performance I(g) is the normalised reciprocal of total pairwise distance (or, as a robustness check, of the diameter). Secrecy S(g) is the expected fraction of the network that stays unexposed when one member is exposed, given an exposure probability per member and a probability that each of that member's links is detected. The chosen network maximises the Nash bargaining product S(g)·I(g) over connected graphs of order n, as a bargain between a "secrecy" planner and an "efficiency" planner.

## Contribution

A simple quantitative model of the secrecy-coordination dilemma that Baker and Faulkner (1993) described for illegal conspiracies, with exact optima for small n and heuristic search for larger n.

## Key results

- Uniform exposure, all links of an exposed member detected: the star graph is optimal for all n (Theorem 4.1).
- Uniform exposure, each link detected with probability p: the complete graph is optimal for p ≤ 1/2 and the star for p ≥ 1/2 (Theorems 4.2-4.3); with the diameter measure the switch is at p = n/(2(n-1)).
- Exposure proportional to information centrality (random-walk stationary distribution), as in a mature operation: cellular graphs are optimal. Exact optima are given for n ≤ 7; for n = 10 the Petersen graph appears near-optimal; at n = 25 cells with degree 5-7 emerge, and at n = 40 a high-degree hub with smaller cells around it.
- These are model optima (derived and computed), not empirical observations; the authors note they are consistent with reported structures of jihadi networks.

## Methods and models

Graph theory plus two-person Nash bargaining over the finite set of (S, I) pairs; proofs for star and complete graphs; random-graph search (500,000 samples) and greedy edge addition for larger n.

## Limitations and open questions

The secrecy measure counts exposure one hop deep only (a detected member exposes his neighbours, not their neighbours). No adversary strategy beyond random or centrality-weighted exposure. No empirical validation. The paper is about hiding members from an outside observer, not about defending against a member who has been turned.

## Relevance to us

Bears on Q1 as a design calculus. A fork-merge parent hiding which children exist and which will return is the "secrecy" planner; the need for children to report and be merged is the "efficiency" planner. The model's answer depends on how exposure works: if any discovered child reveals its direct contacts, route everything through one hub (the parent) so a captured child exposes nothing about its siblings; if discovery concentrates on high-traffic nodes, use cells, i.e. small groups of children that report through a cell lead, so capturing one exposes one cell. For the Q3 attacker the same structure says where to aim: in a star the hub is the prize, and in a cellular design the cell leads are. Cutouts and compartments are the human versions of these structures; [[cowden-2014-pioneering]] shows the opposite case, a home service whose agents were all discoverable. The agent-side unlinkability entries ([[chaum-1981-untraceable]], [[dingledine-2004-tor]]) give the cryptographic means of making links undetectable, which in this model drives p toward 0 and lets the network be dense without losing secrecy.

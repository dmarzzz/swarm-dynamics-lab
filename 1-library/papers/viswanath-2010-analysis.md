---
id: viswanath-2010-analysis
type: paper
title: "An Analysis of Social Network-Based Sybil Defenses"
authors: ["Bimal Viswanath", "Ansley Post", "Krishna P. Gummadi", "Alan Mislove"]
year: 2010
venue: "ACM SIGCOMM 2010"
url: https://conferences.sigcomm.org/sigcomm/2010/papers/sigcomm/p363.pdf
doi: "10.1145/1851182.1851226"
arxiv: null
cite: "Viswanath, B., Post, A., Gummadi, K. P., & Mislove, A. (2010). An Analysis of Social Network-Based Sybil Defenses. In Proceedings of the ACM SIGCOMM 2010 Conference, pp. 363-374. ACM."
topics: [sybil-resistance, meta]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "312 (OpenAlex, 2026-10-03); 105 (Crossref, proceedings DOI)"
code: []
---

## Summary

The authors put SybilGuard, SybilLimit, SybilInfer and SumUp on a common footing: each induces a ranking of nodes by how "close" they are to a trusted node and then cuts the ranking. They show that all of them are in effect detecting the local community around the trusted node. Replacing them with an off-the-shelf local community detection algorithm (Mislove's normalised-conductance method) gives comparable results.

## Contribution

A unifying analysis and a negative result: social-graph Sybil defences inherit the limits of community detection. Networks with strong community structure are inherently more vulnerable, and Sybils can target their few attack edges near the trusted node to look like part of its community.

## Key results

- All four schemes reduce to ranking by community membership around the verifier (analysed and measured on real social graphs).
- Honest nodes in other communities rank below well-placed Sybils, so either many honest nodes are rejected or many Sybils are accepted.
- Targeted attack-edge placement close to the trusted node makes attacks markedly more effective than random placement.
- Proposals for moving forward include using multiple trusted nodes and restricting defences to the verifier's own community.

## Methods and models

Re-implementation of the schemes as ranking functions, ROC-style comparison on several real social network datasets, local community detection baseline.

## Limitations and open questions

Analysis is empirical on particular datasets; it does not give a new defence with guarantees. [[alvisi-2013-sok]] later builds on this, giving community detection with provable guarantees and arguing for local white-listing instead of global detection.

## Relevance to us

Agent swarms often have strong community structure by design (task teams, spatial neighbourhoods, sub-swarms). This paper predicts that any graph-based trust propagation in such swarms will confuse "outside my team" with "Sybil", and that an attacker who attaches near a trusted agent will be accepted. That is a design constraint for reputation systems in multi-agent systems and for the bridge between [[cao-2012-aiding]] style ranking and swarm topologies. Related: [[yu-2006-sybilguard]], [[danezis-2009-sybilinfer]], [[tran-2009-sybil-resilient]].

---
id: shi-2013-sybilshield
type: paper
title: "SybilShield: An agent-aided social network-based Sybil defense among multiple communities"
authors: [Lu Shi, Shucheng Yu, Wenjing Lou, Y. Thomas Hou]
year: 2013
venue: 2013 Proceedings IEEE INFOCOM, Turin, pp. 1034-1042
url: https://www.cnsr.ictas.vt.edu/publication/INFOCOM13_SybilShield.pdf
doi: 10.1109/infcom.2013.6566893
arxiv: null
cite: "Shi, L., Yu, S., Lou, W., & Hou, Y. T. (2013). SybilShield: An agent-aided social network-based Sybil defense among multiple communities. In 2013 Proceedings IEEE INFOCOM, pp. 1034-1042. IEEE. https://doi.org/10.1109/INFCOM.2013.6566893"
topics: [sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "32 (Crossref, 2026-10-03)"
code: []
---

## Summary

Targets the main empirical weakness of SybilGuard/SybilLimit-style defences: they assume the honest region is one fast-mixing blob separated from the Sybil region by few attack edges, but real social graphs are many loosely connected communities, so random routes from a verifier in one community rarely intersect those of an honest suspect in another and honest users get rejected in bulk. SybilShield keeps the random-route intersection test but, when a suspect fails it, the verifier recruits "agents" (nodes it has already accepted, which tend to sit in other communities) to re-run the test from their vantage points and accepts if enough agents vote yes above a threshold. The sociological premise, validated on a 100,000-node MySpace sample partitioned by Louvain into 19 communities (4 large >10,000 nodes, 3 medium, 12 small; average foreign edges 1.4M / 404K / 818 per class), is that inter-community "foreign" edges greatly outnumber the attack edges an adversary can create, so agents are overwhelmingly honest (average 113 / 116 / 12 agents per verifier with 5 / 6 / 1 Sybil among them). Evaluation with 500 injected Sybil nodes, 50 attack edges and 100,000 random verifier-suspect pairs: honest acceptance rises from 37.94% (SybilGuard) to 70.81% (SybilShield), i.e. false positive rate falls from 62.06% to 29.19%, a 32.87-point reduction, while Sybil acceptance rises only 3.06 points. A probabilistic analysis bounds Sybils accepted per attack edge. Read: abstract, introduction, model and assumptions, protocol (random routes plus agents and threshold), evaluation set-up and results (Fig. 2 numbers), comparison to related work, conclusion; analysis section skimmed.

## Contribution

First social-graph Sybil defence designed for multi-community topologies, using already-accepted peers as cross-community verifiers to cut false positives roughly in half at a small cost in false negatives.

## Key results

- Honest acceptance 70.81% vs 37.94% (SybilGuard); FPR 29.19% vs 62.06%.
- Sybil acceptance up by 3.06 points relative to SybilGuard.
- MySpace sample: foreign edges per community far exceed plausible attack edges; Sybil agents are a small minority (about 5%).

## Methods and models

Random routes of length w per community (set by 3-hop sampling), agent voting with threshold t, probabilistic bound on accepted Sybils per attack edge, experiments on a static 100,000-node MySpace crawl with synthetic Sybil region (500 nodes, 50 attack edges).

## Limitations and open questions

Still a 29% false positive rate; single dataset and a single adversary configuration; static graph; agent recruitment assumes verifiers already hold accepted cross-community contacts. Inherits the fast-mixing-within-community assumption and the critique in Viswanath et al. that these schemes reduce to community detection.

## Relevance to us

A concrete data point on how badly the canonical social-graph Sybil defences perform on real community-structured graphs (62% honest rejection) and one way to patch it; relevant if agent networks ever rely on trust graphs among operators. Sits with [[yu-2006-sybilguard]], [[yu-2008-sybillimit]], [[viswanath-2010-analysis]], [[mohaisen-2013-sybil]] and the SoK [[alvisi-2013-sok]]; routing-layer use of the same ideas in [[lesniewski-laas-2008-sybil-proof]]. Root: [[douceur-2002-sybil]].

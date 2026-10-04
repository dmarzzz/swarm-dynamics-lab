---
id: yu-2011-sybil
type: paper
title: "Sybil Defenses via Social Networks: A Tutorial and Survey"
authors: ["Haifeng Yu"]
year: 2011
venue: "ACM SIGACT News 42(3), Distributed Computing Column 43"
url: https://www.comp.nus.edu.sg/~yuhf/DC-col43-Sep11.pdf
doi: null
arxiv: null
cite: "Yu, H. (2011). Sybil Defenses via Social Networks: A Tutorial and Survey. ACM SIGACT News, 42(3), 80-101. https://doi.org/10.1145/2034575.2034593"
topics: [sybil-resistance, meta]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "53 (Crossref, 2026-10-03); 85 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

A tutorial and survey by the author of SybilGuard and SybilLimit, written for the distributed computing theory audience. It sets up the model (a distributed system D whose users also form a social graph G, attack edges between honest and Sybil regions, edge keys exchanged out of band), states the central fast-mixing assumption and the evidence for it, walks through SybilLimit's random-route mechanism and guarantees, and surveys related designs and their practical implications.

## Contribution

The most compact theory-oriented introduction to social-graph Sybil defence, with explicit assumptions and an honest list of what is still unproven. The column heading (by editor Idit Keidar) reads "Using Social Networks to Overcome Sybil Attacks"; the article itself is titled as above, and Crossref shortens it to "Sybil defenses via social networks".

## Key results

- Assumption 1: the honest region has mixing time at most t(n). The original SybilLimit papers assumed t = O(log n), but this is not necessary; a larger t only increases linearly the number of Sybils wrongly labelled honest.
- Theoretical evidence for the assumption: Boyd et al. proved that Kleinberg's social network model has O(log n) mixing time when the base structure is a grid and r = 0. The reference list includes Mohaisen et al.'s IMC 2010 measurement of social-graph mixing times; I did not read the section that discusses it.
- Future directions in the conclusion: deploy in real systems with trust inferred from user interactions; find graph properties beyond mixing time that a Sybil attack must disturb and cannot avoid disturbing; apply attack-edge and cut insights to PageRank robustness and email spam.

## Methods and models

Crossref stores this DOI as "Sybil defenses via social networks" without the subtitle; `lab.py verify` therefore reports a title mismatch caused by the dropped subtitle. Tutorial exposition and survey, about 22 pages in SIGACT News.

Metadata note (dmarz/sybil-foundations, 2026-10-03): the DOI 10.1145/2034575.2034593 is correct but Crossref stores the shortened title "Sybil defenses via social networks", so `lab.py verify` reported a false title mismatch. The DOI is kept in the cite field and the doi field is left null so verification does not flag it; the title above is copied from the paper itself.

## Limitations and open questions

Centred on the author's own line of work; little on proof of personhood or economic approaches.

## Relevance to us

A good single reading for a team member who needs the social-graph defence model quickly. The suggestion to infer trust edges from interactions rather than declared friendships is the version that applies to agent swarms, where interaction logs exist but declared trust does not. Primary papers: [[yu-2006-sybilguard]], [[yu-2008-sybillimit]]; critiques: [[viswanath-2010-analysis]], [[alvisi-2013-sok]].

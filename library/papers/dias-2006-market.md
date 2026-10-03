---
id: dias-2006-market
type: paper
title: 'Market-Based Multirobot Coordination: A Survey and Analysis'
authors:
- 'M. B. Dias'
- 'R. Zlot'
- 'N. Kalra'
- 'A. Stentz'
year: 2006
venue: 'Proceedings of the IEEE'
url: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/JPROC.2006.876939?fields=title,year,authors,venue,abstract,openAccessPdf,externalIds
doi: 10.1109/JPROC.2006.876939
arxiv: null
cite: 'Dias, M. B., Zlot, R., Kalra, N., & Stentz, A. (2006). Market-Based Multirobot Coordination: A Survey and Analysis. Proceedings of the IEEE, 94(7), 1257-1270.'
topics:
- agent-budgets
- swarm-robotics
added_by: dmarz/budget-c
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 'Crossref 2026-10-03: 675'
code: []
---

## Summary

A survey of market-based approaches to coordinating teams of robots, where robots allocate tasks among themselves through auctions and bidding. The abstract says these methods have been applied in domains from mapping and exploration to robot soccer, and that the paper gives an introduction to the approach, a review and analysis of the state of the art, and a discussion of remaining research challenges.

## Contribution

The standard reference survey for auction-based multirobot task allocation, consolidating the line that descends from the contract net ([[smith-1980-contract]]).

## Key results

- Abstract only: no specific quantitative findings stated. Metadata (volume 94, issue 7, pages 1257-1270) from Crossref.

## Methods and models

Literature survey and analysis (not read beyond the abstract). Semantic Scholar lists a green open-access copy on figshare that I did not open.

## Limitations and open questions

Read at abstract level only; claims about which auction types or analyses the survey covers are not checked. Robots in this literature are typically cooperative team members, so honest bidding is assumed rather than enforced (inferred, not checked in the text).

## Relevance to us

The multirobot precedent for letting workers bid for tasks under resource limits, which is the shape of an LLM orchestrator dividing a token budget among sub-agents. Pair with [[wellman-1993-market]] for price-based allocation, [[chevaleyre-2006-issues]] for welfare criteria, and [[yokoo-2004-effect]] for the Sybil risk once bidders are cheap to duplicate.

---
id: scan-papers-active-matter
type: task
title: 'Catalogue the papers: active matter physics'
kind: scan
status: open
priority: p1
owner: null
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- active-matter
---

## Goal

Build the paper base for `active-matter`: the review articles, the seminal papers and the strongest work, so a survey agent can start from a dense library instead of a blank search.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- Marchetti et al. 2013, Hydrodynamics of soft active matter (Rev. Mod. Phys.)
- Toner and Tu 1995, Long-range order in a two-dimensional dynamical XY model (PRL)
- Cates and Tailleur 2015, Motility-induced phase separation (Annu. Rev. Condens. Matter Phys.)
- Bechinger et al. 2016, Active particles in complex and crowded environments (Rev. Mod. Phys.)

## Search plan

- Start from the seeds. For each seminal paper, pull its references (backward) and the papers citing it (forward) from Semantic Scholar: https://api.semanticscholar.org/graph/v1/paper/DOI:<doi>/citations?fields=title,year,externalIds,citationCount&limit=100
- Query arXiv (export.arxiv.org/api/query), Semantic Scholar search and OpenAlex (api.openalex.org/works?search=...) with at least 5 different phrasings of the topic, including the terms used by neighbouring fields.
- Look for review articles first: they give the map and their reference lists are dense seeds.
- Prioritise by relevance to the hackathon, then by citation count, then recency. Catalogue the review papers, the seminal papers, and the strongest recent work.

## Done when

- At least 25 papers catalogued in library/papers/ with this topic, including every review article you found.
- At least 5 of them read in full (read_depth: full), chosen as the most relevant.
- Every paper that ships code has its repo catalogued in library/code/ and linked in `code:`.
- The coverage note below is filled and `python3 scripts/lab.py check` passes.

## Coverage note

The agent that finishes this task writes here: what was searched, counts by type, what is still missing, and which follow-up tasks it opened.

---
id: scan-papers-collective-motion
type: task
title: 'Catalogue the papers: collective motion models'
kind: scan
status: open
priority: p0
owner: null
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- collective-motion
---

## Goal

Build the paper base for `collective-motion`: the review articles, the seminal papers and the strongest work, so a survey agent can start from a dense library instead of a blank search.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- Reynolds 1987, Flocks, herds and schools: a distributed behavioral model (SIGGRAPH), the Boids paper
- Vicsek et al. 1995, Novel type of phase transition in a system of self-driven particles (PRL)
- Couzin et al. 2002, Collective memory and spatial sorting in animal groups (J. Theor. Biol.)
- Ballerini et al. 2008, Interaction ruling animal collective behavior depends on topological rather than metric distance (PNAS)
- Cavagna et al. 2010, Scale-free correlations in starling flocks (PNAS)
- Vicsek and Zafeiris 2012, Collective motion (Physics Reports), a review
- Katz et al. 2011, Inferring the structure and dynamics of interactions in schooling fish (PNAS)

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

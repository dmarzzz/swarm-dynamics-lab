---
id: scan-papers-swarm-robotics
type: task
title: 'Catalogue the papers: swarm robotics'
kind: scan
status: claimed
priority: p0
owner: dmarz/swarm-robotics
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- swarm-robotics
claimed_at: 2026-10-03T17:01Z
updated: 2026-10-03T17:01Z
---

## Goal

Build the paper base for `swarm-robotics`: the review articles, the seminal papers and the strongest work, so a survey agent can start from a dense library instead of a blank search.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- Brambilla et al. 2013, Swarm robotics: a review from the swarm engineering perspective (Swarm Intelligence)
- Rubenstein, Cornejo and Nagpal 2014, Programmable self-assembly in a thousand-robot swarm (Science)
- Werfel, Petersen and Nagpal 2014, Designing collective behavior in a termite-inspired robot construction team (Science)
- Vásárhelyi et al. 2018, Optimized flocking of autonomous drones in confined environments (Science Robotics)
- Dorigo, Theraulaz and Trianni, Swarm robotics: past, present, and future (Proc. IEEE, 2021)
- Hamann, Swarm Robotics: A Formal Approach (book)

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

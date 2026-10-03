---
id: scan-papers-sync-consensus
type: task
title: 'Catalogue the papers: synchronisation, consensus and networked control'
kind: scan
status: claimed
priority: p1
owner: dmarz/sync-consensus
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- sync-consensus
claimed_at: 2026-10-03T17:01Z
updated: 2026-10-03T17:01Z
---

## Goal

Build the paper base for `sync-consensus`: the review articles, the seminal papers and the strongest work, so a survey agent can start from a dense library instead of a blank search.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- Kuramoto model and Strogatz 2000, From Kuramoto to Crawford (Physica D)
- O'Keeffe, Ha and Strogatz 2017, Oscillators that sync and swarm (Nature Communications), the swarmalator paper
- Jadbabaie, Lin and Morse 2003, Coordination of groups of mobile autonomous agents using nearest neighbor rules (IEEE TAC)
- Olfati-Saber 2006, Flocking for multi-agent dynamic systems: algorithms and theory (IEEE TAC)
- Olfati-Saber, Fax and Murray 2007, Consensus and cooperation in networked multi-agent systems (Proc. IEEE)
- Cucker and Smale 2007, Emergent behavior in flocks (IEEE TAC)
- Castellano, Fortunato and Loreto 2009, Statistical physics of social dynamics (Rev. Mod. Phys.)

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

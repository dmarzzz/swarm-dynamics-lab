---
id: scan-papers-llm-agent-swarms
type: task
title: 'Catalogue the papers: llm agent swarms'
kind: scan
status: open
priority: p0
owner: null
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- llm-agent-swarms
---

## Goal

Build the paper base for `llm-agent-swarms`: the review articles, the seminal papers and the strongest work, so a survey agent can start from a dense library instead of a blank search.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- Park et al. 2023, Generative agents: interactive simulacra of human behavior (UIST)
- Du et al. 2023, Improving factuality and reasoning in language models through multiagent debate
- Li et al. 2023, CAMEL: communicative agents for mind exploration
- Wu et al. 2023, AutoGen; Hong et al. 2023, MetaGPT; Qian et al. 2023, ChatDev; Chen et al. 2023, AgentVerse
- Li et al. 2024, More agents is all you need
- Cemri et al. 2025, Why do multi-agent LLM systems fail?
- Large agent-society simulations: Project Sid (Altera, 2024), AgentSociety (2025)

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

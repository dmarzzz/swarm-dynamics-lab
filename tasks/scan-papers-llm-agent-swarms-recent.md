---
id: scan-papers-llm-agent-swarms-recent
type: task
title: Catalogue LLM agent swarms papers from 2024 onward
kind: scan
status: claimed
priority: p0
owner: dmarz/llm-agent-swarms-recent
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- llm-agent-swarms
claimed_at: 2026-10-03T17:01Z
updated: 2026-10-03T17:01Z
---

## Goal

The field moves fast and the seminal scan will skew old. Catalogue 2024 to 2026 work on LLM agent swarms, especially scaling the number of agents, coordination protocols, failure taxonomies, and agent-society simulations. Include strong preprints and workshop papers.

## Search plan

- arXiv listing searches sorted by date, OpenReview (ICLR, NeurIPS, ICML, CoRL), and forward citations of the seminal papers in the sibling scan task.
- Check the accepted-paper lists of the most recent relevant conferences and workshops.

## Done when

- At least 20 papers catalogued in library/papers/ with this topic, including every review article you found.
- At least 4 of them read in full (read_depth: full), chosen as the most relevant.
- Every paper that ships code has its repo catalogued in library/code/ and linked in `code:`.
- The coverage note below is filled and `python3 scripts/lab.py check` passes.

## Coverage note

The agent that finishes this task writes here: what was searched, counts by type, what is still missing, and which follow-up tasks it opened.

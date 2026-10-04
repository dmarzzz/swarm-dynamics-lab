---
id: wild-timeline
type: task
title: Unified incident timeline across the Transluce, collusion.wiki and SwarmTraces datasets
kind: build
status: claimed
priority: p1
owner: shadow/sol-timeline
for: shadow
created: 2026-10-04
created_by: shadow/sol-timeline
depends_on: []
topics:
- swarm-detection
- llm-agent-swarms
claimed_at: 2026-10-04T15:00Z
updated: 2026-10-04T15:24Z
---

## Goal

Descriptive aggregator requested by Shadow (BRIEF-2026-10-03 project C). Put the three public
in-the-wild incident datasets on one daily axis: Transluce URLQuery daily report counts,
collusion.wiki save/delete/probe events per day (plus the rmn.re shortener log and the other-wiki
pages that ship with the dump), and SwarmTraces artifact counts by kind (undated, shown as a bar).
Hand-entered published report dates and the METR Jul 8-13 board window are overlays, labelled
as such. Second question: which target data sources appear in both the Transluce source buckets
and the wiki page families or outbound link hosts, and do their daily series line up.
Post-hoc, no model calls, no causal claim about one dataset preceding another.

## Done when

- Code takes a --data path; raw dataset rows are never committed, only derived daily aggregates.
- One figure (stacked daily timeline with shaded windows) and one table (shared sources with
  per-dataset counts and date spans) saved under researchers/shadow/notes/wild-timeline/.
- FINDING.md (1 page) with question, data, method, numbers, limits, novelty check against
  library/ and the prior work list in the brief.
- lab.py check passes and deliverables are pushed.

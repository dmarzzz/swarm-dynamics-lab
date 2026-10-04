---
id: repair-hypothesis-topic-navigation
type: task
title: Repair noncanonical hypothesis topics blocking dashboard export
kind: admin
status: open
priority: p0
owner: null
for: shadow
created: 2026-10-03
created_by: vishesh/codex-heterogeneous
depends_on: []
topics: [meta, llm-agent-swarms]
---

## Goal

Repair the upstream dashboard failure introduced with three shadow hypotheses. `dashboard/scripts/export.py` fails at `research_navigation.py` with `unknown or duplicate hypothesis topic`. The hypothesis topics include free-form labels not registered in `library/topics.yaml`. Source commit e51f3fe was published 2026-10-04 03:37 UTC. This blocks subsequent dashboard updates, including owner-requested HX score revisions.

## Done when

- Use appropriate existing canonical topic slugs in `shadow-board-nsweep`, `shadow-capture-memory` and `shadow-neff-evidence-board`, preserving scientific text and any useful fine-grained labels in a suitable non-navigation field.
- Run the dashboard export and contract tests, then verify a successful dashboard workflow.
- Preserve hypothesis status and scientific claims; this is a metadata repair, not review or acceptance.

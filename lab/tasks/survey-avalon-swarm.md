---
id: survey-avalon-swarm
type: task
title: 'Survey: swarm-scale hidden-role games as a Sybil / fork-merge testbed'
kind: survey
status: open
priority: p2
owner: null
for: dmarz
created: 2026-10-03
created_by: dmarz/avalon
depends_on:
- scan-papers-avalon-swarm
- scan-code-avalon-swarm
- scan-papers-avalon-scaling
topics:
- llm-agent-swarms
- sybil-resistance
- swarm-detection
- fork-merge-security
---

## Goal

Turn the three Avalon scans into a prior-art survey that decides, per hunch A1-A6
(`5-experiments/studies/dmarz/avalon-swarm-hunches.md`), what has been tested, what the closest attempts found,
and what is still open.

## Done when

- `surveys/avalon-swarm.md` passes the prior-art gate in `lab.py check`.
- Per-hunch table: closest prior, what it measured, what is still unmeasured.
- Explicit answer to: has anyone run an LLM hidden-role game past ~20 seats, with one principal owning several
  seats, or with forks merging back?

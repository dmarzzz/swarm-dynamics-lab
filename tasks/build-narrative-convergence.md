---
id: build-narrative-convergence
type: task
title: Build a cited narrative convergence map across the three researchers
kind: build
status: claimed
priority: p1
owner: shadow/sol-narrative
for: shadow
created: 2026-10-04
created_by: shadow/sol-narrative
depends_on: []
topics:
- meta
- llm-agent-swarms
claimed_at: 2026-10-04T15:29Z
updated: 2026-10-04T17:31Z
---

## Goal

Human-directed synthesis and visualization, not a new experiment. Build a zero-model-call program reading a pinned origin/main snapshot, task metadata, evidence registry, researcher notes and the public hub. Show researcher activity separately from evidence, theme-level connections and three editorial candidate headlines with transparent editable scoring. Publish a static page at https://swarm-narrative.pages.dev and refresh approximately every 45 minutes until 23:00 UTC on 4 October.

## Done when

- [x] Rerunnable build_map.py and narrative.json committed with source provenance.
- [x] Timeline, theme graph, candidate scorecards and cited researcher trajectories live at https://swarm-narrative.pages.dev.
- [x] Automated data checks and desktop/mobile browser smoke tests pass (1440px and 390px).
- [ ] Final refreshed snapshot published by 23:00 UTC.

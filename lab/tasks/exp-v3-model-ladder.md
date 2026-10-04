---
id: exp-v3-model-ladder
type: task
title: "E2: v3 screen on Sonnet 5.5 if Haiku cannot compute"
kind: experiment
status: open
priority: p2
owner: null
for: dmarz
created: 2026-10-04
created_by: dmarz/private-control
depends_on: [exp-v3-screen-diagnostic]
topics: []
---

## Goal

E2. Same 12-world screen plan on claude-sonnet-5-5, only if E1 shows Haiku fails every condition. New qualification, never pooled with Haiku. Plan: [NEXT-EXPERIMENTS.md](../researchers/dmarz/notes/discussion-dose/NEXT-EXPERIMENTS.md). Proposed, not authorized: needs dmarz's go, a committed pre-run review, a claimed box (one run per server), and a source pinned at or after 6563e28. Changes to src/bench_v3 are proposals to dmarz/discussion-bench-v3.

## Done when

- [ ] Pre-run review committed before any paid call.
- [ ] Run on its own claimed box; artifacts verified; claim released.
- [ ] Post-mortem committed with the decision for the next item.

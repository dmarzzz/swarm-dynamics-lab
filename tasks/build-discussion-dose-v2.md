---
id: build-discussion-dose-v2
type: task
title: Build the harder contested-evidence version of discussion-dose (v2), ready to roll out
kind: build
status: claimed
priority: p1
owner: dmarz/discussion-dose
for: dmarz
created: 2026-10-03
created_by: dmarz/discussion-dose
depends_on: []
topics: []
claimed_at: 2026-10-04T00:32Z
updated: 2026-10-04T00:32Z
---

## Goal

Real-model v1 episodes so far sit at a ceiling: the false digest is adopted by the exposed child and then removed in the pre-discussion verification turn, so every dose is identical. Build a separately versioned v2 that removes the easy correction paths in graded levels, with a predeclared calibration rule, offline tests and a frozen paid plan. Human asked for it in parallel so rollout can be chosen once v1 S0 finishes. No paid calls in this task.

## Done when

- [ ] V2 design and decision rule written (researchers/dmarz/notes/discussion-dose/V2-DESIGN.md).
- [ ] v2 world generator, runner, scorer and frozen plans implemented without changing the v1 code path.
- [ ] Offline tests pass for v1 and v2; scripted v2 bundles run end to end.
- [ ] Rollout commands documented; nothing enqueued.

---
id: plan-discussion-v3-successor
type: task
title: Plan the next discussion benchmark diagnostic and offline orchestration
kind: build
status: open
priority: p1
owner: null
for: dmarz
created: 2026-10-03
created_by: dmarz/discussion-bench-v3
depends_on: []
topics: []
---

## Goal

Verify Q0 results are on main, write a bounded next-run diagnostic plan linked to the open repair task, and specify how cloud coordination and server execution continue when the operator laptop is closed. This task plans; it does not launch paid requests or claim an unconfigured cloud environment is ready.

## Done when

- [ ] Verify the Q0 report and safe outcome tables exist on remote main.
- [ ] Commit a concrete diagnostic design, measurements, call counts, gates and follow-up qualification criteria.
- [ ] Document cloud versus local execution, credential/access readiness, crash handling and owner-state cleanup requirements.
- [ ] Link the plan from the benchmark and existing diagnostic task and report the actual launch status.

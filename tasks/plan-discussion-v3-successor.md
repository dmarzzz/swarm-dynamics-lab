---
id: plan-discussion-v3-successor
type: task
title: Plan the next discussion benchmark diagnostic and offline orchestration
kind: build
status: done
priority: p1
owner: dmarz/discussion-bench-v3
for: dmarz
created: 2026-10-03
created_by: dmarz/discussion-bench-v3
depends_on: []
topics: []
claimed_at: 2026-10-04T03:55Z
updated: 2026-10-04T04:00Z
outputs:
- researchers/dmarz/notes/discussion-dose/benchmark-v3/NEXT-RUN.md
- researchers/dmarz/notes/discussion-dose/benchmark-v3/next-run-planning-evidence.json
---

## Goal

Verify Q0 results are on main, write a bounded next-run diagnostic plan linked to the open repair task, and specify how cloud coordination and server execution continue when the operator laptop is closed. This task plans; it does not launch paid requests or claim an unconfigured cloud environment is ready.

## Done when

- [x] Verify the Q0 report and safe outcome tables exist on remote main.
- [x] Commit a concrete diagnostic design, measurements, call counts, gates and follow-up qualification criteria.
- [x] Document cloud versus local execution, credential/access readiness, crash handling and owner-state cleanup requirements.
- [x] Link the plan from the benchmark and existing diagnostic task and report the actual launch status.

## Output

[Next-run plan](../researchers/dmarz/notes/discussion-dose/benchmark-v3/NEXT-RUN.md), [planning evidence](../researchers/dmarz/notes/discussion-dose/benchmark-v3/next-run-planning-evidence.json). Planning complete; paid launch and cloud access remain unconfigured. Implementation belongs to diagnose-discussion-v3-q0.

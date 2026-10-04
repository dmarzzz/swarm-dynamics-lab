---
id: phantom-coast-pc2-runner
type: task
title: Build the Phantom Coast PC-2 launch instrument
kind: build
status: done
priority: p1
owner: vishesh/codex-phantom-coast
for: vishesh
created: 2026-10-03
created_by: vishesh/codex-phantom-coast
depends_on: []
topics: []
claimed_at: 2026-10-04T04:56Z
updated: 2026-10-04T05:04Z
outputs:
- researchers/vishesh/notes/phantom-coast/pc2/RUNBOOK.md
- researchers/vishesh/notes/phantom-coast/pc2/RUNNER-VALIDATION.json
- researchers/vishesh/notes/phantom-coast/pc2/src/run.py
---

## Goal

Implement and fault-check the PC-2 native runner under the published prospective plan. Prepare exact review and launch requirements without claiming an admitted run.

## Done when

- Native choices, maps, durable assignments and bounded budget carry-forward implemented.
- Qualification, stage admission, analysis and replay validated on development fixtures.
- Reviewable launch instructions and exact remaining gates published.

## Coverage note

Published the native readiness package with 42 offline checks, source/budget/admission guards, qualification/analysis, and inspected event rendering. No native PC-2 calls or spend. Required reviewer and operational admission evidence remain explicit in SETUP.md and RUNBOOK.md; readiness task completion is not run admission.

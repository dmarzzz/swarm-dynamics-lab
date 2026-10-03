---
id: build-dashboard-questions
type: task
title: Add question atlas and review tools to the research dashboard
kind: build
status: done
priority: p1
owner: dmarz/dashboard-questions
for: null
created: 2026-10-03
created_by: dmarz/dashboard-questions
depends_on: []
topics:
- meta
claimed_at: 2026-10-03T21:48Z
updated: 2026-10-03T21:56Z
outputs:
- dashboard/QUESTIONS.md
- dashboard/src/views/Questions.tsx
- dashboard/scripts/export.py
---

## Goal

Integrate the canonical question atlas into the existing React dashboard with search, filters, complete candidate details, source links and local human review. The user asked to hold deployment while clarifying Shadow’s old site versus the team deployment. Work stays on a feature branch and draft PR; no merge to main/dashboard-v1 or workflow dispatch.

## Done when

- [x] Questions data exports directly from the canonical bank and passes contract checks.
- [x] The dashboard route supports discovery, full details, stable links and compatible local review import/export.
- [x] Build, type checks, targeted tests and desktop/mobile browser checks pass.
- [x] Deployment ownership and triggers are documented; the change is reviewable without publication.

## Coverage note

Draft PR: https://github.com/dmarzzz/swarm-lab/pull/81. All requested implementation and local validation are complete. Publication remains on hold by the human; do not merge or dispatch deployment. See the dashboard-questions session log for verification and deployment findings.

---
id: build-dashboard-questions
type: task
title: Add question atlas and review tools to the research dashboard
kind: build
status: open
priority: p1
owner: null
for: null  # set to a researcher name to direct the task at them
created: 2026-10-03
created_by: dmarz/dashboard-questions
depends_on: []
topics: [meta]
---

## Goal

Integrate the canonical question atlas into the existing React dashboard with search, filters, complete candidate details, source links and local human review. The user asked to hold deployment while clarifying Shadow’s old site versus the team deployment. Work stays on a feature branch and draft PR; no merge to main/dashboard-v1 or workflow dispatch.

## Done when

- [ ] Questions data exports directly from the canonical bank and passes contract checks.
- [ ] The dashboard route supports discovery, full details, stable links and compatible local review import/export.
- [ ] Build, type checks, targeted tests and desktop/mobile browser checks pass.
- [ ] Deployment ownership and triggers are documented; the change is reviewable without publication.

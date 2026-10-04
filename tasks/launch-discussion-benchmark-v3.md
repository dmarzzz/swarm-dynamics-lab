---
id: launch-discussion-benchmark-v3
type: task
title: Deploy and start the operator-authorized v3 model qualification
kind: build
status: claimed
priority: p1
owner: dmarz/discussion-bench-v3
for: dmarz
created: 2026-10-03
created_by: dmarz/discussion-bench-v3
depends_on: []
topics: []
claimed_at: 2026-10-04T02:38Z
updated: 2026-10-04T02:38Z
---

## Goal

The user requested starting experiments after documenting Vishesh's fixes. Ship a bounded S0 qualification using the repaired v3 benchmark and the cheapest active Anthropic model, report it to the hub, and preserve exact manifests and outputs. Record independent review as pending; the user-authorized engineering run does not approve a hypothesis or release the confirmation holdout.

## Done when

- [x] Freeze authorization, protocol, model settings and visualization mapping.
- [x] Add and test minimal hub reporting and an explicit operator-qualification launch path.
- [x] Allocate a dedicated server with an exclusive fleet claim and deploy the exact committed source.
- [x] Start one 96-case / 636-call qualification batch; verify live progress and durable artifacts.
- [x] Record launch evidence, remaining review/qualification gates and the next decision.

## Launch evidence

[Deployment and next decision](../researchers/dmarz/notes/discussion-dose/benchmark-v3/DEPLOYMENT.md), [initial live snapshot](../researchers/dmarz/notes/discussion-dose/benchmark-v3/launches/v3-q0-a1-start.json). Source `883d310`; server-side tests passed, real model responses and public frames verified. This task completes the launch, not the independent review or result analysis.

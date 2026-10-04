---
id: build-false-alarm-cascade
type: task
title: Prepare the false-alarm cascade experiment (honeypot-vigilance hunch V4) on Opus 5.5 to launch-ready
kind: build
status: open
priority: p1
owner: null
for: dmarz
created: 2026-10-04
created_by: dmarz/pipeline
depends_on: []
topics:
- swarm-detection
- llm-agent-swarms
updated: 2026-10-04T11:18Z
history:
- '2026-10-04T10:47Z released by dmarz/pipeline-alarm: paused at c1de1da6; new owner by the fleet monitor''s assignment: dmarz/scale-xl (Big experiment session on orbital-one); see 5-experiments/studies/dmarz/false-alarm-cascade/HANDOVER.md'
- '2026-10-04T11:18Z released by dmarz/scale-xl: returned to dmarz/pipeline (fleet-monitor stop, usage limit); package at code af115c44, docs 7f5ecb0a; awaiting fleet-monitor check'
---

## Goal

Design and build hunch V4 of [the honeypot-vigilance note](../../5-experiments/studies/dmarz/honeypot-vigilance-hunches.md) in `5-experiments/studies/dmarz/false-alarm-cascade/`: a planted agent wrongly broadcasts that a real resource is a honeypot; measure whether a small group of Opus 5.5 agents abandons that resource and similar real ones, and how long the false belief survives a correction, against a true alarm and a no-alarm control. A minimal turn-based instrument with the lab's own synthetic resources; this is not the general swarm simulator. Hunch-level exploratory study in researcher notes, not a hypothesis. Preparation only: this task launches nothing and makes no model inference call. The run itself goes through the private run queue after the fleet monitor's same-researcher check.

## Done when

- [x] Prospective plan and frozen design committed before implementation.
- [x] Code, offline tests and a scripted zero-model-call stage that passes offline.
- [x] Pre-run review per 5-experiments/toolkit/agent-experiments/RUN-REVIEW.md on main with assignment manifest, call counts, gates, model settings, hard max_calls and the pinned commit (code commit af115c44, source hash 7803e3b8; reviews/chain-001-pre.md).
- [x] Chained launch per 5-experiments/studies/dmarz/pipeline/READY-CHAIN.md with the server as a parameter (READY.yaml with model_ladder; RUN.md; rehearsal 57/57).
- [ ] Run request filed in the private run queue after the fleet monitor's go.

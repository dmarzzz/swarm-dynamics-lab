---
id: build-false-alarm-cascade
type: task
title: Prepare the false-alarm cascade experiment (honeypot-vigilance hunch V4) on Opus 5.5 to launch-ready
kind: build
status: claimed
priority: p1
owner: dmarz/pipeline-alarm
for: dmarz
created: 2026-10-04
created_by: dmarz/pipeline
depends_on: []
topics:
- swarm-detection
- llm-agent-swarms
claimed_at: 2026-10-04T08:07Z
updated: 2026-10-04T08:07Z
---

## Goal

Design and build hunch V4 of [the honeypot-vigilance note](../researchers/dmarz/notes/honeypot-vigilance-hunches.md) in `researchers/dmarz/notes/false-alarm-cascade/`: a planted agent wrongly broadcasts that a real resource is a honeypot; measure whether a small group of Opus 5.5 agents abandons that resource and similar real ones, and how long the false belief survives a correction, against a true alarm and a no-alarm control. A minimal turn-based instrument with the lab's own synthetic resources; this is not the general swarm simulator. Hunch-level exploratory study in researcher notes, not a hypothesis. Preparation only: this task launches nothing and makes no model inference call. The run itself goes through the private run queue after the fleet monitor's same-researcher check.

## Done when

- [x] Prospective plan and frozen design committed before implementation.
- [ ] Code, offline tests and a scripted zero-model-call stage that passes offline.
- [ ] Pre-run review per tooling/agent-experiments/RUN-REVIEW.md on main with assignment manifest, call counts, gates, model settings, hard max_calls and the pinned commit.
- [ ] Chained launch per researchers/dmarz/notes/pipeline/READY-CHAIN.md with the server as a parameter.
- [ ] Run request filed in the private run queue after the fleet monitor's go.

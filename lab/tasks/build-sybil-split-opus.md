---
id: build-sybil-split-opus
type: task
title: Prepare the identity-splitting experiment with fixed attacker resources on Opus 5.5 to launch-ready
kind: build
status: done
priority: p1
owner: dmarz/pipeline-split
for: dmarz
created: 2026-10-04
created_by: dmarz/pipeline
depends_on: []
topics:
- sybil-resistance
- llm-agent-swarms
claimed_at: 2026-10-04T07:52Z
updated: 2026-10-04T09:28Z
outputs:
- 5-experiments/studies/dmarz/sybil-split-opus/reviews/chain-001-pre.md
---

## Goal

Design and build successor 3 of [the next-experiments note](../../5-experiments/studies/dmarz/next-experiments-2026-10-04/README.md) in `researchers/dmarz/notes/sybil-split-opus/`: one attacker's fixed resources split across 1, 3, 9 or 27 identities, admission policies compared at equal check budgets, Opus 5.5 synthesis, extending the sybil-scale-api instrument. Preparation only: this task launches nothing and makes no model inference call. The run itself goes through the private run queue after the fleet monitor's same-researcher check.

## Done when

- [x] Prospective plan and frozen design committed before implementation.
- [x] Code, offline tests and a scripted zero-model-call stage that passes offline.
- [x] Pre-run review per tooling/agent-experiments/RUN-REVIEW.md on main with assignment manifest, call counts, gates, model settings, hard max_calls and the pinned commit.
- [x] Chained launcher (interface probe, qualification, main stage; stops by itself at a failed gate) with the server as a parameter.
- [ ] Run request filed in the private run queue after the fleet monitor's go.

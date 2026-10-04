---
id: build-verify-cost-qwen
type: task
title: Prepare program v5 line V (when is verification worth its cost) to launch-ready
kind: build
status: done
priority: p0
owner: dmarz/pipeline-verify
for: dmarz
created: 2026-10-04
created_by: dmarz/pipeline
depends_on: []
topics:
- llm-agent-swarms
claimed_at: 2026-10-04T10:30Z
updated: 2026-10-04T11:37Z
outputs:
- 5-experiments/studies/dmarz/verify-cost-qwen/reviews/chain-001-pre.md
---

## Goal

Line V of research program v5: can an agent choose checking versus exploration when the optimal action changes with reliability and opportunity cost? 24 layouts x 12 risk/cost cases x 2 equal-information formats, 576 main calls and 24 qualification calls on qwen/qwen3.7-flash, using a dmarz-owned copy of the phantom-coast PC5 contract and engine. Study directory `researchers/dmarz/notes/verify-cost-qwen/`. The program is dmarz's own (research program v5, 2026-10-04); this task implements the line as a ready-chain package. Preparation only: this task launches nothing and makes no model inference call. The run goes through the private run queue after the fleet monitor's same-researcher check.

## Done when

- [x] Plan and frozen design (the program's design for this line) committed before implementation.
- [x] Code, offline tests and a scripted zero-model-call stage that passes offline.
- [x] Pre-run review on main with assignment manifest, call counts, gates, model settings, hard max_calls and the pinned commit.
- [x] Chained launch per researchers/dmarz/notes/pipeline/READY-CHAIN.md with the server as a parameter.
- [ ] Run request filed in the private run queue after the fleet monitor's go.

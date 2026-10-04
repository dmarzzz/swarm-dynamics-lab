---
id: build-sybil-scarcity-opus
type: task
title: Prepare the Sybil scarcity experiment on Opus 5.5 to launch-ready
kind: build
status: claimed
priority: p1
owner: dmarz/pipeline-scarcity
for: dmarz
created: 2026-10-04
created_by: dmarz/pipeline
depends_on: []
topics:
- sybil-resistance
- llm-agent-swarms
claimed_at: 2026-10-04T07:52Z
updated: 2026-10-04T07:52Z
---

## Goal

Turn [the scarcity plan](../researchers/dmarz/notes/sybil-scarcity-plan/README.md) into a launch-ready package in `researchers/dmarz/notes/sybil-scarcity-opus/`: the plan's design with Opus 5.5 as synthesizer (dated amendment; dmarz said Opus for every paid stage on 2026-10-04), reusing the sybil-scale-api instrument. Preparation only: this task launches nothing and makes no model inference call. The run itself goes through the private run queue after the fleet monitor's same-researcher check.

## Done when

- [x] Study directory with frozen design, assignment manifest, code, offline tests and a scripted zero-model-call stage that passes offline. (researchers/dmarz/notes/sybil-scarcity-opus, code commit 30e34577, source hash b37af997: selftest 33 OK, offline S0 168/168, rehearsal passed)
- [x] Pre-run review per tooling/agent-experiments/RUN-REVIEW.md on main with call counts, gates, model settings, hard max_calls and the pinned commit. (reviews/chain-001-pre.md)
- [x] Chained launcher (interface probe, qualification, main stage; stops by itself at a failed gate) with the server as a parameter. (src/chain.py; RUN.md gives the generic private launcher commands with --host)
- [ ] Run request filed in the private run queue after the fleet monitor's go.

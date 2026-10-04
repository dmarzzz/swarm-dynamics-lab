---
id: build-sybil-scarcity-synth
type: task
title: Prepare the scarcity synthesizer follow-up (sybil-scarcity-synth) on Opus 5.5 to launch-ready
kind: build
status: done
priority: p1
owner: dmarz/pipeline-scarcity
for: dmarz
created: 2026-10-04
created_by: dmarz/pipeline
depends_on: []
topics:
- sybil-resistance
- llm-agent-swarms
claimed_at: 2026-10-04T10:13Z
updated: 2026-10-04T11:19Z
outputs:
- 5-experiments/studies/dmarz/sybil-scarcity-synth/reviews/chain-001-pre.md
---

## Goal

Follow-up to [sybil-scarcity-opus](../../5-experiments/studies/dmarz/sybil-scarcity-opus/RESULTS.md) in `researchers/dmarz/notes/sybil-scarcity-synth/`: on the same kind of packets and fresh roots, vary only the synthesizer (reasoning effort low or high, the original prompt or the original plus one frozen evidence rule) and measure whether it adopts the repeated fabrication less when truth is scarce, and what that costs in accuracy when truth is plentiful. The rule is written after seeing the earlier result, so this is a follow-up, not a confirmation. Exploratory study in researcher notes. Preparation only: this task launches nothing and makes no model inference call. The run itself goes through the private run queue after the fleet monitor's same-researcher check.

## Done when

- [x] Prospective plan with the frozen rule wording on main before any fresh root is generated. (6e07eb51)
- [x] Code, offline tests and a scripted zero-model-call stage that passes offline. (code commit ea63999a, source hash b75d7b37: selftest 39 OK, offline S0 128/128, rehearsal 38/38)
- [x] Pre-run review per tooling/agent-experiments/RUN-REVIEW.md on main with assignment manifest, call counts, gates, model settings, hard max_calls and the pinned commit. (reviews/chain-001-pre.md)
- [x] Chained launch per researchers/dmarz/notes/pipeline/READY-CHAIN.md with the server as a parameter. (src/chain.py; RUN.md)
- [ ] Run request filed in the private run queue after the fleet monitor's go.

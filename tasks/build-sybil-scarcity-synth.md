---
id: build-sybil-scarcity-synth
type: task
title: Prepare the scarcity synthesizer follow-up (sybil-scarcity-synth) on Opus 5.5 to launch-ready
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
claimed_at: 2026-10-04T10:13Z
updated: 2026-10-04T10:13Z
---

## Goal

Follow-up to [sybil-scarcity-opus](../researchers/dmarz/notes/sybil-scarcity-opus/RESULTS.md) in `researchers/dmarz/notes/sybil-scarcity-synth/`: on the same kind of packets and fresh roots, vary only the synthesizer (reasoning effort low or high, the original prompt or the original plus one frozen evidence rule) and measure whether it adopts the repeated fabrication less when truth is scarce, and what that costs in accuracy when truth is plentiful. The rule is written after seeing the earlier result, so this is a follow-up, not a confirmation. Exploratory study in researcher notes. Preparation only: this task launches nothing and makes no model inference call. The run itself goes through the private run queue after the fleet monitor's same-researcher check.

## Done when

- [ ] Prospective plan with the frozen rule wording on main before any fresh root is generated.
- [ ] Code, offline tests and a scripted zero-model-call stage that passes offline.
- [ ] Pre-run review per tooling/agent-experiments/RUN-REVIEW.md on main with assignment manifest, call counts, gates, model settings, hard max_calls and the pinned commit.
- [ ] Chained launch per researchers/dmarz/notes/pipeline/READY-CHAIN.md with the server as a parameter.
- [ ] Run request filed in the private run queue after the fleet monitor's go.

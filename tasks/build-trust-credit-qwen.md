---
id: build-trust-credit-qwen
type: task
title: Prepare program v5 line T (trust credit: when verification amplifies capture) to launch-ready
kind: build
status: open
priority: p0
owner: null
for: dmarz
created: 2026-10-04
created_by: dmarz/pipeline
depends_on: []
topics:
- sybil-resistance
- llm-agent-swarms
---

## Goal

Line T of research program v5: does propagating a passed identity's trust credit to its neighbours cause extra attackers to be admitted? 24 fresh roots, 324 scripted identities, three admission rules replayed on one frozen audit sequence, 504 main calls and 24 qualification calls on qwen/qwen3.7-flash. Study directory `researchers/dmarz/notes/trust-credit-qwen/`. The program is dmarz's own (research program v5, 2026-10-04); this task implements the line as a ready-chain package. Preparation only: this task launches nothing and makes no model inference call. The run goes through the private run queue after the fleet monitor's same-researcher check.

## Done when

- [ ] Plan and frozen design (the program's design for this line) committed before implementation.
- [ ] Code, offline tests and a scripted zero-model-call stage that passes offline.
- [ ] Pre-run review on main with assignment manifest, call counts, gates, model settings, hard max_calls and the pinned commit.
- [ ] Chained launch per researchers/dmarz/notes/pipeline/READY-CHAIN.md with the server as a parameter.
- [ ] Run request filed in the private run queue after the fleet monitor's go.
